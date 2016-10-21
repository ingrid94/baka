from tkinter import *
import tkinter.messagebox
import re

from ChooseBlocksCanvas import ChooseBlocksCanvas
from ControlBlock import ControlBlock, ControlBlockLower
from FunctionBlock import FunctionBlock
from PrintBlock import PrintBlock
from ReturnBlock import ReturnBlock
from TypeBlock import TypeBlock


class MoveBlocksCanvas(ChooseBlocksCanvas):
    def __init__(self, root, t1):
        super().__init__(root)
        self.root = root
        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.binding()
        self.stableCanvas = t1
        self.stableCanvas.bind(self.create_blocks)
        self.movable_blocks = {}

    def create_blocks(self, event):
        self.stableCanvas.get_focus_set()
        resp = event.widget.find_overlapping(event.x, event.y, event.x, event.y)
        if len(resp) != 0:
            tag = self.stableCanvas.gettags(resp[0])[0]
            if tag == 'print_block':
                cords = self.stableCanvas.command_block_coords(0, 0, 30, 120)
                assign_block = PrintBlock([0, 0, 30, 120], self.canvas, self.stableCanvas, cords)
                obj_id = assign_block.create_polygon()
                poly_id = assign_block.create_inside_polygon()
                text_id = assign_block.create_text()
                text2_id = assign_block.create_text2()
                self.movable_blocks[obj_id] = assign_block
                self.movable_blocks[poly_id] = assign_block
                self.movable_blocks[text_id] = assign_block
                self.movable_blocks[text2_id] = assign_block
            elif tag == 'return_block':
                cords = self.stableCanvas.command_block_coords(0, 0, 30, 120)
                assign_block = ReturnBlock([0, 0, 30, 120], self.canvas, self.stableCanvas, cords)
                obj_id = assign_block.create_polygon()
                poly_id = assign_block.create_inside_polygon()
                text_id = assign_block.create_text()
                self.movable_blocks[obj_id] = assign_block
                self.movable_blocks[poly_id] = assign_block
                self.movable_blocks[text_id] = assign_block
            elif tag == 'inside_block':
                cords = self.stableCanvas.inside_block_coords(0, 0, 130, 20)
                bool_op_block = FunctionBlock([0, 0, 130, 20], self.canvas, self.stableCanvas, cords, 'dodger blue', 'steel blue')
                obj_id = bool_op_block.create_polygon()
                self.movable_blocks[obj_id] = bool_op_block
            elif tag == 'control_block':
                cords = self.stableCanvas.control_block_coords(0, 0, 30, 35)[0]
                if_block = ControlBlock([0, 0, 30, 35], self.canvas, self.stableCanvas, cords)
                obj_id = if_block.create_polygon()
                self.movable_blocks[obj_id] = if_block
                # lower part of controlBlock
                cords = self.stableCanvas.control_block_coords(0, 0, 30, 35)[1]
                if_block_lower = ControlBlockLower([0, 70, 30, 35], self.canvas, cords)
                obj_id_lower = if_block_lower.create_polygon()
                self.movable_blocks[obj_id_lower] = if_block_lower
                if_block.connected[2] = if_block_lower
                if_block_lower.connected[0] = if_block
            elif tag == 'number':
                self.create_frame('number')
            elif tag == 'variable':
                self.create_frame('variable')
            elif tag == 'string':
                self.create_frame('string')
            elif tag == 'none':
                self.create_type_block('None', None, 8, 'none')
            elif tag == 'true':
                self.create_type_block('True', None, 8, 'true')
            elif tag == 'false':
                self.create_type_block('False', None, 7, 'false')

    def create_frame(self, inside_type):

        text = ""
        if inside_type == 'variable':
            text = "Variables must begin with a letter (a - z, A - Z) or underscore (_). \n" \
                   "Other characters can be letters, numbers or _"
        elif inside_type == 'number':
            text = "Numbers consist of digits (0-9). \n To get floating point number use point (.)"
        elif inside_type == 'string':
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

        confirm = Button(frame, text="Confirm", command=lambda: self.create_type(can, v, inside_type))
        confirm.pack(side=RIGHT, padx=30, pady=10)

    def delete_item(self, frame):
        self.canvas.delete(frame)

    def create_type(self, frame, v, inside_type):
        s = v.get()
        if inside_type == 'number':
            if s.replace('.', '', 1).isdigit():
                self.create_type_block(s, frame, 8, inside_type)
            else:
                tkinter.messagebox.showerror("Error", "It's not a number. Try again. ")
        elif inside_type == 'string':
            p = re.match(r'^(\"|\')(.)*(\"|\')$', s, re.S)
            if p:
                self.create_type_block(s, frame, 6, inside_type)
            else:
                tkinter.messagebox.showerror("Error", "It's not a string. Try again. ")
        elif inside_type == 'variable':
            p = re.match(r'^[a-zA-Z_][\w0-9_]*$', s, re.S)
            if p:
                self.create_type_block(s, frame, 6.5, inside_type)
            else:
                tkinter.messagebox.showerror("Error", "It's not a variable. Try again. ")

    def create_type_block(self, s, frame, times, inside_type):
        w = len(s) * times + 15
        cords = self.stableCanvas.inside_block_coords(0, 0, w, 20)
        type_block = TypeBlock([0, 0, w, 20], self.canvas, self.stableCanvas, cords, 'limegreen', 'green', s, inside_type)
        obj_id = type_block.create_polygon()
        text_id = type_block.create_text()
        self.movable_blocks[obj_id] = type_block
        self.movable_blocks[text_id] = type_block
        if frame is not None:
            self.canvas.delete(frame)

    def create_polygon(self, args, **kw):
        return self.canvas.create_polygon(args, kw)

    def on_token_button_press(self, event):
        active = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if len(active) != 0:
            peale = active[-1]
            self.drag_data["item"] = peale
            self.canvas.tag_raise(peale)
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
            # when block is moved and upper isn't None, then disconnect
            # to disconnect blocks which are connected
            if self.movable_blocks[peale].connected[0] is not None:
                if not isinstance(self.movable_blocks[peale], ControlBlockLower):
                    self.movable_blocks[peale].disconnect_magnet(self.movable_blocks, 'disconnect')

    def on_token_button_release(self, event):
        if self.drag_data["item"] is not None:
            class_instance = self.movable_blocks[self.drag_data["item"]]
            if not isinstance(class_instance, ControlBlockLower):
                class_instance.move_to_magnet(self.movable_blocks)
            if isinstance(class_instance, TypeBlock) and (class_instance.inside_type == 'number' or class_instance.inside_type=='string' or class_instance.inside_type=='variable'):
                class_instance.check_if_frame_needed(self.drag_data["item"], self.movable_blocks)

        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0

    def on_token_motion(self, event):
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]
        if self.drag_data["item"] is not None:
            class_instance = self.movable_blocks[self.drag_data["item"]]
            # changes coordinates and moves blocks
            class_instance.move_connected(delta_x, delta_y)
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
            class_instance.check_magnets_during_move(self.movable_blocks)

    def binding(self):
        self.canvas.bind("<ButtonPress-1>", self.on_token_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_token_button_release)
        self.canvas.bind("<B1-Motion>", self.on_token_motion)