from Block import InsideBlock


class FunctionBlock(InsideBlock):
    def __init__(self, coords, canvas, stableCanvas, poly_cords, color, outline):
        super().__init__(coords, canvas, stableCanvas, poly_cords, color, outline)
        # upper connection, lower connection
        self.connected = []
        self.stableCanvas = stableCanvas

    def move_connected(self, delta_x, delta_y):
        self.change_coords(delta_x, delta_y)
        if self.connected:
            for i in self.connected:
                i.move_connected(delta_x, delta_y)