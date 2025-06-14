import time
import tracemalloc
import heapq

# Estado final desejado
ESTADO_OBJETIVO = (1, 2, 3,
                   4, 5, 6,
                   7, 8, 0)

MOVIMENTOS_POSSIVEIS = {
    'cima': -3,
    'baixo': 3,
    'esquerda': -1,
    'direita': 1
}

def movimento_valido(pos_zero, direcao):
    if direcao == 'cima':
        return pos_zero > 2
    if direcao == 'baixo':
        return pos_zero < 6
    if direcao == 'esquerda':
        return pos_zero % 3 != 0
    if direcao == 'direita':
        return pos_zero % 3 != 2
    return False

def mover_peca(estado, direcao):
    pos_zero = estado.index(0)
    if not movimento_valido(pos_zero, direcao):
        return None
    nova_pos = pos_zero + MOVIMENTOS_POSSIVEIS[direcao]
    novo_estado = list(estado)
    novo_estado[pos_zero], novo_estado[nova_pos] = novo_estado[nova_pos], novo_estado[pos_zero]
    return tuple(novo_estado)

def heuristica_manhattan(estado):
    distancia = 0
    for i, valor in enumerate(estado):
        if valor == 0:
            continue
        linha_atual, coluna_atual = divmod(i, 3)
        linha_obj, coluna_obj = divmod(valor - 1, 3)
        distancia += abs(linha_atual - linha_obj) + abs(coluna_atual - coluna_obj)
    return distancia

def busca_gulosa(estado_inicial):
    fila = []
    heapq.heappush(fila, (heuristica_manhattan(estado_inicial), estado_inicial, []))
    visitados = set()

    while fila:
        heuristica, estado_atual, caminho = heapq.heappop(fila)

        if estado_atual in visitados:
            continue

        visitados.add(estado_atual)

        if estado_atual == ESTADO_OBJETIVO:
            return caminho

        for direcao in MOVIMENTOS_POSSIVEIS:
            novo_estado = mover_peca(estado_atual, direcao)
            if novo_estado and novo_estado not in visitados:
                heapq.heappush(fila, (heuristica_manhattan(novo_estado), novo_estado, caminho + [direcao]))

    return None

def resolver_com_metricas(estado_inicial):
    tracemalloc.start()
    tempo_inicio = time.time()

    caminho_solucao = busca_gulosa(estado_inicial)

    tempo_fim = time.time()
    memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\nResultado:")
    if caminho_solucao:
        print(f"Solução encontrada em {len(caminho_solucao)} movimentos: {caminho_solucao}")
    else:
        print("Nenhuma solução encontrada.")

    print(f"Tempo de execução: {tempo_fim - tempo_inicio:.4f} segundos")
    print(f"Uso de memória (pico): {memoria_pico / 1024:.2f} KB")

def ler_estado_inicial():
    print("Digite os números de 0 a 8 (sem repetir), representando o estado inicial do quebra-cabeça.")
    print("Use espaço para separar os números.")
    
    while True:
        entrada = input("Estado inicial: ").strip().split()
        
        if len(entrada) != 9:
            print("Você deve digitar exatamente 9 números.")
            continue

        try:
            numeros = [int(n) for n in entrada]
        except ValueError:
            print("Apenas números inteiros são permitidos.")
            continue

        if sorted(numeros) != list(range(9)):
            print("Os números devem incluir todos de 0 a 8, sem repetições.")
            continue

        return tuple(numeros)

# Execução principal
if __name__ == "__main__":
    estado_inicial = ler_estado_inicial()
    resolver_com_metricas(estado_inicial)
