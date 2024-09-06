import logging

def kalkulator():
    logging.basicConfig(level=logging.DEBUG)
    while True:
        dzialanie = 0
        k = 0
        i = 0
        x = 1
        skladniki = []
        wynik = 0
        wiadomosc = ''
        dzialanie = int(input('Podaj działanie, posługując się odpowiednią liczbą: 1 Dodawanie, 2 Odejmowanie, 3 Mnożenie, 4 Dzielenie, 5 Wyjscie: '))
        if dzialanie == 5:
            break
        elif dzialanie not in range(1, 5):
            print('Podaj poprawny numer działania!')
            continue
        else:
            while True:
                skladnik = input(f'Podaj składnik {x} lub = aby wyświetlić wynik: ')
                try: 
                    skladnik = float(skladnik)
                except: 
                    if skladnik == '=':
                        break
                    else:
                        print('Podaj prawidłowy składnik!') 
                        continue
                if skladnik == '=':
                    break
                else:
                    if dzialanie == 4 and skladnik == 0.0 and len(skladniki) > 0:
                        print('Nie można dzielić przez 0!')
                        continue
                    else:
                        skladniki.append(skladnik)
                        x+=1
                    
            for k in range(len(skladniki)):
                if k == len(skladniki)-2:
                    wiadomosc = wiadomosc + f'{skladniki[k]} '
                elif k == len(skladniki)-1:
                    wiadomosc = wiadomosc + f'i {skladniki[k]}'
                else:
                    wiadomosc = wiadomosc + f'{skladniki[k]}, '
                k+=1
            if dzialanie == 1:
                wiadomosc = 'Dodaję: ' + wiadomosc
                for skladnik in skladniki:
                    wynik = wynik + skladnik
            elif dzialanie == 2:
                wiadomosc = 'Odejmuję: ' + wiadomosc
                for i in range(len(skladniki)):
                    if i == 0:
                        wynik = skladniki[i]
                    else:
                        wynik = wynik - skladniki[i]
                    i+=1
            elif dzialanie == 3:
                wiadomosc = 'Mnożę: ' + wiadomosc
                for i in range(len(skladniki)):
                    if i == 0:
                        wynik = skladniki[i]
                    else:
                        wynik = wynik * skladniki[i]
                    i+=1
            elif dzialanie == 4:
                wiadomosc = 'Dzielę: ' + wiadomosc
                for i in range(len(skladniki)):
                    if i == 0:
                        wynik = skladniki[i]
                    else:
                        wynik = wynik / skladniki[i]
                    i+=1
            logging.info(wiadomosc)
            logging.info(f'Wynik to: {wynik}')
kalkulator()
    






