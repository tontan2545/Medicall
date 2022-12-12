import ast
from typing import Union

from serial import Serial

from utils.port import get_port


def decode_data(data) -> list:
    str_data = str(data, 'utf-8')
    if type(str_data) == dict:
        dict_data = ast.literal_eval(str_data)
    else:
        dict_data = {}
    return dict_data


class STM32Serial:

    def __init__(self, port: str = None):
        self.reader = Serial(port=get_port(port), baudrate=115200, timeout=.1)

    def read_serial(self) -> Union[str, dict]:
        data = self.reader.readline()
        str_data = str(data, 'utf-8')
        if str_data != "":
            return ast.literal_eval(str_data)
        else:
            return ""
