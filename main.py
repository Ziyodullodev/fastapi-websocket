from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

origins = ["*"]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Group Chat</title>
</head>
<body>
    <input id="roomInput" type="text" placeholder="Chat Room Name">
    <input id="nameInput" type="text" placeholder="Your Name">
    <input id="messageInput" type="text" placeholder="Type your message">
    <button onclick="joinRoom()">Join Room</button>
    <button onclick="sendMessage()">Send</button>
    <div id="chatMessages"></div>

    <script>
        const roomInput = document.getElementById("roomInput");
        const nameInput = document.getElementById("nameInput");
        const messageInput = document.getElementById("messageInput");
        const chatMessages = document.getElementById("chatMessages");
        let socket;

        function joinRoom() {
            const room = roomInput.value;
            socket = new WebSocket(`wss://your_domain.uz/chat/${room}`); # edit this place your domain
            socket.onmessage = function(event) {
                const messageDiv = document.createElement("div");
                messageDiv.textContent = event.data;
                chatMessages.appendChild(messageDiv);
            };
        }

        function sendMessage() {
            const message = messageInput.value;
            const name = nameInput.value;
            socket.send(`${name}: ${message}`);
            messageInput.value = "";
        }
    </script>
</body>
</html>

"""

@app.get("/chat")
async def get():
    return HTMLResponse(chat_template)


active_connections: Dict[str, List[WebSocket]] = {}

@app.websocket("/chat/{room}")
async def websocket_endpoint(room: str, websocket: WebSocket):
    await websocket.accept()
    if room not in active_connections:
        active_connections[room] = []
    active_connections[room].append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            print(f"Message received from {room}: {data}")
            # Broadcast message to all WebSocket connections in the same room
            for ws in active_connections[room]:
                await ws.send_text(data)
    except:
        active_connections[room].remove(websocket)
