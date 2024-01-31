import random
from math import inf
import time
import matplotlib.pyplot as plt
import numpy as np

# Cria as variáveis do problema
#rest1
#rest2
#Vp
#P_max
#Ei=Vp*0.6
#Ed=Vp*0.7
#L=Vp*0.1
#Ef[j]=Ei[j]-Vp[j]+x[j]
#rest1[j]=Ef[j]-L[j]
#rest2=np.sum(x)-P_max
#Var=np.sum(np.abs(Ed[j]-Ef[j]))

#n=22
#Ea=np.zeros(n)
#Var=np.zeros(n)
#rest1=np.zeros(n)
#rest2=np.zeros(n)

#'max_num_iteration':800
#"population_size":800
#'mutation_probability':0.2
#'elit_ratio':0.01
#'crossover_probability':0.3
#'parents_portion':0.3
#'crossover_type':'uniform'
#'max_iteration_without_improv':None

import random
from math import inf
import time

def valorPrevistoVenda(valorProduto):
    Vp = []
    i = 0
    while i < 22:
        Vp.append(random.randrange(valorProduto[i], 1000))
        i+=1
    return Vp

def gerarPopulacaoInicial(tamanho):
    populacao = []
    FITNESS_ZERADO = 0
    for i in range(tamanho):
        populacao.append((geracao, preencherCromossomo(), FITNESS_ZERADO)) #tres atributos na população. O número da geração da população. O cromossomo da população. E o fitness.

    populacao = avaliarPopulacao(populacao)
    return populacao

def inicializarGeracao(populacao_existente):
    populacao = []
    FITNESS_ZERADO = 0
    for i in populacao_existente:
        populacao.append((geracao+1, i, FITNESS_ZERADO))
    populacao = avaliarPopulacao(populacao)
    return populacao

def preencherCromossomo():
    lista_de_valor = [6, 9, 13, 22, 6, 7, 3, 6, 2, 3, 3, 2, 2, 24, 10, 3, 2, 4, 5, 5, 6, 10]
    cromossomo = []
    TAMANHO_CROMOSSOMO = 22
    bool_binario = 0
    i = 0
    while i < TAMANHO_CROMOSSOMO:
        n = lista_de_valor[i] * 5
        cromossomo.append(random.randrange(0, n))
        i += 1
    while calcularPeso(cromossomo) > PESO_MAXIMO:
        cromossomo = []
        i = 0
        while i < TAMANHO_CROMOSSOMO:
            n = lista_de_valor[i] * 5
            cromossomo.append(random.randrange(0, n))
            i += 1
    if calcularPeso(cromossomo) <= PESO_MAXIMO:
        bool_binario = 1
        #print("Wow esse cromossomo não é pesado")
        #print("Peso ", calcularPeso(cromossomo))
        return cromossomo
    #print("O quão pesado é pra não tá gerando?? ", calcularPeso(cromossomo))

def avaliarPopulacao(populacao):
    #avalairPopulacao(populacao, Vp)
    resultados = []
    i = 0;
    valor = 0;
    for individuo in populacao:
        peso = calcularPeso(individuo[1])
        #Adicionar valor à fórmula do fitness
        if peso > PESO_MAXIMO:
            fitness = 0
        elif peso > 0:
            fitness = calcularLucro(individuo[1])
            resultados.append((individuo[0], individuo[1], fitness))
        i += 1;
    return resultados

def calcularPeso(cromossomo):
    peso = 0
    lista_de_pesos = [47, 47, 47, 47, 47, 47, 47, 23, 11, 11, 11, 5, 5, 47, 47, 5, 5, 23, 23, 23, 5, 23]
    for i,j in zip(cromossomo, lista_de_pesos):
        peso += i*j
    return peso

def selecionarMenoresFitness(populacao, tamanho):
    menores_resultados = []
    i = 0
    while i < tamanho:
        try:
            menores_resultados.append(populacao.pop())
        except IndexError:
            print('A lista está vazia')
        i += 1
    return menores_resultados

