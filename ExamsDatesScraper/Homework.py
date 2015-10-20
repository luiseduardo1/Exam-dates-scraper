class Homework:
    """
        Class that represent a homework with the name, due date, due hour and value(%)
    """
    
    def __init__(self, name, dueDate, dueHour, value):

        self.name = name
        self.dueDate = dueDate
        self.dueHour = dueHour
        self.value = value

    def getName(self):
        return self.name

    def getDueDate(self):
        return self.dueDate

    def getDueHour(self):
        return self.dueHour

    def getValue(self):
        return self.value
