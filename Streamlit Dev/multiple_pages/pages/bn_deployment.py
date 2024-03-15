import streamlit as st 
#from deployment.utils import  columns 

import numpy as np
import pandas as pd 
import joblib

model = joblib.load('Bayesian_Network.joblib')

st.title('Gen5 BED Prediction Profiler')
#st.image('dependency_model.png',caption='Dependency Model')
foamheight = st.select_slider('Foam Height',['low','medium','high'])
fb1_volume = st.select_slider('FB1 Volume',['low','medium','high'])
fb1_avg_height = st.select_slider('FB1 Avg Height',['low','medium','high'])
fb1_avg_weight = st.select_slider('FB1 Avg Weight',['low','medium','high'])
pom_ave_height = st.select_slider('POM Ave Height',['low','medium','high'])
d_datum = st.select_slider('D-Datum Avg Height',['low','medium','high'])
hopperA =st.select_slider('Hopper A Degas Value',['low','medium','high'])
hopperB = st.select_slider('Hopper B Degas Value',['low','medium','high'])
vacuum_delta = st.select_slider('Vacuum delta actual (nose - body) InHg',['low','medium','high'])
inkfill_nest = st.select_slider('Inkfill Nest',['P1','P2','P3','P4'])

#["FoamHeight","FB1 Volume","FB1 Avg Height","FB1 Avg Weight","POM Ave Height", "D-Datum Avg Height","Hopper A Degas Value","Hopper B Degas Value","Vacuum delta actual (nose - body) InHg","inkfill_nest"]

def prediction():
    row = np.array([foamheight, fb1_volume, fb1_avg_height, fb1_avg_weight, pom_ave_height, d_datum, hopperA, hopperB, vacuum_delta, inkfill_nest])
    columns = ["FoamHeight", "FB1 Volume", "FB1 Avg Height", "FB1 Avg Weight", "POM Ave Height", "D-Datum Avg Height", "Hopper A Degas Value", "Hopper B Degas Value", "Vacuum delta actual (nose - body) InHg", "inkfill_nest"]
    X = pd.DataFrame([row], columns=columns)
    prediction = model.predict(X)
    return prediction

st.write('Prediction:', prediction())

#if st.button('Predict'):
    #result = prediction()
    #st.write(f'The predicted class is {result}')

