class txt:
    def __init__(self, filename):
        self.filename = filename
    
    def write_content(self, content):
        with open(self.filename, 'w') as file:
            file.write(content)
            print(f"Arquivo {self.filename} gerado com sucesso!")
