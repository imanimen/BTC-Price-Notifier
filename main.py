import plotly.graph_objs as go
import requests

# Define the URL for the API endpoint and the parameters to pass
url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
params = {'vs_currency': 'usd', 'days': '30'}

# Send a GET request to the API and get the response
response = requests.get(url, params=params).json()

# Extract the prices and timestamps from the response
prices = [price[1] for price in response['prices']]
timestamps = [timestamp[0] for timestamp in response['prices']]

# Create a line chart using Plotly
fig = go.Figure(data=go.Scatter(x=timestamps, y=prices))
fig.update_layout(title='Bitcoin Prices over the last 30 days')
fig.show()