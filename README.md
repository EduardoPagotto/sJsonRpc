# sJsonRpc
Wrapper RPC Json Python with class

## Client
- ConnectionControl
- ProxyObject
- RPC_Call

# Server
- RPC_Responser.py

# Setup env
```bash
python3 -m venv .venv
pip3 install -r requirements.txt
pip3 install .

# install dev
pip3 install -e .

#install to env
python setup.py install

# Criará um arquivo .tar.gz no diretório dist.
python setup.py sdist

#  Isso criará um arquivo .whl no diretório dist, que pode ser instalado mais rapidamente.
python setup.py bdist_wheel .
```
