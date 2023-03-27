import json
import os
import multiprocessing
from typing import Optional, Dict, List
def get_threads_for_instance(instances: int) -> int:
    return multiprocessing.cpu_count() // instances

class CerverInstance:
    def __init__(self, tag: str, port: int, ssl: bool, privkey: Optional[str], pubkey: Optional[str], routes: Optional[Dict[str, str]] = None, redirects: Optional[Dict[str, str]] = None) -> None:
        self.port = port
        self.ssl = ssl
        self.tag = tag
        self.routes = routes
        self.redirects = redirects
        if self.ssl and privkey != None and pubkey != None:
            self.privkey = privkey
            self.pubkey = pubkey
    def get_str(self) -> str:
        sslstr = f"""ssl
sslkeys {self.pubkey} {self.privkey}""" if self.ssl else ""
        return f"""port {self.port}
{sslstr}\n{self.__get_routes_and_redirs()}"""
    def __get_routes_and_redirs(self) -> str:
        routestr = ""
        if self.routes != None:
            for route in self.routes:
                routestr += f"loc {route} {self.routes[route]}\n"
        
        if self.redirects != None:
            for redir in self.redirects:
                routestr += f"redirect {redir} {self.redirects[redir]}\n"

        return routestr

class CerverusServer:
    def __init__(self, name: str, instances: List[CerverInstance], routes: Dict[str, str], root: str, fallback: str, redirects: Optional[Dict[str, str]] = None, threads=0) -> None:
        self.name = name
        self.instances = instances
        self.routes = routes
        self.redirects = redirects
        self.root = root
        self.fallback = fallback
        self.threads = threads
    def __get_str(self) -> str:
        routestr = ""
        for route in self.routes:
            routestr += f"loc {route} {self.routes[route]}\n"

        if self.redirects != None:
            for redir in self.redirects:
                routestr += f"redirect {redir} {self.redirects[redir]}\n"

        return f"""root {self.root}
threads {self.threads}
{routestr}
fallback {self.fallback}"""

    def serialize(self, dirpath = "./configs/"):
        for instance in self.instances:
            path = f"{dirpath}{self.name}/{instance.tag}.config"
            if not os.path.exists(f"{dirpath}{self.name}/"):
                os.makedirs(f"{dirpath}{self.name}/")
            server_str = self.__get_str()
            instance_specific_str = instance.get_str()
            server_config_str = f"""{server_str}\n{instance_specific_str}"""
            with open(path, "w") as outfile:
                outfile.write(server_config_str)

    


class CerverusConfig:
    def __init__(self, servers: List[CerverusServer]) -> None:
        self.servers: list[CerverusServer] = servers
    def serialize(self, config_files_loc="./configs/"):
        for server in self.servers:
            server.serialize(config_files_loc)
            pass


def get_dict_optional(dictionary, key):
    try:
        return dictionary[key]
    except KeyError:
        return None 
    

def read_config(config_file: str) -> CerverusConfig:
    with open(config_file) as conf_json:
        servers = json.load(conf_json)
        server_list = []
        for server in servers:
            server_routes = server["paths"]
            server_redirects = get_dict_optional(server, "redirects")
            fallback = server["fallback"]
            root = server["root"]
            name = server["name"]

            instances = []
            for i in server["instances"]:
                port = i["port"]
                tag = i["tag"]
                i_routes = get_dict_optional(i, "paths")
                i_redirects = get_dict_optional(i, "redirects")
                privkey = None
                pubkey = None
                try:
                    ssl = i["ssl"]
                    if ssl:
                        pubkey = i["ssl_pub"]
                        privkey = i["ssl_priv"]
                except KeyError:
                    ssl = False
                instance = CerverInstance(tag, port, ssl, privkey, pubkey, i_routes, i_redirects)
                instances.append(instance)
            s = CerverusServer(name, instances, server_routes, root, fallback, server_redirects, threads=get_threads_for_instance(len(instances)))
            server_list.append(s)
    return CerverusConfig(server_list)