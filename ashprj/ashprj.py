import argparse
import json
import os.path
import sys
from datetime import datetime
from typing import Any

from progress.bar import Bar
from pydantic import BaseModel


class AshprjFile(BaseModel):
    name: str
    path: str
    content: bytes = b""

    def __key(self):
        return self.content

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, AshprjFile):
            return self.__key() == other.__key()
        return NotImplemented


def ashprj_open(file_name: str):
    print(file_name)
    if os.path.isfile(file_name):
        with open(file_name, "rb") as f:
            file_data = f.read()
        file_data_parts = []
        prev_part = 0
        print(len(file_data))
        limit = int(len(file_data) / 2)
        for cursor in range(0, limit):
            part = file_data[cursor*2:cursor*2+2]
            part_hex = bytes(part).hex()
            if part_hex[0:2] == "66" and part_hex[2:4] != "00":
                cur_part = cursor*2
                file_data_parts.append(file_data[prev_part:cur_part])
                prev_part = cur_part
        for part in file_data_parts:
            print(part)


def main():
    parser = argparse.ArgumentParser(
        prog="ashprj_open",
        description="Attempt to understand Ashampoo Burning Stutio file format *.ashprj",
    )
    parser.add_argument("file_name", type=str, help="File path and name")
    args = parser.parse_args()
    ashprj_open(args.file_name)


if __name__ == "__main__":
    main()
