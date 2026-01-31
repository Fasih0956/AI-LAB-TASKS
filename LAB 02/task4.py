class Course:
    def __init__(self,course_name,instructor,num_of_students):
        self.__course_name = course_name
        self.__instructor = instructor
        self.__num_of_students = num_of_students
        self.students = {}

    def enroll(self,name,id,contact):
        self.students[id] = {
            "Name" : name,
            "Contact" : contact
        }
    def unenroll(self, id):
        if id in self.students:
            unenrolled = self.students.pop(id)
            print(f"Unenrolled student: {unenrolled}")
            self.__num_of_students -= 1
        else:
            print(f"Student ID {id} not found.")    

    def display_course_info(self):
        print(f"Course Name: {self.__course_name}")
        print(f"Instructor: {self.__instructor}")
        print(f"Number of Students: {self.__num_of_students}")
        print("Students Info:")
        for sid, info in self.students.items():
            print(f"ID: {sid}, Name: {info['Name']}, Contact: {info['Contact']}")    

st1 = Course("AI 2002" , "Sir Atif Luqman" , 5)
st1.enroll("Fasih Ahmed" , "24K-0956" , 923010034567)
st1.enroll("Saad Tahir" , "24K-0851" , 923010034568)
st1.enroll("Habib Farooqi" , "24K-0604" , 923010034569)
st1.enroll("Raed Ovais" , "24K-1033" , 923010034547)
st1.enroll("Uzair Ibrahim" , "24K-0867" , 923010034267)

print("---Displaying Course Info---")
st1.display_course_info()

print("\n---Deleting Student with Id 24K-0867---")
st1.unenroll("24K-0867")

print("\n---Displaying Course Info After unenrolling Student---")
st1.display_course_info()






