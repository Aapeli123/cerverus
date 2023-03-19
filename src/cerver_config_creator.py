import json

class CerverConfig:
    def __init__(self) -> None:
        pass    

def read_config(config_file: str) -> CerverConfig:
    with open(config_file) as conf_json:
        data = json.load(conf_json)
        print(data)
    return CerverConfig()