from tkinter import *

from Block import InsideBlock


class OneMagnetBlock(InsideBlock):
    def __init__(self, coords, canvas, stableCanvas, poly_cords, text, text_len, color, outline, inside_color):
        super().__init__(coords, canvas, stableCanvas, poly_cords, color, outline)
        self.text = text
        # connection to "under" block, first inside block
        self.connected = [None, None]

        self.obj_id = None
        self.first_poly_id = None
        self.first_poly_coords = []
        self.text_id = None
        self.text_coords = []
        self.inside_color = inside_color

        # inside the block
        self.default_items_id = []
        self.default_items_on_block = None

        self.first_inside_length = 40
        self.first_inside_height = 16
        self.block_length = self.coords[2]
        self.block_height = self.coords[3]
        self.text_len = text_len

    def create_text(self):
        self.text_coords = [self.coords[0] + 15, self.coords[1]+2]
        self.text_id = self.canvas.create_text(self.text_coords, anchor=NW, text=self.text)
        self.default_items_on_block = self
        self.default_items_id.append(self.text_id)
        return self.text_id

    def create_first_polygon(self):
        self.first_poly_coords = self.stableCanvas.inside_block_coords(self.text_len + 30, self.coords[1]+2,
                                                            self.first_inside_length, self.first_inside_height)
        self.first_poly_id = self.canvas.create_polygon(self.first_poly_coords, fill=self.inside_color)
        self.default_items_on_block = self
        self.default_items_id.append(self.first_poly_id)
        return self.first_poly_id

    def move_connected(self, delta_x, delta_y):
        self.change_coords(delta_x, delta_y)

        # moves first polygon magnet
        old_first_poly_coords = self.first_poly_coords
        self.first_poly_coords = [old_first_poly_coords[0] + delta_x, old_first_poly_coords[1] + delta_y,
                                  old_first_poly_coords[2], old_first_poly_coords[3]]

        # moves text
        old_text_coords = self.text_coords
        self.text_coords = [old_text_coords[0] + delta_x, old_text_coords[1] + delta_y]
        self.canvas.move(self.text_id, delta_x, delta_y)

        self.canvas.tag_raise(self.obj_id)
        # leaves the text on top always
        self.canvas.tag_raise(self.text_id)

        if self.connected[1] is None:
            self.canvas.tag_raise(self.first_poly_id)
            self.canvas.move(self.first_poly_id, delta_x, delta_y)