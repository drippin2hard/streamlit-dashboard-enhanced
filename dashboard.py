import streamlit as st
import pandas as pd

st.header("2024 AHI 507 Streamlit Example")
st.subheader("We are going to go through a couple different examples of loading and visualization information into this dashboard")

st.text("""In this streamlit dashboard, we are going to focus on some recently released school learning modalities data from the NCES, for the years of 2021.""")

# ## https://healthdata.gov/National/School-Learning-Modalities-2020-2021/a8v3-a3m3/about_data
df = pd.read_csv("https://healthdata.gov/resource/a8v3-a3m3.csv?$limit=500000") ## changed to 500k to read all data 

## data cleaning 
df['week_recoded'] = pd.to_datetime(df['week'])
df['zip_code'] = df['zip_code'].astype(str)

df['week'].value_counts()

## box to show how many rows and columns of data we have: 
col1, col2, col3 = st.columns(3)
col1.metric("Columns", df.shape[1]) 
col2.metric("Rows", len(df))
col3.metric("Number of unique districts/schools:", df['district_name'].nunique())


st.dataframe(df)



table = pd.pivot_table(df, values='student_count', index=['week'],
                       columns=['learning_modality'], aggfunc="sum")

table = table.reset_index()
table.columns

## line chart by week 
st.bar_chart(
    table,
    x="week",
    y="Hybrid",
)

st.bar_chart(
    table,
    x="week",
    y="In Person",
)

st.bar_chart(
    table,
    x="week",
    y="Remote",
)



col4 = st.columns(1)  # Create the column layout
total_students = df['student_count'].sum()  # Calculate the sum of the column
st.metric("Sum of Students In All States Combined", total_students)  # Display the metric



statewise_sum = df.groupby('state')['student_count'].sum().reset_index()

# Rename columns for clarity
statewise_sum.columns = ['State', 'Total Students']

# Display the data as a table in the dashboard
st.subheader("Sum of Students per State")
st.dataframe(statewise_sum)

# Optional: Display as a bar chart
st.bar_chart(statewise_sum, x='State', y='Total Students', use_container_width=True)



# Count the number of times each state appears in the data
state_counts = df['state'].value_counts().reset_index()

# Rename columns for clarity
state_counts.columns = ['State', 'Count']

# Display the data as a table
st.subheader("Number of Times Each State Appears in the Data")
st.dataframe(state_counts)

# Optional: Display as a bar chart
st.bar_chart(state_counts, x='State', y='Count', use_container_width=True)

