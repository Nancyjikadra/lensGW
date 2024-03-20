import numpy as np
import sys
from lensGW.solver.solver import lens_eq_solutions
from lenstronomy.LensModel.lens_model import LensModel  
from lensGW.utils.utils import discardOverlaps

def OneDeflector(source_ra,
                 source_dec,
                 lens_model_list,
                 kwargs_lens,
                 **kwargs):

    # default solverKwargs
    solverKwargs = {'Scaled'           : kwargs['Scaled'],
                    'ScaleFactor'      : kwargs['ScaleFactor'],
                    'SearchWindowMacro': kwargs['SearchWindowMacro'],
                    'PixelsMacro'      : 10**4,
                    'PrecisionLimit'   : 10**(-13),
                    'OverlapDistMacro' : 10**(-13), # prescription: solutions whose distance is less than 10**(-15) rad (\sim 2*1.e-4 micro arcsec) are considered overlaps
                    'NearSource'       : False,
                    'Optimization'     : kwargs['Optimization'],
                    'Verbose'          : False} 
    
    # kwargs that need rescaling if Scaled is True
    ToBeScaled = ['PrecisionLimit', 'OverlapDistMacro']
    
    # update solverKwargs with kwargs
    for key in solverKwargs.keys():
        if key in kwargs:
            value = kwargs[key]
            solverKwargs.update({key: value})
        elif key in ToBeScaled:
            if solverKwargs['Scaled']:
                value = solverKwargs[key]/solverKwargs['ScaleFactor']
                solverKwargs.update({key: value})
        if (key == 'Scaled') and solverKwargs[key]:
            if 'ScaleFactor' not in kwargs:
                sys.stdout.write('\n')
                sys.stdout.write("Scaled units requested, but ScaleFactor not specified: it will be set to {0}\n\n".format(solverKwargs['ScaleFactor']))
    
    if solverKwargs['SearchWindowMacro'] is None:
        sys.stderr.write('\n\nMust specify a search window for the macromodel to perform the analysis\n')
        return None, None, None
     
    # repeat for the optimization-related settings if the optimization mode is active
    if solverKwargs['Optimization']:                           
        optimizationKwargs = {'OptimizationWindowMacro': 2,
                              'OptimizationPixelsMacro': 90,
                              'MinDistMacro': None,
                              'ImprovementMacro': None,
                              'OptimizationPrecisionLimitMacro': 10**(-15)}
                              
        # optimization kwargs that need rescaling if Scaled is True
        ToBeScaledOptimization = ['MinDistMacro', 'OptimizationPrecisionLimitMacro']
        
        # update solverKwargs with optimizationKwargs
        for key in optimizationKwargs.keys():
            if key in kwargs:
                value = kwargs[key]
                solverKwargs.update({key: value})
            elif key in ToBeScaledOptimization:
                if solverKwargs['Scaled']:
                    if optimizationKwargs[key] is None:
                        value = optimizationKwargs[key]
                    else:
                        value = optimizationKwargs[key]/solverKwargs['ScaleFactor']
                    solverKwargs.update({key: value})
                else:
                    value = optimizationKwargs[key]
                    solverKwargs.update({key: value})
            else:
                value = optimizationKwargs[key]
                solverKwargs.update({key: value})
                
    # parse the remaining relevant arguments 
    search_window_m  = solverKwargs['SearchWindowMacro']    
    min_distance_m   = solverKwargs['SearchWindowMacro']/solverKwargs['PixelsMacro']
        
    # instantiate the lens model
    lens_model  = LensModel(lens_model_list=lens_model_list)
     
    prev_Img_ra, prev_Img_dec, pixel_width = lens_eq_solutions(source_ra  = source_ra,
                                                               source_dec  = source_dec,
                                                               x_center      = source_ra,
                                                               y_center      = source_dec,
                                                               search_window = search_window_m,
                                                               min_distance  = min_distance_m,
                                                               lens_model    = lens_model,
                                                               kwargs_lens   = kwargs_lens,
                                                               macromodel    = True,
                                                               **solverKwargs) 

    if len(prev_Img_ra)==0 and solverKwargs['NearSource'] == False:
        sys.stderr.write('\nNo images found for the macromodel, try different settings\n')
        return None, None, None

    if solverKwargs['NearSource']:
        NearSourceKwargs = {'SearchWindowNearSource': None,
                            'PixelsNearSource': 10**3}
                                  
        # update NearSourceKwargs with kwargs
        for key in NearSourceKwargs.keys():
            if key in kwargs:
                value = kwargs[key]
                NearSourceKwargs.update({key: value})
        
        # sanity check on the window near source
        if NearSourceKwargs['SearchWindowNearSource'] is None:
            sys.stderr.write('\n\nMust specify a value for the search window near the source')
            return None, None, None
                
        # update NearSourceKwargs with solverKwargs
        for key in solverKwargs.keys():
            if key != 'SearchWindowMacro' and key != 'PixelsMacro':
                value = solverKwargs[key]
                NearSourceKwargs.update({key: value})
        
        # parse the remaining relevant arguments
        search_window_ns = NearSourceKwargs['SearchWindowNearSource']
        min_distance_ns  = search_window_ns/NearSourceKwargs['PixelsNearSource']
            
        # check for images very close to the source, which may have been missed when images' displacements are wide
        if solverKwargs['Verbose']: sys.stdout.write('\n---- Near Source analysis ----\n')
        prev_Img_ra_ns, prev_Img_dec_ns, pixel_width_ns = lens_eq_solutions(source_ra  = source_ra,
                                                                            source_dec  = source_dec,
                                                                            x_center      = source_ra,
                                                                            y_center      = source_dec,
                                                                            search_window = search_window_ns,
                                                                            min_distance  = min_distance_ns,
                                                                            lens_model    = lens_model,
                                                                            kwargs_lens   = kwargs_lens,
                                                                            macromodel    = True,
                                                                            **NearSourceKwargs) 
                                                                            
        # append to the previous solutions if there are new ones, then discard the overlaps  
        if len(prev_Img_ra_ns)>0:
            
            prev_Img_ra  = list(prev_Img_ra)
            prev_Img_dec = list(prev_Img_dec)
            
            prev_Img_ra.extend(prev_Img_ra_ns)
            prev_Img_dec.extend(prev_Img_dec_ns)
            
            prev_Img_ra  = np.array(prev_Img_ra)
            prev_Img_dec = np.array(prev_Img_dec)
            
            # not used now, serves as input for the discardOverlaps routine
            dummy_deltas       = np.zeros(len(prev_Img_ra))
            Img_ra, Img_dec, _ = discardOverlaps(prev_Img_ra, prev_Img_dec, dummy_deltas, solverKwargs['OverlapDistMacro'])  
        else:
            #sys.stdout.write('\n')
            #sys.stdout.write('\n\nNO IMAGES FOUND BY THE NEAR SOURCE CHECK\n\n')
            #sys.stdout.write('\n-----------------------------\n\n')
            
            Img_ra  = prev_Img_ra
            Img_dec = prev_Img_dec

    else:
        Img_ra  = prev_Img_ra
        Img_dec = prev_Img_dec
    
    # sanity check on the number of solutions
    if len(Img_ra)==0:
        sys.stderr.write('\nNo images found for the macromodel, try different settings\n')
        return None, None, None

    return Img_ra, Img_dec, pixel_width

    
    
