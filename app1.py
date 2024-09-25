import streamlit as st
import pandas as pd
import snowflake.connector
import matplotlib.pyplot as plt
import plotly.express as px


def init_connection():
    return snowflake.connector.connect(
        user='KIRANKHANAN',
        password='Meera@123',
        account='mtcdzli-pc42483',
        warehouse='COMPUTE_WH',
        database='MENTALHEALTH',
        schema='MENTALHEALTHDIS',
        insecure_mode=True
    )

conn = init_connection()

# Query data from Snowflake
@st.cache
def load_data():
    query = "SELECT * FROM MENTALHEALTH.MENTALHEALTHDIS.MENTALHEALTH20182021"
    df = pd.read_sql(query, conn)
    return df

def app():
    # Load data
    data = load_data()

    # Streamlit Dashboard Title
    st.title("Mental Health Analysis in Indian Districts")

    # Year Selection
    years = data['YEAR'].unique()
    year_selected = st.selectbox("Select Year", years)

    # Filter data based on the selected year
    filtered_data = data[data['YEAR'] == year_selected]

    # Create a button to display the selected year of visualization
    if st.button('Show Year of Visualization'):
        st.write(f"Year of Data: {year_selected}")

    # Visualization 1: Total Cases by District
    st.subheader("Total Mental Health Cases by District in " + str(year_selected))
    fig = px.bar(filtered_data, x='DISTRICT', y='TOTAL', title="Total Mental Health Cases by District")
    st.plotly_chart(fig)

    # Visualization 2: Breakdown by Disorder
    st.subheader("Breakdown of Cases by Mental Health Disorder in Each District in " + str(year_selected))
    district_selected = st.selectbox("Select a District", filtered_data['DISTRICT'].unique())
    district_data = filtered_data[filtered_data['DISTRICT'] == district_selected]

    # Plot stacked bar chart for mental health disorders
    disorders = ['SEVERE_MENTAL_DISORDER_(SMD)', 'COMMON_MENTAL _DISORDER(CMD)', 
                 'ALCOHOL_&_SUBSTANCE_ABUSE', 'CASES_REFERRED_TO_HIGHER_CENTRES', 
                 'SUICIDE_ATTEMPT_CASES', 'OTHERS']

    disorder_values = district_data[disorders].iloc[0]

    # Create a bar chart
    fig, ax = plt.subplots()
    ax.bar(disorders, disorder_values, color=['blue', 'green', 'red', 'orange', 'purple', 'brown'])
    ax.set_ylabel('Number of Cases')
    ax.set_title(f"Mental Health Disorder Breakdown for {district_selected} in " + str(year_selected))

    # Rotate the x-axis labels for better readability
    ax.set_xticklabels(disorders, rotation=45, ha='right')  # Rotate labels 45 degrees and align them to the right

    # Display the plot
    st.pyplot(fig)

    # Percentage Breakdown
    st.subheader("Percentage Breakdown of Cases in Selected District in " + str(year_selected))
    pie_fig = px.pie(
        names=disorders,
        values=disorder_values,
        title=f"Percentage Breakdown of Mental Health Issues in {district_selected}"
    )
    st.plotly_chart(pie_fig)
