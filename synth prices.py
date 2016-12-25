import webbrowser, requests, bs4, pprint, re

offerList = []
offerPrices = []
categories = ['http://allegro.pl/instrumenty-klawiszowe-i-midi-syntezatory-i-klawiatury-sterujace-122795?buyUsed=1', 'http://allegro.pl/instrumenty-klawiszowe-i-midi-moduly-brzmieniowe-i-samplery-122804?buyUsed=1']
              

regex = re.compile('[^0-9]')

## Check how many pages of offers there are

for k in range (0, 2):
    allegro = requests.get(categories[k])
    try:
        allegro.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))

    allegroSoup = bs4.BeautifulSoup(allegro.text, 'html.parser')
    lastPage = allegroSoup.select('.pagination .last')[0].getText()


    ## iterate through pages

    for j in range (1, int(lastPage)+1):
        allegro = requests.get(categories[k] + '&p=' + str(j))

        allegroSoup = bs4.BeautifulSoup(allegro.text, 'html.parser')    


        ## iterate through offers on a page to get titles

        offerTitles = allegroSoup.select('.offer-title')
        for i in range (0, len(offerTitles)):
            offerList += [offerTitles[i].getText()] 


        ## iterate through offers on a page to get Price

        offerPrice = allegroSoup.select('.offer-price > .offer-buy-now > .statement')
        for i in range (0, len(offerTitles)):
            cena = ''
            cena = offerPrice[i].getText()
            cena = regex.sub('', cena)
            cena = cena[:len(cena)-2]
            offerPrices += [cena] 


## Print list of all offers

## pp = pprint.PrettyPrinter(indent=4)
## pp.pprint(offerList)

for i in range (0, len(offerList)):
    if "dave" not in offerList[i].lower(): 
        continue
    print(offerList[i] + ' ' + offerPrices[i]) ## str(offerList[i]) + ' ' +
print ('ilość cen: ' + str(len(offerPrices)) + ' ilość tytułów: ' + str(len(offerList)))

