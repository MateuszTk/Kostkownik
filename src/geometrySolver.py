import numpy as np

def CalcLine(pointA, pointB):
    deltaX = pointA[0] - pointB[0]
    deltaY = pointA[1] - pointB[1]
    
    if deltaX == 0:
        deltaX = 0.01 
    p = deltaY / deltaX
    q = pointA[1] - p * pointA[0]
    return [p, q]
    
def CalcIntersection(lineA, lineB):
    x = (lineB[1] - lineA[1]) / (lineA[0] - lineB[0])
    y = x * lineA[0] + lineA[1]
    return [x, y]
    
def DisectSquare(pointA, pointB, pointC, pointD):
    lineAB = CalcLine(pointA, pointB)
    lineBC = CalcLine(pointB, pointC)
    lineCD = CalcLine(pointC, pointD)
    lineAD = CalcLine(pointA, pointD)
    
    diagonalA = CalcLine(pointA, pointC)
    diagonalB = CalcLine(pointB, pointD)
    midPoint = CalcIntersection(diagonalA, diagonalB)
    
    ##
    horizonAB = CalcIntersection(lineAD, lineBC)
    midPointAB = CalcIntersection(CalcLine(midPoint, horizonAB), lineAB)
    
    #
    lineAB1 = CalcLine(horizonAB, CalcIntersection(diagonalA, CalcLine(pointD, midPointAB)))
    pointAB1 = CalcIntersection(lineAB, lineAB1)
    pointCD2 = CalcIntersection(lineCD, lineAB1)
    
    lineAB2 = CalcLine(horizonAB, CalcIntersection(diagonalB, CalcLine(pointC, midPointAB)))
    pointAB2 = CalcIntersection(lineAB, lineAB2)
    pointCD1 = CalcIntersection(lineCD, lineAB2)
    ##
    horizonBC = CalcIntersection(lineAB, lineCD)
    midPointBC = CalcIntersection(CalcLine(midPoint, horizonBC), lineBC)
    
    #
    lineBC1 = CalcLine(horizonBC, CalcIntersection(diagonalB, CalcLine(pointA, midPointBC)))
    pointBC1 = CalcIntersection(lineBC, lineBC1)
    pointAD1 = CalcIntersection(lineAD, lineBC1)
    
    lineBC2 = CalcLine(horizonBC, CalcIntersection(diagonalA, CalcLine(pointD, midPointBC)))
    pointBC2 = CalcIntersection(lineBC, lineBC2)
    pointAD2 = CalcIntersection(lineAD, lineBC2)
    
    ##
    pointE = CalcIntersection(lineAB1, lineBC1)
    pointF = CalcIntersection(lineAB2, lineBC1)
    pointG = CalcIntersection(lineAB2, lineBC2)
    pointH = CalcIntersection(lineAB1, lineBC2)
    
    squares = [[0.0] * 2 for i in range(9)]

    squares[0] = CalcIntersection(CalcLine(pointA, pointE), CalcLine(pointAB1, pointAD1))
    squares[1] = CalcIntersection(CalcLine(pointAB1, pointF), CalcLine(pointAB2, pointE))
    squares[2] = CalcIntersection(CalcLine(pointAB2, pointBC1), CalcLine(pointB, pointF))
    
    squares[3] = CalcIntersection(CalcLine(pointAD1, pointH), CalcLine(pointE, pointAD2))
    squares[4] = CalcIntersection(CalcLine(pointE, pointG), CalcLine(pointF, pointH))
    squares[5] = CalcIntersection(CalcLine(pointF, pointBC2), CalcLine(pointBC1, pointG))
    
    squares[6] = CalcIntersection(CalcLine(pointAD2, pointCD2), CalcLine(pointH, pointD))
    squares[7] = CalcIntersection(CalcLine(pointH, pointCD1), CalcLine(pointG, pointCD2))
    squares[8] = CalcIntersection(CalcLine(pointG, pointC), CalcLine(pointBC2, pointCD1))

    return squares

def ConstructPositions(centers, upsideDown = False): #construct sample positions based on 6 edge points
    squares = [[0] * 2 for i in range(27)]

    if upsideDown:
        squares[0:9] = DisectSquare(centers[2], centers[5], centers[6], centers[3])
        squares[9:18] = DisectSquare(centers[0], centers[2], centers[3], centers[1])
        squares[18:27] = DisectSquare(centers[3], centers[6], centers[4], centers[1])
    else:
        squares[0:9] = DisectSquare(centers[5], centers[3], centers[0], centers[2])
        squares[9:18] = DisectSquare(centers[0], centers[3], centers[4], centers[1])
        squares[18:27] = DisectSquare(centers[3], centers[5], centers[6], centers[4])
        
    return squares
