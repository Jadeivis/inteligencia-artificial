import random
import time
import math
from typing import List, Tuple

# --------------------------
# Funções auxiliares
# --------------------------
def distancia(c1, c2):
    return math.hypot(c1[0] - c2[0], c1[1] - c2[1])

def total_distancia(caminho, cidades):
    return sum(distancia(cidades[caminho[i]], cidades[caminho[i + 1]]) for i in range(len(caminho) - 1)) + distancia(cidades[caminho[-1]], cidades[caminho[0]])

def criar_caminho_aleatorio(n):
    caminho = list(range(n))
    random.shuffle(caminho)
    return caminho

def criar_caminho_heuristico(cidades):
    n = len(cidades)
    restante = list(range(n))
    atual = restante.pop(0)
    caminho = [atual]
    while restante:
        proxima = min(restante, key=lambda i: distancia(cidades[atual], cidades[i]))
        restante.remove(proxima)
        caminho.append(proxima)
        atual = proxima
    return caminho

# --------------------------
# Crossover
# --------------------------
def crossover_um_ponto(pai1, pai2):
    ponto = random.randint(1, len(pai1) - 2)
    filho = pai1[:ponto] + [gene for gene in pai2 if gene not in pai1[:ponto]]
    return filho

def crossover_dois_pontos(pai1, pai2):
    p1, p2 = sorted(random.sample(range(len(pai1)), 2))
    meio = pai1[p1:p2]
    resto = [gene for gene in pai2 if gene not in meio]
    return resto[:p1] + meio + resto[p1:]

def crossover_uniforme(pai1, pai2):
    filho = []
    for i in range(len(pai1)):
        gene = pai1[i] if random.random() < 0.5 else pai2[i]
        if gene not in filho:
            filho.append(gene)
    # Corrigir duplicatas e faltantes
    faltantes = [g for g in range(len(pai1)) if g not in filho]
    return filho + faltantes

# --------------------------
# Mutação
# --------------------------
def mutacao(caminho, taxa):
    for i in range(len(caminho)):
        if random.random() < taxa:
            j = random.randint(0, len(caminho) - 1)
            caminho[i], caminho[j] = caminho[j], caminho[i]
    return caminho

# --------------------------
# Algoritmo Genético
# --------------------------
def algoritmo_genetico(cidades: List[Tuple[float, float]], n_geracoes=500, tamanho_pop=100, crossover_tipo="um_ponto", mutacao_nivel="baixa", inicializacao="aleatoria", criterio="geracoes"):

    inicio = time.time()
    n = len(cidades)

    taxas_mutacao = {"baixa": 0.01, "media": 0.05, "alta": 0.1}
    taxa_mut = taxas_mutacao.get(mutacao_nivel, 0.01)

    if inicializacao == "heuristica":
        pop = [criar_caminho_heuristico(cidades)] + [criar_caminho_aleatorio(n) for _ in range(tamanho_pop - 1)]
    else:
        pop = [criar_caminho_aleatorio(n) for _ in range(tamanho_pop)]

    melhor_caminho = min(pop, key=lambda c: total_distancia(c, cidades))
    melhor_distancia = total_distancia(melhor_caminho, cidades)
    cont_igual = 0

    for geracao in range(n_geracoes):
        nova_pop = []

        pop = sorted(pop, key=lambda c: total_distancia(c, cidades))
        elite = pop[:10]
        nova_pop.extend(elite)

        while len(nova_pop) < tamanho_pop:
            pai1, pai2 = random.sample(elite, 2)
            if crossover_tipo == "um_ponto":
                filho = crossover_um_ponto(pai1, pai2)
            elif crossover_tipo == "dois_pontos":
                filho = crossover_dois_pontos(pai1, pai2)
            else:
                filho = crossover_uniforme(pai1, pai2)

            filho = mutacao(filho, taxa_mut)
            nova_pop.append(filho)

        pop = nova_pop
        atual_melhor = min(pop, key=lambda c: total_distancia(c, cidades))
        atual_dist = total_distancia(atual_melhor, cidades)

        if atual_dist < melhor_distancia:
            melhor_distancia = atual_dist
            melhor_caminho = atual_melhor
            cont_igual = 0
        else:
            cont_igual += 1

        if criterio == "convergencia" and cont_igual >= 50:
            break

    fim = time.time()
    tempo_exec = fim - inicio
    return melhor_caminho, melhor_distancia, tempo_exec

# --------------------------
# Entrada do usuário
# --------------------------
def main():
    n = int(input("Digite o número de cidades: "))
    cidades = []
    for i in range(n):
        coord = input(f"Digite as coordenadas X e Y da cidade {i+1} (separadas por espaço): ")
        x, y = map(float, coord.strip().split())
        cidades.append((x, y))


    crossover_tipo = input("Tipo de crossover (um_ponto, dois_pontos, uniforme): ").strip()
    mutacao_nivel = input("Nível de mutação (baixa, media, alta): ").strip()
    inicializacao = input("Inicialização da população (aleatoria, heuristica): ").strip()
    criterio = input("Critério de parada (geracoes, convergencia): ").strip()

    melhor_caminho, dist, tempo = algoritmo_genetico(
        cidades,
        crossover_tipo=crossover_tipo,
        mutacao_nivel=mutacao_nivel,
        inicializacao=inicializacao,
        criterio=criterio
    )

    print("\n=== Resultado ===")
    print("Melhor caminho encontrado:", [i+1 for i in melhor_caminho])
    print("Distância total:", round(dist, 2))
    print("Tempo de execução: %.4f segundos" % tempo)

if __name__ == "__main__":
    main()
