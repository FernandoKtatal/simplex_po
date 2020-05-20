import numpy as np


def init_matrix(x):
    zero_matrix = np.zeros((x,x))
    return zero_matrix

def add_Z_row(matrix, z_equation, qtdFolga):
    z_equation = getFunction(z_equation)
    i = 0
    
    while i < qtdFolga:
        z_equation = np.append(z_equation, float(0))
        setResult_to_end(z_equation)
        i+=1

    matrix = (np.r_[ [z_equation], matrix ])
    return matrix

def setResult_to_end(item):
    aux = item[-2]
    item[-2] = item[-1]
    item[-1] = aux

def addFolga(matrix, rows, index):
    matrix = np.c_[matrix, np.eye(rows)[index]]
    
    for item in matrix:
        setResult_to_end(item)

    return matrix

def addCondition(matrix, size, condition):
    function = getFunction(condition)

    for row in range(size):
        offset = 0
        for j in matrix[row,:]:
            if j != 0:
                offset += 1
        if(offset == 0):
            matrix[row] = function
            break
    
def getFunction(eq):
    eq = eq.split(',')
    if '>=' in eq:
        maior_igual = eq.index('>=')
        del eq[maior_igual]
        eq = [float(i)*-1 for i in eq]                      #   'convertendo' para '>='
        return eq
    if '<=' in eq:                                          #   condiçao que esperamos
        menor_igual = eq.index('<=')
        del eq[menor_igual]
        eq = [float(i) for i in eq]
        return eq
    if '=' in eq:                                           #   feito para a equacao Z
        igual = eq.index('=')
        del eq[igual]
        eq = [float(i) for i in eq]
        return eq

def z_has_negative(matrix):
    for item in matrix[0]:
        if item < 0:
            return True
        else:
            return False
    
def getColumnPivoZ(matrix):
    index = 0
    lowervalue = matrix[0][0]
    
    for item in matrix[0]:
        if lowervalue > item:
            lowervalue = item
            index += 1

    return index

def getRowPivo(matrix,columnPivo):
    i = 0 
    index = 1
    lowervalue = matrix[0][-1] / matrix[0][columnPivo]
    
    while i < len(matrix):
        if lowervalue > (matrix[i][-1] / matrix[i][columnPivo]):
            lowervalue = (matrix[i][-1] / matrix[i][columnPivo])
            index += i
        i+=1

    return index

def divideRow(pivotValue, row, matrix):
    i = 0
    while i < len(matrix[row]):
        matrix[row][i] /= pivotValue
        i += 1

def othercolunszero(matrix, rowPivo, columnPivo):
    rowindex = 0

    for item in matrix:
        index = 0
        comparation = item == matrix[rowPivo]
        if not (comparation.all()):
            qtd = (item[columnPivo]) / 1 
            if qtd != 0:
                while index < len(matrix[rowPivo]):
                    item[index] += (matrix[rowPivo][index]) * (-qtd)
                    index += 1

def solution(matrix, dictionary):
    for item in matrix[1:]:
        index = 0
        for value in item:
            if value == float(1):
                break
            index += 1

        dictionary['x'+str(index+1)] = item[-1]

    return(dictionary)


def minZ(z_equation, conditions):
    dictionary = {}                                         #   Cria dicionario que vai conter as respostas
    row_column = 3
    matrix = init_matrix(row_column)                        #   Cria uma matriz (preenchidas com zero)
    size = len(matrix[:,0])
    qtdFolga = 0
    qtdInitVariables = 0
    
    z_equation = '-3,-5,=,0'                                #   equação após passar tudo para apenas um lado
    conditions = ['1,0,<=,4','0,2,<=,12', '3,2,<=,18']      #   inequaçoes passadas como condicoes
    
    for func in conditions:
        addCondition(matrix, size, func)                    #   adiciona as condicoes a matriz criada no inicio


    while qtdFolga < len(conditions):
        matrix = addFolga(matrix, size, qtdFolga)           #   adiciona as variavies de folga (1 para cada inequacao)
        qtdFolga += 1                                       #   contador da qtd de variais de folgas (caso necessario)

    matrix = add_Z_row(matrix,z_equation,qtdFolga)

    initalTablo = matrix

    while z_has_negative(matrix):
        columnPivo = getColumnPivoZ(matrix)                 #   coluna a ser escolhida
        rowPivo = getRowPivo(matrix[1:], columnPivo)        #   linha a ser escolhida
        pivotValue = matrix[rowPivo][columnPivo]            #   valor do pivo escolhido
        divideRow(pivotValue, rowPivo, matrix )             #   divide a propria linha pelo valor do Pivo
        othercolunszero(matrix, rowPivo, columnPivo)        #   zera as outras linhas da coluna do pivo

    print(matrix)
    print()

    dictionary['z'] = matrix[0][-1]                         #   adiciona o valor de z ao dicionario
    dictionary = solution(matrix,dictionary)                #   adiciona o valores das outras variaveis ao dicionario
    print(dictionary)                                       #   imprime a resposta







if __name__ == "__main__":
        
    z_equation = '-3,-5,=,0'                                #   equação após passar tudo para apenas um lado
    conditions = ['1,0,<=,4','0,2,<=,12', '3,2,<=,18']      #   inequaçoes passadas como condicoes
    
    minZ(z_equation, conditions)
