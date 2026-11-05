class Grid:
    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth

        self.matrix = [[15 for _ in range(width)] for _ in range(heigth)]
