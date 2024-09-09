def add(a, b, *args):
    addv = 0
    for x in args:
        addv+=x
    return a + b + addv

def sub(a, b):
    return a - b

def mul(a, b, *args):
    addv = 1
    for x in args:
        addv*=x
    return a * b * addv

def div(a, b):
    return a / b


def get_additional_valus(op):
    if op not in ['1', '3']:
        return []
    args = []
    while True:
        v = input("Podaj kolejna wartosc lub naciśnij enter aby zakończyć: ")
        if v == "":
            break
        try: 
            v = float(v)
        except:
            print('Podaj prawidłową liczbę!')
            continue
        args.append(v)
    return args

def get_data():
    op = input("Podaj działanie, posługując się odpowiednią liczbą: 1 Dodawanie, 2 Odejmowanie, 3 Mnożenie, 4 Dzielenie: ")
    while True:
        a  = input("Podaj składnik 1. ")
        try:
            a = float(a)
            break
        except:
            print('Podaj prawidłową liczbę!')
    while True:
        b  = input("Podaj składnik 2. ")
        try:
            b = float(b)
            if op == '4' and b == 0: print('Nie można dzielić przez 0!')
            else:
               break
        except:
            print('Podaj prawidłową liczbę!')
    args = get_additional_valus(op)
    return str(op), float(a), float(b), args

operations = {
    '1': add,
    '2': sub,
    '3': mul,
    '4': div
}

def info(op, a, b, *args):
    if op=='1': message = 'Dodaję: '
    elif op=='2': message = 'Odejmuję: '
    elif op=='3': message = 'Mnożę: '
    elif op=='4': message = 'Dzielę: '

    message = message + str(a) + ' i ' + str(b)
    for arg in args:
        message = message + ', ' + str(arg)
    return message

    
def main():
    op, a, b, args = get_data()
    result = operations[op](a, b, *args)
    message = info(op, a, b, *args)
    print(message)
    print(f'Wynik to: {result}')
    con = input("Czy chcesz kontynuować? (tak/nie)")
    return con

if __name__ == "__main__":
    while True:
        con = main()
        if con.lower() == 'tak':
            continue
        else:
            break
