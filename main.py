import zipfile
import datetime


class VShell:
    def __init__(self):
        self.currentPath = "iso/"
        self.directory = zipfile.ZipFile('iso.zip', 'r')
        self.directory.extractall()

        self.commands = {
            "pwd": self.pwd,
            "ls": self.ls,
            "cat": self.cat,
            "cd": self.cd
        }
        self.commandsKeys = ["pwd", "ls", "cat", "cd"]

    def changePath(self, path):
        res = ""

        if len(path) >= 2 and path[:2] == '..':
            path = '/'.join(self.currentPath[:-1].split('/')[:-path.count('..')])
            if path != "":
                path += "/"
                if path in self.directory.namelist() or path == "iso/":
                    res = path

        elif self.currentPath + path in self.directory.namelist():
            res = self.currentPath + path

        return res

    def pwd(self, arg):
        print(self.currentPath)

    def ls(self, drc):
        if len(drc) != 0:
            path = self.changePath(drc[0])
        else:
            path = self.currentPath
        if path == "":
            print("ls: can't cd to " + drc[0] + ": No such file or directory")
        else:
            for file in self.directory.infolist():
                date = datetime.datetime(*file.date_time)
                name = file.filename
                if (len(path) < len(name) and name[:len(path)] == path)\
                        and path.count('/') == name[:-1].count('/'):
                    print(f"{name:15}\t{file.file_size:5}\t {date.strftime('%H:%M %d.%m.%Y'):15}")

    def cat(self, fileName):  # Функция
        if not len(fileName):
            text = input()
            print(text)
        else:
            path = self.changePath(fileName[0]);
            if path == "":
                print("cat: can't cd to " + fileName[0] + ": No such file or directory")
            else:
                file = self.directory.open(path)
                print(file.read().decode("utf-8"))

    def cd(self, drc):
        if len(drc) == 0:
            self.currentPath = "iso/"
        else:
            path = self.changePath(drc[0])
            if path == '':
                print("cd: can't cd to " + drc[0] + ": No such file or directory")
            else:
                self.currentPath = path

    def runTheCommand(self, command):
        if len(command) == 0:
            pass
        elif command[0] not in self.commandsKeys:
            print(str(command[0])+': command not found')
        else:
            self.commands.get(command[0])(command[1:])

    def run(self):
        while True:
            command = input(self.currentPath + ": ").split()
            self.runTheCommand(command)


if __name__ == '__main__':
    vshell = VShell()
    vshell.run()