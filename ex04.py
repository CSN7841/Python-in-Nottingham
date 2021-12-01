class File:

    # Init
    def __init__(self, name, owner, permission):
        self.name = name
        self.permission = permission
        self.owner = owner

    # All have file have owner
    def chown(self, owner="default"):
        self.owner = owner


# For print \t in ls()
def tabs(times):
    for i in range(times):
        print("\t", end="")


class PlainFile(File):
    # Classname
    className = "PlainFile"

    # Inherit from File
    def __init__(self, name, owner="default", permission="rwxr--r--"):
        super().__init__(name, owner, permission)

    # For printing
    def __str__(self):
        return f"{self.className}({self.name})"


class Directory(File):
    className = "Directory"
    fileStr = ""

    # Inherit from File
    def __init__(self, name, fileList, owner="default", permission="rwxr--r--"):
        super().__init__(name, owner, permission)
        # A list for store file list
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
            # If error set to ""
            self.fileStr = ""
        return f"{self.className}({self.name},[{self.fileStr}])"

    def findFolder(self, fList, depth, op):
        # Traverse the list
        for files in fList:
            # Check the class if it is PlainFile just print
            if files.className == "PlainFile":
                # My func for print \t
                tabs(depth)
                # -l is for ls -l
                if op == "-l":
                    print(f"{files.permission}  {files.owner}  {files.name}")
                else:
                    print(f"{files.name}")
            else:
                # If it is a Directory
                tabs(depth)
                if op == "-l":
                    print(f"{files.permission}  {files.owner}  {files.name}")
                else:
                    print(f"{files.name}")
                # Go deeper
                depth += 1
                # Recursion
                self.findFolder(files.list, depth, op)
                # Go out
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
        # A list to store the order of file
        self.fileDir = []
        # Save all root in rootDir for compare or restore
        self.rootDir = Dir
        # For current working Dir
        self.currentDir = Dir
        # Init for the first root folder
        self.fileDir.append(Dir)

    def pwd(self):
        # If not use fs.pwd uncomment following
        print(f"{self.currentDir.name}")

        # If want to see path like absolute path uncomment following
        # paths = ""
        # for files in self.fileDir:
        #     paths += f"/{files.name}"
        # print(paths)

        # If print(fs.pwd()) use following
        return f"{self.currentDir.name}"

    # A method for output path in method find()
    def getPath(self):
        paths = ""
        for files in self.fileDir:
            paths += f"/{files.name}"
        return paths

    # To use ls() in Directory
    def ls(self, op=""):
        self.currentDir.ls(op)

    def cd(self, filename):
        # For ".."
        if filename == "..":
            if self.currentDir == self.rootDir:
                return
            else:
                # Remove the file from tail
                del self.fileDir[-1]
                self.currentDir = self.fileDir[-1]
                return

        else:
            if self.currentDir.className == "PlainFile":
                return
            # Loop for finding file
            for files in self.currentDir.list:
                if files.name == filename:
                    if files.className == "PlainFile":
                        print(f"{filename} is not a directory !")
                        return
                    else:
                        # Add file to the end of list
                        self.fileDir.append(files)
                        # Set current directory to here we are
                        self.currentDir = files
        if self.currentDir.name != filename:
            print("The directory does not exist!")

    def create_file(self, name, owner="default", permission="rwxr--r--"):
        # If the list is empty just add new file
        if not self.currentDir.list:
            self.currentDir.list += [PlainFile(name, owner, permission)]
        else:
            # If not empty to see exists or not
            for files in self.currentDir.list:
                if name == files.name:
                    print(f"The file {files.name} already exists!")
                    return
            self.currentDir.list += [PlainFile(name, owner, permission)]
            return

    def mkdir(self, name, owner="default", permission="rwxr--r--"):
        # Same as create_file(self, name)
        if not self.currentDir.list:
            self.currentDir.list += [Directory(name, [], owner, permission)]
        else:
            for files in self.currentDir.list:
                if name == files.name:
                    print(f"The directory {files.name} already exists!")
                    return
                else:
                    self.currentDir.list += [Directory(name, [], owner, permission)]
                    return

    def rm(self, name):
        # Loop the find the same name file
        for files in self.currentDir.list:
            if name == files.name and files.className == "Directory":
                # If list not empty
                if files.list:
                    print("The directory is not empty !")
                    return
                else:
                    self.currentDir.list.remove(files)
            elif name == files.name and files.className == "PlainFile":
                self.currentDir.list.remove(files)
                return files
        print(f"The file '{name}' does not exist !")
        return

    def find(self, name):
        # For mark found or not
        global found
        found = False
        # For store the path to output
        global path
        path = ""
        for files in self.currentDir.list:
            if files.className == "Directory" and files.name != name:
                # cd() to next Directory
                self.cd(files.name)
                # Recursion
                self.find(name)
                # Go back
                self.cd("..")
                # If found stop loop
                # Found folder
                if found:
                    return path
            elif files.name == name:
                # Found file
                found = True
                path = f"{self.getPath()}" + "/" + name
                return path
                # print(f"{self.getPath()}" + "/" + name)
        return "File not found !"

    def chown(self, name, owner):
        for files in self.currentDir.list:
            if name == files.name:
                files.chown(owner)

    # Recursion for change all owner
    def chown_R(self, newOwner):
        self.currentDir.chown(newOwner)
        if self.currentDir.className == "PlainFile":
            return
        for files in self.currentDir.list:
            if files.className == "Directory":
                files.chown(newOwner)
                self.cd(files.name)
                # Recursion
                self.chown_R(newOwner)
                self.cd("..")
            else:
                files.chown(newOwner)

    # My method to input like "777" "755" to change mod
    def chmod(self, command, filename):
        # Two list for store weight and char
        pers = [4, 2, 1, 0]
        pers_cs = ["r", "w", "x"]
        bit = [0, 0, 0]
        if len(command) != 3:
            print("Command not right !")
            return
        for files in self.currentDir.list:
            if files.name == filename:
                temp = ""
                for index in range(len(command)):
                    # [i, j, k] is the index of pers
                    [i, j, k] = calPer(pers, int(command[index]))
                    # Set the bit [0, 0, 0] to some like [1, 0, 1] which is related to ["r", "w", "x"]
                    for bits in [i, j, k]:
                        # bits are for [i, j, k] indicate where is 1 in bit[0, 0, 0]
                        # If j = 2 so bit[j = 2] should be 1 [0, 0, 1]
                        if bits <= 2:
                            bit[bits] = 1
                    for perIndex in range(len(bit)):
                        if bit[perIndex] != 0:
                            temp += pers_cs[perIndex]
                        else:
                            temp += "-"
                    files.permission = temp
                    # Zero them
                    bit = [0, 0, 0]
                return
        print(f"{filename} is not here !")

    # Init str like [root,home,lfz] [root,home,thor]
    def mv(self, filepath, target):
        self.currentDir = self.rootDir
        # To store local path
        localPath = []
        # Target folder
        targetPath = []
        # Buffer for chars
        temp = ""

        # Traverse the input char by char
        for index in range(len(filepath)):
            # Read "/" at the beginning pass
            if filepath[index] == "/" and index == 0:
                continue
            # Read a "/" add a word
            elif filepath[index] == "/":
                localPath.append(temp)
                temp = ""
            # Read char one by one
            else:
                temp += filepath[index]

        # Put the last word into list
        localPath.append(temp)
        # Restore temp
        temp = ""

        # The same
        for index in range(len(target)):
            if target[index] == "/" and index == 0:
                continue
            elif target[index] == "/":
                targetPath.append(temp)
                temp = ""
            else:
                temp += target[index]

        # Put the last word into list
        targetPath.append(temp)

        # print(localPath)
        # print(targetPath)

        #####
        # Go to Dir and delete file
        for now in localPath[0:len(localPath) - 1]:
            if self.currentDir.name == now:
                continue
            self.cd(now)

        # I change the return of rm() make it return the delete file's info
        fileTemp = self.rm(str(localPath[-1]))
        if fileTemp is None:
            return

        # Back to User's original directory
        for times in range(len(localPath) - 1):
            self.cd("..")

        # Go to Dir and new a file
        for now in targetPath:
            self.cd(now)

        # Create a new file with the same properties
        if fileTemp is not None:
            self.create_file(fileTemp.name, fileTemp.owner, fileTemp.permission)

        # Back to User's original directory
        for times in range(len(targetPath)):
            self.cd("..")


