import graph


gf = graph.Graph()  # Cria uma instância da classe Graph

arquivo = "votacoesVotos-2023.xlsx"  # Substitua com o nome do arquivo XLSX

gf.ler_arquivo(arquivo)  # Chama o método ler_arquivo() com o nome do arquivo como argumento