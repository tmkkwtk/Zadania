import re

def palindrom(wyraz):   
    wyraz = re.sub(r'[^a-zA-Z]', '', wyraz)
    wyraz = wyraz.lower() 
    return True if wyraz==wyraz[::-1] and wyraz.isalpha() else False

print(palindrom('Ka j4ak3'))


    