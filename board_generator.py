import random
def generate_matrix(n, mines):
    matrix = [[0 for i in range(n)] for j in range(n)]
    i = 0
    while i < mines:
        row = random.randint(0, n-1)
        col = random.randint(0, n-1)
        i+=1
        if matrix[row][col] == 0:

            matrix[row][col] = "X"
            directions = [
                [row, col-1],
                [row, col+1],
                [row-1, col],
                [row+1, col],
                [row+1, col+1],
                [row+1, col-1],
                [row-1, col+1],
                [row-1, col-1]
            ]
            for j in range(len(directions)):
                x = directions[j][0]
                y = directions[j][1]
                if (x < n and x >= 0) and (y < n and y >=0):
                    matrix[x][y] +=1
        else:
            i-=1
    return matrix

# matrix = generate_matrix(15, 25)
# for row in matrix:
#     print(row)