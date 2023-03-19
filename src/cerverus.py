import config

class Cerverus:
    def __init__(self, config: config.CerverusConfig) -> None:
        self.config = config

    def gen_configs(self):
        self.config.serialize()
    def start():
        pass


conf = config.read_config("./cerverus.json")

cerverus = Cerverus(conf)
cerverus.gen_configs()
