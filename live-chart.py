import plotly.graph_objs as go
import websocket
import json
import threading
import time

# Define the symbols to track
symbols = ['btcusdt', 'ethusdt']

# Define the WebSocket endpoint URL
socket = "wss://stream.binance.com:9443/ws"

# Define the initial data for the line chart
data = {}
for symbol in symbols:
    data[symbol] = {'timestamps': [], 'prices': []}

# Define a function to handle incoming WebSocket messages
def on_message(ws, message):
    data = json.loads(message)
    if 'e' in data and data['e'] == 'trade':
        symbol = data['s'].lower()
        if symbol in symbols:
            price = float(data['p'])
            timestamp = data['T'] / 1000
            data[symbol]['timestamps'].append(timestamp)
            data[symbol]['prices'].append(price)
            update_chart()

# Define a function to connect to the WebSocket endpoint
def on_open(ws):
    for symbol in symbols:
        ws.send(json.dumps({"method": "SUBSCRIBE", "params": [f"{symbol}@trade"], "id": 1}))

# Create a WebSocket object and connect to the endpoint
ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)

# Define a function to run the WebSocket connection in a separate thread
def run_ws():
    ws.run_forever()

# Define a function to update the line chart with the latest data
def update_chart():
    traces = []
    for symbol in symbols:
        trace = go.Scatter(x=data[symbol]['timestamps'], y=data[symbol]['prices'], name=symbol.upper())
        traces.append(trace)
    layout = go.Layout(title='Live Cryptocurrency Prices', xaxis=dict(title='Time'), yaxis=dict(title='Price (USD)'))
    fig = go.Figure(data=traces, layout=layout)
    fig.show()

# Start the WebSocket connection and update the chart in separate threads
thread1 = threading.Thread(target=run_ws)
thread1.start()

# Keep the main thread running to continue updating the chart
while True:
    update_chart()
    time.sleep(10)