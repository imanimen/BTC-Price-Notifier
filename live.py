import websocket
import json
import threading
import time

# Define the symbols to track
symbols = ['btcusdt', 'ethusdt']

# Define the WebSocket endpoint URL
socket = "wss://stream.binance.com:9443/ws"

# Define a function to handle incoming WebSocket messages
def on_message(ws, message):
    data = json.loads(message)
    if 'e' in data and data['e'] == 'trade':
        symbol = data['s'].lower()
        if symbol in symbols:
            price = float(data['p'])
            print(f'{symbol.upper()} price: {price}')

# Define a function to connect to the WebSocket endpoint
def on_open(ws):
    for symbol in symbols:
        ws.send(json.dumps({"method": "SUBSCRIBE", "params": [f"{symbol}@trade"], "id": 1}))

# Create a WebSocket object and connect to the endpoint
ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)

# Define a function to run the WebSocket connection in a separate thread
def run_ws():
    ws.run_forever()

# Start the WebSocket connection in a separate thread
thread = threading.Thread(target=run_ws)
thread.start()

# Keep the main thread running to continue printing price updates
while True:
    time.sleep(10)