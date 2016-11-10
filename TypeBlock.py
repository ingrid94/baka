from tkinter import *
import tkinter.messagebox

from Block import InsideBlock


class TypeBlock(InsideBlock):
    def __init__(self, coords, canvas, stableCanvas, poly_cords, color, outline, string, inside_type):
        super().__init__(coords, canvas, stableCanvas, poly_cords, color, outline)
        self.string_on_block = string
        self.text_id = None
        self.text_coords = [self.coords[0] + 12, self.coords[1] + 1]
        self.inside_type = inside_type
        self.connected = [None]

    def create_text(self):
        self.text_id = self.canvas.create_text(self.text_coords, anchor=NW, text=self.string_on_block)
        self.default_items_id.append(self.text_id)
        return self.text_id

    def move_connected(self, delta_x, delta_y):
        self.change_coords(delta_x, delta_y)
        # moves text
        old_text_coords = self.text_coords
        self.text_coords = [old_text_coords[0] + delta_x, old_text_coords[1] + delta_y]
        self.canvas.move(self.text_id, delta_x, delta_y)
        self.canvas.tag_raise(self.obj_id)
        # leaves the text on top always
        self.canvas.tag_raise(self.text_id)

    def check_if_frame_needed(self, clicked_id, movable_blocks):
        if clicked_id == self.text_id:
            self.create_frame(movable_blocks)

    def create_frame(self, movable_blocks):

        text = ""
        if self.inside_type == 'variable':
            text = "Variables must begin with a letter (a - z, A - Z) or underscore (_). \n" \
                   "Other characters can be letters, numbers or _"
        elif self.inside_type == 'number':
            text = "Numbers consist of digits (0-9). \n To get floating point number use point (.)"
        elif self.inside_type == 'string':
            text = "String literals are written in single or double quotes. "

        frame = Frame(self.canvas)
        can = self.canvas.create_window(250, 200, window=frame)

        introduction = Label(frame, text=text)
        introduction.pack(pady=10)

        v = StringVar()
        e = Entry(frame, textvariable=v)
        e.pack()

        cancel = Button(frame, text="Cancel", command=lambda: self.delete_item(can))
        cancel.pack(side=LEFT, padx=30, pady=10)

        confirm = Button(frame, text="Confirm", command=lambda: self.create_type(can, v, self.inside_type, movable_blocks))
        confirm.pack(side=RIGHT, padx=30, pady=10)

    def delete_item(self, frame):
        self.canvas.delete(frame)

    def create_type(self, frame, v, inside_type, movable_blocks):
        s = v.get()
        if inside_type == 'number':
            if s.replace('.', '', 1).isdigit():
                self.change_type_block(s, frame, 8, movable_blocks)
            elif s is "" and self.string_on_block is not None:
                self.change_type_block(self.string_on_block, frame, 6, movable_blocks)
            else:
                tkinter.messagebox.showerror("Error", "It's not a number. Try again. ")
        elif inside_type == 'string':
            p = re.match(r'^(\"|\')(.)*(\"|\')$', s, re.S)
            if p:
                self.change_type_block(s, frame, 6, movable_blocks)
            elif s is "" and self.string_on_block is not None:
                self.change_type_block(self.string_on_block, frame, 6, movable_blocks)
            else:
                tkinter.messagebox.showerror("Error", "It's not a string. Try again. ")
        elif inside_type == 'variable':
            p = re.match(r'^[a-zA-Z_][\w0-9_]*$', s, re.S)
            if p:
                self.change_type_block(s, frame, 6, movable_blocks)
            elif s is "" and self.string_on_block is not None:
                self.change_type_block(self.string_on_block, frame, 6, movable_blocks)
            else:
                tkinter.messagebox.showerror("Error", "It's not a variable. Try again. ")

    def change_type_block(self, s, frame, times, movable_blocks):
        self.string_on_block = s
        w = len(s) * times + 15
        self.poly_cords = self.stableCanvas.inside_block_coords(self.coords[0], self.coords[1], w, 20)
        del movable_blocks[self.obj_id]
        self.canvas.delete(self.obj_id)
        self.obj_id = self.create_polygon()
        movable_blocks[self.obj_id] = self
        self.canvas.itemconfig(self.text_id, text=s)
        self.canvas.tag_raise(self.text_id)
        if frame is not None:
            self.canvas.delete(frame)