# sJsonRpc
Wrapper RPC Json Python with class

## Client
- ConnectionControl
- ProxyObject
- RPC_Call

## Server
- RPC_Responser.py

## Setup env
```bash
python3 -m venv .venv
pip3 install -r requirements.txt
pip3 install .

```

## Atention to test

```bash
└── tests
    ├── async_client.py  # Async client using zencomm as socke comunication
    ├── async_server.py  # Async server using zencomm as socke comunication
    ├── client.py        # Client using zencomm as socke comunication
    └── server.py        # Server using zencomm as socke comunication
```
