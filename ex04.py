class File:
    owner = "default"

    def __init__(self, name):
        self.name = name
        self.permission = "rwxr--r--"

    def chown(self, owner="default"):
        self.owner = owner

    def ls(self):
        self.ls()


def tabs(times):
    for i in range(times):
        print("\t", end="")


class PlainFile(File):
    className = "PlainFile"

    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return f"{self.className}({self.name})"


class Directory(File):
    className = "Directory"
    fileStr = ""

    def __init__(self, name, fileList):
        super().__init__(name)
        self.list = fileList

    def __str__(self):
        try:
            self.fileStr = self.fileStr + str(self.list[0])
            for others in self.list[1:]:
                self.fileStr = f"{self.fileStr},{str(others)}"
        except IndexError:
            self.fileStr = ""
        return f"{self.className}({self.name},[{self.fileStr}])"

    def findFolder(self, fList, depth):

        for file in fList:
            if file.className == "PlainFile":
                tabs(depth)
                print(f"{file.permission}  {file.owner}  {file.name}")
            else:
                tabs(depth)
                print(f"{file.permission}  {file.owner}  {file.name}")
                depth += 1
                self.findFolder(file.list, depth)
                depth -= 1

    def ls(self, op=""):
        if op == "":
            print(f"{self.permission}  {self.owner}  {self.name}")
            if len(self.list) > 0:
                self.findFolder(self.list, 1)


# FileSystem
class FileSystem:
    fileDir = []

    def __init__(self, Dir):
        self.rootDir = Dir
        self.currentDir = Dir
        self.fileDir.append(self.currentDir)

    def pwd(self):
        path = ""
        for file in self.fileDir:
            path += f"/{file.name}"
        print(path)

    def ls(self):
        # for file in self.currentDir.list:
        #     print(file.name)
        self.currentDir.ls()

    def cd(self, filename):
        if filename == "..":
            if self.currentDir == self.rootDir:
                return
            else:
                del self.fileDir[-1]
                for file in self.fileDir:
                    self.currentDir = file
                return

        else:
            if self.currentDir.className == "PlainFile":
                return
            for file in self.currentDir.list:
                if file.name == filename:
                    if file.className == "PlainFile":
                        print(f"{filename} is not a directory !")
                        return
                    else:
                        self.fileDir.append(file)
                        self.currentDir = file
                        break
        if self.currentDir.name != filename:
            print("The directory does not exist!")

    def create_file(self, name):
        for file in self.currentDir.list:
            if name == file.name:
                print(f"The file {file.name} already exists!")
                return
            else:
                self.currentDir.list += [PlainFile(name)]
                return

    def mkdir(self, name):
        for file in self.currentDir.list:
            if name == file.name:
                print(f"The directory {file.name} already exists!")
                return
            else:
                self.currentDir.list += [Directory(name, [])]
                return

    def rm(self, name):
        for file in self.currentDir.list:
            if name == file.name and file.className == "Directory":
                if file.list:
                    print("The directory is not empty !")
                    return
                self.currentDir.list.remove(file)
                return
        print("The file does not exist !")

    def find(self, name):
        if not self.findAll(name):
            print("File not found !")

    def findAll(self, name):

        global found
        if self.currentDir.className == "PlainFile":
            return
        for file in self.currentDir.list:
            if file.className == "Directory":
                found = False
                self.cd(file.name)
                self.findAll(name)
                if not found:
                    self.cd("..")
                else:
                    return True
            else:
                if file.name == name:
                    found = True
                    self.fileDir.append(file)
                    return f"{self.pwd()}/{name}"
        return False

    def chown_R(self, newOwner):
        self.currentDir.chown(newOwner)
        if self.currentDir.className == "PlainFile":
            return
        for file in self.currentDir.list:
            if file.className == "Directory":
                file.chown(newOwner)
                self.cd(file.name)
                self.chown_R(newOwner)
                self.cd("..")
            else:
                file.chown(newOwner)

    def chmod(self, command, filename):
        pers = [4, 2, 1, 0]
        pers_cs = ["r", "w", "x", "-"]
        bit = [0, 0, 0]
        if len(command) != 3:
            print("Command not right !")
            return
        for file in self.currentDir.list:
            if file.name == filename:
                temp = ""
                # Problem
                for index in range(0, len(command)):
                    i, j, k = calPer(pers, int(command[index]))

                    temp += pers_cs[i] + pers_cs[j] + pers_cs[k]
                    # file.permission[i*3-3:i*3-1] =
                    file.permission = temp
                    print(i, j, k)
                return
        print(f"{filename} is not here !")

    def mv(self, filepath, path):
        localPath = []
        targetPath = []
        temp = ""

        for index in range(len(path)):
            if path[index] == "/":
                targetPath.append(temp)
                temp = ""
            else:
                temp += path[index]

        for index in range(len(filepath)):
            if filepath[index] == "/":
                localPath.append(temp)
                temp = ""
            else:
                temp += filepath[index]
        print(localPath)
        print(targetPath)


def calPer(pers, num):
    for i in range(len(pers)):
        for j in range(len(pers)):
            for k in range(len(pers)):
                if pers[i] + pers[j] + pers[k] == num:
                    return i, j, k


root = Directory("root", [PlainFile("boot.exe"), Directory("home", [
    Directory("thor", [PlainFile("hunde.jpg"), PlainFile("quatsch.txt")]),
    Directory("isaac", [PlainFile("gatos.jpg")])])])

# print(root)

# file = PlainFile("boot.exe")
# folder = Directory("Downloads", [])
# print(f'file.owner: {file.owner}; folder: {folder.owner}')
#
# file.chown("root")
# folder.chown("isaac")
# print(f'file.owner: {file.owner}; folder: {folder.owner}')

# root.ls()

fs = FileSystem(root)

fs.pwd()
fs.cd("home")
# fs.ls()
fs.cd("isaac")
# fs.ls()
fs.pwd()
fs.cd("..")
fs.pwd()
# fs.ls()
fs.create_file("lfz")
# fs.ls()
fs.mkdir("2333333")
# fs.ls()
fs.find("lfz")
# fs.ls()
fs.chown_R("root")
fs.pwd()
fs.chmod("777", "lfz")
fs.chmod("531", "2333333")
fs.mkdir("wwww")
fs.rm("wwww")
fs.ls()
fs.mv("/root/home/lfz", "/root/home/thor")
