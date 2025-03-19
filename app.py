import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

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
        data_clean['Status'] = ['Improved' if row['Change'] > 0 else 'Worsened' if row['Change'] < 0 else 'Lost'
                                for _, row in data_clean.iterrows()]

        # 1. Grouped Bar Chart: Before and After Clicks
        fig1 = px.bar(data_clean, 
                      x='Top queries', 
                      y=['Before Update Clicks', 'After Update Clicks'], 
                      title="Before and After Update Clicks Comparison",
                      labels={'Top queries': 'Query', 'value': 'Clicks'},
                      color_discrete_map={'Before Update Clicks': 'blue', 'After Update Clicks': 'green'})

        # 2. Heatmap: Change in Clicks Across Queries (using Plotly)
        # Using pivot_table instead of pivot to handle duplicate queries
        heatmap_data = data_clean.pivot_table(index='Top queries', columns='Status', values='Change', aggfunc='mean')

        fig2 = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='Viridis',  # You can change this to any colorscale you prefer
        ))

        fig2.update_layout(
            title='Heatmap of Click Changes by Query Status',
            xaxis=dict(title='Status'),
            yaxis=dict(title='Queries'),
        )

        # 3. Box Plot: Distribution of Clicks Before and After Update
        fig3 = px.box(data_clean, 
                      x="Status", 
                      y="Before Update Clicks", 
                      points="all", 
                      title="Distribution of Clicks Before Update",
                      labels={'Before Update Clicks': 'Clicks'})

        fig4 = px.box(data_clean, 
                      x="Status", 
                      y="After Update Clicks", 
                      points="all", 
                      title="Distribution of Clicks After Update",
                      labels={'After Update Clicks': 'Clicks'})

        # 4. Scatter Plot: Impact of Update (using Absolute Size for better visualization)
        fig5 = px.scatter(data_clean,
                          x='Before Update Clicks', 
                          y='After Update Clicks', 
                          size=np.abs(data_clean['Change']),  # Use absolute size for the points
                          color='Status',
                          title="Impact of Update on Clicks",
                          labels={'Before Update Clicks': 'Clicks Before Update',
                                  'After Update Clicks': 'Clicks After Update'})

        # 5. Pie Chart: Percentage of Queries Improved, Worsened, or Lost
        fig6 = px.pie(data_clean, 
                      names='Status', 
                      title="Impact of Update on Queries (Improved, Worsened, Lost)",
                      labels={'Status': 'Update Impact'})

        # 6. Cumulative Distribution Function (CDF) using Plotly
        before_clicks = np.sort(data_clean['Before Update Clicks'])
        y_before = np.arange(1, len(before_clicks) + 1) / len(before_clicks)
        after_clicks = np.sort(data_clean['After Update Clicks'])
        y_after = np.arange(1, len(after_clicks) + 1) / len(after_clicks)

        fig7 = go.Figure()

        fig7.add_trace(go.Scatter(
            x=before_clicks, 
            y=y_before, 
            mode='lines', 
            name='Before Update',
            line=dict(color='blue')
        ))

        fig7.add_trace(go.Scatter(
            x=after_clicks, 
            y=y_after, 
            mode='lines', 
            name='After Update',
            line=dict(color='green')
        ))

        fig7.update_layout(
            title='CDF of Clicks Before and After Update',
            xaxis=dict(title='Clicks'),
            yaxis=dict(title='CDF'),
            showlegend=True
        )

        # Display the DataFrame with Streamlit
        st.write("Here is the dataset used for the analysis:")
        st.dataframe(data_clean)

        # Show the plots
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
        st.plotly_chart(fig3)
        st.plotly_chart(fig4)
        st.plotly_chart(fig5)
        st.plotly_chart(fig6)
        st.plotly_chart(fig7)
    else:
        st.error("The uploaded file must contain 'Top queries', '3/7/25 - 3/12/25 Clicks', and '3/14/25 - 3/18/25 Clicks' columns.")
