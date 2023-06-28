import requests

url = 'https://api.dadosabertos.camara.leg.br/api/v2/votacoes'
def fazer_requisicao_votacoes():
    response = requests.get(url)
    
    if response.status_code == 200:
       dados = response.json()
       return dados
    else:
        print('Erro na requisição. Código de status:', response.status_code)
        return None



def ler_arquivo_url():
    try:
          
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve algum erro na requisição

        informacoes = []
        linhas = response.text.split("\n")  # Divide o conteúdo da resposta em linhas
        
        for linha in linhas:
            linha = linha.strip().split(";")
            idVotacao = linha[0]
            voto = linha[3]
            idDep = linha[4]
            nomeDep = linha[6]
            informacoes.append((idVotacao, voto, idDep, nomeDep))
        
        return informacoes
    
    except requests.exceptions.RequestException as e:
        print("Ocorreu um erro na requisição:", e)
        return []
