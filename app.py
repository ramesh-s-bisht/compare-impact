import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy import stats

# Streamlit App Layout
st.title('Clicks Before vs After Google Update')
st.write("Upload a CSV file containing the data to visualize the clicks before and after the update.")

# File uploader for the user to upload a CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV into a DataFrame
    data = pd.read_csv(uploaded_file)

    # Display the first few rows of the data to the user
    st.write("Preview of the uploaded data:")
    st.write(data.head())

    # Ensure the necessary columns are present in the uploaded data
    required_columns = ['Top queries', '3/7/25 - 3/12/25 Clicks', '3/14/25 - 3/18/25 Clicks']
    if all(col in data.columns for col in required_columns):
        # Prepare the data for the analysis
        data_clean = data[['Top queries', '3/7/25 - 3/12/25 Clicks', '3/14/25 - 3/18/25 Clicks']]

        # Clean data (handling any missing values or zeros)
        data_clean['Before Update Clicks'] = data_clean['3/7/25 - 3/12/25 Clicks'].fillna(0)
        data_clean['After Update Clicks'] = data_clean['3/14/25 - 3/18/25 Clicks'].fillna(0)

        # Calculate the change in clicks and classify the status
        data_clean['Change'] = data_clean['After Update Clicks'] - data_clean['Before Update Clicks']
        data_clean['Status'] = ['Improved' if row['Change'] > 0 else 'Worsened' if row['Change'] < 0 else 'No Change'
                                for _, row in data_clean.iterrows()]

        # Trendline for sum of clicks before and after
        sum_before = data_clean['Before Update Clicks'].sum()
        sum_after = data_clean['After Update Clicks'].sum()

        # Create a trendline for sum of all clicks before and after the update
        trendline_x = ['Before Update', 'After Update']
        trendline_y_before = [sum_before, sum_before]  # Keep constant for before update
        trendline_y_after = [sum_after, sum_after]  # Keep constant for after update

        fig1 = go.Figure()

        # Plot the Before Update trendline
        fig1.add_trace(go.Scatter(
            x=trendline_x,
            y=trendline_y_before,
            mode='lines',
            name='Before Update Trendline',
            line=dict(color='blue')
        ))

        # Plot the After Update trendline
        fig1.add_trace(go.Scatter(
            x=trendline_x,
            y=trendline_y_after,
            mode='lines',
            name='After Update Trendline',
            line=dict(color='green')
        ))

        # Update layout with dual axes
        fig1.update_layout(
            title='Trendline of Total Clicks Before and After Update',
            xaxis_title='Update Phase',
            yaxis_title='Total Clicks Before Update',
            yaxis2=dict(
                title='Total Clicks After Update',
                overlaying='y',
                side='right'
            )
        )

        # 2. Scatter Plot: Impact of Update on Clicks with OLS Trendline
        # Perform OLS regression (least squares) to get the trendline
        slope, intercept, r_value, p_value, std_err = stats.linregress(data_clean['Before Update Clicks'], data_clean['After Update Clicks'])

        # Create the interactive scatter plot using Plotly
        fig2 = px.scatter(data_clean,
                          x='Before Update Clicks', 
                          y='After Update Clicks', 
                          color='Status',
                          hover_data=['Top queries', 'Change', 'Before Update Clicks', 'After Update Clicks'],
                          labels={'Before Update Clicks': 'Clicks Before Update',
                                  'After Update Clicks': 'Clicks After Update'},
                          title="Impact of Update on Clicks",
                          color_discrete_map={'Improved': 'green', 'Worsened': 'red', 'No Change': 'blue'})

        # Add the OLS trendline to the scatter plot
        fig2.add_traces(
            go.Scatter(
                x=data_clean['Before Update Clicks'],
                y=slope * data_clean['Before Update Clicks'] + intercept,
                mode='lines',
                name='OLS Trendline',
                line=dict(color='blue', dash='dash')
            )
        )

        # Calculate the counts of each status
        status_counts = data_clean['Status'].value_counts()

        # Pie chart showing the percentage of Improved, Worsened, No Change statuses
        fig3 = px.pie(
            names=status_counts.index, 
            values=status_counts.values, 
            title='Click Status Distribution After Update'
        )

        # Display the DataFrame with Streamlit
        st.write("Here is the dataset used for the analysis:")
        st.dataframe(data_clean)

        # Show the plots
        st.plotly_chart(fig1)  # Trendline with dual axes
        st.plotly_chart(fig2)  # Scatter plot with OLS trendline
        st.plotly_chart(fig3)  # Pie chart for click status distribution

    else:
        st.error("The uploaded file must contain 'Top queries', '3/7/25 - 3/12/25 Clicks', and '3/14/25 - 3/18/25 Clicks' columns.")
