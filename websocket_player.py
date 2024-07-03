import asyncio
import websockets
import json

# Load JSON data from the file
try:
    with open('Data.txt', 'r') as f:
        json_data = f.readlines()
        print(f"Loaded {len(json_data)} lines of data from file.")
except Exception as e:
    print(f"Error reading JSON file: {e}")
    json_data = []

async def send_data(websocket, path):
    try:
        print("Client connected")
        while True:  # Loop to send data continuously
            for line in json_data:
                await websocket.send(line.strip())
                print(f"Sent data: {line.strip()}")
                await asyncio.sleep(0.05)  # Add delay to simulate real-time data stream
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed with error: {e}")
    except Exception as e:
        print(f"Error sending data: {e}")

async def start_server():
    while True:
        try:
            server = await websockets.serve(send_data, "0.0.0.0", 2053)
            print("WebSocket server started on ws://0.0.0.0:2053")
            await server.wait_closed()
        except Exception as e:
            print(f"Error starting or running WebSocket server: {e}")
            print("Restarting server in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    print("Starting WebSocket server...")
    asyncio.run(start_server())
