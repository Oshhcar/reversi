
from flask import Flask, request
import random
import sys

heuristica = [[120,-20,20,5,5,20,-20,120],
[-20,-40,-5,-5,-5,-5,-40,-20],
[20,-5,15,3,3,15,-5,20],
[5,-5,3,3,3,3,-5,5],
[5,-5,3,3,3,3,-5,5],
[20,-5,15,3,3,15,-5,20],
[-20,-40,-5,-5,-5,-5,-40,-20],
[120,-20,20,5,5,20,-20,120]]

def dibujarEstado(estado):
    # This function prints out the board that it was passed. Returns None.
    HLINE = '  +---+---+---+---+---+---+---+---+'
    VLINE = '  |   |   |   |   |   |   |   |   |'

    print('    1   2   3   4   5   6   7   8')
    print(HLINE)
    for y in range(8):
        print(VLINE)
        print(y+1, end=' ')
        for x in range(8):
            print('| %s' % (estado[x][y]), end=' ')
        print('|')
        print(VLINE)
        print(HLINE)

def getNuevoEstado():
    estado = []
    for i in range(8):
        estado.append([2] * 8)

    return estado

def getEstado(estado):
    array = [int(x) for x in str(estado)]

    estado = getNuevoEstado()
    x = 0
    y = 0
    for i in array:
        estado[x][y] = i
        x += 1
        if(x == 8):
            x = 0
            y += 1

    return estado

def estaEnTablero(x, y):
    return x >= 0 and x <= 7 and y >= 0 and y <=7

def esMovimientoValido(estado, turno, xMov, yMov):
    if(estado[xMov][yMov] != 2 or not estaEnTablero(xMov, yMov)):
        return False

    estado[xMov][yMov] = turno

    if(turno == 1):
        otroTurno = 0
    else:
        otroTurno = 1

    movimientosVoltear = []

    for xdir, ydir in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x,y = xMov, yMov
        x+= xdir
        y+= ydir
        
        if estaEnTablero(x, y) and estado[x][y] == otroTurno:
            x+= xdir
            y+= ydir
            if not estaEnTablero(x,y):
                continue
            while estado[x][y] == otroTurno:
                x+= xdir
                y+= ydir
                if not estaEnTablero(x, y):
                    break
            if not estaEnTablero(x,y):
                continue
            if estado[x][y] == turno:
                while True:
                    x-= xdir
                    y-= ydir
                    if x == xMov and y == yMov:
                        break
                    movimientosVoltear.append([x,y])
    estado[xMov][yMov] = 2
    if len(movimientosVoltear) == 0:
        return False
    return movimientosVoltear

def getMovimientosValidos(estado, turno):
    movimientos = []

    for x in range(8):
        for y in range(8):
            if(esMovimientoValido(estado, turno, x, y) != False):
                movimientos.append([x,y])
    return movimientos

def getValorEstado(estado, turno):
    valor = 0

    for x in range(8):
        for y in range(8):
            if estado[x][y] == turno:
                valor += 1
    return valor

def getCopiaEstado(estado):
    copiaEstado = getNuevoEstado()

    for x in range(8):
        for y in range(8):
            copiaEstado[x][y] = estado[x][y]
    
    return copiaEstado


def hacerMovimiento(estado, turno, xMov, yMov):
    movimientosVoltear = esMovimientoValido(estado, turno, xMov, yMov)

    if(movimientosVoltear == False):
        return False
    
    estado[xMov][yMov] = turno
    for x,y in movimientosVoltear:
        estado[x][y] = turno
    return True

def esEsquina(x, y):
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

def getMovimiento(estado, turno):

    posiblesMovimientos = getMovimientosValidos(estado, turno)
    random.shuffle(posiblesMovimientos)

    for x,y in posiblesMovimientos:
        if esEsquina(x,y):
            return str(y)+""+str(x)
        
    mejorValor = -10000
    mejorMovimiento = -1

    for x,y in posiblesMovimientos:
        copiaEstado = getCopiaEstado(estado)
        hacerMovimiento(copiaEstado, turno, x, y)
        valor = heuristica[x][y]#*getValorEstado(estado, turno)
        #valor = heuristica[x][y]
        #valor = valorMin(copiaEstado, turno, x, y, 1)
        if(valor > mejorValor):
            mejorMovimiento = str(y)+""+str(x)
            mejorValor = valor
    return mejorMovimiento

