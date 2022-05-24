with open("C:/opencv/development/face/map.txt", mode = "rt", encoding = 'utf-8') as f :
    stringList =f.readlines()
    item = stringList[0] # 문자열 형식
    item_lst = list(map(int, item)) # 문자 하나씩 쪼개어 리스트에 저장 -> 정수형
    print(item_lst)