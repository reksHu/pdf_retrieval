import attr
from typing import List
from path import Path


@attr.s(auto_attribs=True)
class Configuration:
    keywords: List = attr.ib(default=[])
    raw_file_location: str = attr.ib(default="")
    excel_file: str = attr.ib(default="result.xlsx")