# put your python code here
class_one_students = int(input())
class_one_needed_desks = class_one_students / 2
class_1_remainder = class_one_students % 2

class_two_students = int(input())
class_two_needed_desks = class_two_students / 2
class_2_remainder = class_two_students % 2

class_three_students = int(input())
class_three_needed_desks = class_three_students / 2
class_3_remainder = class_three_students % 2

all_remainder = (class_3_remainder + class_2_remainder +
                 class_1_remainder)

smallest_desk_purchasable = (class_one_needed_desks +
                             class_two_needed_desks + class_three_needed_desks +
                             all_remainder)

print(int(smallest_desk_purchasable))
