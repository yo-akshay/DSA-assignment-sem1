from sys import getsizeof

class Hashing:

    def __init__(self):
        self.customers = [[] for i in range(10007)]

    def getHash(self, key):
        sum=0
        i = 0
        for char in key:
            sum = sum + ord(char) * (31**i)
            i+=1
        hash = sum%10007
        return hash

    def insertVisitor(self, key, value):
        hash = self.getHash(key)
        self.customers[hash].append([key,value])
        return True





class FileOperation:
    def __init__(self):
        self.inputFile = "inputPS20.txt"
        self.promptFile = "promptsPS20.txt"
        self.outputFile = "outputPS20.txt"
    
    def readInputFile(self):
        file = open(self.inputFile, "r")
        return file
    
    def writeOutputFilePostInsert(self,insertCount):
        file = open(self.outputFile,"w")
        file.write("---------- insert ----------\n")
        file.write("Total visitor details entered: {}\n".format(str(insertCount)))
        file.write("----------------------------\n")
        file.close()
        
        
class Validations:
    pass


if __name__ == "__main__":
    fileOperation = FileOperation()
    hashing = Hashing()
    file = fileOperation.readInputFile()
    insertCount = 0
    for line in file:
        key = line.split(',')[0].strip()
        value = [i.strip() for i in line.split(',')[1:]]
        result = hashing.insertVisitor(key, value)
        if result:
            insertCount+=1
    file.close()
    
    fileOperation.writeOutputFilePostInsert(insertCount)
    