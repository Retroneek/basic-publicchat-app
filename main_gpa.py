import json
import xmljson

class_selection = False
API_URL = json.load(open('config.json'))

with open('class.json', 'r') as file:
    classes = json.load(file)

with open('grade_map.json', 'r') as grade_map:
    grade_scale = json.load(grade_map)

username = input('Username:')
password = input('Password:')

canvas = Canvas(API_URL['domain'])


if not(classes):
    print('There are no classes')
    class_selection = True

else:
    while True:
        mod_classes = input('Do you want reset your classes? \nYes [Y] No [N] Login to FCPS [V]')
        if (mod_classes.upper() == 'Y'):
            class_selection = True
            break
        elif (mod_classes.upper() == 'N'):
            break
        elif (mod_classes.upper() == 'V'):
            gradebook = sv.get_student_info()['@Cour']
            print(gradebook)
            break
        else:

            print('You must choose Yes or No...')

class Advanced:
    def __init__(self):
        self.diff = 'Advanced'
        self.boost = 1
class Honors:
    def __init__(self):
        self.diff = 'Honors'
        self.boost = 0.5
class Regulars:
    def __init__(self):
        self.diff = 'Regulars'
        self.boost = 0

while class_selection:
    courses_obj = []
    courses_list = []
    classes = {}
    courses_amount = int(input('How many classes are in this semester?:\n'))
    for i in range(courses_amount):
        class_name = input(f'Period {i+1}: ')
        courses_list.append(class_name)
        class_dif = int(input('Regulars [1] \nHonors [2]\nAdvanced [3]'))
        if class_dif == 1:
            class_name = Regulars()
        elif class_dif == 2:
            class_name = Honors()
        elif class_dif == 3:
            class_name = Advanced()
        courses_obj.append(class_name)
    for i in range(courses_amount):
        classes.update({f'{courses_list[i]}':f'{courses_obj[i].diff}'})
        print(f'Period {i+1}:', courses_list[i], f'({courses_obj[i].diff})')
        
    while True:
        confirm_classes = input('Do you want confirm your classes? \nYes [Y] No [N]')
        if (confirm_classes.upper() == 'Y'):
            with open('class.json', 'w') as file:
                json.dump(classes, file, indent=4)
            class_selection = False
            break
        elif (confirm_classes.upper() == 'N'):
            break
        else:
            print('You must choose Yes or No...')

print(grade_scale)
while True:     
    i = 0
    grade_avg = 0
    for courses in classes:
        class_name = courses
        i += 1

        print(f'Period {i}:', class_name)
        if classes.get(f'{courses}') == 'Advanced':
            courses = Advanced()
        elif classes.get(f'{courses}') == 'Honors':
            courses = Honors()
        elif classes.get(f'{courses}') == 'Regulars':
            courses = Regulars()

        grade_valid = True
        while grade_valid:
            grade_letter = (input('Grade Recieved for this class:')).upper()
            for grade in grade_scale:
                if grade_letter == grade:
                    if(grade_letter != 'F'):
                        grade_avg += grade_scale.get(f"{grade_letter}") + courses.boost
                    grade_valid = False

        print(f'Period {i}:', class_name, grade_letter)
    print(grade_avg/i)