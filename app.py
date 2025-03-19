import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy import stats

# Streamlit App Layout
st.title('Clicks Before vs After Google Update')
st.write("Upload a CSV file containing the data to visualize the clicks before and after the update.")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Load the data from the uploaded CSV file
    data = pd.read_csv(uploaded_file)

    # Check the first few rows of the uploaded data
    st.write("Preview of the uploaded data:")
    st.write(data.head())

    # Prepare the data for the analysis
    if 'Top queries' in data.columns and '3/7/25 - 3/12/25 Clicks' in data.columns and '3/14/25 - 3/18/25 Clicks' in data.columns:
        data_clean = data[['Top queries', '3/7/25 - 3/12/25 Clicks', '3/14/25 - 3/18/25 Clicks']]

        # Clean data (handling any missing values or zeros)
        data_clean.loc[:, 'Before Update Clicks'] = data_clean['3/7/25 - 3/12/25 Clicks'].fillna(0)
        data_clean.loc[:, 'After Update Clicks'] = data_clean['3/14/25 - 3/18/25 Clicks'].fillna(0)

        # Calculate the change in clicks and classify the status
        data_clean.loc[:, 'Change'] = data_clean['After Update Clicks'] - data_clean['Before Update Clicks']
        data_clean.loc[:, 'Status'] = ['Improved' if row['Change'] > 0 else 'Worsened' if row['Change'] < 0 else 'Lost'
                                       for _, row in data_clean.iterrows()]

        # Perform OLS regression (least squares) to get the trendline
        slope, intercept, r_value, p_value, std_err = stats.linregress(data_clean['Before Update Clicks'], data_clean['After Update Clicks'])

        # Create the interactive scatter plot using Plotly
        fig = px.scatter(data_clean,
                         x='Before Update Clicks',
                         y='After Update Clicks',
                         color='Status',
                         hover_data=['Top queries', 'Change'],
                         labels={'Before Update Clicks': 'Clicks Before Update',
                                 'After Update Clicks': 'Clicks After Update'},
                         title="Clicks Before vs After Google Update (Interactive)",
                         color_discrete_map={'Improved': 'green', 'Worsened': 'red', 'Lost': 'gray'})

        # Add the OLS trendline to the plot
        fig.add_traces(
            go.Scatter(
                x=data_clean['Before Update Clicks'],
                y=slope * data_clean['Before Update Clicks'] + intercept,
                mode='lines',
                name='OLS Trendline',
                line=dict(color='blue', dash='dash')
            )
        )

        # Set the same scale for both axes
        fig.update_layout(
            xaxis=dict(
                zeroline=False,    # No zero line on x-axis
                showgrid=False,    # Hide gridlines
                ticks="outside"
            ),
            yaxis=dict(
                zeroline=False,    # No zero line on y-axis
                showgrid=False,    # Hide gridlines
                ticks="outside"
            )
        )

        # Display the interactive plot
        st.plotly_chart(fig)
    else:
        st.error("The uploaded file must contain 'Top queries', '3/7/25 - 3/12/25 Clicks', and '3/14/25 - 3/18/25 Clicks' columns.")
