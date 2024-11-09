import streamlit as st 
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler , LabelEncoder , OneHotEncoder
import pandas as pd
import pickle

model=tf.keras.models.load_model('model.h5')

with open('onhot_encoder_geo' , 'rb') as file:
  onehot_encoder_geo=pickle.load(file)

with open('label_encoder_gender' , 'rb') as file:
  label_encoder_gender=pickle.load(file)

with open('scaler' , 'rb') as file:
  scaler=pickle.load(file)
  
st.title('Customer Chrun prediction')

geography = st.selectbox('Geography', onehot_encoder_geo.categories_[0])
gender = st.selectbox('Gender', label_encoder_gender.classes_)
age = st.slider('Age', 18, 92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
estimated_salary = st.number_input('Estimated Salary')
tenure = st.slider('Tenure', 0, 10)
num_of_products = st.slider('Number of Products', 1, 4)
has_cr_card = st.selectbox('Has Credit Card', [0, 1])
is_active_member = st.selectbox('Is Active Member', [0, 1])

input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Gender': [label_encoder_gender.transform([gender])[0]],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary]
})


geo_encode = onehot_encoder_geo.transform([[geography]]).toarray()
geo_encode_df = pd.DataFrame(geo_encode , columns=onehot_encoder_geo.get_feature_names_out(['Geography']))
input_data_df=pd.DataFrame(input_data)

input_data_df=pd.concat([input_data_df ,geo_encode_df] , axis=1)

input_data_scaled=scaler.transform(input_data_df)
prediction=model.predict(input_data_scaled)
prediction_prob=prediction[0][0]
st.write(prediction_prob)
if prediction_prob>0.5:
  st.write('Likey to churn')
else:
  st.write('Unlike to churn')
  
 