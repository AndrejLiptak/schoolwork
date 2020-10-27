def genres(path: str) -> None:
    with open(path) as file:
        file_lines = file.readlines()
    res = {}
    for line in file_lines:
        line = line.split(",")
        res[line[5]] = res.get(line[5], 0) + 1
    for genre in sorted(res):
        print(genre + ': ' + str(res[genre]))
