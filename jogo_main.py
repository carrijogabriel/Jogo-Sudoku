##Começo criando a matriz 9x9 com 0 em cada posição que serão os números que vão aparecer 
import numpy as np
import random

##Inicialmente criei essa função para gerar uma matriz inicial aleatória, mas acabava que não seguia as regras de completá-la depois e todas dava sem solução
#def gerar_jogo_inicial_aleatorio():      ##função para gerar uma matriz de jogo inicial aleatória
#    matriz = np.zeros((9,9),dtype=int)   ##começo criando uma matriz 9x9 de zeros, com todos sendo do tipo inteiro
#    numeros_adicionados = 0              ##variável para adicionar números no lugar dos 0, começa vazia
#    while numeros_adicionados <= random.randint(30,40):     ##enquanto a quantidade de números adicionados for menor ou igual a 
#                                                            ##a uma quantidade aleatória de números entre 30 e 40 que serão
#                                                            ##gerados a cada jogo faço o restante
#        linha = random.randint(0,8)                         ##uma linha aleatória
#        coluna = random.randint(0,8)                        ##uma coluna aleatória
#        numero = random.randint(1,9)                        ##um número aleatório
#        if matriz[linha, coluna] == 0:
#            if verificar_sudoku(matriz, linha, coluna, numero):
#                matriz[linha, coluna] = numero
#                numeros_adicionados += 1
#    return matriz




def sudoku_legivel(jogo):                 ##função para deixar o jogo mais visível
    for i in range(9):                    ##começo indo de linha em linha da matriz do array
        if i % 3 == 0 and i != 0:         ##se a linha for divisível por 3 (0,3,6,9), e não for 0, faço esses traços para separar o bloco de 3x3
            print('-'*12)
        linha = ''                        ##linha começa vazia porque vou adicionando itens
        for j in range(9):                ##enquanto faço o for de linhas, faço o de colunas, quando completar 3, como acima, a linha recebe | para separar blocos 3x3
            if j % 3 == 0 and j != 0:
                linha += '|'
            if jogo[i,j] == 0:            ##se na posição de linha e coluna que estiver for preechida com 0, linha recebe .
                linha += '.'
            else:                         ##mas se estiver preechida com outro valor, linha vai receber o número na posição
                linha += f'{jogo[i,j]}'
        print(linha)                      ##no final do for das colunas de cada linha printo a linha


def verificar_sudoku(jogo, linha, coluna, numero):   ##verifico se um número em posição do jogo é aceito ou não 
    linha_atual = jogo[linha,:]                      ##na linha que verifico, vou percorrendo a matriz coluna por coluna
    for cont in range(9):
        if linha_atual[cont] == numero:        ##nessa linha, vejo se tem uma coluna que já tem o número, se tiver retorna falso
            return False
    coluna_atual = jogo[:, coluna]             ##para a coluna que verifico, vou percorrendo linha a linha
    for cont in range(9):
        if coluna_atual[cont] == numero:       ##se naquela coluna alguma linha já tiver o número, retorna falso
            return False
    inic_bloco_linha = (linha // 3) * 3        ##aqui eu divido a matriz em vários blocos 3x3, nesse caso dividindo a linha por 3 (// para achar só a parte inteira)
                                               ##e multiplico por três para achar onde começa a linha do bloco  (ex: se for a linha 7 ela começa na 6, então vai ser 6,7,8)
    inic_bloco_coluna = (coluna // 3) * 3      ##mesma coisa que na linha de cima mas agora para coluna
    for i in range(3):
        for j in range(3):                     ##dentro de cada linha percorro cada coluna do bloco
            if jogo[inic_bloco_linha + i, inic_bloco_coluna + j] == numero:      ##faço no jogo na posição de linha onde achei que começa a linha do bloco
                                                                                 ##mais o i para achar a linha de agora e na posição que começa o bloco mais j
                                                                                 ##para achar a coluna de agora, e nesse bloco vejo se já tem o número, retornando falso se sim
                return False
    return True                                ##se não tiver o número em lugar nenhum retorno verdadeiro


def resolvendo_sudoku(jogo):                   ##função para resolver o sudoku
    for linha in range(9):
        for coluna in range(9):
            if jogo[linha,coluna] == 0:        ##para cada coluna em cada linha verifico se está com número ou não, ou seja, se está com 0
                for n in range(1,10):          ##se estiver com 0 percorro do 1 ao 9 para tentar completar a posição
                    if verificar_sudoku(jogo, linha, coluna, n):    ##chamo a função de verificação do número para ver se o número pode entrar na posição
                        jogo[linha,coluna] = n           ##se puder completar coloco o número no lugar do 0
                        if resolvendo_sudoku(jogo):      ##faço uma recursividade chamando novamente a função resolvendo_sudoku e se der tudo certo retorno True
                            return True
                        jogo[linha, coluna] = 0        ##se não puder completar com aquele número mantenho 0
                return False                   ##retorno False se não for possível completar nenhum
    return True                                ##retorno True se der certo e completar voltando ao início do for da linha, até terminar


##primeiro chamo a função de gerar uma matriz aleatória para criar uma matriz que contenha 9 linhas e 9 colunas 
matriz_np = gerar_jogo_inicial_aleatorio()

##print(matriz_np)                         ##fiz esse print para ver a matriz inicial, ver se estava certa
##sudoku_legivel(matriz_np)                ##fiz esse print para ver se a matriz estava formatando corretamente
##print(verificar_sudoku(matriz_np,0,6,3)) ##fiz esse print apenas como exemplo para testar se estava funcionando a verificação se um número 
                                           ##podia entrar naquela linha e coluna, no caso o número 3 na posição [0,6]

print("\033[32m=== SUDOKU ===\033[m")
sudoku_legivel(matriz_np)                  ##mostrei a matriz inicial com posições para completar que são representadas por .
print()

if resolvendo_sudoku(matriz_np):           ##chamo a função de resolução se for True
    print("\033[32m=== SUDOKU RESOLVIDO ===\033[m")
    sudoku_legivel(matriz_np)              ##mostro o sudoku resolvido
else: 
    print("SEM SOLUÇÃO.")                  ##se não for posível resolver, mostro que foi sem solução