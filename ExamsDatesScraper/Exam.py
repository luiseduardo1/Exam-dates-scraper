class Exam:
    """
        Class that represent a exam with its name, date, time period and value(%)
    """
    def __init__(self, name, date, timePeriod, local, value):

        self.name = name
        self.date = date
        self.timePeriod = timePeriod
        self.local = local
        self.value = value

    def getName(self):
        return self.name

    def getDate(self):
        return self.date

    def getTimePeriod(self):
        return self.timePeriod

    def getLocal(self):
        return self.local

    def getValue(self):
        return self.value
