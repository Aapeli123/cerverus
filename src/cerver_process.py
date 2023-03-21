import subprocess
import signal
# Wrapper for for the subprocess handler
class CerverProcess:
    def __init__(self, config_file: str, cerver_pth: str = "./cerver/cerver") -> None:
        self.config_file = config_file
        self.subprocess = None
        self.__cerver_path = cerver_pth
        print(config_file)

    def start(self):
        self.subprocess = subprocess.Popen([self.__cerver_path, self.config_file])
    
    def stop(self):
        self.subprocess.send_signal(signal.SIGINT)

    def restart(self):
        self.stop()
        self.start()