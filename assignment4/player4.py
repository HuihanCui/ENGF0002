from board import Direction, Rotation, Action, Board, Block, Shape
from random import Random
import time

I = [[(-1, 0), (0, 0), (1, 0), (2, 0)],
         [(0, -1), (0, 0), (0, 1), (0, 2)],
         [(-1, 0), (0, 0), (1, 0), (2, 0)],
         [(0, -1), (0, 0), (0, 1), (0, 2)]]
J = [[(-2, 0), (-1, 0), (0, 0), (0, -1)],
         [(-1, 0), (0, 0), (0, 1), (0, 2)],
         [(0, 1), (0, 0), (1, 0), (2, 0)],
         [(0, -2), (0, -1), (0, 0), (1, 0)]]
L = [[(-2, 0), (-1, 0), (0, 0), (0, 1)],
         [(1, 0), (0, 0), (0, 1), (0, 2)],
         [(0, -1), (0, 0), (1, 0), (2, 0)],
         [(0, -2), (0, -1), (0, 0), (-1, 0)]]
O = [[(0, 0), (0, 1), (1, 0), (1, 1)],
         [(0, 0), (0, 1), (1, 0), (1, 1)],
         [(0, 0), (0, 1), (1, 0), (1, 1)],
         [(0, 0), (0, 1), (1, 0), (1, 1)]]
S = [[(1, -1), (1, 0), (0, 0), (0, 1)],
         [(-1, 0), (0, 0), (0, 1), (1, 1)],
         [(1, -1), (1, 0), (0, 0), (0, 1)],
         [(-1, 0), (0, 0), (0, 1), (1, 1)]]
T = [[(0, -1), (0, 0), (0, 1), (1, 0)],
         [(-1, 0), (0, 0), (1, 0), (0, -1)],
         [(0, -1), (0, 0), (0, 1), (-1, 0)],
         [(-1, 0), (0, 0), (1, 0), (0, 1)]]
Z = [[(0, -1), (0, 0), (1, 0), (1, 1)],
         [(-1, 0), (0, 0), (0, -1), (1, -1)],
         [(0, -1), (0, 0), (1, 0), (1, 1)],
         [(-1, 0), (0, 0), (0, -1), (1, -1)]]

shapeDir = {
        Shape.I: I, Shape.J: J, Shape.L: L, Shape.O: O, Shape.S: S, Shape.T: T, Shape.Z: Z
}

class Player:
    def choose_action(self, board):
        raise NotImplementedError

class Lucy(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def maxHeightColumn(self, sandbox):
        columns = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for x in range(10):
            for y in range(23):
                if (x, y) in sandbox.cells:
                    columns[x] = y
                    break
        return columns

    def maxHeightBoard(self, sandbox):
        min = 24
        for y in range(sandbox.height):
            for x in range(sandbox.width):
                if (x, y) in sandbox.cells:
                    if y < min:
                        min = y
        return min

    def maxHeightSpecific(self, sandbox, x):
        min = 24
        for y in range(sandbox.height):
            if (x, y) in sandbox.cells:
                if y < min:
                    min = y
        return min

    def holes(self, sandbox):
        count = 0
        columncount = 0
        for x in range(10):
            columnBool = 0
            height = self.maxHeightSpecific(sandbox, x)
            for y in range(23, height, -1):
                if y != 0:
                    if (x, y) not in sandbox.cells:
                        count += 1
                        columnBool = 1
            if columnBool == 1:
                columncount += 1
        return count, columncount

    def bumpiness(self, sandbox):
        total = 0
        heights = self.maxHeightColumn(sandbox)
        for x in range(sandbox.width - 1):
            total += abs(heights[x] - heights[x + 1])
        return total

    def ColumnTransitions(self, sandbox):
        transition = 0
        for j in range(10):
            for i in range(23, 1, -1):
                if (j, i) not in sandbox.cells and (j, i - 1) in sandbox.cells:
                    transition += 1
                if (j, i) in sandbox.cells and (j, i - 1) not in sandbox.cells:
                    transition += 1
        return transition

    def RowTransitions(self, sandbox):
        transition = 0
        for i in range(23, 0, -1):
            for j in range(9):
                if (j, i) not in sandbox.cells and (j + 1, i) in sandbox.cells:
                    transition += 1
                if (j, i) in sandbox.cells and (j + 1, i) not in sandbox.cells:
                    transition += 1
        return transition

    def emptyColumn(self, sandbox):
        count = 0
        index = []
        for i in range(10):
            Bool = 0
            for j in range(24):
                if (i, j) in sandbox.cells:
                    Bool += 1
            if Bool == 0:
                count += 1
                index.append(i)
        return count, index

    def Wells(self, sandbox):
        sums = [0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136, 153, 171, 190, 210]
        wells = 0
        sum = 0
        for j in range(10):
            for i in range(23, -1, -1):
                if (i, j) not in sandbox.cells:
                    if (j - 1 < 0 or (i, j - 1) in sandbox.cells) and (j + 1 >= 10 or (i, j + 1) in sandbox.cells):
                        wells += 1
                    else:
                        sum += sums[wells]
                        wells = 0
                else:
                    sum += sums[wells]
                    wells = 0
        return sum

    def completedLine(self, sandbox):
        result = 0
        for i in range(23, 0, -1):
            count = 0
            for j in range(10):
                if (j, i) in sandbox.cells:
                    count += 1
            if count == 10:
                result += 1
        return result

    def score_system(self, sandbox):
        weights = [15, 390, -60, -0.1, -55, -50, -20, -100, -60]
        height = self.maxHeightBoard(sandbox) * weights[0]
        completeLines = self.completedLine(sandbox) * weights[1]
        holes, columnWithHoles = self.holes(sandbox)
        Holes = holes * weights[2]
        colHoles = columnWithHoles * weights[8]
        Bumpiness = self.bumpiness(sandbox) * weights[3]
        empty, _ = self.emptyColumn(sandbox)
        emptycol = empty * weights[4]
        colT = self.ColumnTransitions(sandbox) * weights[5]
        rowT = self.RowTransitions(sandbox) * weights[6]
        well = self.Wells(sandbox)
        wells = well * weights[7]
        totalScore = height + completeLines + Holes + colHoles + Bumpiness + emptycol + colT + rowT + wells
        return totalScore

    def choose_action(self, board):
        bestScore = -1000000
        bestMoves = []
        for columns in range(board.width):
            for rotation in range(4):
                moves = []
                sandbox = board.clone()
                x = sandbox.falling.left
                landed = False
                for rotations in range(rotation):
                    if sandbox.falling is not None:
                        landed = sandbox.rotate(Rotation.Anticlockwise)
                        moves.append(Rotation.Anticlockwise)
                        if not landed:
                            x = sandbox.falling.left
                        else:
                            break
                while x > columns and not landed:
                    landed = sandbox.move(Direction.Left)
                    moves.append(Direction.Left)
                    if sandbox.falling is not None:
                        x = sandbox.falling.left
                while x < columns and not landed:
                    landed = sandbox.move(Direction.Right)
                    moves.append(Direction.Right)
                    if sandbox.falling is not None:
                        x = sandbox.falling.left
                if landed == False:
                    sandbox.move(Direction.Drop)
                    moves.append(Direction.Drop)
                score = self.score_system(sandbox)
                if score > bestScore:
                    bestScore = score
                    bestMoves = moves
        return bestMoves


SelectedPlayer = Lucy
