# write your code here
file_range = 11
for current_file in range(1, file_range):
    file_name = f'file{current_file}.txt'
    with open(file_name, 'w') as file:
        file.write(str(current_file))
import os
print(os.path.isdir('task'))