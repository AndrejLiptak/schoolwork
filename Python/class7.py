def pascal(n):
    arrays = []
    for i in range(n):
        row = [1 for _ in range(i+1)]
        for j in range(1,i):
            row[j] = arrays[i-1][j-1] + arrays[i-1][j]
        arrays.append(row)
    return arrays

def print_pascal(pascal):
    max_number_size = len(str(pascal[-1][len(pascal)//2])) + 2
    pascal.reverse()
    for row in pascal:
        line = ""
        for x in row:
            line += ("{0: ^" + str(max_number_size) + "}").format(x)
        print(("{0: ^" + str(max_number_size * len(pascal[0])) + "}").format(line))


print_pascal(pascal(10))

