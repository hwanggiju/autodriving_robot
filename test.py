with open("C:/opencv/development/face/map.txt", mode = "rt", encoding = 'utf-8') as f :
    stringList =f.readlines()
    item_lst = list(stringList) # 문자 하나씩 쪼개어 리스트에 저장 -> 정수형
    for i in item_lst :
        line_lst = list(i)
        for j in line_lst :
            if j == '0':
                print('\033[37m■', end = '')
            elif j == '1' :
                print('\033[33m■', end = '')
            elif j == '2' :
                print('\033[31m■', end = '')
            elif j == '3' :
                print('\033[34m■', end = '')
            elif j == '4' :
                print('\033[30m■', end = '')
            elif j == '5' :
                print('\033[35m■', end = '')
            elif j == '6' :
                print('\033[30m■', end = '')
            else :
                print()
            
    