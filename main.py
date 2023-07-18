import graph
import csv
import api

valor = int(input("Informe como você quer tratar os seus dados:\n1-Via nome de arquivo. Ex. 'Votacoes.csv' \n2-Via API\n"))

match valor:
    case 1:
        arquivo = input("Informe o nome do arquivo CSV:")
        gf = graph.Graph()  # Cria uma instância da classe Graph
        gf.ler_arquivo(arquivo)  # Chama o método ler_arquivo() com o nome do arquivo como argumento
        print ("Adicione um arquivo txt já criado em sua pasta para que possamos adicionar o resultado desejado.")
        arquivo = input("Informe o nome do arquivo txt de saida:")
        gf.escrever_grafo_em_txt(arquivo)
    case 2:
        print("O arquivo através da API contém uma limatação que ainda tratamos, estamos trabalhando em uma atualização para lhe atender.")
        print("Rodando arquivo....")
        api = api.caminho () 
    case _:
        print("O valor Indisponivel tente novamente")