import tkinter.messagebox
from tkinter import *

from Block import CommandBlock


class VariableBlock(CommandBlock):
    def __init__(self, coords, canvas, stableCanvas, poly_cords, variable_name, len):
        super().__init__(coords, canvas, stableCanvas, poly_cords)
        self.string = '='
        self.variable_name = variable_name
        self.variable_name_block_len = len
        self.variable_name_poly_id = None
        self.variable_name_id = None
        self.text_id = None
        self.poly_id = None
        self.variable_poly_coords = [self.coords[0] + 10, self.coords[1] + 9, len, 16]
        self.name_text_coords = [self.coords[0] + 20, self.coords[1] + 9]
        self.text_coords = [self.coords[0]+self.variable_name_block_len + 22, self.coords[1]+5]
        # self.inside_magnet_coords = None
        self.inside_poly_coords = [self.coords[0] + self.variable_name_block_len + 40, self.coords[1]+10, 50, 15]
        self.inside_color = 'light pink'
        self.variable_color = 'limegreen'

    def create_polygon(self):
        self.poly_cords = self.stableCanvas.command_block_coords(self.coords[0], self.coords[1], self.coords[2],
                                                                 self.coords[3] + self.variable_name_block_len)
        self.obj_id = self.canvas.create_polygon(self.poly_cords, fill=self.color, outline=self.outline)
        return self.obj_id

    def create_variable_polygon(self):
        poly_coords = self.stableCanvas.inside_block_coords(self.coords[0] + 10, self.coords[1] + 9, self.variable_name_block_len, 16)
        self.variable_name_poly_id = self.canvas.create_polygon(poly_coords, fill=self.variable_color)
        self.default_items_on_block = self
        self.default_items_id.append(self.variable_name_poly_id)
        return self.variable_name_poly_id

    def create_variable_name(self):
        self.variable_name_id = self.canvas.create_text(self.name_text_coords, anchor=NW, text=self.variable_name)
        self.default_items_on_block = self
        self.default_items_id.append(self.variable_name_id)
        return self.variable_name_id

    def create_text(self):
        self.text_coords = [self.coords[0] + self.variable_name_block_len + 22, self.coords[1] + 5]
        self.text_id = self.canvas.create_text(self.text_coords, anchor=NW, text=self.string, font='bold')
        self.default_items_on_block = self
        self.default_items_id.append(self.text_id)
        return self.text_id

    def create_inside_polygon(self):
        poly_coords = self.stableCanvas.inside_block_coords(self.inside_poly_coords[0], self.inside_poly_coords[1], self.inside_poly_coords[2], self.inside_poly_coords[3])
        self.poly_id = self.canvas.create_polygon(poly_coords, fill=self.inside_color)
        self.default_items_on_block = self
        self.default_items_id.append(self.poly_id)
        return self.poly_id

    def change_inside_coords(self, delta_x, delta_y):

        old_variable_poly_coords = self.variable_poly_coords
        self.variable_poly_coords = [old_variable_poly_coords[0] + delta_x, old_variable_poly_coords[1] + delta_y,
                                     old_variable_poly_coords[2], old_variable_poly_coords[3]]
        self.canvas.move(self.variable_name_poly_id, delta_x, delta_y)

        old_name_coords = self.name_text_coords
        self.name_text_coords = [old_name_coords[0] + delta_x, old_name_coords[1] + delta_y]
        self.canvas.move(self.variable_name_id, delta_x, delta_y)

        old_text_coords = self.text_coords
        self.text_coords = [old_text_coords[0] + delta_x, old_text_coords[1] + delta_y]
        self.canvas.move(self.text_id, delta_x, delta_y)

        old_poly_coords = self.inside_poly_coords
        self.inside_poly_coords = [old_poly_coords[0] + delta_x, old_poly_coords[1]+delta_y, old_poly_coords[2], old_poly_coords[3]]

        self.canvas.tag_raise(self.text_id)
        self.canvas.tag_raise(self.variable_name_poly_id)
        self.canvas.tag_raise(self.variable_name_id)

        if self.connected[2] is None:
            self.canvas.tag_raise(self.poly_id)
            self.canvas.move(self.poly_id, delta_x, delta_y)

    def delete_inside_poly(self, movable_blocks):
        if self.poly_id:
            del movable_blocks[self.poly_id]
            self.canvas.delete(self.poly_id)
            self.default_items_id.remove(self.poly_id)
            self.poly_id = None

    # all methods under to change variable name
    def check_if_frame_needed(self, clicked_id, movable_blocks):
        if clicked_id == self.variable_name_id or clicked_id == self.variable_name_poly_id:
            self.create_frame(movable_blocks)

    def create_frame(self, movable_blocks):

        text = "Variables must begin with a letter (a - z, A - Z) or underscore (_). \n" \
                   "Other characters can be letters, numbers or _"

        frame = Frame(self.canvas)
        can = self.canvas.create_window(250, 200, window=frame)

        introduction = Label(frame, text=text)
        introduction.pack(pady=10)

        v = StringVar()
        e = Entry(frame, textvariable=v)
        e.pack()

        cancel = Button(frame, text="Cancel", command=lambda: self.delete_item(can))
        cancel.pack(side=LEFT, padx=30, pady=10)

        confirm = Button(frame, text="Confirm", command=lambda: self.create_type(can, v, movable_blocks))
        confirm.pack(side=RIGHT, padx=30, pady=10)

    def delete_item(self, frame):
        self.canvas.delete(frame)

    def create_type(self, frame, v, movable_blocks):
        s = v.get()
        p = re.match(r'^[a-zA-Z_][\w0-9_]*$', s, re.S)
        if p:
            self.change_type_block(s, frame, 6, movable_blocks)
        elif s is "" and self.variable_name is not None:
            self.change_type_block(self.variable_name, frame, 5.5, movable_blocks)
        else:
            tkinter.messagebox.showerror("Error", "It's not a variable. Try again. ")

    def change_type_block(self, s, frame, times, movable_blocks):
        self.variable_name = s
        w = len(s) * times + 15
        delta_x = w - self.variable_name_block_len
        self.variable_name_block_len = w
        # changes CommandBlock size
        del movable_blocks[self.obj_id]
        self.canvas.delete(self.obj_id)
        self.create_polygon()
        movable_blocks[self.obj_id] = self
        # changes variable block size
        del movable_blocks[self.variable_name_poly_id]
        self.canvas.delete(self.variable_name_poly_id)
        self.create_variable_polygon()
        movable_blocks[self.variable_name_poly_id] = self
        # changes variable name
        self.canvas.itemconfig(self.variable_name_id, text=s)
        # changes '=' position
        self.canvas.move(self.text_id, delta_x, 0)
        # changes inside block position
        self.canvas.move(self.poly_id, delta_x, 0)
        # raises texts and inside polygon
        self.canvas.tag_raise(self.text_id)
        self.canvas.tag_raise(self.variable_name_id)
        self.canvas.tag_raise(self.poly_id)

        if frame is not None:
            self.canvas.delete(frame)