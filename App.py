# -*- coding: utf-8 -*-
"""App.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19wSoqtlLl7kkLEMsoQ8HSLog-8dRujC9
"""

#!pip install streamlit
#!pip install gdown
#!pip install --upgrade tensorflow

import streamlit as st
import tensorflow as tf
import pandas as pd
import numpy as np
import gdown
import os

# Direct download link of the model file from Google Drive
url = 'https://drive.google.com/uc?id=1v33PXoCE6EAyacP885qwIUnr5AWZAWjL'

# Path to save the downloaded model file
model_path = 'my_model.keras'

# Download the model if it does not exist
if not os.path.exists(model_path):
    with st.spinner('Downloading model...'):
        gdown.download(url, model_path, quiet=False)

# Load the model
model = tf.keras.models.load_model(model_path)

# Define the expected features in the same order as the model was trained
expected_features = [
    'CreditScore', 'Geography','Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts',
    'HasCrCard', 'IsActiveMember', 'EstimatedSalary'
]

# Define function to preprocess input data
def preprocess_input(CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts,
                     HasCrCard, IsActiveMember, EstimatedSalary):
    # Create a DataFrame with the input data
    input_data = pd.DataFrame({
        'CreditScore': [CreditScore],
        'Geography': [Geography],
        'Gender': [Gender],
        'Age': [Age],
        'Tenure': [Tenure],
        'Balance': [Balance],
        'NumOfProducts': [NumOfProducts],
        'HasCrCard': [HasCrCard],
        'IsActiveMember': [IsActiveMember],
        'EstimatedSalary': [EstimatedSalary]
    })

    # Encoding of all categorical variables
    input_data_encoded = pd.get_dummies(input_data)

    # Ensure the input data matches the model's expected features
    for feature in expected_features:
        if feature not in input_data_encoded.columns:
            input_data_encoded[feature] = 0  # Add missing features with default value 0

    input_data_encoded = input_data_encoded[expected_features]

    # Convert to numpy array of type float32
    input_data_encoded = input_data_encoded.astype(np.float32).to_numpy()

    return input_data_encoded

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: blue;
    }
    .title {
        color: purple;
        text-align: center;
        font-size: 40px;
    }
    .widget-label {
        color: #ff6347;
        font-weight: bold;
    }
    .prediction-result {
        color: green;
        font-size: 30px;
        text-align: center;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Create the web interface
def main():
    st.markdown('<div class="title">Bank Churn Prediction Model</div>', unsafe_allow_html=True)

    CreditScore = st.number_input('Credit Score', min_value=350, max_value=850)
    Geography = st.selectbox('Geography',  ['France', 'Germany', 'Spain'])
    Gender = st.selectbox('Gender', ['Male', 'Female'])
    Age = st.number_input('Age', min_value=18, max_value=92)
    Tenure = st.number_input('Tenure', min_value=0, max_value=10)
    Balance = st.number_input('Balance', min_value=0, max_value=250900)
    NumOfProducts = st.number_input('NumOfProducts', min_value=1, max_value=4)
    credit_levels = {0: 'No', 1: 'Yes'}
    options = [f"{key}-{value}" for key, value in credit_levels.items()]
    HasCrCard = st.selectbox('Does the Customer Possess Credit Card?', options)
    active_levels = {0: 'No', 1: 'Yes'}
    options = [f"{key}-{value}" for key, value in active_levels.items()]
    IsActiveMember = st.selectbox('Is the Customer Active?', options)
    EstimatedSalary = st.number_input('Estimated Salary', min_value=11, max_value=200000)

    if st.button('Predict'):
        HasCrCard = int(HasCrCard.split('-')[0])
        IsActiveMember = int(IsActiveMember.split('-')[0])
        input_data = preprocess_input(CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts,
                                      HasCrCard, IsActiveMember, EstimatedSalary)
        try:
            prediction = model.predict(input_data)[0][0]  # Get the prediction score
            if prediction < 0.5:
                st.markdown('<div class="prediction-result">Prediction: Customer will not leave the bank</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="prediction-result">Customer will leave the bank</div>', unsafe_allow_html=True)
        except Exception as e:
            st.write(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
