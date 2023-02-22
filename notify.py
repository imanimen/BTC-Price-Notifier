import websocket
import json
import threading
import os

# Define the symbol to track and the price threshold for the alarm
symbol = 'btcusdt'
threshold = 24687.72

# Define the WebSocket endpoint URL
socket = "wss://stream.binance.com:9443/ws"

# Define a function to handle incoming WebSocket messages
def on_message(ws, message):
    data = json.loads(message)
    if 'e' in data and data['e'] == 'trade':
        symbol_data = data['s'].lower()
        if symbol_data == symbol:
            price = float(data['p'])
            if price < threshold:
                print(f"Alert: {symbol.upper()} price is below {threshold:.2f} USD!")
                os.system('aplay /usr/share/sounds/freedesktop/index.theme')

# Define a function to connect to the WebSocket endpoint
def on_open(ws):
    ws.send(json.dumps({"method": "SUBSCRIBE", "params": [f"{symbol}@trade"], "id": 1}))

# Create a WebSocket object and connect to the endpoint
ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)

# Define a function to run the WebSocket connection in a separate thread
def run_ws():
    ws.run_forever()

# Start the WebSocket connection in a separate thread
thread1 = threading.Thread(target=run_ws)
thread1.start()