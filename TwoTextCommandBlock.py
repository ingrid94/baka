from tkinter import *


from OneTextCommandBlock import OneTextCommandBlock


class TwoTextCommandBlock(OneTextCommandBlock):
    def __init__(self, coords, canvas, stableCanvas, poly_cords, color, outline, string, string2, inside_color):
        super().__init__(coords, canvas, stableCanvas, poly_cords, color, outline, string, inside_color)
        self.string2 = string2
        self.text2_id = None
        self.text2_coords = [self.coords[3]-10, self.coords[1]+10]
        self.inside_poly_coords = [self.coords[0]+45, self.coords[1]+7, 16, 50]
        self.inside_color = inside_color

    def create_text2(self):
        self.text2_id = self.canvas.create_text(self.text2_coords, anchor=NW, text=self.string2)
        self.default_items_on_block = self
        self.default_items_id.append(self.text2_id)
        return self.text2_id

    def change_inside_coords(self, delta_x, delta_y):
        old_text_coords = self.text_coords
        self.text_coords = [old_text_coords[0] + delta_x, old_text_coords[1] + delta_y]
        self.canvas.move(self.text_id, delta_x, delta_y)
        old_text2_coords = self.text2_coords
        self.text2_coords = [old_text2_coords[0] + delta_x, old_text2_coords[1] + delta_y]
        self.canvas.move(self.text2_id, delta_x, delta_y)
        old_poly_coords = self.inside_poly_coords
        self.inside_poly_coords = [old_poly_coords[0] + delta_x, old_poly_coords[1]+delta_y, old_poly_coords[2], old_poly_coords[3]]
        self.canvas.tag_raise(self.text_id)
        self.canvas.tag_raise(self.text2_id)
        if self.connected[2] is None:
            self.canvas.tag_raise(self.poly_id)
            self.canvas.move(self.poly_id, delta_x, delta_y)

    def delete_inside_poly(self, movable_blocks):
        if self.poly_id:
            del movable_blocks[self.poly_id]
            self.canvas.delete(self.poly_id)
            self.default_items_id.remove(self.poly_id)
            self.poly_id = None