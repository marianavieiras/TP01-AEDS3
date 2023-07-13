import requests

ano = input("Ano que deseja fazer leitura: ")
dataFim = None

if ano == '2023':
    mes = input("Insira o mês atual: ")
    dia = input("Insira o dia atual: ")  
    dataFim = f'{ano}-{mes}-{dia}'
    dataInicio = f'{ano}-01-01'
else:
    dataFim = f'{ano}-12-31'
    dataInicio = f'{ano}-01-01'



url = f"https://dadosabertos.camara.leg.br/api/v2/votacoes?dataInicio={dataInicio}&dataFim={dataFim}&ordem=DESC"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    for votacao in data["dados"]:
       # print(votacao["id"])

        idVotacao = votacao["id"]
        urlVotacao = f"https://dadosabertos.camara.leg.br/api/v2/votacoes/{idVotacao}/votos"
        responseVotacao = requests.get(urlVotacao)

        if responseVotacao.status_code == 200:
            leitura = responseVotacao.json()
            for votacao in leitura["dados"]: 
                for deputado in votacao[",nome"]:
                        print(deputado)
        else:
            print("Erro na requisição:", response.status_code)
else:
    print("Erro na requisição:", response.status_code)