# A method for calculating the "777" and find the subscript to return
def calPer(pers, num):
    for i in range(len(pers)):
        for j in range(len(pers)):
            for k in range(len(pers)):
                if pers[i] + pers[j] + pers[k] == num:
                    return [i, j, k]


print("Testing question 1")

# question 1 should allow to create simple files and folders:
file = PlainFile("boot.exe")
folder = Directory("Downloads", [])

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
fs.mkdir("test")
fs.cd("test")
fs.create_file("test.txt")
fs.cd("..")
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
# fs.pwd()
# fs.ls()
print(fs.find("boot.exe"))  # shouldn't find it!
print(fs.find("thor"))
# fs.pwd()

# My other test case
# ls -l and chmod
# fs = FileSystem(root)
fs.cd("..")
fs.chmod("753", "home")
# fs.ls("-l")

# I have the idea of making mv, by using two list to store path one by one
# like [root,home,lfz] [root,home,thor]
# Just use cd() while searching in lists
fs.cd("home")
# fs.cd("..")
fs.create_file("lfz")
fs.chown("lfz", "Steven")
fs.chmod("777", "lfz")
fs.ls()
fs.mv("/root/home/lf", "/root/home/thor")
fs.ls("-l")
fs.pwd()
# fs.chown_R("Steven")
# fs.ls("-l")
