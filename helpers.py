import os

import yaml
from path import Path

from configuration import Configuration


def get_package_root_path():
    """
    获取程序运行根目录
    :return:
    """
    return os.path.dirname(__file__)


def get_results_path() -> Path:
    return Path(get_package_root_path()) / "results"


def load_config() -> Configuration:
    config_path = "config.yaml"
    content = Path(config_path).read_text(encoding="utf-8")
    c_loader = yaml.load(content, yaml.FullLoader)
    configuration = Configuration(**c_loader["configuration"])
    return configuration