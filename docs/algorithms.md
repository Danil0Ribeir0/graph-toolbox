📂 Documentação de Algoritmos - Graph-Toolbox
Esta biblioteca fornece uma implementação robusta em Python para modelagem e processamento de grafos, focada em algoritmos de otimização e conectividade.

🧠 Algoritmos Implementados
1. Conectividade (DFS - Busca em Profundidade)
Classe: GraphTraversal

Método: is_connected(graph)

Descrição: Utiliza uma busca em profundidade recursiva para verificar se todos os nós do grafo são alcançáveis a partir de um ponto inicial.

Uso: Essencial para validar se algoritmos de caminho mínimo ou ciclos eulerianos podem ser aplicados com sucesso.

2. Caminho Mínimo (Dijkstra)
Classe: PathFinder

Método: dijkstra(graph, start_node)

Funcionamento: Encontra a distância mais curta da origem para todos os outros nós em um grafo com pesos.

Diferencial: Utiliza uma fila de prioridade (heapq) para garantir eficiência, explorando sempre o caminho de menor custo acumulado primeiro.

Restrição: Projetado para arestas com pesos não negativos.

3. Árvore Geradora Mínima (Algoritmo de Prim)
Classe: SpanningTree

Método: prim(graph, start_node)

Objetivo: Conecta todos os nós do grafo utilizando o menor custo total de arestas possível, garantindo a ausência de ciclos.

Saída: O método retorna um novo objeto Graph contendo apenas as arestas que compõem a MST (Minimum Spanning Tree).

Aplicação: Ideal para projetos de infraestrutura e redes onde o custo de conexão deve ser minimizado.

4. Validação de Ciclo Euleriano
Classe: EulerianValidator

Método: has_cycle(graph)

Lógica: Verifica se o grafo possui um circuito que passa por todas as arestas exatamente uma vez.

Critérios de Validação:

O grafo deve ser totalmente conectado.

Todos os nós devem possuir grau par (número de conexões).