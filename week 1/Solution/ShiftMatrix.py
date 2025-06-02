def rotate_outer_elements(matrix, n):
    outer = [matrix[0][0], matrix[0][1], matrix[0][2],
             matrix[1][2], matrix[2][2], matrix[2][1],
             matrix[2][0], matrix[1][0]]
    
    n = n % 8
    rotated = outer[-n:] + outer[:-n]
    
    matrix[0][0], matrix[0][1], matrix[0][2] = rotated[0], rotated[1], rotated[2]
    matrix[1][2], matrix[2][2], matrix[2][1] = rotated[3], rotated[4], rotated[5]
    matrix[2][0], matrix[1][0] = rotated[6], rotated[7]
    
    return matrix

matrix = [list(map(int, input().split())) for _ in range(3)]
n = int(input())

result = rotate_outer_elements(matrix, n)

for row in result:
    print(" ".join(map(str, row)))
