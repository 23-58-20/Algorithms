def findMaxInsertableSize(heights, col, width, height):
    curHeight = heights[col]
    maxInsertable = 1
    for i in range(1, min(curHeight, len(heights) - col, width - 1, height - 1)):
        # максимальный размер не превышает количество свободных клеток в столбце и количества столбцов справа
        if heights[col + i] < curHeight:  # если очередной размер не вмещается
            return maxInsertable
        maxInsertable += 1
    return maxInsertable


def findInsertion(heights, width, height, printDebug):
    insertInd = heights.index(max(heights))
    # Вернется первое вхождение - левая клетка самой верхней свободной строки
    if heights[insertInd] == 0:
        return 0, 0
    maxSize = findMaxInsertableSize(heights, insertInd, width, height)
    if printDebug:
        print(f'Вставка в столбец {insertInd} квадратов до размера {maxSize}')
    return insertInd, maxSize


def heightsFromSolution(curSolution, width, height):
    heights = [height for _ in range(width)]
    for ind, size in curSolution:
        for col in range(ind, ind+size):
            # занимаем свободные клетки
            heights[col] -= size
    return heights


def printSolution(solution, width, height):
    heights = [height for _ in range(width)]
    print(len(solution))
    for ind, size in solution:
        print(ind + 1, height - heights[ind] + 1, size)
        for col in range(ind, ind + size):
            heights[col] -= size


def isPrime(num):
    if num == 2:
        return False
    for divisor in range(2, int(num**0.5) + 1):
        if num % divisor == 0:
            return False
    return True


def findMinPartition(width, height, printResult, countSolutionsNum, printDebug):
    solutions = []

    if width == height and isPrime(width):  # частная оптимизация для квадрата с простой стороной
        partialSolutions = [[(0, width // 2 + 1), (width // 2 + 1, width // 2), (0, width // 2)]]
    else:
        partialSolutions = [[]]

    while partialSolutions:
        curSolution = partialSolutions.pop(0)  # берем элемент из очереди
        if printDebug:
            print(f'Обработка решения {curSolution}')
        heights = heightsFromSolution(curSolution, width, height)  # восстанавливаем состояние из частичного решения
        ind, maxInsertableSquare = findInsertion(heights, width, height, printDebug)
        if maxInsertableSquare:
            for insertSize in range(1, maxInsertableSquare + 1):
                partialSolutions.append(curSolution + [(ind, insertSize)])  # расширяяем частичное решение
        else:  # нечего вставить только тогда, когда решение найдено
            solutions.append(curSolution)
            if not countSolutionsNum:  # если достаточно одного решения
                if printResult:
                    printSolution(curSolution, width, height)
                break
            elif len(solutions[0]) < len(curSolution):  # если найдено более длинное решение
                print(f'Минимальных решений: {len(solutions) - 1}')
                if printResult:
                    print('Пример решения:')
                    printSolution(solutions[0], width, height)
                break
            elif len(partialSolutions) == 0:  # если решение - самое длинное из возможных
                print(f'Минимальных решений: {len(solutions)}')
                if printResult:
                    print('Пример решения:')
                    printSolution(solutions[0], width, height)
                break


if __name__ == '__main__':
    printDebug = True
    countSolutionsNum = True
    printResult = True
    sizes = list(map(int, input().split()))
    if len(sizes) == 1:
        width = height = sizes[0]
    else:
        width, height = sizes

    findMinPartition(width, height, printResult, countSolutionsNum, printDebug)
