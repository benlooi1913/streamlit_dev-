import streamlit as st 
import pandas as pd 

st.title('Welcome to Streamlit!')

st.write("Our 1st Dataframe")

df = pd.DataFrame({
    'column_1':[1,2,3,4,5,6],
    'column_2':[1,2,3,4,5,6]
})

st.write(df)

st.write(df.describe())
st.dataframe(df.info())