import pandas as pd
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

        # Calculate the total clicks before and after the update
        total_before = data_clean['Before Update Clicks'].sum()
        total_after = data_clean['After Update Clicks'].sum()

        # Calculate the change in clicks
        total_change = total_after - total_before
        trend_change_text = f"Total Change in Clicks: {'+' if total_change > 0 else ''}{total_change}"

        # 1. Bar Chart to show total Before vs After Update Clicks
        fig1 = go.Figure()

        # Add Before Update Clicks
        fig1.add_trace(go.Bar(
            x=['Before Update'],
            y=[total_before],
            name='Before Update Clicks',
            marker=dict(color='blue')
        ))

        # Add After Update Clicks
        fig1.add_trace(go.Bar(
            x=['After Update'],
            y=[total_after],
            name='After Update Clicks',
            marker=dict(color='green')
        ))

        # Update layout with the total change annotation
        fig1.update_layout(
            title='Total Clicks Before and After Update',
            xaxis_title='Update Phase',
            yaxis_title='Total Clicks',
            showlegend=True,
            annotations=[
                go.layout.Annotation(
                    x=0.5,
                    y=1.05,
                    xref="paper",
                    yref="paper",
                    text=trend_change_text,
                    showarrow=False,
                    font=dict(size=14, color='black'),
                    align="center"
                )
            ]
        )

        # 2. Scatter Plot: Impact of Update on Clicks
        # Calculate the change in clicks for each query and classify the status
        data_clean['Change'] = data_clean['After Update Clicks'] - data_clean['Before Update Clicks']
        data_clean['Status'] = ['Improved' if row['Change'] > 0 else 'Worsened' if row['Change'] < 0 else 'No Change'
                                for _, row in data_clean.iterrows()]

        # Scatter plot with Before vs After Update Clicks
        fig2 = px.scatter(data_clean,
                          x='Before Update Clicks', 
                          y='After Update Clicks', 
                          color='Status',
                          hover_data=['Top queries', 'Change', 'Before Update Clicks', 'After Update Clicks'],
                          labels={'Before Update Clicks': 'Clicks Before Update',
                                  'After Update Clicks': 'Clicks After Update'},
                          title="Impact of Update on Clicks",
                          color_discrete_map={'Improved': 'green', 'Worsened': 'red', 'No Change': 'blue'})

        # 3. Pie chart showing the percentage of Improved, Worsened, No Change statuses
        # Calculate the counts of each status
        status_counts = data_clean['Status'].value_counts()

        fig3 = px.pie(
            names=status_counts.index, 
            values=status_counts.values, 
            title='Click Status Distribution After Update'
        )

        # Display the DataFrame with Streamlit
        st.write("Here is the dataset used for the analysis:")
        st.dataframe(data_clean)

        # Show the plots
        st.plotly_chart(fig1)  # Bar chart comparison for Before vs After Update Clicks
        st.plotly_chart(fig2)  # Scatter plot for Before vs After Update Clicks
        st.plotly_chart(fig3)  # Pie chart for click status distribution

    else:
        st.error("The uploaded file must contain 'Top queries', '3/7/25 - 3/12/25 Clicks', and '3/14/25 - 3/18/25 Clicks' columns.")
