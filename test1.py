import csv

f = open("map.csv", "w")

StartEndRow = [1 for _ in range(40)]
MiddleRow = [0 for _ in range(40)]
MiddleRow[0] = 1
MiddleRow[39] = 1

writer = csv.writer(f)

writer.writerow(StartEndRow)
for i in range(38) : 
    writer.writerow(MiddleRow)
writer.writerow(StartEndRow)
f.close