def selecionarMaioresFitness(populacao, tamanho):
    maiores_resultados = []
    populacao.reverse()
    i = 0
    while i < tamanho:
        try:
            maiores_resultados.append(populacao.pop())
        except IndexError:
            print('A lista está vazia')
        i += 1
    return maiores_resultados

def gerarFilhos(populacao):
    filhos = []
    tamanho = TAX_CROSSOVER ##testar com porcentagem da população no lugar de "0.3"
    while tamanho > 0 and len(populacao) >= 2:
        pai = populacao.pop(random.choice(range(len(populacao))))
        mae = populacao.pop(random.choice(range(len(populacao))))
        filho = pai[1][:12] + mae[1][12:]
        filha = mae[1][:12] + pai[1][12:]
        filhos.append(filha)
        filhos.append(filho)
        tamanho -= 1

    return filhos

def imprimirPopulacao(mensagem, populacao):
    print(mensagem)
    for individuo in populacao:
        print(individuo)

def completarPopulacao(populacao):
    while(TAM_POPULACAO > len(populacao)):
        aux = gerarPopulacaoInicial(TAM_POPULACAO-len(populacao))
        populacao.extend(aux)
    return populacao

def melhorResultado(populacao):
    global melhor_resultado
    global melhor_fitness
    try:
        if populacao[0][2] >= melhor_fitness:
            melhor_fitness = populacao[0][2]
            melhor_resultado = populacao[0]
    except IndexError:
        print("Fora do range")

def calcularLucro(cromossomo):
    lista_de_valor = [6, 9, 13, 22, 6, 7, 3, 6, 2, 3, 3, 2, 2, 24, 10, 3, 2, 4, 5, 5, 6, 10]
    valor = 0
    for i,j in zip(cromossomo, lista_de_valor):
        valor += i*j
    return valor

def maiorLucro(populacao):
    global melhor_lucro
    global posicao_lucro
    global cromossomo_lucro
    global fitness_lucro
    try:
        for i in populacao:
            if calcularLucro(i[1]) >= melhor_lucro:
                melhor_lucro = calcularLucro(i[1])
                posicao_lucro = i[0]
                cromossomo_lucro = i[1]
                fitness_lucro = i[2]
    except IndexError:
        print("Fora do range")

def mutar(populacao):
   lista_de_valor = [6, 9, 13, 22, 6, 7, 3, 6, 2, 3, 3, 2, 2, 24, 10, 3, 2, 4, 5, 5, 6, 10]
   for individuo in populacao:
       cromossomo = individuo[1]
       for i in range(len(cromossomo)):
           for j in range(4):
               if random.random() < TAXA_DE_MUTACAO: #tentar fazer esse com o porcentual da população
                cromossomo[i] = random.randrange(0, lista_de_valor[i]*5)
                #if i < 4:
                #    cromossomo[i] = random.randrange(0, 2)
                #elif i < 8:
                #    cromossomo[i] = random.randrange(0, 4)
                #else:
                #    cromossomo[i] = random.randrange(0, 64)

   return avaliarPopulacao(populacao)

lista_de_valor = [6, 9, 13, 22, 6, 7, 3, 6, 2, 3, 3, 2, 2, 24, 10, 3, 2, 4, 5, 5, 6, 10]
lista_de_quantidade_produtos = [37674, 16872, 18702, 9186, 12474, 37980, 9180, 4716, 42120, 97380, 30876, 21732, 4620, 38586, 11406, 4884, 6756, 2592, 6660, 11784, 17652, 1800]
lista_de_quantidade_plastico_por_garrafa = [47, 47, 47, 47, 47, 47, 47, 23, 11, 11, 11, 5, 5, 47, 47, 5, 5, 23, 23, 23, 5, 23]
tempo_o = time.time()
TAXA_DE_MUTACAO = 0.5
TAM_POPULACAO = 1500
TAX_CROSSOVER = 0.5
TAM_ELITE = 10%TAM_POPULACAO
TAM_MUTACAO = 5%TAM_POPULACAO

