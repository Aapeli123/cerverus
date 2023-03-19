import json
import os
class CerverInstance:
    def __init__(self, tag: str, port: int, ssl: bool, privkey: str | None, pubkey: str | None) -> None:
        self.port = port
        self.ssl = ssl
        self.tag = tag
        if self.ssl and privkey != None and pubkey != None:
            self.privkey = privkey
            self.pubkey = pubkey
    def get_str(self) -> str:
        sslstr = f"""ssl
sslkeys {self.pubkey} {self.privkey}""" if self.ssl else ""
        return f"""port {self.port}
{sslstr}
        """
        
class CerverusServer:
    def __init__(self, name: str, instances: list[CerverInstance], routes: dict[str, str], root: str, fallback: str) -> None:
        self.name = name
        self.instances = instances
        self.routes = routes
        self.root = root
        self.fallback = fallback
    
    def __get_str(self) -> str:
        routestr = ""
        for route in self.routes:
            routestr += f"loc {route} {self.routes[route]}\n"

        return f"""root {self.root}
{routestr}
fallback {self.fallback}
        """

    def serialize(self, dirpath = "./configs/"):
        for instance in self.instances:
            path = f"{dirpath}{self.name}/{instance.tag}.config"
            if not os.path.exists(f"{dirpath}{self.name}/"):
                os.makedirs(f"{dirpath}{self.name}/")
            server_str = self.__get_str()
            instance_specific_str = instance.get_str()
            server_config_str = f"""{instance_specific_str}
{server_str}
            """
            with open(path, "w") as outfile:
                outfile.write(server_config_str)

    


class CerverusConfig:
    def __init__(self, servers: list[CerverusServer]) -> None:
        self.servers: list[CerverusServer] = servers
    def serialize(self, config_files_loc="./configs/"):
        for server in self.servers:
            server.serialize(config_files_loc)
            pass
            

def read_config(config_file: str) -> CerverusConfig:
    with open(config_file) as conf_json:
        servers = json.load(conf_json)
        server_list = []
        for server in servers:
            routes = server["paths"]
            fallback = server["fallback"]
            root = server["root"]
            name = server["name"]

            instances = []
            for i in server["instances"]:
                port = i["port"]
                tag = i["tag"]
                privkey = None
                pubkey = None
                try:
                    ssl = i["ssl"]
                    if ssl:
                        pubkey = i["ssl_pub"]
                        privkey = i["ssl_priv"]
                except KeyError:
                    ssl = False
                instance = CerverInstance(tag, port, ssl, privkey, pubkey)
                instances.append(instance)
            s = CerverusServer(name, instances, routes, root, fallback)
            server_list.append(s)
    return CerverusConfig(server_list)