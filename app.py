import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

# Generate sample data similar to the one you're working with
np.random.seed(42)
data = {
    'Top queries': [f"Query {i}" for i in range(1, 21)],
    '3/7/25 - 3/12/25 Clicks': np.random.randint(50, 200, 20),
    '3/14/25 - 3/18/25 Clicks': np.random.randint(50, 200, 20)
}

data_clean = pd.DataFrame(data)
data_clean['Before Update Clicks'] = data_clean['3/7/25 - 3/12/25 Clicks']
data_clean['After Update Clicks'] = data_clean['3/14/25 - 3/18/25 Clicks']
data_clean['Change'] = data_clean['After Update Clicks'] - data_clean['Before Update Clicks']
data_clean['Status'] = ['Improved' if row['Change'] > 0 else 'Worsened' if row['Change'] < 0 else 'Lost'
                        for _, row in data_clean.iterrows()]

# Create a grouped bar chart: Before and After Clicks
fig1 = px.bar(data_clean, 
              x='Top queries', 
              y=['Before Update Clicks', 'After Update Clicks'], 
              title="Before and After Update Clicks Comparison",
              labels={'Top queries': 'Query', 'value': 'Clicks'},
              color_discrete_map={'Before Update Clicks': 'blue', 'After Update Clicks': 'green'})

# Create a heatmap: Change in Clicks Across Queries
pivot_data = data_clean.pivot('Top queries', 'Status', 'Change')
plt.figure(figsize=(10, 6))
sns.heatmap(pivot_data, annot=True, cmap="coolwarm", center=0)
plt.title('Heatmap of Click Changes by Query Status')
plt.show()

# Create a box plot: Distribution of Clicks Before and After Update
fig2 = px.box(data_clean, 
              x="Status", 
              y="Before Update Clicks", 
              points="all", 
              title="Distribution of Clicks Before Update",
              labels={'Before Update Clicks': 'Clicks'})

fig3 = px.box(data_clean, 
              x="Status", 
              y="After Update Clicks", 
              points="all", 
              title="Distribution of Clicks After Update",
              labels={'After Update Clicks': 'Clicks'})

# Scatter Plot: Impact of Update (using Absolute Size for better visualization)
fig4 = px.scatter(data_clean,
                  x='Before Update Clicks', 
                  y='After Update Clicks', 
                  size=np.abs(data_clean['Change']),  # Use absolute size for the points
                  color='Status',
                  title="Impact of Update on Clicks",
                  labels={'Before Update Clicks': 'Clicks Before Update',
                          'After Update Clicks': 'Clicks After Update'})
fig4.show()

# Pie Chart: Percentage of Queries Improved, Worsened, or Lost
fig5 = px.pie(data_clean, 
              names='Status', 
              title="Impact of Update on Queries (Improved, Worsened, Lost)",
              labels={'Status': 'Update Impact'})
fig5.show()

# Cumulative Distribution Function (CDF)
before_clicks = np.sort(data_clean['Before Update Clicks'])
y_before = np.arange(1, len(before_clicks) + 1) / len(before_clicks)
after_clicks = np.sort(data_clean['After Update Clicks'])
y_after = np.arange(1, len(after_clicks) + 1) / len(after_clicks)

plt.figure(figsize=(10, 6))
plt.plot(before_clicks, y_before, label='Before Update')
plt.plot(after_clicks, y_after, label='After Update')
plt.title('CDF of Clicks Before and After Update')
plt.xlabel('Clicks')
plt.ylabel('CDF')
plt.legend()
plt.show()

# Show the example figures for Streamlit
import ace_tools as tools; tools.display_dataframe_to_user(name="Example Data", dataframe=data_clean)
