import csv
import sys
import requests
import txt
class Graph:
  #Construtor do grafo
  def __init__(self):
    self.dadosvotacao = []
    self.deputados = []
    self.grafo = {}
    self.num_vert = 0
    self.arestas = 0

    
  #Adicionar aresta com valor 1 do vértice u ao vértice v
  def add_aresta(self, u, v, w=1):
    if(u in self.grafo):
        if (v in self.grafo[u]):
          self.grafo[u][v] += 1
          return
    else:
      self.grafo[u] = {}
    self.grafo[u][v] = w
    self.arestas += 1
    
 #Essa função agrupa os deputados que realizam o mesmo tipo de voto em uma mesma votação, 
 # criando uma aresta e/ou aumentado o peso da aresta caso esses votos sejam iguais
  def agrupaVotos(self, linhas):
    for i in range(1, linhas):
      nomeD1 = self.dadosvotacao[i][3]
      idVota1 = self.dadosvotacao[i][0]
      votoD1 = self.dadosvotacao[i][1] 
      for j in range(i+1, linhas):
        nomeD2 = self.dadosvotacao[j][3]
        idVota2 = self.dadosvotacao[j][0]
        votoD2 = self.dadosvotacao[j][1]
        if idVota1 == idVota2:
          if votoD1 == votoD2:
            u = nomeD1
            v = nomeD2
            self.add_aresta(u, v)
        else:
          break

  #Como o meu numero de vertices é definido pela quantidade de deputados, 
  # por meio desta função é possivel definir essa quantidade baseado no 
  # tamanho do array deputados sendo seu indice nesse array o que define 
  # o seu indice na lista de adijacencias
  def calculaNumVert(self, lines):
    for i in range(1,lines):
      idDep = self.dadosvotacao[i][2]
      if(idDep not in self.deputados):
        self.deputados.append(idDep)
    self.num_vert = len(self.deputados)    

  #Ler um arquivo csv
  def ler_arquivo(self, nome_arq):
    try:
      with open(nome_arq, 'r', encoding='utf-8') as arq:
          informacoes = []
          lines = sum(1 for _ in arq)# Quantidade de linhas do arquivo
          arq.seek(0)  # Retorna ao início do arquivo

          for _ in range(lines):
            linha = arq.readline()
            linha = linha.strip().split(";")
            idVotacao = linha[0]
            voto = linha[3]
            idDep = linha[4]
            nomeDep = linha[6]
            informacoes = (idVotacao, voto, idDep, nomeDep)

            self.dadosvotacao.append(informacoes)
      self.calculaNumVert(lines)
      self.agrupaVotos(lines)
    except FileNotFoundError:
      print("Não foi possível encontrar ou ler o arquivo!")

  def escrever_grafo_em_txt(self, nome_arquivo):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
      linha = f"{self.num_vert} {self.arestas}\n"
      arquivo.write(linha)
      for u, arestas in self.grafo.items():
        for v, peso in arestas.items():
          u = u.replace("'", "").replace('"', '')
          u = u.replace(" ", "_")
          v = v.replace("'", "").replace('"', '')
          v = v.replace(" ", "_")
          linha = f"{u} {v} {peso}\n"
          arquivo.write(linha)
    print("Grafo gravado no arquivo:", nome_arquivo)