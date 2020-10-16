
from flask import Flask, request
import random

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
            return [x,y]
    
    mejorValor = -1

    for x,y in posiblesMovimientos:
        copiaEstado = getCopiaEstado(estado)
        hacerMovimiento(copiaEstado, turno, x, y)
        valor = getValorEstado(estado, turno)
        if(valor > mejorValor):
            mejorMovimiento = str(y)+""+str(x)
            mejorValor = valor
    return mejorMovimiento
    

#turno = 1
#estado = 2222222222222222222222222221022222201222222222222222222222222222

#estado = getEstado(estado)

#print(getMovimiento(estado, turno))

app = Flask(__name__)

@app.route('/reversi', methods=['GET'])
def reversi():
    try:
        turno = int(request.args.get('turno'))
        estado = int(request.args.get('estado'))

        #turno = 1
        #estado = 2222222222222222222222222221022222201222222222222222222222222222
        if(turno != '' and estado != ''):
            estado = getEstado(estado)
            print(getMovimientosValidos(estado, turno))
            respuesta = getMovimiento(estado, turno)
            return respuesta
        else:
            return '00'
    except:
        return '00'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)