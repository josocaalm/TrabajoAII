#enconding: latin1

from urllib.request import urlopen
import json

def ISO3166CodeToCountry():
    url = "http://data.okfn.org/data/core/country-codes/r/country-codes.json"
    html = urlopen(url).read()

    jsonData = json.loads(html.decode("utf-8"))
    dictCodeToCountry = dict()
    
    for elem in jsonData:
        countryName = elem["name"]
        countryCode = elem["ISO3166-1-Alpha-2"]
        dictCodeToCountry[countryCode] = countryName
        
    return dictCodeToCountry