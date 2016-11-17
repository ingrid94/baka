from tkinter import *


class TwoMagnetBlock:
    def __init__(self, coords, canvas, stableCanvas, poly_cords, text, text_len, color, outline, inside_color):
        self.coords = coords
        self.canvas = canvas
        self.stableCanvas = stableCanvas
        self.poly_cords = poly_cords
        self.text = text
        self.color = color
        self.outline = outline
        # connection to "under" block
        self.connected = [None]

        self.obj_id = None
        self.first_poly_id = None
        self.text_id = None
        self.text_coords = []
        self.inside_color = inside_color

        # inside the block
        self.default_items_id = []
        self.default_items_on_block = None

        self.first_inside_length = 40
        self.first_inside_height = 16
        self.second_inside_length = 40
        self.second_inside_height = 16
        self.block_length = self.coords[2]
        self.block_height = self.coords[3]
        self.text_len = text_len

    def create_polygon(self):
        self.obj_id = self.canvas.create_polygon(self.poly_cords, fill=self.color, outline=self.outline)
        return self.obj_id

    def create_first_polygon(self):
        poly_coords = self.stableCanvas.inside_block_coords(self.coords[0] + 10, self.coords[1]+2,
                                                            self.first_inside_length, self.first_inside_height)
        self.first_poly_id = self.canvas.create_polygon(poly_coords, fill=self.inside_color)
        self.default_items_on_block = self
        self.default_items_id.append(self.first_poly_id)
        return self.first_poly_id

    def create_text(self):
        self.text_coords = [self.first_inside_length + 22, self.coords[1]-1]
        self.text_id = self.canvas.create_text(self.text_coords, anchor=NW, text=self.text, font='bold')
        self.default_items_on_block = self
        self.default_items_id.append(self.text_id)
        return self.text_id

    def create_second_polygon(self):
        poly_coords = self.stableCanvas.inside_block_coords(
            self.coords[0] + 10 + self.first_inside_length + 10 + self.text_len + 10,
            self.coords[1] + 2, self.second_inside_length, self.second_inside_height)
        self.first_poly_id = self.canvas.create_polygon(poly_coords, fill=self.inside_color)
        self.default_items_on_block = self
        self.default_items_id.append(self.first_poly_id)
        return self.first_poly_id

