with open("static/save.txt", 'w') as f :
    for i in range(6) :
        f.write("%d번째 줄\n"%i)