import requests

class Grafo:
    def __init__(self):
        self.dadosvotacao = []
        self.deputados = []
        self.grafo = {}
        self.num_vert = 0
        self.arestas = 0

    def add_aresta(self, u, v, w=1):
        if u in self.grafo:
            if v in self.grafo[u]:
                self.grafo[u][v] += 1
                return
        else:
            self.grafo[u] = {}
        self.grafo[u][v] = w
        self.arestas += 1

    def agrupaVotos(self, linhas):
        for i in range(1, linhas):
            nomeD1 = self.dadosvotacao[i][1]
            idVota1 = self.dadosvotacao[i][0]
            votoD1 = self.dadosvotacao[i][3]
            for j in range(i + 1, linhas):
                nomeD2 = self.dadosvotacao[j][1]
                idVota2 = self.dadosvotacao[j][0]
                votoD2 = self.dadosvotacao[j][3]
                if idVota1 == idVota2:
                    if votoD1 == votoD2:
                        u = nomeD1
                        v = nomeD2
                        self.add_aresta(u, v)
                else:
                    break

    def calculaNumVert(self, lines):
        for i in range(1, lines):
            idDep = self.dadosvotacao[i][2]
            if idDep not in self.deputados:
                self.deputados.append(idDep)

        self.num_vert = len(self.deputados)

    def ler_arquivo(self, nome_arq):
        try:
            with open(nome_arq, 'r', encoding='utf-8') as arq:
                informacoes = []
                for linha in arq:
                    linha = linha.strip().split("\t")
                    if len(linha) >= 4:
                        idVotacao = linha[0]
                        nome_deputado = linha[1]
                        idDep = linha[2]
                        tipo_voto = linha[3]
                        informacoes = (idVotacao, nome_deputado, idDep, tipo_voto)
                        self.dadosvotacao.append(informacoes)
                print(self.dadosvotacao)

                self.calculaNumVert(len(self.dadosvotacao))
                self.agrupaVotos(len(self.dadosvotacao))
        except FileNotFoundError:
            print("Não foi possível encontrar ou ler o arquivo!")
        except IndexError:
            print("Índice inválido na leitura do arquivo TXT. Verifique se o arquivo está formatado corretamente.")
            
    def export_to_txt(self, nome_arquivo):
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
                arquivo.write(f"{self.num_vert} {self.arestas}\n")
                for u, arestas in self.grafo.items():
                    for v, peso in arestas.items():
                        u = u.replace("'", "").replace('"', '')
                        u = u.replace(" ", "_")
                        v = v.replace("'", "").replace('"', '')
                        v = v.replace(" ", "_")
                        linha = f"{u} {v} {peso}\n"
                        arquivo.write(linha)
            print("Grafo gravado no arquivo:", nome_arquivo)
        except IOError:
            print("Erro ao escrever o arquivo TXT.")

def caminho():
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
        votos_info = []
        for votacao in data["dados"]:
            idVotacao = votacao["id"]
            urlVotacao = f"https://dadosabertos.camara.leg.br/api/v2/votacoes/{idVotacao}/votos"
            responseVotacao = requests.get(urlVotacao)
            if responseVotacao.status_code == 200:
                leitura = responseVotacao.json()
                for item in leitura["dados"]:
                    id = item["deputado_"]["id"]
                    nome_deputado = item["deputado_"]["nome"]
                    tipo_voto = item["tipoVoto"]
                    votos_info.append(f"{idVotacao}\t{nome_deputado}\t{id}\t{tipo_voto}")
            else:
                print("Erro na requisição:", responseVotacao.status_code)
        
        if votos_info:
            with open("dados_exportados.txt", "w", encoding='utf-8') as txt_file:
                for info in votos_info:
                    txt_file.write(info + "\n")
            print("Dados exportados para o arquivo TXT: dados_exportados.txt")
            grafo = Grafo()
            grafo.ler_arquivo("dados_exportados.txt")
            grafo.export_to_txt("grafo.txt")
            print("Grafo gravado no arquivo: grafo.txt")
            # Executar o grafo após a leitura e exportação
            # Exemplo: grafo.executar()
        else:
            print("Nenhum dado encontrado.")
    else:
        print("Erro na requisição:", response.status_code)


