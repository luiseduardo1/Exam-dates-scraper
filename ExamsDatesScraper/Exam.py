class Exam:
    """
        Class that represent a exam with its name, date and time period
    """
    def __init__(self, name, date, timePeriod):

        self.name = name
        self.date = date
        self.timePeriod = timePeriod

    def getName(self):
        return self.name

    def getDate(self):
        return self.date

    def getTimePeriod(self):
        return self.timePeriod
