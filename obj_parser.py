def parse_obj(filename, vertices, normals, textures, faces):
    file = open(filename)
    line = file.readline()
    while line:
        line = line.strip().split()
        if not line:
            line = file.readline()
            continue
        if line[0] == 'v':
            vertices.append(list(map(float, line[1:])))
        if line[0] == 'vn':
            normals.append(list(map(float, line[1:])))
        if line[0] == 'vt':
            textures.append(list(map(float, line[1:])))
        if line[0] == 'f':
            faces.append(list(map(lambda x: list(map(float, x.split('/'))), line[1:])))
        line = file.readline()
    file.close()