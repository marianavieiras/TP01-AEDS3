import csv
import requests
import txt

class Graph:
  #Construtor do grafo
  def __init__(self, num_vert = 0, arestas = None):
    self.dadosvotacao = []
    self.deputados = []
    self.num_vert = num_vert
    if arestas == None:
      self.arestas = [[]for _ in range(num_vert)]
    else:
      self.arestas = arestas

    
  #Adicionar aresta com valor 1 do vértice u ao vértice v
  def add_aresta(self, u, v, w = 1):
    if u < self.num_vert and v < self.num_vert:
      self.arestas.append((u, v, w))
    else:
      print("Aresta inválida!")
      
  #Remove uma aresta
  def remove_aresta(self, u, v):
    if u < self.num_vert and v < self.num_vert:
      if self.mat_adj[u][v] != 0:   
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
    for i in range(len(self.arestas)):
      aresta = self.arestas[i]
      print("",aresta[0])
      if aresta[0] == u and aresta[1] == v:
        print("\nRepetiu u =" ,u, "e V = ", v)
        self.arestas[i][2]+=1
        return 1
    return 0
  
 #Essa função agrupa os deputados que realizam o mesmo tipo de voto em uma mesma votação, 
 # criando uma aresta e/ou aumentado o peso da aresta caso esses votos sejam iguais
  def agrupaVotos(self, linhas):
    for i in range(linhas):
      analisando = self.dadosvotacao[i]
      if(i+1 <= linhas): #evitando alcançar um indice que não existe
        for j in range(i+1 , 130):
          if(analisando[0] == self.dadosvotacao[j][0]):
            if(analisando[1] == self.dadosvotacao[j][1]):
              u = self.deputados.index(analisando[2])
              v = self.deputados.index(self.dadosvotacao[j][2])
              if(self.buscaAresta(u, v) == 0): 
                self.add_aresta(u,v)

          else:
            print("Arestas = ", self.arestas)
            continue
          #analisado.append(analisando)
          #print(analisado,"\n")
          #self.comparaVotos(analisando, analisado)

  #Como o meu numero de vertices é definido pela quantidade de deputados, 
  # por meio desta função é possivel definir essa quantidade baseado no 
  # tamanho do array deputados sendo seu indice nesse array o que define 
  # o seu indice na lista de adijacencias
  def calculaNumVert(self, lines):
    for i in range(lines):
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
            #print(informacoes)
            self.dadosvotacao.append(informacoes)
      self.calculaNumVert(lines)
      self.agrupaVotos(lines)  
         
    except FileNotFoundError:
      print("Não foi possível encontrar ou ler o arquivo!")
  def gerar (self):
    generator = txt('meu_arquivo.txt')
    content = self.arestas
    generator.write_content(content)
