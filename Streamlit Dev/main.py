import streamlit as st 
import pandas as pd 
from io import StringIO

st.title("Streamlit Dev tutorial")
st.subheader(".....bla bla bla")
st.header("header")
st.text("paragraph text, i'm learning streamlit. The aim of learning streamlit is for model deployment")
st.markdown('HTML property in the text"",**Hello** World')

#Widget 
#uploade a csv file 
uploaded_file = st.file_uploader("Choose a file",type=['csv'])
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)

#download the file as csv 
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(dataframe)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='iris.csv',
    mime='text/csv',
)

selected = st.checkbox("I agree")
clicked = st.button("Click me")
activated = st.toggle("Activate")