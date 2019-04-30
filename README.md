# toach-fix-connector

## Commands to build and run acceptor (server) and initiator (client) applications

1. Build docker compose
    - docker-compose --file docker-compose.yml build
2. Check if all services are running
    - docker-compose --file docker-compose.yml ps
3. Execute it on one terminal to view server's logs
    - docker logs --tail 100 -f server
4. Open another terminal window and execute to attach bash to running initiator service
    - docker exec -it client bash
5. Execute python script in initiator's bash
    - python3 initiator_runner.py
6. Press 1 to send SecurityDefinitionRequest message
7. Logs will appear in acceptor terminal and initiator terminal