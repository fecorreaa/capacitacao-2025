from ambiente import Ambiente
from drone import Drone
import time 

def imprimir_ambiente(ambiente):
    print("Mapa do Ambiente( _ = Chão, █ = Obstáculo): \n\n")
    mapa_visual = ""
    for altura in ambiente.terreno:
        if altura > 0:
            mapa_visual += "█"
        else:
            mapa_visual += "_"
    print(mapa_visual)
    print('\n')



def main():
    print('\n --------------------------------------------------')
    print('Iniciando a simulação do drone...')
    print('Pressione CTRL+C para parar a qualquer momento.')
    print('-------------------------------------------------- \n')

    ambiente_voo = Ambiente(tamanho=100)
    drone_ = Drone(posicao_inicial=(10, 50, 0, 0), ambiente=ambiente_voo)

    print('\n Informações dos obstáculos criados: ')

    for i, obs in enumerate(ambiente_voo.info_obstaculo):
        print(f"  - Obstáculo #{i+1}: Posição inicial={obs['posicao']}, Largura={obs['largura']}, Altura={obs['altura']}, Comprimento = {obs['comprimento']}")
    print("-" * 100) 

    imprimir_ambiente(ambiente_voo)
    


    try:
        for passo in range(180):

            if passo == 60:
                print('\n\n Mudar a altitude para 30 \n')
                drone_.altitude_alvo = 30

            if passo == 120:
                print('\n\n Mudar altitude para 70 \n')
                drone_.altitude_alvo = 70

            drone_.executar()
            drone_.fisica()
            drone_.reportar_status()
            time.sleep(0.2)
    
    except KeyboardInterrupt:
        print('Simulação interrompida. \n')

    print('Fim da simulação.')


if __name__ == "__main__":
    main()