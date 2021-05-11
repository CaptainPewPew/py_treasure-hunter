try :
    hall_of_fame = open('Winners1.txt', 'r')
    print(" Hall OF Fame ")
    print("==============")
    for line in hall_of_fame:
        print line.strip().center(14)
    print("==============\n")
    hall_of_fame.close()
except IOError:
    print (" Hall OF Fame ")
    print ("==============")
    print ("<-- Empty! -->")
    print ("==============\n")

winner_name = raw_input("What's your name stranger? ")
hall_of_fame = open("Winners1.txt",'a')
hall_of_fame.write(str(winner_name) + "\n")
hall_of_fame.close()
