def palindrom(wyraz):
    counter=0
    for i in range(len(wyraz)):
        if wyraz[i]==wyraz[-i-1]:
            counter+=1       
    return True if counter>=len(wyraz)-1 else False

print(palindrom('kajak'))


    