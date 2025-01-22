# Dependencies for LensGW
![alt text](https://github.com/SSingh087/lensGW/blob/main/lensGW.png)
 
---

# Gravitational Wave Classification  

This project focuses on the **identification of lensed and unlensed gravitational waves**, aiming to extract comprehensive source information. Developed in collaboration with a **PhD researcher from the University of Glasgow**, the project explores cutting-edge techniques in astrophysics and machine learning to classify gravitational waveforms. Despite hardware limitations, the model achieved **98% accuracy**, providing valuable insights into source characteristics.  

The project is ongoing, with plans to enhance the accuracy further and integrate additional features.  

---

## Overview  

### 🎯 **Goals**  
1. **Classify gravitational waves** into lensed and unlensed categories.  
2. Generate gravitational waveforms using the **PyCBC Python library**.  
3. Extract and forecast source characteristics from classified waves.  

### 📊 **Current Achievements**  
- **98% classification accuracy** using a custom machine learning model.  
- Successfully generated gravitational waveforms to simulate real-world conditions.  
- Developed a robust methodology for feature extraction and source prediction.  

---

## Features  

### 🌀 **Gravitational Waveform Generation**  
- Leveraged the **PyCBC library** to generate realistic gravitational waveforms.  
- Simulated lensed and unlensed waves for model training and testing.  

### 🤖 **Machine Learning Model**  
- Designed a machine learning model to classify waveforms with high accuracy.  
- Employed innovative techniques to overcome **hardware limitations**.  

### 🔍 **Source Analysis**  
- Forecasted source characteristics based on classified waveforms.  
- Provided insights into the origin and nature of gravitational waves.  

---

## Tech Stack  

| Technology      | Description                                           |  
|------------------|-------------------------------------------------------|  
| **Python**      | Core programming language for development.             |  
| **PyCBC**       | Used for generating gravitational waveforms.           |  
| **Scikit-Learn**| Machine learning model development and evaluation.     |  
| **NumPy/Pandas**| Data manipulation and analysis.                        |  
| **Matplotlib**  | Visualization of waveforms and model performance.      |  

---

## Installation  

Follow these steps to set up the project locally:  

1. **Clone the repository:**  
   ```bash  
   git clone https://github.com/Nancyjikadra/lensGW.git  
   cd lensGW  
   ```  

2. **Create a virtual environment (optional):**  
   ```bash  
   python -m venv venv  
   source venv/bin/activate   # On Windows: venv\Scripts\activate  
   ```  

3. **Install dependencies:**  
   ```bash  
   pip install -r requirements.txt  
   ```  

4. **Run the project:**  
   ```bash  
   python main.py  
   ```  

---

## Usage  

### **1. Generating Waveforms**  
- The script uses PyCBC to generate both lensed and unlensed gravitational waveforms.  
- Configuration can be adjusted in the `waveform_generator.py` file.  

### **2. Training the Model**  
- The training script uses the generated waveforms to build the classification model.  
- Run the training process with:  
   ```bash  
   python train_model.py  
   ```  

### **3. Testing and Evaluation**  
- Test the model's accuracy using real-world or simulated data.  
- Results, including classification metrics and confusion matrices, will be saved in the `results/` directory.  

---

## Results  

- **Accuracy:** 98%  
- **Recall:** High recall ensures most gravitational waves are correctly classified.  
- **Insights:** Predicted source characteristics from the classified waveforms.  
---

## Contributions  

Contributions are welcome! To contribute:  

1. Fork the repository.  
2. Create a new feature branch.  
   ```bash  
   git checkout -b feature/your-feature-name  
   ```  
3. Commit your changes.  
   ```bash  
   git commit -m "Add your message here"  
   ```  
4. Push your branch.  
   ```bash  
   git push origin feature/your-feature-name  
   ```  
5. Open a pull request on GitHub.  

---

## License  

This project is licensed under the [MIT License](LICENSE).  
