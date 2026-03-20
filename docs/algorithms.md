# 📂 Documentação de Algoritmos: Graph-Toolbox

A **Graph-Toolbox** é uma biblioteca Python desenvolvida para a modelagem, processamento e análise eficiente de grafos. Esta documentação detalha as implementações dos algoritmos principais, com foco em conectividade, caminhos mínimos e otimização de infraestruturas.

---

## 🧠 1. Verificação de Conectividade (DFS - *Depth-First Search*)

**Classe:** `GraphTraversal`  
**Método:** `is_connected(graph) -> bool`

**Descrição Técnica:**
O algoritmo implementa uma Busca em Profundidade (DFS) recursiva para determinar se o grafo é conexo. A partir de um vértice arbitrário, o algoritmo explora o mais profundamente possível ao longo de cada ramificação antes de realizar o retrocesso (*backtracking*). O grafo é classificado como conexo se, ao término da travessia, a cardinalidade do conjunto de vértices visitados for exatamente igual ao número total de vértices do grafo.

* **Complexidade de Tempo:** $O(|V| + |E|)$, onde $|V|$ é o número de vértices e $|E|$ o número de arestas.
* **Aplicação Prática:** Atua como um validador de pré-requisito fundamental. Muitos algoritmos complexos (como a detecção de Ciclos Eulerianos) exigem que a topologia da rede seja um componente fortemente ou fracamente conexo para operar corretamente.

---

## 📍 2. Caminho Mínimo de Fonte Única (Algoritmo de Dijkstra)

**Classe:** `PathFinder`  
**Método:** `dijkstra(graph, start_node) -> dict`

**Descrição Técnica:**
Implementação do clássico algoritmo de Dijkstra para solucionar o problema do caminho mínimo de fonte única (*single-source shortest path*). O algoritmo adota um paradigma guloso (*greedy*), realizando o relaxamento sucessivo das arestas para encontrar o trajeto de menor custo acumulado do `start_node` para todos os outros vértices da rede.

Para garantir a máxima eficiência, a implementação utiliza uma fila de prioridade baseada em *min-heap* (via módulo nativo `heapq` do Python). Isso permite que a extração do próximo vértice não visitado mais próximo seja feita de forma logarítmica, e não linear.

* **Restrição Matemática:** O algoritmo requer que o grafo não possua arestas com pesos negativos (o que invalidaria a propriedade gulosa da fronteira de otimização).
* **Complexidade de Tempo:** $O((|V| + |E|) \log |V|)$ graças à otimização com o *heap*.
* **Aplicação Prática:** Roteamento de pacotes IP, sistemas de navegação GPS e planejamento de rotas em malhas logísticas.

---

## 🌳 3. Árvore Geradora Mínima (Algoritmo de Prim)

**Classe:** `SpanningTree`  
**Método:** `prim(graph, start_node) -> Graph`

**Descrição Técnica:**
O Algoritmo de Prim é utilizado para extrair a Árvore Geradora Mínima (MST - *Minimum Spanning Tree*) de um grafo não direcionado, conexo e valorado. A partir do `start_node`, o algoritmo mantém um corte (*cut*) no grafo, dividindo os vértices entre os que já pertencem à MST e os que ainda não pertencem. A cada iteração, ele cruza esse corte adicionando a aresta de menor peso disponível, garantindo a ausência de ciclos.

O método preserva a imutabilidade do grafo de entrada: a saída é instanciada como um novo objeto `Graph`, contendo estritamente todos os vértices originais e as $|V|-1$ arestas que compõem a MST.

* **Complexidade de Tempo:** $O(|E| \log |V|)$ com a utilização de uma fila de prioridade para a seleção das arestas de corte.
* **Aplicação Prática:** Otimização de custos na construção de infraestruturas físicas, como cabeamento de redes locais (LAN), circuitos impressos (PCBs), encanamentos e malhas de distribuição elétrica.

---

## 🔄 4. Validação de Ciclo Euleriano

**Classe:** `EulerianValidator`  
**Método:** `has_cycle(graph) -> bool`

**Descrição Técnica:**
Este algoritmo avalia a existência de um Ciclo Euleriano — um circuito fechado que transita por *absolutamente todas as arestas* do grafo exatamente uma única vez, retornando ao vértice de origem. 

Em vez de executar uma busca exaustiva que teria um custo computacional proibitivo, o método valida a estrutura do grafo em tempo linear aplicando os axiomas do Teorema de Euler. Para que `has_cycle` retorne `True`, a topologia deve satisfazer simultaneamente dois critérios rigorosos:

1. **Conectividade Integral:** Todos os vértices com grau maior que zero devem pertencer a um único componente conexo.
2. **Paridade de Grau:** Todo e qualquer vértice do grafo deve possuir um grau par. Isso garante que, para cada aresta de "entrada" em um vértice, exista uma aresta de "saída" disponível.

* **Complexidade de Tempo:** $O(|V| + |E|)$ para a checagem dos graus e validação da conectividade subjacente.
* **Aplicação Prática:** Roteamento de serviços urbanos que exigem cobertura total de vias (como coleta de lixo, inspeção de linhas de energia, e limpa-neves) e montagem de fragmentos de DNA em bioinformática.