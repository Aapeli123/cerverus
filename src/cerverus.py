#!/bin/python3

from typing import List
import config
import argparse
from cerver_process import CerverProcess

class Cerverus:
    def __init__(self, config: config.CerverusConfig) -> None:
        self.cervers: List[CerverProcess] = []
        self.config = config

    def gen_configs(self):
        self.config.serialize()
    def start():
        pass


parser = argparse.ArgumentParser(
    prog="cerverus",
    usage="cerverus [config_file]",
)

parser.add_argument("config_file")
parser.add_argument("-c", "--cerver", help="Path to the cerver executable", metavar="executable",required=False, default="./cerver/cerver")
args = parser.parse_args()
print("Welcome to Cerverus:")

print(f"Using config file {args.config_file}")
print(f"Using cerver executable: {args.cerver}")
conf = config.read_config(args.config_file)

cerverus = Cerverus(conf)
cerverus.gen_configs()
