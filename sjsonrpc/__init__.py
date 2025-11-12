'''
Created on 20241001
Update on 20251110
@author: Eduardo Pagotto
'''

__json_rpc_version__ : str = '2.0'
__version__ : str = "2.0.0"

class ExceptionJsonRPC(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
