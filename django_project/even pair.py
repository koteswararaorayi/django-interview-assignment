s = '3gy41d216'
for i in range(len(s)-1):
    if s[i].isdigit():
        x=int(s[i])
        if x%2==0:
            if s[i+1].isdigit():
                j = int(s[i+1])
                if j%2 == 0:
                    print (True)
                    break
                elif j%2 != 0:
                    if (i+2)<len(s):
                        if s[i+2].isdigit():
                            k = int(s[i+2])
                            if k%2 == 0:
                                print (True)
                                break
                    else:
                        print(False)
                        break

                else:
                    print(False)
            else:
                continue
        else:
            if i == (len(s)-2):
                print(False)
    else:
        if i == (len(s)-2):
            print(False)

    