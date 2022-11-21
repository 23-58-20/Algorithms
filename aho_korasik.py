class Node:
    def __init__(self, parent, sym, height):
        self.parent = parent
        self.sym = sym
        self.words = []
        self.terminal = []  # список слов, оканчивающихся в этой вершине
        self.height = height
        self.children = dict()
        self.link = None

    def __repr__(self):
        res = f'{self.height}.{self.sym}: ' if self.sym else 'Head: '
        if len(self.children):
            for child in self.children.values():
                res += f"'{child.sym}', "
        else:
            res += '-- '
        if self.link:
            res += f'link: {self.link.height}.{self.link.sym}'
        else:
            res += f'link: ---'
        return res


class Trie:
    def __init__(self):
        self.head = Node(None, 'Head', 0)
        self.nodesNum = 1

    def addWord(self, s, num):
        cur = self.head
        for letter in s:
            if letter not in cur.children:  # если такой вершины нет, создаем ее
                cur.children[letter] = Node(cur, letter, cur.height + 1)
                if debug:
                    print(f'Новая вершина: {cur.children[letter]}')
                self.nodesNum += 1
            cur = cur.children[letter]
            cur.words.append(num)
        cur.terminal.append(num)  # обозначаем номер слова, заканчивающегося в этом символе

    def setLinks(self):
        if debug:
            print('\nИщем ссылки\n')
        self.head.link = self.head
        queue = []

        for child in self.head.children.values():
            child.link = self.head  # ссылки из детей головного элемента всегда ведут в головной элемент
            queue.extend(child.children.values())
        if debug:
            print('Задали ссылки корню и его прямым потомкам')
        while queue:  # обход в ширину
            cur = queue.pop(0)
            if debug:
                print(f'Обработка вершины {cur}')
            queue.extend(cur.children.values())
            sym = cur.sym
            prev = cur.parent.link  # рассматриваем ссылку текущего родителя
            if debug:
                print(f'  Просмотр ссылки {prev}')
            while not (sym in prev.children) and not (prev is self.head):  # пока не найден подходящий путь
                if debug:
                    print(f'    Просмотр предыдущей ссылки {prev.link}')
                prev = prev.link  # переходим по ссылкам
            cur.link = prev.children[sym] if (sym in prev.children) \
                else self.head
            if debug:
                print(f'  Найденная ссылка: {cur.link}')

    def findOccurrences(self, text):
        if debug:
            print('\nИщем вхождения\n')
        occurrences = dict()
        cur = self.head
        for ind, letter in enumerate(text, 2):
            if debug:
                print(f'Буква {ind-1}:{letter}')
            while letter not in cur.children and not (cur is self.head):  # переходим по ссылкам, если нет нужного пути
                cur = cur.link
                if debug:
                    print(f'  Переход назад по ссылке в {cur}')
            if letter in cur.children:
                cur = cur.children[letter]
                if debug:
                    print(f'  Переход вперед в {cur}')
            if letter == cur.sym:
                extra = cur  # дополнительная переменная для проверки всех суффиксных ссылок
                while not (extra is self.head):
                    if extra.terminal:  # если какое-то слово закончилось в этой вершине
                        if debug:
                            print(f'  В вершине {extra} окончились строки: {extra.terminal}')
                            print(f'  Найдено вхождение образца {extra.terminal} с индекса {ind - extra.height}')
                        if ind - extra.height in occurrences:
                            occurrences[ind - extra.height].extend(extra.terminal)
                        else:
                            occurrences[ind - extra.height] = extra.terminal.copy()
                    extra = extra.link
                    if debug:
                        print(f'  Проверка суффикса: {extra}')
        return occurrences


    def printTrie(self, node=None, indent=0):
        if node is None:
            node = self.head
        print(f'{indent * " "}{node}')
        for child in node.children.values():
            self.printTrie(child, indent + 2)

    def countNodes(self):
        return self.nodesNum


def revertDict(oldDict):
    reverted = dict()
    for key, value in oldDict.items():
        for ind in value:
            if ind in reverted:
                reverted[ind].append(key)
            else:
                reverted[ind] = [key]
    return reverted