#PESO_MAXIMO ANTERIORMENTE CALCULADO 189000000 12720

PESO_MAXIMO = 14000
POSICAO_INDEX = 0
POSICAO_CROMOSSOMO = 1
POSICAO_FITNESS = 2
#num q a gente tava usando antes: 500
NUM_GERACOES = 20
geracao = 0
max_index = 0
nova_geracao = []
populacao = []
melhor_resultado = None
melhor_resultado_final = None
#lucro
posicao_lucro = None
melhor_lucro = 0
cromossomo_lucro = None
fitness_lucro = None
melhor_fitness = 0
populacao = gerarPopulacaoInicial(TAM_POPULACAO)
#pro grafico
par = []
x_values = []
y_values = []
print("Execução | Nº Gerações | Tamanho População | Taxa de Cruzamento | Taxa de Mutação | Melhor Fitness | Peso Fitness")
while geracao < NUM_GERACOES:
    #faz o cruzamento, a mutação e depois o fitness
    populacao = sorted(populacao, key=lambda x: x[POSICAO_FITNESS], reverse=True)
    melhores_resultados = selecionarMenoresFitness(populacao, TAM_ELITE)
    piores_resultados = selecionarMaioresFitness(populacao, TAM_MUTACAO)
    nova_geracao.clear()
    nova_geracao = inicializarGeracao(gerarFilhos(populacao))
    nova_geracao.extend(melhores_resultados)
    piores_resultados = mutar(piores_resultados)
    nova_geracao.extend(piores_resultados)
    nova_geracao = completarPopulacao(nova_geracao)
    nova_geracao = sorted(nova_geracao, key=lambda x: x[POSICAO_FITNESS], reverse=True)
    #tentar implementar pelo método da roleta
    melhorResultado(nova_geracao)
    #lucro
    maiorLucro(nova_geracao)
    populacao = nova_geracao
    par.append((nova_geracao[0], nova_geracao[2]))
    x_values.append(nova_geracao[0])
    y_values.append(nova_geracao[2])
    geracao += 1
    for i in nova_geracao:
        print(i)
    print("1", geracao, TAM_POPULACAO, TAX_CROSSOVER, TAXA_DE_MUTACAO, melhor_resultado[2], calcularPeso(melhor_resultado[1]))
plt.figure(figsize=(8, 6))

print("Melhor resultado global:")
print(melhor_resultado)
print("Lucro do melhor resultado global:")
print(calcularLucro(melhor_resultado[1]))
print("Peso do melhor resultado global:")
print(calcularPeso(melhor_resultado[1]))
#ele tá pegando o menor dos maiores valores (seleção por rankeamento)
print("Melhor lucro global:")
print(posicao_lucro, cromossomo_lucro, fitness_lucro, melhor_lucro)
print("Peso do melhor lucro global:")
print(posicao_lucro, calcularPeso(cromossomo_lucro))
print("Resultado iteração final:")
print(nova_geracao[0])
print("Lucro do resultado final:")
print("dps eu faço hehe")
print("Tempo de execução: {:.1f}".format(time.time()-tempo_o))

pairs = [{'x': 1, 'y': 12443}, {'x': 2, 'y': 10879}, {'x': 3, 'y': 8373}, {'x': 4, 'y': 12257}, {'x': 5, 'y': 12135}, {'x': 6, 'y': 16923}, {'x': 7, 'y': 11338}, {'x': 8, 'y': 11603}, {'x': 9, 'y': 12572}, {'x': 10, 'y': 18798}]

x_values = [pair['x'] for pair in pairs]
y_values = [pair['y'] for pair in pairs]

plt.plot(x_values, y_values)
plt.xlabel('Número execução')
plt.ylabel('Valores Fitness')
plt.show()
