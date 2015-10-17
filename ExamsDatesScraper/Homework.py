class Homework:
    """
        Class that represent a homework with the name, due date and due hour
    """
    
    def __init__(self, name, dueDate, dueHour):

        self.name = name
        self.dueDate = dueDate
        self.dueHour = dueHour

    def getName(self):
        return self.name

    def getDueDate(self):
        return self.dueDate

    def getDueHour(self):
        return self.dueHour
