import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
DISCOVERY_URL = os.getenv("DISCOVERY_URL")

async def register(username: str, host: str, port: int):
    async with httpx.AsyncClient() as client:
        peer_data = {"username": username, "host": host, "port": port}
        response = await client.post(f"{DISCOVERY_URL}/register/", json=peer_data)
        print("Response:", response.status_code, response.json() if response.status_code == 200 else response.text)

async def available_peers():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DISCOVERY_URL}/available")
        if response.status_code == 200:
            peers = response.json()
            print("Available peers:", peers)
            return peers
        return []

async def handle_client(reader, writer):
    data = await reader.read(1000)
    print(f"\nMessage received: {data.decode()}")

async def tcp_server(host: str, port: int):
    server = await asyncio.start_server(handle_client, host, port)
    async with server:
        print(f"Listening on {host}:{port}...")
        await server.serve_forever()

async def send_message(peer_host: str, peer_port: int, msg: str):
    reader, writer = await asyncio.open_connection(peer_host, peer_port)
    writer.write(msg.encode())
    await writer.drain()
    print(f"Sent \"{msg}\"")
    writer.close()
    await writer.wait_closed()

async def main():
    username = input("Enter your username: ")
    host = "0.0.0.0"
    port = int(input("Enter your port: "))

    await register(username, host, port)

    asyncio.create_task(tcp_server(host, port))

    while True:
        cmd = input("\nCommand (list/send/quit): ").lower().strip()
        if cmd == "list":
            await available_peers()
        elif cmd == "send":
            peers = await available_peers()
            if not peers:
                continue
            target = input("Enter target username: ")
            peer = next((p for p in peers if p["username"] == target), None)
            if peer:
                msg = input("Enter message: ")
                await send_message(peer["host"], peer["port"], f"{username}: {msg}")
            else:
                print("Peer not found")
        elif cmd == "quit":
            print("Exiting...")
            break

if __name__ == "__main__":
    asyncio.run(main())
