import heapq
saveGraph = True
if saveGraph:
    from graphviz import Digraph
    graphImg = Digraph(filename='A_graph.gv')

debug = True


def heuristic(a, last):
    return abs(ord(a) - ord(last))


graph = dict()
first, last = map(str, input().split())
while True:
    try:
        a, b, dist = input().split()
        if saveGraph:
            graphImg.edge(a, b, label=dist)
        dist = float(dist)
        if a not in graph:
            # создание вложенного словаря
            graph[a] = dict()
        graph[a][b] = dist
        if debug:
            print(f'Добавлено ребро {a}->{b} с весом {dist}')
    except ValueError:
        break
    except EOFError:
        break

queue = []
fullPath = []
pathLen = dict()  # физическая стоимость до данной вершины
pathLen[first] = 0
heapq.heappush(queue, (heuristic(first, last), -1, first))  # используется стандартная библиотека heapq
ind = -1

while queue:
    ind += 1
    cur_elem = heapq.heappop(queue)
    if debug:
        print(f'\nИз очереди взята вершина {ind}: "{cur_elem[2]}", фактическая длина пути до нее: {pathLen[cur_elem[2]]}')
    fullPath.append((cur_elem[1], cur_elem[2]))  # индекс предыдущего элемента и вершина
    if debug:
        print(f'В решение добавлена вершина {cur_elem[2]}, предыдушая вершина: {cur_elem[1]}')
    if cur_elem[2] == last:
        if debug:
            print('Это конечная вершина!')
        break
    if cur_elem[2] in graph:
        for vertex in graph[cur_elem[2]]:
            realPath = pathLen[cur_elem[2]] + graph[cur_elem[2]][vertex]
            if debug:
                print(f'Обработка ребра {cur_elem[2]}->{vertex} стоимостью {graph[cur_elem[2]][vertex]}')
                print(f'    Найден путь до вершины {vertex} длины {pathLen[cur_elem[2]]} + {graph[cur_elem[2]][vertex]} = {realPath}')
                print(f'    Сохраненный путь до вершины {vertex}: {pathLen[vertex] if vertex in pathLen else None}')
            if vertex not in pathLen or realPath < pathLen[vertex]:
                if debug:
                    print(f'    Найденный путь - кратчайший')
                pathLen[vertex] = realPath  # обновляем сохраненную стоимость
                priority = realPath + heuristic(vertex, last)
                heapq.heappush(queue, (priority, ind, vertex))
                if debug:
                    print(f'    В очередь добавлена вершина {vertex} с приоритетом {realPath} + {heuristic(vertex, last)} = {priority} и предыдущей вершиной {ind}')
                    print(f'    Текущий вид очереди: {queue}')
            elif debug:
                print('    Это не кратчайший путь')

path = ''
if debug:
    print(f'\nВсе пройденные вершины: {fullPath}')
i = len(fullPath) - 1
if debug:
    print('Восстанавливаем путь:')
while i >= 0:
    if debug:
        print(f'Добавим вершину {i}:{fullPath[i][1]}, перейдем к {fullPath[i][0]}')
    path += fullPath[i][1]
    i = fullPath[i][0]
print(path[::-1])

if saveGraph:
    for i in range(1, len(fullPath)):
        graphImg.edge(fullPath[fullPath[i][0]][1], fullPath[i][1],  label=str(i), fontcolor='blue', color='blue')
    for i in range(1, len(path)):
        graphImg.edge(path[i], path[i-1], color='red')
    graphImg.view()
