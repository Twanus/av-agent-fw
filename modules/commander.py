from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self, client):
        pass


# TESTING
class DetectOSCommand(Command):
    def execute(self, client):
        stdin, stdout, stderr = client.exec_command(
            "cat /etc/os-release | grep '^ID='"
        )
        output = stdout.read().decode()
        return output.split("=")[1].strip()


class PlainCommand(Command):
    def __init__(self, command):
        self.command = command

    def execute(self, client):
        stdin, stdout, stderr = client.exec_command(f"{self.command}")
        return stdout.read().decode()


class EchoCommand(Command):
    def __init__(self, message):
        self.message = message

    def execute(self, client):
        stdin, stdout, stderr = client.exec_command(f"echo {self.message}")
        return stdout.read().decode()


class ListFilesCommand(Command):
    def __init__(self, directory):
        self.directory = directory

    def execute(self, client):
        stdin, stdout, stderr = client.exec_command(f"ls {self.directory}")
        return stdout.read().decode()
