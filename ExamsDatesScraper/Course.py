class Course:
    """
    Course class contains all the exams and homeworks for that specific course
    """

    def __init__(self, courseName):

        self.courseName = courseName
        self.examsList = []
        self.homeworksList = []

    def getCourseName(self):
        return self.courseName


    def getExamsList(self):
        return self.examsList

    def getHomeworksList(self):
        return self.homeworksList