def getSubstrings(pattern, wildCard):
    substrs = dict()
    curSubstr = ''
    num = 1
    for ind, letter in enumerate(pattern, 1):
        if letter != wildCard:
            curSubstr += letter
            if debug:
                print(f'В текущее слово добавлен символ {ind}:{letter}')
        elif curSubstr:
            if debug:
                print(f'Найден {wildCard}, добавлено слово {curSubstr}')
            substrs[num] = (ind - len(curSubstr), curSubstr)
            num += 1
            curSubstr = ''
        elif debug:
                print(f'Пропущен {wildCard}')
    if curSubstr:
        substrs[num] = (len(pattern) + 1 - len(curSubstr), curSubstr)
        if debug:
            print(f'Добавлено слово {curSubstr}')
    return substrs


debug = True
printTrie = True
printIntersections = True
countNodes = True
intersections = dict()

step = 1
text = input()
trie = Trie()
words = dict()
if step == 1:
    i = int(input())
    for i in range(i):
        word = input()
        trie.addWord(word, i + 1)
        words[i + 1] = word
    trie.setLinks()
    if printTrie:
        trie.printTrie()
    occurrences = trie.findOccurrences(text)

    if countNodes:
        print(trie.countNodes())
    for key in sorted(occurrences.keys()):
        for value in sorted(occurrences[key]):
            print(key, value)

    if printIntersections:
        if debug:
            print('\nИщем пересечения')
        for index in range(len(text)):
            if debug:
                print(f'\nОбработка индекса {index}')
            for left_border in occurrences:
                if left_border <= index:
                    for word_num in occurrences[left_border]:
                        if debug:
                            print(f'Обработка вхождения {words[word_num]} с индекса {left_border}')
                        if len(words[word_num]) + left_border > index:
                            if debug:
                                print(f'{words[word_num]} входит в индекс {index}')
                            if index in intersections:
                                intersections[index].append(words[word_num])
                            else:
                                intersections[index] = [words[word_num]]
        for ind in intersections:
            if len(intersections[ind]) > 1:
                print(f'В индексе {ind} пересекаются образцы: {intersections[ind]}')

elif step == 2:
    pattern = input()
    wildCard = input()
    substrs = getSubstrings(pattern, wildCard)
    ind = 0
    for key, value in substrs.items():
        trie.addWord(value[1], key)
    trie.setLinks()
    if printTrie:
        trie.printTrie()
    if countNodes:
        print(trie.countNodes())
    occurrences = trie.findOccurrences(text)
    if printIntersections:
        if debug:
            print('\nИщем пересечения')
        for index in range(len(text)):
            if debug:
                print(f'\nОбработка индекса {index}')
            for left_border in occurrences:
                if left_border <= index:
                    for word_num in occurrences[left_border]:
                        if debug:
                            print(f'Обработка вхождения {substrs[word_num][1]} с индекса {left_border}')
                        if len(substrs[word_num][1]) + left_border > index:
                            if debug:
                                print(f'{substrs[word_num][1]} входит в индекс {index}')
                            if index in intersections:
                                intersections[index].append(substrs[word_num][1])
                            else:
                                intersections[index] = [substrs[word_num][1]]
        for ind in intersections:
            if len(intersections[ind]) > 1:
                print(f'В индексе {ind} пересекаются образцы: {intersections[ind]}')
    occurrencesReverted = revertDict(occurrences)  # ключ - номер строки, значение - список вхождений
    result = []
    if len(occurrencesReverted.values()) == len(substrs):
        firstSubstrIndices = occurrencesReverted[1]  # по всем вхождениям первой подстроки
        for elem in firstSubstrIndices:
            if debug:
                print(f'Пробуем собрать слово с индекса {elem}')
            curDist = 0
            if 0 < elem + 1 - substrs[1][0]:
                if elem + 1 - substrs[1][0] + len(pattern) <= len(text) + 1:  # исключаем случаи выхода за край
                    for i in range(2, len(substrs) + 1):
                        curDist += substrs[i][0] - substrs[i - 1][0]  # последовательно проверяем, что на каждую
                        if debug:
                            print(f'  Подстрока {i} должна быть на символе {elem + curDist}')
                        if elem + curDist not in occurrencesReverted[i]:  # подстроку есть соответствующее вхождение
                            if debug:
                                print(f'  Подстрока не найдена')
                            break
                        elif debug:
                            print('  Подстрока найдена')
                    else:
                        result.append(elem + 1 - substrs[1][0])
                elif debug:
                    print(f'  Шаблон выходит за пределы строки')
        for elem in result:
            print(elem)
