file = open('map.txt', 'r')
lst_line = []
line = file.readlines()
lst_line.append(line).split('\n')
file.close()
print(lst_line)