from tkinter import *

from Block import CommandBlock


class OneTextCommandBlock(CommandBlock):
    def __init__(self, coords, canvas, stableCanvas, poly_cords, color, outline, string, inside_color):
        super().__init__(coords, canvas, stableCanvas, poly_cords, color, outline)
        self.string = string
        self.text_coords = [self.coords[0]+7, self.coords[1]+10]
        self.inside_magnet_coords = None
        self.inside_poly_coords = [self.coords[0]+50, self.coords[1]+7, 16, 50]
        self.inside_color = inside_color
        self.text_id = None

    def create_text(self):
        self.text_id = self.canvas.create_text(self.text_coords, anchor=NW, text=self.string)
        self.default_items_on_block = self
        self.default_items_id.append(self.text_id)
        return self.text_id

    def create_inside_polygon(self):
        poly_coords = self.stableCanvas.inside_block_coords(self.inside_poly_coords[0], self.inside_poly_coords[1],
                                                            self.inside_poly_coords[2], self.inside_poly_coords[3])
        self.poly_id = self.canvas.create_polygon(poly_coords, fill=self.inside_color)
        self.default_items_id.append(self.poly_id)
        return self.poly_id

    def change_inside_coords(self, delta_x, delta_y):
        old_text_coords = self.text_coords
        self.text_coords = [old_text_coords[0] + delta_x, old_text_coords[1] + delta_y]
        self.canvas.move(self.text_id, delta_x, delta_y)
        old_poly_coords = self.inside_poly_coords
        self.inside_poly_coords = [old_poly_coords[0] + delta_x, old_poly_coords[1]+delta_y, old_poly_coords[2], old_poly_coords[3]]
        self.canvas.tag_raise(self.text_id)
        if self.connected[2] is None:
            self.canvas.tag_raise(self.poly_id)
            self.canvas.move(self.poly_id, delta_x, delta_y)

    def delete_inside_poly(self, movable_blocks):
        if self.poly_id:
            del movable_blocks[self.poly_id]
            self.canvas.delete(self.poly_id)
            self.default_items_id.remove(self.poly_id)
            self.poly_id = None