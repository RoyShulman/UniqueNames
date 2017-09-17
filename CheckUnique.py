from __future__ import division

def count_unique_names(bill_first_name, bill_last_name, ship_first_name, ship_last_name, bill_name_on_card):
    num_unique_names = 3
    #lowercase all the names since uppercase letters don't matter
    bill_first_name = bill_first_name.lower()
    bill_last_name = bill_last_name.lower()
    ship_first_name = ship_first_name.lower()
    ship_last_name = ship_last_name.lower()
    bill_name_on_card = bill_name_on_card.lower()
    #assuming card name has both first and last name
    first_bill_name_on_card, last_bill_name_on_card = bill_name_on_card.split(" ")


    #check for middle names(assuming only 1 nickname)
    bill_nickname = ""
    ship_nickname = ""
    splitted_bill_first_name = bill_first_name.split(" ")
    if len(splitted_bill_first_name) == 2:
        #found nickname
        bill_first_name = splitted_bill_first_name[0]
        bill_nickname = splitted_bill_first_name[1]
    splitted_ship_first_name = ship_first_name.split(" ")
    if len(splitted_ship_first_name) == 2:
        #found nickname
        ship_first_name = splitted_ship_first_name[0]
        ship_nickname = splitted_ship_first_name[1]


    #unique names are names with distance/(max(len(name1,name2)) < 0.6
    #after checking names and nicknames I felt this is the best distance formula I could make without researching many words


    #check if last names are similar. If not then no need to check if first names are.
    if is_similar(bill_last_name, ship_last_name):
        #They are check first names
        if is_similar(bill_first_name, ship_first_name):
            #found the same person
            num_unique_names -= 1
        else:
            #check nicknames assuming nicknames can't be last names and different people can have the same nickname
            if ship_nickname != "":
                if is_similar(ship_nickname, bill_first_name):
                    #found similar nicknames and billing name
                    num_unique_names -= 1
            elif bill_nickname != "":
                if is_similar(bill_nickname, ship_first_name):
                    #found similar nickname and shippping name
                    num_unique_names -= 1

    if num_unique_names == 2:
        #only need to check the card for one name because there is only a possibility for 2 people
        #This is assuming nicknames can't be on the card
        if is_similar(first_bill_name_on_card, bill_first_name):
            if is_similar(last_bill_name_on_card, bill_last_name):
                #found the same person
                num_unique_names -= 1

        elif is_similar(first_bill_name_on_card, bill_last_name):
            #The name is written the other way around
            if is_similar(last_bill_name_on_card, bill_first_name):
                #found the same person
                num_unique_names -= 1
    else:
        #Possible 3 people need to check both names
        if is_similar(first_bill_name_on_card, bill_first_name):
            if is_similar(last_bill_name_on_card, bill_last_name):
                #found the same person
                num_unique_names -= 1
        elif is_similar(first_bill_name_on_card, bill_last_name):
            if is_similar(last_bill_name_on_card, bill_first_name):
                num_unique_names -= 1
        #check the shipping name
        if is_similar(first_bill_name_on_card, ship_first_name):
            if is_similar(last_bill_name_on_card, ship_last_name):
                num_unique_names -= 1
        elif is_similar(first_bill_name_on_card, ship_last_name):
            if is_similar(last_bill_name_on_card, ship_first_name):
                num_unique_names -= 1

    return num_unique_names

def is_similar(name1, name2):
    #returns True if names are similar
    distance = calculate_similarity(name1, name2)
    max_len = max(len(name1), len(name2))
    return (distance / max_len) < 0.6

def calculate_similarity(name1, name2):
    #This function calculates the amount of edits needed to go from one word to the other
    #Based on Levenshtein Distance algorithm

    length_name1 = len(name1)
    length_name2 = len(name2)
    if length_name1 == 0:
        if length_name2 != 0:
            return length_name2
        return -1
    else:
        if length_name2 == 0:
            return length_name1

    #both strings are not empty create matrix to compare them

    matrix = [[0]*(length_name2 + 1) for x in xrange(length_name1 + 1)]

    for i in xrange(length_name1 + 1):
        matrix[i][0] = i

    for i in xrange(length_name2 + 1):
        matrix[0][i] = i

    cost = 0
    minimun = 0
    for i in xrange(1, length_name1 + 1):
        for j in xrange(1, length_name2 + 1):
            if name1[i - 1] == name2[j - 1]:
                cost = 0
            else:
                cost = 1
            minimun = min(1 + matrix[i - 1][j], 1 + matrix[i][j - 1],cost + matrix[i - 1][j - 1])
            matrix[i][j] = minimun
    distance = matrix[length_name1 - 1][length_name2 - 1]

    return distance

if __name__ == "__main__":
    print count_unique_names("aaron", "Egli", "erin", "Egli", "Michele Egli")
    print count_unique_names("Deborah", "Egli", "Debbie", "Egli", "Debbie Egli")
    print count_unique_names("Deborah", "Egni", "Deborah", "Egli", "Deborah Egli")
    print count_unique_names("Deborah S", "Egli", "Deborah", "Egli", "Egli Deborah")
    print count_unique_names("Michele", "Egli", "Deborah", "Egli", "Michele Egli")
    print count_unique_names("Aaron",  "shulman", "Erin", "Shulman", "Aaron Shulman")
    print count_unique_names("Abner B", "Yaffe", "Ab", "Yaffe", "Abner Yaffe")