from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from stem.control import Controller
import stem.process
from .models import OnionRequest, TorResponse
import asyncio
import base64
import socket
import socks

app = FastAPI()

# Enable CORS for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Entry Proxy"}

@app.post("/relay", response_model=TorResponse)
async def relay_package(request: OnionRequest):
    """
    Accept an onion package and forward it to the Tor network.
    The package is expected to be pre-encrypted from the browser.
    """
    try:
        # Validate package structure
        if not request.packages or len(request.packages) != 3:
            raise HTTPException(
                status_code=400,
                detail="Invalid package structure. Must contain exactly 3 layers."
            )

        # Connect to Tor controller
        controller = Controller.from_port()
        await asyncio.to_thread(controller.authenticate)

        try:
            # Create circuit using the specified entry node
            circuit_id = await asyncio.to_thread(
                controller.new_circuit,
                [request.entry_node],
                await_build=True
            )

            # Configure SOCKS proxy
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket

            # Create a socket connection through Tor
            s = socket.socket()
            s.settimeout(30)  # 30 second timeout

            try:
                # Connect to the onion service
                s.connect((request.packages[-1].next_hop, 80))

                # Send the HTTP request with the encrypted data
                s.send(base64.b64decode(request.packages[-1].data))

                # Receive the response
                response = b""
                while True:
                    try:
                        chunk = s.recv(4096)
                        if not chunk:
                            break
                        response += chunk
                    except socket.timeout:
                        break

                return TorResponse(
                    content=response.decode(),
                    status=200
                )
            finally:
                s.close()
        finally:
            # Clean up
            await asyncio.to_thread(controller.close)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
