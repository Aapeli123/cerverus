#!/bin/python3

from typing import List
import config
import argparse
from cerver_process import CerverProcess
import time
class Cerverus:
    def __init__(self, config: config.CerverusConfig, configs_dir: str = "./configs/") -> None:
        self.cervers: List[CerverProcess] = []
        self.configs_dir = configs_dir
        for s in config.servers:
            for i in s.instances:
                self.cervers.append(CerverProcess(f"{configs_dir}{s.name}/{i.tag}.config"))
        self.config = config

    def gen_configs(self):
        self.config.serialize(self.configs_dir)

    def start(self):
        for cerverProc in self.cervers:
            cerverProc.start()
    
    def stop(self):
        for cerverProc in self.cervers:
            cerverProc.stop()

parser = argparse.ArgumentParser(
    prog="cerverus",
    usage="cerverus [config_file]",
)

parser.add_argument("config_file", help="JSON file that defines what servers should run")
parser.add_argument("-c", "--cerver", help="Path to the cerver executable", metavar="executable",required=False, default="./cerver/cerver")
args = parser.parse_args()
print("Welcome to Cerverus:")

print(f"Using config file {args.config_file}")
print(f"Using cerver executable: {args.cerver}")
conf = config.read_config(args.config_file)

cerverus = Cerverus(conf)
cerverus.gen_configs()

cerverus.start()
input()
cerverus.stop()
