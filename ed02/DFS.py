import time
import tracemalloc

# Estado objetivo desejado
ESTADO_OBJETIVO = (1, 2, 3,
                   4, 5, 6,
                   7, 8, 0)

MOVIMENTOS_POSSIVEIS = {
    'cima': -3,
    'baixo': 3,
    'esquerda': -1,
    'direita': 1
}

# Verifica se o movimento é permitido a partir da posição atual
def movimento_valido(posicao_zero, direcao):
    if direcao == 'cima':
        return posicao_zero > 2
    if direcao == 'baixo':
        return posicao_zero < 6
    if direcao == 'esquerda':
        return posicao_zero % 3 != 0
    if direcao == 'direita':
        return posicao_zero % 3 != 2
    return False

# Executa o movimento e retorna o novo estado
def mover_peca(estado_atual, direcao):
    posicao_zero = estado_atual.index(0)
    if not movimento_valido(posicao_zero, direcao):
        return None
    nova_posicao = posicao_zero + MOVIMENTOS_POSSIVEIS[direcao]
    novo_estado = list(estado_atual)
    novo_estado[posicao_zero], novo_estado[nova_posicao] = novo_estado[nova_posicao], novo_estado[posicao_zero]
    return tuple(novo_estado)

# Implementação da busca em profundidade com limite
def busca_em_profundidade(estado_inicial, limite_profundidade=40):
    pilha = [(estado_inicial, [], 0)]
    estados_visitados = set()

    while pilha:
        estado_atual, caminho, profundidade = pilha.pop()

        if estado_atual in estados_visitados:
            continue

        estados_visitados.add(estado_atual)

        if estado_atual == ESTADO_OBJETIVO:
            return caminho

        if profundidade >= limite_profundidade:
            continue

        for direcao in MOVIMENTOS_POSSIVEIS:
            novo_estado = mover_peca(estado_atual, direcao)
            if novo_estado and novo_estado not in estados_visitados:
                pilha.append((novo_estado, caminho + [direcao], profundidade + 1))

    return None

# Função para resolver o quebra-cabeça e medir desempenho
def resolver_quebra_cabeca_com_metricas(estado_inicial):
    tracemalloc.start()
    tempo_inicio = time.time()

    caminho_solucao = busca_em_profundidade(estado_inicial)

    tempo_fim = time.time()
    memoria_atual, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\nResultado:")
    if caminho_solucao:
        print(f"Solução encontrada em {len(caminho_solucao)} movimentos: {caminho_solucao}")
    else:
        print("Nenhuma solução encontrada (ou limite de profundidade atingido).")

    print(f"Tempo de execução: {tempo_fim - tempo_inicio:.4f} segundos")
    print(f"Uso de memória (pico): {memoria_pico / 1024:.2f} KB")

# Função para ler o estado inicial do usuário
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
    resolver_quebra_cabeca_com_metricas(estado_inicial)
    