def palindrom(wyraz):     
    return True if wyraz==wyraz[::-1] and wyraz.isalpha() else False

print(palindrom('kajak'))


    