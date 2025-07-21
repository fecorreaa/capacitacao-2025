class Ambiente:

    def __init__(self, tamanho=100): #__init__ é o construtor da classe
        self.tamanho = tamanho 
        self.terreno = [0] * tamanho # chão plano (altura 0)
        self.info_obstaculo = [] #guardar as infos dos obstaculos
        self._gerar_obstaculo()
    

    def _gerar_obstaculo (self): # p criar obstaculos
        obstaculos = [
            {'posicao': 20, 'largura': 5, 'altura': 9, 'comprimento': 10},
            {'posicao': 45, 'largura': 7, 'altura': 15, 'comprimento': 15},
            {'posicao': 79, 'largura': 10, 'altura': 11, 'comprimento': 8}
        ]
        
        for obstaculo in obstaculos:
            self.info_obstaculo.append(obstaculo)

            posicao = obstaculo['posicao']
            largura = obstaculo['largura']
            altura = obstaculo['altura']
            comprimento = obstaculo['comprimento']


            #substituição dos 0s pela altura
            for i in range(largura):
                if(posicao + i) < self.tamanho:
                    self.terreno[posicao + i] = altura


    def obter_altura(self, x_pos):

        x = int(round(x_pos)) # arredondado

        if 0 <= x <self.tamanho:
            return self.terreno[x]
        
        else:
            return 0