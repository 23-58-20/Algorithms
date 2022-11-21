def get_edge_width(graph, source, destination):
    if source in graph:
        if destination in graph[source]:
            return graph[source][destination]
    return 0  # если ребра нет, считаем, что пропускная способность - 0


def get_path(paths_graph, first_vertex, last_vertex):
    if debug:
        print('\nВосстанавливаем пройденный путь')
    found_paths = [[first_vertex]]
    res_paths = []
    while found_paths:  # поиск в ширину
        if debug:
            print(f'Очередь обработки: {found_paths}')
        path = found_paths.pop(0)
        if debug:
            print(f'    Текущий путь: {path}')
        if path[-1] in paths_graph:
            for vertex in paths_graph[path[-1]]:  # рассматриваем все пути
                if debug:
                    print(f'    Путь {path} можно расширить до {vertex}')
                found_paths.append(path + [vertex])
                if vertex == last_vertex:  # нашли путь в сток
                    if debug:
                        print(f'{vertex} - сток; итоговый путь: {found_paths[-1]}')
                    res_paths.append(found_paths[-1])
    if debug and not res_paths:
        print(f'Пути не найдено - конец алгоритма')
    return res_paths


def get_min_edge(network_graph, flows_graph, path):
    found_min = None
    if debug:
        print(f'\nИщем минимальную остаточную пропускную способность в пути {path}')
    for j in range(len(path) - 1):
        # остаточная пропускная способность - максимальный поток за вычетом уже текущего потока
        cur = get_edge_width(network_graph, path[j], path[j + 1]) - flows_graph[path[j]][path[j + 1]]
        if debug:
            print(f'    Максимальное увеличение в ребре {path[j]}->{path[j + 1]}: {cur}')
        if found_min is None or cur < found_min:
            found_min = cur
            if debug:
                print(f'    Новое минимальное найденное увеличение: {found_min}')
    if debug:
        print(f'\nНайденный минимум: {found_min}')
    return found_min


max_network = dict()
flows = dict()
cur_front = []
debug = True
edges_num = int(input())
start = input()
finish = input()
for i in range(edges_num):
    a, b, max_flow = input().split()
    max_flow = int(max_flow)
    if a in max_network:
        max_network[a][b] = max_flow
    else:
        max_network[a] = dict()
        max_network[a][b] = max_flow
    if debug:
        print(f'Добавлено ребро {a}->{b} с пропускной способностью {max_flow}')

for a in max_network:
    for b in max_network[a]:
        if a not in flows:
            flows[a] = dict()
        flows[a][b] = 0

        if b not in flows:
            flows[b] = dict()
        flows[b][a] = 0


while True:
    if debug:
        print(f'\n\n\nПробуем найти способ увеличить поток')
    paths = dict()  # запоминаем, откуда перешли в данную вершину
    cur_front = set(start)
    passed = set(start)
    while cur_front:
        if debug:
            print(f'\nВершины текущего фронта: {cur_front}')
        next_front = set()
        next_front_candidates = []
        for vert in cur_front:
            if debug:
                print(f'Обработка вершины {vert}')
            for next_vert in flows[vert]:
                next_front_candidates.append((vert, flows[vert][next_vert], next_vert))  # все ребра текущего фронта
                if debug:
                    print(f'    Потенциальное ребро {vert}->{next_vert}:')
                    print(f'        поток: {flows[vert][next_vert]} из {get_edge_width(max_network, vert, next_vert)}')
        next_front_candidates = sorted(next_front_candidates,  # сортируем по пропускной способности
                                       key=lambda x: get_edge_width(max_network, x[0], x[2]) - x[1], reverse=True)
        if debug:
            print('Ребра отсортированы по максимальной остаточной пропускной способности')
        for vert, edge_flow, next_vert in next_front_candidates:
            if debug:
                edge_width = get_edge_width(max_network, vert, next_vert)
                print(f'Ребро {vert}->{next_vert} с текущим потоком {edge_flow} из {edge_width}')
            if next_vert not in passed and (get_edge_width(max_network, vert, next_vert) - edge_flow) > 0:
                if debug:
                    flow_add = get_edge_width(max_network, vert, next_vert) - edge_flow
                    print(f'    В ребро {vert}->{next_vert} можно добавить {flow_add}')
                next_front.add(next_vert)
                if debug:
                    print(f'    {next_vert} - вершина следующего фронта')
                paths[vert] = [next_vert] if vert not in paths else paths[vert] + [next_vert]
                if debug:
                    print(f'    Запомним переход {vert}->{next_vert}')
            elif debug:
                if next_vert in passed:
                    print(f'    Вершина {next_vert} уже обработана')
                else:
                    print(f'    В ребро {vert}->{next_vert} нельзя добавить поток')

        for vert in next_front:
            passed.add(vert)  # вершины предыдущих фронтов игнорируются
            if debug:
                print(f'В обработанные вершины добавлена {vert}')
        if debug:
            print(f'Вершины обработанных фронтов: {passed}')
        cur_front = next_front

    cur_paths = get_path(paths, start, finish)
    if cur_paths:
        cur_min = 0
        for path in cur_paths:
            min_edge = get_min_edge(max_network, flows, path)
            if min_edge > cur_min:
                cur_path = path
                cur_min = min_edge
    else:
        break
    if debug:
        print(f'Увеличим поток на {cur_min} в пути {cur_path}')
    for i in range(len(cur_path) - 1):
        if debug:
            flow = flows[cur_path[i]][cur_path[i + 1]]
            back_flow = flows[cur_path[i + 1]][cur_path[i]]
            new_flow = flow + cur_min
            new_back_flow = back_flow - cur_min
            print(f'    Увеличим поток в {cur_path[i]}->{cur_path[i + 1]} с {flow} до {new_flow}')
            print(f'    Уменьшим поток в {cur_path[i + 1]}->{cur_path[i]} с {back_flow} до {new_back_flow}\n')
        flows[cur_path[i]][cur_path[i + 1]] += cur_min
        flows[cur_path[i + 1]][cur_path[i]] -= cur_min  # уменьшаем поток в противоположном ребре

max_flow = 0
for vert in flows[start]:
    max_flow += flows[start][vert]  # сумма потоков из первой вершины
print(max_flow)
for vertex1 in sorted(max_network.keys()):
    for vertex2 in sorted(max_network[vertex1].keys()):
        print(vertex1, vertex2, max(flows[vertex1][vertex2], 0))
