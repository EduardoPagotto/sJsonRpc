# Simple Json RPC Wrapper (sJsonRpc)
Just a simple Json RPC Python wrapper class

## Client class
New connections kind just overload "ConnectionControl.py" with any protocol/socket<p>
In ./tests/ has a several examples using zencomm(simple binary socket protocol)

## Server class
New server just overload "RPC_Responser.py" using any kind of socket/protocol

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
