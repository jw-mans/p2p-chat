import asyncio
import logging as log
from peer_requests.register import register
from peer_requests.available_peers import available_peers
from peer_requests.send import send
from tcp.server import tcp_server
from account.account import Account

async def main():
    acc = Account.load()
    if not acc:
        username = input("Enter your username: ")
        host = "127.0.0.1"  # local test
        port = int(input("Enter your port: "))

        from models.peer import Peer
        peer = Peer(username, host, port)
        acc = Account(peer)
        log.info("Account created")
    else:
        log.info(f"Loaded account: {acc.username} ({acc.host}:{acc.port})")

    # TCP-server task
    server_task = asyncio.create_task(tcp_server(host, port))
    # pause to reach start
    await asyncio.sleep(0.1)

    await register(username, host, port)

    while True:
        cmd = input("\nCommand (list/send/quit): ").lower().strip()
        log.debug(f"\"{cmd}\" command choosen")
        if cmd == "list":
            await available_peers()
        elif cmd == "send":
            peers = await available_peers()
            if not peers:
                log.info("Peers not found.")
                continue
            target = input("Enter target username: ")
            peer = next((p for p in peers if p["username"] == target), None)
            if peer:
                msg = input("Enter message: ")
                await send(peer["host"], peer["port"], f"{username}: {msg}")
            else:
                log.info("Peer not found")
        elif cmd == "quit":
            log.info("Exiting...")
            server_task.cancel()
            break

if __name__ == "__main__":
    asyncio.run(main())
