class File:
    # default value of owner
    owner = "default"

    def __init__(self, name, owner):
        self.name = name
        self.permission = "rwxr--r--"
        self.owner = owner

    def chown(self, owner="default"):
        self.owner = owner

    def ls(self):
        self.ls()


# For print \t in ls()
def tabs(times):
    for i in range(times):
        print("\t", end="")


class PlainFile(File):
    className = "PlainFile"

    def __init__(self, name, owner="default"):
        super().__init__(name, owner)

    # For printing
    def __str__(self):
        return f"{self.className}({self.name})"


class Directory(File):
    className = "Directory"
    fileStr = ""

    def __init__(self, name, fileList, owner="default"):
        super().__init__(name, owner)
        self.list = fileList

    # For printing
    def __str__(self):
        try:
            # Add the tail string
            self.fileStr += str(self.list[0])
            # Print from the second object
            for others in self.list[1:]:
                self.fileStr = f"{self.fileStr},{str(others)}"
                break
        except IndexError:
            self.fileStr = ""
        return f"{self.className}({self.name},[{self.fileStr}])"

    def findFolder(self, fList, depth, op):
        for files in fList:
            if files.className == "PlainFile":
                tabs(depth)
                if op == "-l":
                    print(f"{files.permission}  {files.owner}  {files.name}")
                else:
                    print(f"{files.name}")
            else:
                tabs(depth)
                if op == "-l":
                    print(f"{files.permission}  {files.owner}  {files.name}")
                else:
                    print(f"{files.name}")
                depth += 1
                self.findFolder(files.list, depth, op)
                depth -= 1

    def ls(self, op=""):
        # If here is not ls("-l")
        if op == "":
            print(f"{self.name}")
            if len(self.list) > 0:
                self.findFolder(self.list, 1, op)
        if op == "-l":
            print(f"{self.permission}  {self.owner}  {self.name}")
            if len(self.list) > 0:
                self.findFolder(self.list, 1, op)


# FileSystem
class FileSystem:

    def __init__(self, Dir):
        self.fileDir = []
        self.rootDir = Dir
        self.currentDir = Dir
        self.fileDir.append(Dir)

    def pwd(self):
        # print(f"'{self.currentDir.name}'")
        path = ""
        for files in self.fileDir:
            path += f"/{files.name}"
        # print(path)
        return path

    def ls(self, op=""):
        # for file in self.currentDir.list:
        #     print(file.name)
        self.currentDir.ls(op)

    def cd(self, filename):
        if filename == "..":
            if self.currentDir == self.rootDir:
                return
            else:
                del self.fileDir[-1]
                self.currentDir = self.fileDir[-1]
                # for files in self.fileDir:
                #     self.currentDir = files
                return

        else:
            if self.currentDir.className == "PlainFile":
                return
            for files in self.currentDir.list:
                if files.name == filename:
                    if files.className == "PlainFile":
                        print(f"{filename} is not a directory !")
                        return
                    else:
                        self.fileDir.append(files)
                        self.currentDir = files
                        # break
        if self.currentDir.name != filename:
            print("The directory does not exist!")

    def create_file(self, name):
        if not self.currentDir.list:
            self.currentDir.list += [PlainFile(name)]
        else:
            for files in self.currentDir.list:
                if name == files.name:
                    print(f"The file {files.name} already exists!")
                    return
                else:
                    self.currentDir.list += [PlainFile(name)]
                    return

    def mkdir(self, name, owner="default"):
        if not self.currentDir.list:
            self.currentDir.list += [Directory(name, [], owner)]
        else:
            for files in self.currentDir.list:
                if name == files.name:
                    print(f"The directory {files.name} already exists!")
                    return
                else:
                    self.currentDir.list += [Directory(name, [])]
                    return

    def rm(self, name):
        for files in self.currentDir.list:
            if name == files.name and files.className == "Directory":
                if files.list:
                    print("The directory is not empty !")
                    return
                else:
                    self.currentDir.list.remove(files)
            elif name == files.name and files.className == "PlainFile":
                self.currentDir.list.remove(files)
                return
        print("The file does not exist !")

    def find(self, name):
        global found
        found = False
        for files in self.currentDir.list:
            if files.className == "Directory":
                self.cd(files.name)
                self.find(name)
                if not found:
                    self.cd("..")
            elif files.name == name:
                found = True
                print(f"{self.pwd()}" + "/" + name)
                # return self.pwd() + "/" + name
        return False

    def chown_R(self, newOwner):
        self.currentDir.chown(newOwner)
        if self.currentDir.className == "PlainFile":
            return
        for files in self.currentDir.list:
            if files.className == "Directory":
                files.chown(newOwner)
                self.cd(files.name)
                self.chown_R(newOwner)
                self.cd("..")
            else:
                files.chown(newOwner)

    def chmod(self, command, filename):
        pers = [4, 2, 1, 0]
        pers_cs = ["r", "w", "x", "-"]
        # bit = [0, 0, 0]
        if len(command) != 3:
            print("Command not right !")
            return
        for files in self.currentDir.list:
            if files.name == filename:
                temp = ""
                # Problem
                for index in range(0, len(command)):
                    i, j, k = calPer(pers, int(command[index]))
                    temp += pers_cs[i] + pers_cs[j] + pers_cs[k]
                    # file.permission[i*3-3:i*3-1] =
                    files.permission = temp
                    # print(i, j, k)
                return
        print(f"{filename} is not here !")

    # like [root,home,lfz] [root,home,thor]
    def mv(self, filepath, target):
        localPath = []
        targetPath = []
        temp = ""

        for index in range(len(filepath)):
            if filepath[index] == "/" and index == 0:
                continue
            elif filepath[index] == "/":
                localPath.append(temp)
                temp = ""
            else:
                temp += filepath[index]

        localPath.append(temp)
        temp = ""

        for index in range(len(target)):
            if target[index] == "/" and index == 0:
                continue
            elif target[index] == "/":
                targetPath.append(temp)
                temp = ""
            else:
                temp += target[index]

        targetPath.append(temp)

        # print(localPath)
        # print(targetPath)

        for now in localPath[0:len(localPath) - 1]:
            if self.currentDir.name == now:
                continue
            self.cd(now)
        self.rm(localPath[-1])

        for times in range(len(localPath) - 1):
            self.cd("..")

        for now in targetPath:
            self.cd(now)
        self.create_file(localPath[-1])

        for times in range(len(targetPath)):
            self.cd("..")