def getMovimientoMiniMax(estado, turno):

    posiblesMovimientos = getMovimientosValidos(estado, turno)
    random.shuffle(posiblesMovimientos)

    for x,y in posiblesMovimientos:
        if esEsquina(x,y):
            return str(y)+""+str(x)
    
    if(turno == 1):
        otroTurno = 0
    else:
        otroTurno = 1

    mejorValor = -100000
    mejorValor2 = -1
    mejorMovimiento = -1

    print(posiblesMovimientos)

    for x,y in posiblesMovimientos:
        #print("getMovimientoMiniMax ",x,y,mejorMovimiento)
        copiaEstado = getCopiaEstado(estado)
        hacerMovimiento(copiaEstado, turno, x, y)
        #valor = getValorEstado(estado, turno)*heuristica[x][y]
        #valor = heuristica[x][y]
        valor = valorMin(copiaEstado, turno, x, y, 3)
        valor2 = getValorEstado(estado, turno)
        #print(valor)
        if(valor > mejorValor or (valor == mejorValor and valor2 > mejorValor2)):
            mejorMovimiento = str(y)+""+str(x)
            mejorValor = valor
            mejorValor2 = valor2

    return mejorMovimiento


def valorMax(estado, turno, xAnt, yAnt, prof):
    mejorValor = -10000

    if(turno == 1):
        otroTurno = 0
    else:
        otroTurno = 1

    if prof <= 0:
        return heuristica[xAnt][yAnt]#*getValorEstado(estado, turno)
    else :
        posiblesMovimientos = getMovimientosValidos(estado, turno)
        random.shuffle(posiblesMovimientos)
        for x,y in posiblesMovimientos:
            copiaEstado = getCopiaEstado(estado)
            hacerMovimiento(copiaEstado, turno, x, y)
            valor = valorMin(copiaEstado, turno, x, y, prof-1)
            if(valor > mejorValor):
                mejorValor = valor
        return mejorValor

def valorMin(estado, turno, xAnt, yAnt, prof):
    peorValor = 100000

    if(turno == 1):
        otroTurno = 0
    else:
        otroTurno = 1

    if prof <= 0:
        return heuristica[xAnt][yAnt]#*getValorEstado(estado, turno)
    else:
        posiblesMovimientos = getMovimientosValidos(estado, turno)
        random.shuffle(posiblesMovimientos)
        for x,y in posiblesMovimientos:
            #print("Min",x,y)
            copiaEstado = getCopiaEstado(estado)
            hacerMovimiento(copiaEstado, turno, x, y)
            valor = valorMax(copiaEstado, turno, x, y, prof-1)
            if(valor < peorValor):
                peorValor = valor
        return peorValor

#turno = 1
#estado = '2222222222222222222222222221022222201222222222222222222222222222'
#estado = '0211112020111012110011111110111221100110121112102220122022001220'
#estado = getEstado(estado)

#print(getMovimiento(estado, turno))
#print(getMovimientoMiniMax(estado, turno))

app = Flask(__name__)

@app.route('/reversi', methods=['GET'])
def reversi():
    turno = int(request.args.get('turno'))
    estado = request.args.get('estado')
    if(turno != None and estado != None):
        try:
            #turno = 1
            #estado = 2222222222222222222222222221022222201222222222222222222222222222
            #print(estado)
            estado = getEstado(estado)
            #dibujarEstado(estado)
            #print(getMovimientosValidos(estado, turno))
            respuesta = getMovimientoMiniMax(estado, turno)
            #respuesta = getMovimiento(estado, turno)
            #print(respuesta)
            #respuesta = '00'
            return respuesta
        
        except: #Exception as e:
            #e = sys.exc_info()[0]
            #print(e.message)
            return getMovimiento(estado, turno)
    else:
            return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)