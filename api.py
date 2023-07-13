import requests

url = "https://dadosabertos.camara.leg.br/api/v2/votacoes"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    for votacao in data["dados"]:
        print(votacao["id"])
else:
    print("Erro na requisição:", response.status_code)
