import websocket
import json

def on_open(ws):
    subMsg = {"method": "SUBSCRIBE","params":["btcusdt@markPrice@1s"],"id": 1}
    ws.send(json.dumps(subMsg))
    print("Opened connection")

def on_message(ws, message):
    data = json.loads(message)
    print(data["p"])

url = "wss://fstream.binance.com/ws"
ws = websocket.WebSocketApp(url,on_open=on_open,on_message=on_message)
ws.run_forever()