import streamlit as st
import numpy as np
import pandas as pd

# Display a title and some text
st.title('My First Streamlit App')
st.write("Here's our first attempt at using data to create a table:")

# Creating a simple dataframe
df = pd.DataFrame({
  'first column': np.arange(1, 11),
  'second column': np.random.randn(10)
})

# Display the dataframe as a table
st.write(df)

# Create a line chart
st.line_chart(df)

