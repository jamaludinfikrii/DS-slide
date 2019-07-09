import requests
import pandas as pd

res = requests.get('http://api-pokemon-baron.herokuapp.com/pokemon',
    params={ 'generation': 2, 'legendary': 'True'}
)

# print(res.text)

json_data = res.json()

dfPokemon = pd.DataFrame(json_data, columns=json_data[0].keys())
dfPokemon.to_json('2ndlegendary.json', orient='split')