def microimages(source_ra,
                source_dec,
                lens_model_list,
                kwargs_lens,
                **kwargs):
    import time 
    
    # default kwargs for the complete model
    solverKwargs = {'Scaled'           : kwargs['Scaled'],  
                    'ScaleFactor'      : kwargs['ScaleFactor'],    
                    'OnlyMacro'        : kwargs['OnlyMacro'], 
                    'MacroIndex'       : [0],                
                    'ImgIndex'         : None,  
                    'SearchWindow'     : kwargs['SearchWindow'],
                    'Pixels'           : 10**5, 
                    'OverlapDist'      : 10**(-13), 
                    'PrecisionLimit'   : 10**(-15), 
                    'Optimization'     : kwargs['Optimization'],
                    'Verbose'          : False} 
    
    # kwargs that need rescaling if Scaled is True
    ToBeScaled = ['OverlapDist', 'PrecisionLimit']
    
    # update the solverkwargs with kwargs
    for key in solverKwargs.keys():
        if key in kwargs:
            value = kwargs[key]
            solverKwargs.update({key: value})
        elif key in ToBeScaled:
            if solverKwargs['Scaled']:
                value = solverKwargs[key]/solverKwargs['ScaleFactor']
                solverKwargs.update({key: value})
                
    # add the extra kwargs
    for key in kwargs.keys():
        if key not in solverKwargs:
            value = kwargs[key]
            solverKwargs.update({key: value})
      
    # set up only the macromodel analysis if all the lenses are defined as macromodel
    if len(lens_model_list) == len(solverKwargs['MacroIndex']):
        solverKwargs.update({'OnlyMacro': True})
        
    # flags for only macromodel/complete analysis
    only_macro  = solverKwargs['OnlyMacro']

    if solverKwargs['SearchWindow'] is None and not only_macro:
        sys.stderr.write('\n\nMust specify a search window for the complete model to perform the analysis\n')
        return None, None, None
    
    # indices of the macromodel components
    macro_index = solverKwargs['MacroIndex']
     
    # solve for the macromodel first
    macromodel_list   = [lens_model_list[index] for index in macro_index]
    macromodel_kwargs = [kwargs_lens[index] for index in macro_index]

    MacroImg_ra, MacroImg_dec, Macro_pixel_width = OneDeflector(source_ra    = source_ra,
                                                                 source_dec    = source_dec,
                                                                 lens_model_list = macromodel_list,
                                                                 kwargs_lens     = macromodel_kwargs,
                                                                 **solverKwargs)   
    
    if only_macro:
        return MacroImg_ra, MacroImg_dec, Macro_pixel_width  
    
    else:
    
        # settings for the complete model
        model_list    = lens_model_list
        model_kwargs  = kwargs_lens
        search_window = solverKwargs['SearchWindow']
        min_distance  = solverKwargs['SearchWindow']/solverKwargs['Pixels']
        
        # instantiate the complete lens model
        lens_model_complete = LensModel(lens_model_list=model_list)
        
        # index of the macroimage to zoom on
        img_idx       = solverKwargs['ImgIndex']
        
        # update solverKwargs for the complete model analysis 
        if solverKwargs['Optimization']:                           
            optimizationKwargs = {'OptimizationWindow': 2,
                                  'OptimizationPixels': 60,
                                  'MinDist': None,
                                  'Improvement': None,
                                  'OptimizationPrecisionLimit': 10**(-20)}
                                  
            # optimization kwargs that need rescaling if Scaled is True
            ToBeScaledOptimization = ['MinDist', 'OptimizationPrecisionLimit']
            
            # update solverKwargs with optimizationKwargs
            for key in optimizationKwargs.keys():
                if key not in solverKwargs:
                    if key in ToBeScaledOptimization and solverKwargs['Scaled']:
                        if optimizationKwargs[key] is None:
                            value = optimizationKwargs[key]
                        else:
                            value = optimizationKwargs[key]/solverKwargs['ScaleFactor']
                    else:
                        value = optimizationKwargs[key]
                    solverKwargs.update({key: value})

        if solverKwargs['Optimization']:  
            for key, value in solverKwargs.items():
                if 'Macro' in key in key: pass
                elif 'NearSource' in key: pass
                else:
                    if key != 'ScaleFactor' or (key == 'ScaleFactor' and solverKwargs['Scaled']):
                        if key == 'PrecisionLimit' and solverKwargs['Optimization']: pass

        else:
            for key, value in solverKwargs.items():
                if 'Macro' in key: pass
                elif 'NearSource' in key: pass
        
        # pick up the given macroimage, if selected. Iterate over all the macroimages otherwise
        if img_idx  is None:
            img_idx = range(len(MacroImg_ra))
            
        # solve for the images around each macroimage (both for the complete model and the background only)        
        if solverKwargs['Verbose']: sys.stdout.write('\n---- Complete model analysis ----\n\n')
        
        # will store the images before overlap removal
        prev_Img_ra  = [] 
        prev_Img_dec = [] 
        
        # initialize the pixel width to that of the macromodel
        initial_pixel_width = Macro_pixel_width
        
        for idx in img_idx:
            x0, x1       = MacroImg_ra[idx],MacroImg_dec[idx]   
            center_x     = x0
            center_y     = x1

            temp_Img_ra, temp_Img_dec, pixel_width = lens_eq_solutions(source_ra  = source_ra,
                                                                       source_dec  = source_dec,
                                                                       x_center      = center_x,
                                                                       y_center      = center_y,
                                                                       search_window = search_window,
                                                                       min_distance  = min_distance,
                                                                       lens_model    = lens_model_complete,
                                                                       kwargs_lens   = model_kwargs,
                                                                       macromodel    = False,
                                                                       **solverKwargs) 
            
            # store minimum pixel size, in case numerical differentiation is requested
            if pixel_width>initial_pixel_width:
                pixel_width = initial_pixel_width
            initial_pixel_width = pixel_width
        
            # append to the the temporary solutions
            prev_Img_ra.extend(temp_Img_ra)
            prev_Img_dec.extend(temp_Img_dec)

        # discard the overlaps
        dummy_deltas       = np.zeros(len(prev_Img_ra))
        Img_ra, Img_dec, _ = discardOverlaps(prev_Img_ra, prev_Img_dec, dummy_deltas, solverKwargs['OverlapDist'])       

        # sanity check on the number of solutions
        if len(Img_ra)==0:
            sys.stderr.write('\n\nNo images found for the complete model\n')
            return None, None, None

        if solverKwargs['Verbose']: sys.stdout.write('Elapsed time: {0} seconds\n\n'.format(end-start)) 
        
        return Img_ra, Img_dec, MacroImg_ra, MacroImg_dec, pixel_width      
