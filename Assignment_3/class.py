import datetime, time

class Person:
    def __init__(self, name, age, energy, sex=None):
        self.name = name
        self.age = age
        self.energy = energy
        self.sex = sex
    
    def getSurname(self):
        return self.name.split()[-1]

    def getBirthyear(self):
        now = datetime.datetime.now()
        return now.year - self.age 

    def sleep(self, hours):
        self.energy += hours * 10
        print(f'That was needed! You now have {self.energy} energy')

    def getCoffee(self, ml):
        self.energy += 0.2 * ml
        print(f'Yum! You now have {self.energy} energy')
    
class Student(Person):
    def __init__(self, grades, education, university, currentCourses, currentSemester, studyGroup=None, **kwargs):
        super().__init__(**kwargs)
        self.grades = grades
        self.education = education
        self.university = university
        self.currentCourses = currentCourses
        self.currentSemester = currentSemester
        self.studyGroup = studyGroup

    def study(self, minutes):
        if self.energy > minutes * 0.5:
            self.energy -= minutes * 0.5
            print(f'You successfully studied for {minutes} minutes, you now have {self.energy} energy left!')
        else:
            print("You're too tired to study! Consider drinking some coffee or getting some sleep :)")

    def takeExam(self, course):
        try:
            self.currentCourses.remove(course.name)
        except:
            print(f"This is the exam for {course.name}, and you aren't currently enrolled in this course")
        else: 
            self.energy -= self.energy
            print(f'Congrats! You completed the exam for {course.name}. Your courses now consist of {self.currentCourses}')
            course.professor.examsToGrade += 1
            


class Professor(Person):
    def __init__(self, favoriteSubject, coursesTaught, **kwargs):
        super().__init__(**kwargs)
        self.favoriteSubject = favoriteSubject
        self.coursesTaught = coursesTaught 
        self.examsToGrade = 0

    def gradeStudent(self, student, course, grade):
        student.grades[str(course.name)] = int(grade)
        return print(f"The student {student.name}'s exam for the course {course.name} has been graded!" )
        # Using str & int to ensure correct format


class University:
    def __init__(self, name, location, faculty, students):
        self.name = name
        self.location = location
        self.faculty = faculty
        self.students = students
        
class Education:
    def __init__(self, name, field, courses, enrolledStudents):
        self.name = name
        self.field = field
        self.courses = courses
        self.enrolledStudents = enrolledStudents
    
    def sendMessageTo(self, recipient):
        msg = input('Please input your message: ')
        print(f'TO {recipient} \n{msg} \nFROM {self.name}')

    def getCourses(self):
        courseList = []
        for course in self.courses:
            courseList.append(course.name)
        return courseList

    def organizeEvent(self, event):
        pass

class Course:
    def __init__(self, name, professor, subjects, usualClassroom, enrolledStudents):
        self.name = name
        self.professor = professor
        self.subjects = subjects
        self.usualClassroom = usualClassroom
        self.enrolledStudents = enrolledStudents

    def sendMessageTo(self, recipient):
        msg = str(input('Please input your message: '))
        print(f'TO {recipient} \n{msg} \nFROM {self.name}')  

    def scheduleExam(self, date):
        pass

    def scheduleLecture(self, date, subject):
        pass

    def getCourseStudents(self):
        studentNames = []
        for student in self.enrolledStudents:
            studentNames.append(student.name)
        return studentNames


def main():
    delay = 1

    studentInstance = Student(
        name = 'Albin Sand',
        age = 22,
        energy = 50,
        grades = {'IxD': 10, 'CoD': 4, 'AP': 10, 'SS': 4},
        education = 'Digital Design',
        university = 'Aarhus University',
        currentCourses = ['IxT', 'PFK', 'PFTH'],
        currentSemester = '3rd',
        studyGroup = ['Gabriel', 'Lissa', 'Victor']
    )

    studentInstance2 = Student(
        name = 'Victor Rasmussen',
        age = 22,
        energy = 50,
        grades = {'IxD': 7, 'CoD': 4, 'AP': 10, 'SS': 4},
        education = 'Digital Design',
        university = 'Aarhus University',
        currentCourses = ['IxT', 'PFK', 'PFTH'],
        currentSemester = '3rd',
        studyGroup = ['Gabriel', 'Lissa', 'Albin']
    )


    professorInstance = Professor(
        name = 'German Leiva',
        age = 34,
        energy = 50,
        coursesTaught = ['IxT'],
        favoriteSubject = 'Vue JS'
    )
    
    courseInstance = Course(
        name = 'IxT',
        professor = professorInstance,
        subjects = ['HCI', 'Human Psychology', 'Multimodal Interaction', 'WIMP', 'Ubicomp', 'Prototyping'],
        usualClassroom = 'Schön 144',
        enrolledStudents = [studentInstance, studentInstance2]
    )

    universityInstance = University(
        name = 'Aarhus University',
        location = 'Aarhus',
        faculty = [professorInstance],
        students = [studentInstance, studentInstance2]
    )

    educationInstance = Education(
        name = 'Digital Design',
        field = 'Humanities',
        courses = [courseInstance],
        enrolledStudents = [studentInstance, studentInstance2]
    )

    print(f'The student {studentInstance.name} was born in {studentInstance.getBirthyear()}')
    time.sleep(delay)
    print(f"The professor's surname is {professorInstance.getSurname()}")
    time.sleep(delay)
    studentInstance.sleep(hours = 3)
    time.sleep(delay)
    studentInstance2.getCoffee(ml = 330)
    time.sleep(delay)
    studentInstance.study(minutes = 60)
    time.sleep(delay)
    studentInstance.study(minutes = 10000)
    time.sleep(delay)
    studentInstance2.takeExam(courseInstance)
    time.sleep(delay)
    studentInstance2.takeExam(courseInstance)
    time.sleep(delay)
    print(f"The professor {professorInstance.name} has {professorInstance.examsToGrade} exams to grade")
    time.sleep(delay)
    professorInstance.gradeStudent(studentInstance2, courseInstance, 12)
    time.sleep(delay)
    print(f"The student {studentInstance2.name}'s grades consists of the following {studentInstance2.grades}")
    time.sleep(delay)
    print(f'The education consists of the following courses: {educationInstance.getCourses()}')
    time.sleep(delay)
    educationInstance.sendMessageTo('Lissa')
    time.sleep(delay)
    print(f'The course consists of the following students: {courseInstance.getCourseStudents()}')


if __name__ == '__main__':
    main()
