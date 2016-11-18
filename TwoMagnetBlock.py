from tkinter import *

from Block import OneMagnetBlock


class TwoMagnetBlock(OneMagnetBlock):
    def __init__(self, coords, canvas, stableCanvas, poly_cords, text, text_len, color, outline, inside_color):
        super().__init__(coords, canvas, stableCanvas, poly_cords, text, text_len, color, outline, inside_color)
        self.text = text
        # connection to "under" block, first inside block, second inside block
        self.connected = [None, None, None]

        self.second_poly_id = None
        self.second_poly_coords = []

        self.second_inside_length = 40
        self.second_inside_height = 16

    def create_first_polygon(self):
        self.inside_poly_coords = [self.coords[0] + 10, self.coords[1]+2,
                                   self.first_inside_length, self.first_inside_height]
        first_poly_coords = self.stableCanvas.inside_block_coords(self.coords[0] + 10, self.coords[1]+2,
                                                                  self.first_inside_length, self.first_inside_height)
        self.first_poly_id = self.canvas.create_polygon(first_poly_coords, fill=self.inside_color)
        self.default_items_on_block = self
        self.default_items_id.append(self.first_poly_id)
        return self.first_poly_id

    def create_text(self):
        if self.text == 'and' or self.text == 'or':
            self.text_coords = [self.first_inside_length + 22, self.coords[1] + 2]
            self.text_id = self.canvas.create_text(self.text_coords, anchor=NW, text=self.text)
        else:
            self.text_coords = [self.first_inside_length + 22, self.coords[1] - 1]
            self.text_id = self.canvas.create_text(self.text_coords, anchor=NW, text=self.text, font='bold')
        self.default_items_on_block = self
        self.default_items_id.append(self.text_id)
        return self.text_id

    def create_second_polygon(self):
        self.second_poly_coords = [self.coords[0] + 10 + self.first_inside_length + 10 + self.text_len + 10,
                                   self.coords[1] + 2, self.second_inside_length, self.second_inside_height]
        second_poly_coords = self.stableCanvas.inside_block_coords(
            self.coords[0] + 10 + self.first_inside_length + 10 + self.text_len + 10,
            self.coords[1] + 2, self.second_inside_length, self.second_inside_height)
        self.second_poly_id = self.canvas.create_polygon(second_poly_coords, fill=self.inside_color)
        self.default_items_on_block = self
        self.default_items_id.append(self.second_poly_id)
        return self.second_poly_id

    def move_connected(self, delta_x, delta_y):
        self.change_coords(delta_x, delta_y)
        if self.default_items_on_block is not None:
            self.default_items_on_block.change_inside_coords(delta_x, delta_y)
        if self.connected[1] is not None:
            self.connected[1].move_connected(delta_x, delta_y)
            for i in self.connected[1].default_items_id:
                self.canvas.tag_raise(i)
        if self.connected[2] is not None:
            self.connected[2].move_connected(delta_x, delta_y)
            for i in self.connected[2].default_items_id:
                self.canvas.tag_raise(i)

    def change_inside_coords(self, delta_x, delta_y):

        # moves first polygon magnet
        old_first_poly_coords = self.inside_poly_coords
        self.inside_poly_coords = [old_first_poly_coords[0] + delta_x, old_first_poly_coords[1] + delta_y,
                                  old_first_poly_coords[2], old_first_poly_coords[3]]

        # moves text
        old_text_coords = self.text_coords
        self.text_coords = [old_text_coords[0] + delta_x, old_text_coords[1] + delta_y]
        self.canvas.move(self.text_id, delta_x, delta_y)

        # moves second polygon magnet
        old_second_poly_coords = self.second_poly_coords
        self.second_poly_coords = [old_second_poly_coords[0] + delta_x, old_second_poly_coords[1] + delta_y,
                                   old_second_poly_coords[2], old_second_poly_coords[3]]

        self.canvas.tag_raise(self.obj_id)
        # leaves the text on top always
        self.canvas.tag_raise(self.text_id)

        if self.connected[1] is None:
            self.canvas.tag_raise(self.first_poly_id)
            self.canvas.move(self.first_poly_id, delta_x, delta_y)

        if self.connected[2] is None:
            self.canvas.tag_raise(self.second_poly_id)
            self.canvas.move(self.second_poly_id, delta_x, delta_y)

