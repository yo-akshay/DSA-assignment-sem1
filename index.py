from datetime import *

currentDate = "01-Jan-1900"


class Hashing:

    def __init__(self):
        self.customers = [[] for i in range(10007)]

    def getHash(self, key):
        sum = 0
        i = 0
        for char in key:
            sum = sum + ord(char) * (31 ** i)
            i += 1
        hash = sum % 10007
        return hash

    def getCityHash(self, city):
        sum = 0
        i = 0
        for char in city:
            sum = sum + ord(char) * (31 ** i)
            i += 1
        hash = sum % 23
        return hash

    def insertVisitor(self, key, value):
        global currentDate
        hash = self.getHash(key)
        self.customers[hash].append([key, value])
        if datetime.strptime(value[1], '%d-%b-%Y') > datetime.strptime(currentDate, '%d-%b-%Y'):
            currentDate = value[1]

        return True

    def findVisitor(self, name):
        global currentDate
        foundVisitorCount = 0
        foundVisitors = []
        hash = self.getHash(name)
        hashedCustomers = self.customers[hash]
        for hashedCustomer in hashedCustomers:
            if hashedCustomer[0] == name and str(hashedCustomer[1][1]) == str(currentDate):
                foundVisitorCount += 1
                foundVisitors.append(hashedCustomer)
        return foundVisitorCount, foundVisitors

    def visitorCount(self, date):
        count = 0
        for customer in self.customers:
            if len(customer) > 0:
                for datum in customer:
                    if datetime.strptime(datum[1][1], '%d-%b-%Y') == date:
                        count += 1
        return count

    def birthdayVisitor(self, birthDateFrom, birthDateTo):
        visitorList = []
        for customer in self.customers:
            if len(customer) > 0:
                for datum in customer:
                    date = datetime.strptime(datum[1][2].split('-')[0] + '-' + datum[1][2].split('-')[1], '%d-%b')
                    if birthDateFrom <= date <= birthDateTo:
                        visitorList.append(datum)
        return visitorList


class FileOperation:
    def __init__(self):
        self.inputFile = "inputPS20.txt"
        self.promptFile = "promptsPS20.txt"
        self.outputFile = "outputPS20.txt"

    def readInputFile(self):
        file = open(self.inputFile, "r")
        return file

    def readPromptFile(self):
        file = open(self.promptFile, "r")
        return file

    def writeOutputFilePostInsert(self, insertCount):
        file = open(self.outputFile, "w")
        file.write("---------- insert ----------\n")
        file.write("Total visitor details entered: {}\n".format(str(insertCount)))
        file.write("----------------------------\n")
        file.close()

    def writeOutputFilePostFindVisitor(self, name, foundVisitorCount, foundVisitors):
        global currentDate
        file = open(self.outputFile, "a")
        file.write("---------- findvisitor ----------\n")

        if foundVisitorCount > 0:
            file.write(
                "{0} visitors with name {1} found visiting on {2} \n".format(str(foundVisitorCount), name, currentDate))
            for foundVisitor in foundVisitors:
                file.write("{0} {1}, {2}, {3}\n".format(foundVisitor[0], foundVisitor[1][0], foundVisitor[1][3],
                                                        foundVisitor[1][4]))
        else:
            file.write(
                "{0} visitors with name {1} found visiting on {2} \n".format(str(foundVisitorCount), name, currentDate))
        file.write("---------------------------------\n")
        file.close()

    def writeOutputFilePostVisitorCount(self, count, date):
        file = open(self.outputFile, "a")
        file.write("\n---------- visitorCount: ----------\n")
        file.write("{0} visitors found visiting on {1}\n".format(str(count), date))
        file.write("---------------------------------\n")
        file.close()

    def writeOutputFilePostBirthdayVisitor(self, visitorList, birthDateFrom, birthDateTo):
        file = open(self.outputFile, "a")
        file.write("\n---------- birthdayVisitor: ----------\n")
        file.write(
            "{0} visitors have upcoming birthdays between {1} and {2}\n".format(str(len(visitorList)), birthDateFrom,
                                                                                birthDateTo))
        for visitor in visitorList:
            file.write("{0} {1}, {2}, {3}\n".format(visitor[0], visitor[1][0], visitor[1][2], visitor[1][4]))
        file.write("---------------------------------\n")
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
            insertCount += 1
    file.close()
    fileOperation.writeOutputFilePostInsert(insertCount)

    value_FindVisitor = ""
    filePrompt = fileOperation.readPromptFile()
    for line in filePrompt:
        if line.startswith("findVisitor:"):
            name = line.split(':')[1].strip()
            foundVisitorCount, foundVisitors = hashing.findVisitor(name)
            fileOperation.writeOutputFilePostFindVisitor(name, foundVisitorCount, foundVisitors)
        elif line.startswith("visitorCount:"):
            date = line.split(':')[1].strip()
            count = hashing.visitorCount(datetime.strptime(date, '%d-%b-%Y'))
            fileOperation.writeOutputFilePostVisitorCount(count, date)
        elif line.startswith("birthdayVisitor:"):
            birthDateFrom = line.split(':')[1].strip()
            birthDateTo = line.split(':')[2].strip()
            visitorList = hashing.birthdayVisitor(datetime.strptime(birthDateFrom, '%d-%b'),
                                                  datetime.strptime(birthDateTo, '%d-%b'))
            fileOperation.writeOutputFilePostBirthdayVisitor(visitorList, birthDateFrom, birthDateTo)
        else:
            print('Invalid Command')
    filePrompt.close()
