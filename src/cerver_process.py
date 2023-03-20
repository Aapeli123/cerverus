import subprocess
import signal
# Wrapper for for the subprocess handler
class CerverProcess:
    def __init__(self, config_file: str, cerver_pth: str = "./cerver/cerver") -> None:
        self.config_file = config_file
        self.subprocess = None
        self.__cerver_path = cerver_pth

    def start(self):
        self.subprocess = subprocess.Popen(self.config_file, executable=self.__cerver_path)
        pass
    
    def stop(self):
        self.subprocess.send_signal(signal.SIGINT)
        output = str(self.subprocess.stdout)
        print(f"PROCESS OUTPUT:\n{output}")

    def restart(self):
        self.stop()
        self.start()