def calPer(pers, num):
    for i in range(len(pers)):
        for j in range(len(pers)):
            for k in range(len(pers)):
                if pers[i] + pers[j] + pers[k] == num:
                    return i, j, k


# print("Testing question 1")

# question 1 should allow to create simple files and folders:
# file = PlainFile("boot.exe")
# folder = Directory("Downloads", [])

root = Directory("root", [PlainFile("boot.exe"), Directory("home", [
    Directory("thor", [PlainFile("hunde.jpg"), PlainFile("quatsch.txt")]),
    Directory("isaac", [PlainFile("gatos.jpg")])])])

print("Testing question 2")

# question 2: implement the str

print(root)

print("Testing question 3")

# question 3: test chown()
file = PlainFile("boot.exe")
folder = Directory("Downloads", [])
print(f'file.owner: {file.owner}; folder: {folder.owner}')
file.chown("root")
folder.chown("isaac")
print(f'file.owner: {file.owner}; folder: {folder.owner}')

print("Testing question 4")

# question 4: ls() doesn't return anything but prints.
root.ls()

# question 5: create FileSystem
print("Testing question 5a: basic filesystem and pwd")

fs = FileSystem(root)

# 5a:
print(fs.pwd())

print("Testing question 5b: ls in working directory")

# 5b:
fs.ls()

# 5c:

print("Testing question 5c: cd")

# if you try to move to a non existing directory or to a file,
# the method should complain:
fs.cd("casa")
# But you can move to an existing directory in the working directory.
fs.cd("home")
# if we now do ls(), you should only see the content in home:
fs.ls()

# you can't go backwards yet...

print("Testing question 5d:  mkdir and create file")
fs = FileSystem(root)  # re-initialise fs


fs.mkdir("test")
# the owner of the directory should be 'default' as not indicated.
# fs.mkdir("test","isaac") would set the owner to isaac
fs.cd("test")
fs.create_file("test.txt")
fs.ls()

print("Testing question 5e:  dot dot")

# to test this properly, let's create the entire file system using our previous functions!

root = Directory("root", [], owner="root")
fs = FileSystem(root)
fs.create_file("boot.exe")
# when creating a file we do not need to indicate owner,
# it will be the same as the working directory
fs.mkdir("home", owner="root")
fs.cd("home")
fs.mkdir("thor", owner="thor")
fs.mkdir("isaac", owner="isaac")
fs.cd("thor")
fs.create_file("hunde.jpg")
fs.create_file("quatsch.txt")
fs.cd("..")
fs.cd("isaac")
fs.create_file("gatos.jpg")
fs.cd("..")
fs.cd("..")
fs.ls()

print("Testing question 5f:  rm")
# shouldn't work!
fs.rm("test")
fs.cd("test")
fs.rm("test.txt")
fs.cd("..")
fs.rm("test")
fs.ls()

print("Testing question 5g:  find")

print(fs.find("gatos.jpg"))
fs.cd("home")
print(fs.find("boot.exe"))  # shouldn't find it!

# My other test case
# ls -l and chmod
# fs = FileSystem(root)
# fs.chmod("777", "home")
# fs.ls("-l")

# I have the idea of making mv, by using two list to store path one by one
# like [root,home,lfz] [root,home,thor]
# Just use cd() while searching in lists
# fs.pwd()
# fs.cd("home")
# fs.create_file("lfz")
# fs.mv("/root/home/lfz", "/root/home/thor")
# fs.ls()
