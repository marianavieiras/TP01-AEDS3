import time # Linha para importar a biblioteca para calcular tempo de execução.

class Grafo:

  def __init__(self, num_vert = 0, num_arestas = 0, lista_adj = None, mat_adj = None, repre=False, pond=True, negativo=False):
    self.num_vert = num_vert
    self.num_arestas = num_arestas
    self.repre=repre # Variável utilizada para definir a representação
    self.pond=pond   # Variável utilizada para definir se o grafo é ponderado
    self.negativo=negativo # Variável utilizada para defininir se o grafo possui arestas negativas
    if lista_adj is None:
      self.lista_adj = [[] for i in range(num_vert)]
    else:
      self.lista_adj = lista_adj
    if mat_adj is None:
      self.mat_adj = [[0 for j in range(num_vert)] for i in range(num_vert)]
    else:
      self.mat_adj = mat_adj
    
  def add_aresta(self, u, v, w = 1):
    """Adiciona aresta de u a v com peso w"""
    self.num_arestas += 1
    if u < self.num_vert and v < self.num_vert:
      self.lista_adj[u].append((v, w))
      self.mat_adj[u][v] = w
    else:
      print("Aresta invalida!")

  def remove_aresta(self, u, v):
    """Remove aresta de u a v, se houver"""
    if u < self.num_vert and v < self.num_vert:
      if self.mat_adj[u][v] != 0:
        self.num_arestas -= 1
        self.mat_adj[u][v] = 0
        for (v2, w2) in self.lista_adj[u]:
          if v2 == v:
            self.lista_adj[u].remove((v2, w2))
            break
      else:
        print("Aresta inexistente!")
    else:
      print("Aresta invalida!")

  def grau(self, u):
    """Retorna o grau do vertice u"""
    return len(self.lista_adj[u])

  def adjacente(self, u, v):
    """Determina se v é adjacente a u"""
    if self.mat_adj[u][v] != 0:
      return True
    else:
      return False

  def adjacentes_peso(self, u):
    """Retorna a lista dos vertices adjacentes a u no formato (v, w)"""
    return self.lista_adj[u]

  def adjacentes(self, u):
    """Retorna a lista dos vertices adjacentes a u"""
    adj = []
    for i in range(len(self.lista_adj[u])):
      (v, w) = self.lista_adj[u][i]
      adj.append(v)
    return adj

  def densidade(self):
    """Retorna a densidade do grafo"""
    return self.num_arestas / (self.num_vert * (self.num_vert - 1))

  def subgrafo(self, g2):
    """Determina se g2 e subgrafo de self"""
    if g2.num_vert > self.num_vert:
      return False
    for i in range(len(g2.mat_adj)):
      for j in range(len(g2.mat_adj[i])):
        if g2.mat_adj[i][j] != 0 and self.mat_adj[i][j] == 0:
          return False
    return True

  def ler_arquivo(self, nome_arq):
    """Le arquivo de grafo no formato dimacs"""
    try:
      arq = open("Arquivos/"+nome_arq)
      #Leitura do cabecalho
      str = arq.readline()
      str = str.split(" ")
      self.num_vert = int(str[0])
      if self.num_vert>1000: # Linha para definir qual a melhor estrutura para representar o grafo.
        self.repre=True
      cont_arestas = int(str[1])
      #Inicializacao das estruturas de dados
      self.lista_adj = [[] for i in range(self.num_vert)]
      self.mat_adj = [[0 for j in range(self.num_vert)] for i in range(self.num_vert)] 
      #Le cada aresta do arquivo
      for i in range(0,cont_arestas):
        str = arq.readline()
        str = str.split(" ")
        u = int(str[0]) #Vertice origem
        v = int(str[1]) #Vertice destino
        w = int(str[2]) #Peso da aresta
        self.add_aresta(u, v, w)
        if w == 0:   # Flag para definir se o grafo é ponderado ou não.
          self.pond=False
        if w < 0 :   # Flag para definir se o grafo possui arestas negativas.
          self.negativo=True
    except IOError:
      print("Nao foi possivel encontrar ou ler o arquivo!")

  def busca_profundidade(self, s):
    """Retorna a ordem de descoberta dos vertices pela 
       busca em profundidade a partir de s"""
    desc = [0 for v in range(self.num_vert)]
    S = [s]
    R = [s]
    desc[s] = 1
    while S:
      u = S[-1]
      desempilhar = True
      for (v, w) in self.lista_adj[u]:
        if desc[v] == 0:
          desempilhar = False
          S.append(v)
          R.append(v)
          desc[v] = 1
          break
      if desempilhar:
        S.pop(-1)
    return R
  
  def busca_profundidade_rec(self, s, R, desc):
    """Retorna a ordem de descoberta dos vertices pela 
       busca em profundidade a partir de s"""
    R.append(s)
    desc[s] = 1
    for (v, w) in self.lista_adj[s]:
      if desc[v] == 0:
        self.busca_profundidade_rec(v, R, desc)
    return R
  
  def busca_largura(self, s):
    """Retorna a ordem de descoberta dos vertices pela 
       busca em largura a partir de s"""
    desc = [0 for v in range(self.num_vert)]
    Q = [s]
    R = [s]
    desc[s] = 1
    while Q:
      u = Q.pop(0)
      for (v, w) in self.lista_adj[u]:
        if desc[v] == 0:
          Q.append(v)
          R.append(v)
          desc[v] = 1
    return R
  
  def conexo(self, s):
    """Retorna Ture se o grafo e conexo e False caso contrario
       baseado na busca em largura"""
    desc = [0 for v in range(self.num_vert)]
    Q = [s]
    R = [s]
    desc[s] = 1
    while Q:
      u = Q.pop(0)
      for (v, w) in self.lista_adj[u]:
        if desc[v] == 0:
          Q.append(v)
          R.append(v)
          desc[v] = 1
    for i in range(len(desc)):
      if desc[i] == 0:
        return False
    return True

  def ciclo(self, s):
    """Retorna Ture se o grafo tem ciclo e False caso contrario
       baseado na busca em largura"""
    desc = [0 for v in range(self.num_vert)]
    for s in range(self.num_vert):
      if desc[s] == 0:
        Q = [s]
        R = [s]
        desc[s] = 1
        while Q:
          u = Q.pop(0)
          for (v, w) in self.lista_adj[u]:
            if desc[v] == 0:
              Q.append(v)
              R.append(v)
              desc[v] = 1
            else:
              return True
    return False
  
  #Busca em largura : Grafos não ponderados
  #Dijkstra: Grafos em geral que não tenha arestas negativas 
  #Bellman-Ford: Grafos em Geral, mas lida com arestas de peso negativo 
  
  # Algoritmos desenvolvidos para o trabalho
  
  def menu(self,nome,origem,destino):
    
    self.ler_arquivo(nome)
    
    # Para utilizar o algoritmo de DJIKSTRA: Descomentar a linha do if
    # e apagar "or self.pond == True and self.negativo == False" da linha que faz a chamada do Bellman_ford
    
    #if self.pond == True and self.negativo == False:
       #self.dijkstra(origem,destino)
    if self.pond == True and self.negativo == True or self.pond == True and self.negativo == False:
      self.Bellman_ford(origem,destino)  
    if self.pond == False and self.negativo ==False:
      self.busca_largura_alterado(origem,destino) 
     
  #Algoritmo de busca em largura adaptado para o problema do caminho mínimo.
  
  def busca_largura_alterado(self, s, destino):
    """Retorna a ordem de descoberta dos vertices pela 
       busca em largura a partir de s"""
       
    inicio = time.time() # Inicio do Timer para calcular o tempo de execução
    
    pred = [None for v in range(self.num_vert)]
    dist = [float('inf') for v in range(self.num_vert)]
    dist[s]=0
    Q = [s]
  
    while Q:
      u = Q.pop(0)
      for (v, w) in self.lista_adj[u]:
        if dist[v] == float("inf"):
          dist[v] = dist[u]+1
          pred[v]=u
          Q.append(v)
          
    fim = time.time()
    resultado=fim-inicio # Variável utilizada para calcular o tempo final de execução do algoritmo
    
    # Linha para realizar a impressão dos resultados
    
    print("\nAlgoritmo: Busca em Largura\n")
    print(f"Vertice origem: {s}")
    print(f"Vertice destino: {destino}")
    print("Processando...")
    print(f"Caminho: {self.recupera(s,destino,pred)}")
    print(f"Custo: {dist[destino]}")
    print(f"Tempo de execução: {resultado} segundos")
    
    if self.repre == False:
      print("\nMelhor representação: Matriz de adjacência\n")
      #print(self.mat_adj)
    else:
      print("Melhor representação: Lista de adjacência\n")
      #print(self.lista_adj)    
    return dist, pred
  
  # Função criada para recuperar o caminho minimo
  @staticmethod
  def recupera(origem,destino,pred):
    
    C=[destino]
    aux=destino
      
    while aux != origem: # Linhas para recuperar o caminho de um vertice ao outro.
      aux=pred[aux]
      C.append(aux)
       
    C.reverse() # Linha para inverter o conteudo de C para recuperar o caminho corretamente.
    return C
  
  #Algoritmo de Dijkstra para resolver o problema do caminho mínimo

  @staticmethod
  def func_min(Q,dist):
    
    menor = float('inf') # Usa a distancia da primeira comparação como infinita
    vertice=None
    for v in Q: # Faz comparação entre a distancia entre os vertices da lista, retornando a menor
      if dist[v] < menor:
        menor = dist[v]
        vertice= v
        
    return vertice   
        
  def dijkstra(self,s,destino):
    
    inicio = time.time() # Inicio do Timer para calcular o tempo de execução
    
    dist = [float('inf') for v in range(self.num_vert)] # Vetor que armazena a distancia entre os vertices
    pred = [None for v in range(self.num_vert)]         # Vetor que armazena os predecessores
    dist[s]=0                                           # Linha para definir a distancia dos vertices iniciais como 0
    Q = [v for v in range(self.num_vert)]               # Linha para iniciar o Q com os vertices do grafo 
    
    while Q != []: 
      u=self.func_min(Q,dist) # Chamada da função para retornar o vertice com a menor distancia
      Q.remove(u)             # Remove o vertice da lista Q
      for (v,w) in self.adjacentes_peso(u): # Retorna os adjacentes com o peso e faz o calculo do caminho minimo
        vert=v
        peso=w
        if dist[vert]>dist[u]+peso:
            dist[vert]=dist[u]+peso
            pred[vert]=u
    
    fim = time.time()
    resultado=fim-inicio # Variável utilizada para calcular o tempo final de execução do algoritmo
    
    # Linha para realizar a impressão dos resultados
    
    print("\nAlgoritmo: Dijkstra\n")
    print(f"Vertice origem: {s}")
    print(f"Vertice destino: {destino}")
    print("Processando...")
    print(f"Caminho: {self.recupera(s,destino,pred)}")
    print(f"Custo: {dist[destino]}")
    print(f"Tempo de execução: {resultado} segundos")
    
    if self.repre == False:
      print("\nMelhor representação: Matriz de adjacência\n")
      #print(self.mat_adj)
    else:
      print("Melhor representação: Lista de adjacência\n")
      #print(self.lista_adj)
    
    return dist,pred

  #Algoritmo do Bellman-Ford para resolver o problema do caminho mínimo 
    
  def Bellman_ford(self,s,destino):
    
    inicio = time.time() # Inicio do Timer para calcular o tempo de execução
    
    dist = [float('inf') for v in range(self.num_vert)] # Vetor que armazena a distancia entre os vertices
    pred = [None for v in range(self.num_vert)]         # Vetor que armazena os predecessores
    Q = [v for v in range(self.num_vert)] 
    dist[s]=0
    tuplas=[] 
    
    for v in Q: # Linhas utilizadas para pegar os valores do vertice de entrada saida e o seu peso
      for j in self.lista_adj[v]:
        tuplas.append((v,j[0],j[1]))

    for i in range(self.num_vert-1):
      mudou = False    # Flag para caso não ocorra mudanças encerrar o ciclo prematuramente
      for b in tuplas: # Utiliza as variáveis gravadas em nas tuplas para fazer o calculo de distancia
        u=b[0]
        v=b[1]
        w=b[2]
        if dist[v]>dist[u]+w:
            dist[v]=dist[u]+w
            pred[v]=u
            mudou = True
      
      if mudou is False:
        break
    
    fim = time.time()
    resultado=fim-inicio # Variável utilizada para calcular o tempo final de execução do algoritmo
    
    #Linhas para realizar a impressão dos resultados
    
    print("\nAlgoritmo: Bellman-Ford\n")
    print(f"Vertice origem: {s}")
    print(f"Vertice destino: {destino}")
    print("Processando...")
    print(f"Caminho: {self.recupera(s,destino,pred)}")
    print(f"Custo: {dist[destino]}")
    print(f"Tempo de execução: {resultado} segundos")
    
    if self.repre == False:
      print("\nMelhor representação: Matriz de adjacência\n")
      #print(self.mat_adj)
    else:
      print("Melhor representação: Lista de adjacência\n")
      #print(self.lista_adj)
    
    return dist,pred
            
        