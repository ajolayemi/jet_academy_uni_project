#!/usr/bin/env python
import os
# Module to be used to find the mean of values
import statistics

# Stores those departments that require more than one
# exam to determine whether to accept applicant or no
DEPTS_CHOICE = {'Physics': ['Physics', 'Mathematics'],
                'Engineering':  ['Engineering', 'Mathematics'],
                'Biotech': ['Chemistry', 'Physics']}

FILE_COLUMNS = {'Physics': 2,
                'Chemistry': 3,
                'Biotech': 3,
                'Mathematics': 4,
                'Engineering': 5,
                'Special Exam': 6,
                'first_choice': 7, 'second_choice': 8,
                'third_choice': 9}



def file_writer(file_name: str,
                information: str):
    with open(file_name, 'a') as output_file:
        output_file.write(information)


def check_file_existence(file_name):
    """ Checks if a file exists and remove it eventually """
    if os.path.exists(file_name):
        os.remove(file_name)
        return True


class AdmissionProcessor:
    """ Manages admission process into University """

    def __init__(self, file_path):
        self.file = file_path
        self.max_students = int(input())
        self.students = []
        self.dept_admitted_students = {}
        self.students_dict = {}
        self.students_depts = {}

    def build_string(self):
        """ Builds the output value that will be returned to
        user. """
        ranked_dept = self.read_dept_from_file()
        self.admission_decider()
        # A variable to keep track of how
        for current_dept in ranked_dept:
            file_name = f'{current_dept}.txt'
            # Check to see if the file has already been created
            # before
            check_file_existence(file_name)
            current_info = self.dept_admitted_students[current_dept]

            ranked_current_info = sorted(current_info, key=lambda x: (-x[1], x[0]))
            for admitted_student in ranked_current_info:
                output = f'{admitted_student[0]} {admitted_student[1]}\n'
                file_writer(file_name=file_name,
                            information=output)
        return 'Ok'

    def admission_decider(self):
        processed_students = []
        # Call upon the function that reads general info
        # about applicants. This method updates the value
        # of self.students_dict
        self.read_applicants_from_file()
        # Call upon the function that reads all departments from
        # applicants file and store it returned value in a variable
        # called departments
        departments = self.read_dept_from_file()
        # An empty dict where keys will be department names
        # and the values will be a nested list containing the names
        # of admitted students and their exam scores.
        admitted_students = {}
        # A dict that stores the number of students that has being
        # admitted into a department
        admitted_students_stats = {}
        # This will tell the function which choice to consider
        # it's initial value is 1 which means all applicants first
        # choice will be reviewed first
        current_choice = 1
        # Start looping over department list
        # Keep looping as long as their are still unprocessed
        # students
        while 0 < current_choice <= 3:
            for dept in departments:
                current_students = self.filter_students(
                    choice=current_choice,
                    department=dept
                )
                if dept not in admitted_students:
                    admitted_students[dept] = []
                    admitted_students_stats[dept] = 1
                for student in current_students:
                    student_name = student[0]
                    if admitted_students_stats[dept] <= self.max_students and \
                            student_name not in processed_students:
                        # Admit student
                        appended_info = [student[0], student[1]]
                        admitted_students[dept].append(appended_info)
                        # Increase department stat
                        admitted_students_stats[dept] += 1
                        # remove student from the list of applicants
                        processed_students.append(student_name)

                    else:
                        # Meaning that the department is already full
                        continue

                # s_processed_students = sorted(processed_students, key=lambda x: (-x[1]))
                # processed_students = []
                # admitted_students[dept] = s_processed_students
            current_choice += 1
        self.dept_admitted_students = admitted_students
        return admitted_students

    def filter_students(self, department: str,
                        choice: int) -> list:
        """ Reads the selected department from students_depT
         (an instance of AdmissionProcessor class) based on
        whether it should be students' first, second or third choice.
        """
        # Call upon the function that reads students department
        # choice from file
        self.read_applicants_from_file()
        self.get_student_depts()
        # Call upon the function that reads all info regarding student
        # from file
        department_students = []
        if self.students_depts == {}:
            return []
        else:
            for current_student in self.students_depts:
                if 0 <= choice > 3:
                    return []
                else:
                    current_student_first = self.students_depts[current_student][0]
                    current_student_second = self.students_depts[current_student][1]
                    current_student_third = self.students_depts[current_student][2]
                    student_score = self.score_decider(
                        student_name=current_student,
                        department_name=department
                    )
                    appended_info = [current_student, student_score]
                    if choice == 1 and current_student_first == department:
                        department_students.append(appended_info)
                    elif choice == 2 and current_student_second == department:
                        department_students.append(appended_info)
                    elif choice == 3 and current_student_third == department:
                        department_students.append(appended_info)
            ranked_students = sorted(department_students, key=lambda x: (-x[1], x[0]))
            return ranked_students

    def score_decider(self, student_name: str, department_name: str):
        """ Decides which of the two functions that gets student score to
        call upon by checking if the current departments takes into consideration
        the score of other exams as well or not.
        Returns the associated score. """
        # If a department takes into consideration other exams score
        if department_name in DEPTS_CHOICE:
            departments = DEPTS_CHOICE[department_name]
            # Call upon the function that gets mean score
            score = self.get_student_mean_score(
                student_name=student_name,
                exams=departments
            )
            return score
        else:
            score = self.get_student_dept_score(
                student_name=student_name,
                department=department_name
            )
            return score

    def get_student_mean_score(self, student_name: str,
                               exams: list[str]):
        scores = []

        self.read_applicants_from_file()
        student_info = self.students_dict.get(student_name, [])
        if student_info == 0:
            return 0
        else:
            # Loop over the list passed in by user
            for requested_exam in exams:
                # Start looping over student info which
                for current_exam in student_info:
                    # Check to see if the requested exam is equals the current
                    # value of current_exam
                    if requested_exam == current_exam[0]:
                        scores.append(float(current_exam[1]))
                    else:
                        continue
            # Get the last value in student_info list as it will be that of
            # special exam
            student_special_exam_score = student_info[-1][1]
            mean_score = statistics.mean(scores)
            returned_score = max(student_special_exam_score, mean_score)
            return returned_score

    def get_student_dept_score(self, student_name: str,
                               department: str):
        score = 0
        self.read_applicants_from_file()
        student_info = self.students_dict.get(student_name, [])
        if student_info is []:
            return 0
        else:
            for current_dept in student_info:
                if current_dept[0] == department:
                    score = current_dept[1]
                    break
                else:
                    score = 0
            student_special_exam_score = student_info[-1][1]
            return max(score, student_special_exam_score)

    def get_student_depts(self):
        """ Returns a dict where keys are students name and the values
        are a list containing the departments chosen by each students
        in the order they are in applicants file. """
        with open(self.file) as input_file:
            if not os.path.isfile(self.file):
                self.students_depts = {}
                return self.students_depts
            else:
                for line in input_file:
                    current_line = line.split()
                    current_student = f'{current_line[0]} {current_line[1]}'
                    first_choice = current_line[FILE_COLUMNS['first_choice']]
                    second_choice = current_line[FILE_COLUMNS['second_choice']]
                    third_choice = current_line[FILE_COLUMNS['third_choice']]
                    final_info = [first_choice, second_choice, third_choice]
                    if current_student not in self.students_depts:
                        self.students_depts[current_student] = final_info
                    else:
                        pass
        input_file.close()
        return self.students_depts

    def read_dept_from_file(self):
        """ Reads from file and returns a list of
        all departments chosen by students. """
        all_departments = []
        # Check to see whether file really exists
        if not os.path.isfile(self.file):
            return None
        else:
            with open(self.file) as input_file:
                for line in input_file:
                    current_depts = line.split()[FILE_COLUMNS['first_choice']:]
                    for department in current_depts:
                        if department not in all_departments:
                            all_departments.append(department)
                        else:
                            continue
            input_file.close()
            ranked_departments = sorted(all_departments)
            return ranked_departments

    def read_applicants_from_file(self):
        """ Reads from file_path and returns a nested list
        of applicants info in this format:
        [[student_name, student_GPA, first_choice, second_choice, third_choice]]. """
        # Check to see that file really exists
        if not os.path.isfile(self.file):
            return []
        else:
            with open(self.file) as applicants_file:
                for line in applicants_file:
                    current_line = line.split()
                    student_name = f'{current_line[0]} {current_line[1]}'
                    physics_score = ['Physics',
                                     float(current_line[FILE_COLUMNS['Physics']])]
                    chemistry_score = ['Chemistry',
                                       float(current_line[FILE_COLUMNS['Chemistry']])]
                    biotech_score = ['Biotech',
                                     float(current_line[FILE_COLUMNS['Biotech']])]
                    math_score = ['Mathematics',
                                  float(current_line[FILE_COLUMNS['Mathematics']])]
                    engineering_score = ['Engineering',
                                         float(current_line[FILE_COLUMNS['Engineering']])]
                    special_exam_score = ['Special',
                                          float(current_line[FILE_COLUMNS['Special Exam']])]

                    final_info = [physics_score, chemistry_score, biotech_score,
                                  math_score, engineering_score, special_exam_score]
                    # Add the current student name to the students_dict if it isn't
                    # already a key
                    if student_name not in self.students_dict:
                        self.students_dict[student_name] = final_info
            applicants_file.close()
            return self.students_dict


def main(file_path):
    """ Runs AdmissionProcessor class. """
    class_init = AdmissionProcessor(file_path=file_path)
    output_ = class_init.build_string()
    return output_


if __name__ == '__main__':
    test = main('applicant_list.txt')
    print(test)
