import csv
import requests

class Graph:
  #Construtor do grafo
  def __init__(self, num_vert = 0, lista_adj = None, mat_adj = None , arestas = None):
    self.dadosvotacao = []
    self.num_vert = num_vert
    if lista_adj == None:
      self.lista_adj = [[]for _ in range(num_vert)]
    else: 
      self.lista_adj = lista_adj
    if arestas == None:
      self.arestas = [[]for _ in range(num_vert)]
    else:
      self.arestas = arestas
    
  #Adicionar aresta com valor 1 do vértice u ao vértice v
  def add_aresta(self, u, v, w = 1):
    self.num_arestas += 1
    if u < self.num_vert and v < self.num_vert:
      self.arestas.append((u, v, w))
      self.lista_adj[u].append((v, w)) 
    else:
      print("Aresta inválida!")
      
  #Remove uma aresta
  def remove_aresta(self, u, v):
    if u < self.num_vert and v < self.num_vert:
      if self.mat_adj[u][v] != 0:
        self.num_arestas += 1
        self.mat_adj[u][v] = 0
        for (v2, w2) in self.lista_adj[u]:
          if v2 == v:
            self.lista_adj[u].remove((v2, w2))
            break
      else:
        print("Aresta inexistente!")
    else:
      print("Aresta invalida!")

  def buscaAresta(self,u,v):
    return 0
  def comparaVotos(self,analisando, analisado):
    for voto in analisado:
      if voto[1] == analisando[1]:
        self.buscaArestaVotes()
    return 0
 
  def agrupaVotos(self, linhas):
    analisado = []
    for i in range(linhas):
      analisando = self.dadosvotacao[i]
      while analisando[0] == self.dadosvotacao[i+1][0]:
        analisado.append(analisando)
        self.comparaVotos(analisando, analisado)
        
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
            print("informacoes =", informacoes)
            self.dadosvotacao.append(informacoes)
      self.agrupaVotos(lines)  
         
    except FileNotFoundError:
      print("Não foi possível encontrar ou ler o arquivo!")


