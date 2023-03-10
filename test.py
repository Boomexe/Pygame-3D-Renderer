vertexes = [
    [63, 63, 63],
    [63, -63, 63],
    [-63, -63, 63],
    [-63, 63, 63],
    [63, 63, -63],
    [63, -63, -63],
    [-63, -63, -63],
    [-63, 63, -63]
]

def project_vertex(vertex: list[int, int, int], focal_length: int) -> list[int, int]:
    x, y, z = vertex

    x_projected = (focal_length * x)