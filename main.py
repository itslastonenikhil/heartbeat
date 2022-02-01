import streamlit as st;
import pandas as pd;
import numpy as np;
import pickle;

from PIL import Image
img = Image.open('heartbeat.png')
st.set_page_config(
        page_title="Heartbeat",
        page_icon=img,
        layout="wide",
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        
       margin-top: 0px;
       padding-top: 0px;
    }}
    
</style>
""",
        unsafe_allow_html=True,
    )

def text(content, color, size):
     st.markdown(f'<h1 style="color:{color};font-size:{size}px;">{content}</h1>', unsafe_allow_html=True)

def link(url, content, color, size):
     st.markdown(f'<a href="{url}" target= "_blank" style="color:{color};font-size:{size}px;text-decoration: none;">{content}</a>', unsafe_allow_html=True)

text("Heartbeat", "#05B2DC", 46)
text("Noninvasive machine-learning-based heart disease predictor", "#AAD922", 30)


#-------------------
#Load trained models
#-------------------

# MLP model
mlp_model = pickle.load(open('mlp_model.pkl', 'rb'))

# Min-max scaler

mm_scalar = pickle.load(open('mm_scalar.pkl', 'rb'))


thal_dict =  {'3 = Normal':3, '6 = Fixed Defect':6, '7 = Reversable Defect': 7}
exang_dict = {'Yes':1, 'No': 0}

with st.sidebar.form(key='predict'):
        ca = st.selectbox('Number of major vessels colored by floursopy',
        (0, 1, 2, 3), key='ca')

        thal = st.selectbox('Thalium stress result',
        ('3 = Normal','6 = Fixed Defect', '7 = Reversable Defect'), key='thal')

        exang = st.selectbox('Exercise Induced Angina',
        ('Yes', 'No'), key='exang')
        
        
        oldpeak = st.number_input("ST depression induced by exercise relative to rest", 
        key='oldpeak', min_value=0.0)

        thalach = st.slider(
        'Maximum heart rate achieved',0,250, 72)

        trestbps = st.number_input('Resting Blood Pressure(in mm Hg)', key="trestbps", step=1, min_value=1, max_value=220, value=120)

        
        submitted = st.form_submit_button('Generate Report')

# Input array format: ca, thal, oldpeak, exang, thalach, trestbps
input = [ca, thal_dict[thal], oldpeak, exang_dict[exang], thalach, trestbps]
input = np.array(input)

input_ = input.reshape(1, -1)
input_ = mm_scalar.transform(input_)

text("Report", "#05B2DC", 28)

col1, col2, col3= st.columns([1, 1, 1])

with col1:
        st.metric("Number of major vessels colored by floursopy:", ca)
        st.metric("Thalium stress result: ", thal)

with col2:
        st.metric("Exercise Induced Angina: ", exang)
        st.metric("ST depression induced by exercise: ", oldpeak)

with col3:
        st.metric("Maximum heart rate achieved: ", thalach)
        st.metric("Resting Blood Pressure(in mm Hg): ", trestbps)

text("Result", "#05B2DC", 28)
if not submitted:
    st.subheader('Report not generated')
if submitted: #making and printing our prediction
    
    result = mlp_model.predict(input_)
    

    if(result[0]):
        text('Positive: You may have heart disease.', "#F18F01", 24)
    else:
        text('Negative: You do not have a heart disease.', "#AAD922", 24)

        

col11, col22= st.columns([1, 1])
with col22: 
        
        st.write('Machine Learning Model: Multi-Layer Perceptron(MLP)')
        st.write('Accuracy: Above 80%')
        st.write('Developed by Nikhil Maurya')
        link('https://www.linkedin.com/in/nikhilmaurya/', "linkedin.com/in/nikhilmaurya/", "#05B2DC", 16)

       

 #ca: number of major vessels (0-3) colored by flourosopy
 #thal: 3 = normal; 6 = fixed defect; 7 = reversable defect
 #oldpeak: ST depression induced by exercise relative to rest
 #exang: exercise induced angina (1 = yes; 0 = no)
 #thalach: maximum heart rate achieved
 #trestbps: resting blood pressure (in mm Hg on admission to the hospital)
