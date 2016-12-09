from tkinter import *
import tkinter.messagebox
import re

from ChooseBlocksCanvas import ChooseBlocksCanvas


# calc: 'limegreen', 'green'
class MoveBlocksCanvas(ChooseBlocksCanvas):

    def __init__(self, root, t1):
        super().__init__(root)
        self.root = root
        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.binding()
        self.stableCanvas = t1
        self.stableCanvas.bind(self.create_blocks)
        self.movable_blocks = {}
        self.photo = None
        self.item = None

    def create_bin(self):
        # delete icon: "https://icons8.com/web-app/362/Delete"
        self.photo = PhotoImage(file="Delete-52.gif")
        self.item = self.canvas.create_image(460, 35, image=self.photo)
        self.movable_blocks[self.item] = 'bin'

    def create_blocks(self, event):
        self.stableCanvas.get_focus_set()
        resp = event.widget.find_overlapping(event.x, event.y, event.x, event.y)
        if len(resp) != 0:
            tag = self.stableCanvas.gettags(resp[0])[0]
            if tag == 'print_block':
                cords = self.stableCanvas.command_block_coords(0, 0, 30, 120)
                print_block = TwoTextCommandBlock([0, 0, 30, 120], self.canvas, self.stableCanvas, cords, 'violet red',
                                                  'purple', 'print(', ')', 'light pink')
                obj_id = print_block.create_polygon()
                poly_id = print_block.create_inside_polygon()
                text_id = print_block.create_text()
                text2_id = print_block.create_text2()
                self.movable_blocks[obj_id] = print_block
                self.movable_blocks[poly_id] = print_block
                self.movable_blocks[text_id] = print_block
                self.movable_blocks[text2_id] = print_block
            elif tag == 'return_block':
                cords = self.stableCanvas.command_block_coords(0, 0, 30, 120)
                return_block = OneTextCommandBlock([0, 0, 30, 120], self.canvas, self.stableCanvas, cords, 'violet red',
                                                   'purple', 'return', 'light pink')
                obj_id = return_block.create_polygon()
                poly_id = return_block.create_inside_polygon()
                text_id = return_block.create_text()
                self.movable_blocks[obj_id] = return_block
                self.movable_blocks[poly_id] = return_block
                self.movable_blocks[text_id] = return_block
            elif tag == 'variable_block':
                self.create_frame('variable_assign')
            elif tag == 'list_block':
                self.create_frame('list')
            elif tag == 'if_block':
                cords = self.stableCanvas.control_block_coords(0, 0, 30, 110, 25)[0]
                if_block = ControlBlock([0, 0, 30, 110, 25], self.canvas, self.stableCanvas, cords, 'orange',
                                        'chocolate', 'if ', 'peachpuff')
                obj_id = if_block.create_polygon()
                inside_id = if_block.create_inside_polygon()
                text_id = if_block.create_text()
                self.movable_blocks[obj_id] = if_block
                self.movable_blocks[inside_id] = if_block
                self.movable_blocks[text_id] = if_block
                # lower part of controlBlock
                cords = self.stableCanvas.control_block_coords(0, 0, 30, 110, 25)[1]
                if_block_lower = ControlBlockLower([0, 70, 30, 110, 25], self.canvas, cords)
                obj_id_lower = if_block_lower.create_polygon()
                self.movable_blocks[obj_id_lower] = if_block_lower
                if_block.connected[3] = if_block_lower
                if_block_lower.connected[0] = if_block
            elif tag == 'number':
                self.create_frame('number')
            elif tag == 'variable':
                self.create_frame('variable')
            elif tag == 'variable_assign':
                self.create_frame('variable_assign')
            elif tag == 'string':
                self.create_frame('string')
            elif tag == 'none':
                self.create_type_block('None', None, 8, 'none', 'dodger blue', 'steel blue')
            elif tag == 'true':
                self.create_type_block('True', None, 8, 'true', 'dodger blue', 'steel blue')
            elif tag == 'false':
                self.create_type_block('False', None, 7, 'false', 'dodger blue', 'steel blue')
            # second column blocks
            elif tag == 'equals':
                # args: block length, text length, text
                self.create_two_magnet_block(140, 20, "==")
            elif tag == 'not_equal':
                self.create_two_magnet_block(140, 20, "!=")
            elif tag == 'greater':
                self.create_two_magnet_block(130, 10, '>')
            elif tag == 'smaller':
                self.create_two_magnet_block(130, 10, '<')
            elif tag == 'greater_or_equal':
                self.create_two_magnet_block(140, 20, '>=')
            elif tag == 'smaller_or_equal':
                self.create_two_magnet_block(140, 20, '<=')
            elif tag == 'or':
                self.create_two_magnet_block(130, 10, 'or')
            elif tag == 'and':
                self.create_two_magnet_block(130, 15, 'and')
            elif tag == 'not':
                cords = self.stableCanvas.inside_block_coords(0, 0, 20, 90)
                one_magnet_block = OneMagnetBlock([0, 0, 20, 90], self.canvas, self.stableCanvas, cords, 'not ',
                                                  10, 'dodger blue', 'steel blue', 'sky blue')
                obj_id = one_magnet_block.create_polygon()
                first_poly_id = one_magnet_block.create_first_polygon()
                text_id = one_magnet_block.create_text()
                self.movable_blocks[obj_id] = one_magnet_block
                self.movable_blocks[first_poly_id] = one_magnet_block
                self.movable_blocks[text_id] = one_magnet_block

    def create_frame(self, inside_type):

        text = ""
        if inside_type == 'variable' or inside_type == 'variable_assign' or inside_type == 'list':
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
                self.create_type_block(s, frame, 8, inside_type, 'dodger blue', 'steel blue')
            else:
                tkinter.messagebox.showerror("Error", "It's not a number. Try again. ")
        elif inside_type == 'string':
            p = re.match(r'^(\"|\')(.)*(\"|\')$', s, re.S)
            if p:
                self.create_type_block(s, frame, 6, inside_type, 'dodger blue', 'steel blue')
            else:
                tkinter.messagebox.showerror("Error", "It's not a string. Try again. ")
        elif inside_type == 'variable' or inside_type == 'variable_assign' or inside_type == 'list':
            p = re.match(r'^[a-zA-Z_][\w0-9_]*$', s, re.S)
            if p and inside_type == 'variable':
                self.create_type_block(s, frame, 6, inside_type, 'dodger blue', 'steel blue')
            elif p and (inside_type == 'variable_assign' or inside_type == 'list'):
                self.create_variable_block(s, frame, 6, inside_type)
            else:
                tkinter.messagebox.showerror("Error", "It's not a variable. Try again. ")

    def create_type_block(self, s, frame, times, inside_type, color, outline):
        w = len(s) * times + 15
        cords = self.stableCanvas.inside_block_coords(0, 0, 16, w)
        type_block = TypeBlock([0, 0, 16, w], self.canvas, self.stableCanvas, cords, color, outline, s, inside_type)
        obj_id = type_block.create_polygon()
        text_id = type_block.create_text()
        self.movable_blocks[obj_id] = type_block
        self.movable_blocks[text_id] = type_block
        if frame is not None:
            self.canvas.delete(frame)

    def create_variable_block(self, s, frame, times, inside_type):
        w = len(s) * times + 15
        cords = self.stableCanvas.command_block_coords(0, 0, 30, 110)
        if inside_type == 'variable_assign':
            variable_block = VariableBlock([0, 0, 30, 110], self.canvas, self.stableCanvas, cords, 'violet red',
                                           'purple', s, w)
        else:
            variable_block = ListBlock([0, 0, 30, 110], self.canvas, self.stableCanvas, cords, 'violet red',
                                       'purple', s, w)
        obj_id = variable_block.create_polygon()
        variable_poly_id = variable_block.create_variable_polygon()
        variable_name_id = variable_block.create_variable_name()
        text_id = variable_block.create_text()
        inside_poly_id = variable_block.create_inside_polygon()
        if inside_type == 'list':
            text2_id = variable_block.create_text2()
            self.movable_blocks[text2_id] = variable_block
        self.movable_blocks[obj_id] = variable_block
        self.movable_blocks[variable_poly_id] = variable_block
        self.movable_blocks[variable_name_id] = variable_block
        self.movable_blocks[text_id] = variable_block
        self.movable_blocks[inside_poly_id] = variable_block
        if frame is not None:
            self.canvas.delete(frame)

    def create_two_magnet_block(self, blo_len, text_len, text):
        cords = self.stableCanvas.inside_block_coords(0, 0, 20, blo_len)
        two_magnet_block = TwoMagnetBlock([0, 0, 20, blo_len], self.canvas, self.stableCanvas, cords, text, text_len,
                                          'dodger blue', 'steel blue', 'sky blue')
        obj_id = two_magnet_block.create_polygon()
        first_poly_id = two_magnet_block.create_first_polygon()
        text_id = two_magnet_block.create_text()
        second_poly_id = two_magnet_block.create_second_polygon()
        self.movable_blocks[obj_id] = two_magnet_block
        self.movable_blocks[first_poly_id] = two_magnet_block
        self.movable_blocks[text_id] = two_magnet_block
        self.movable_blocks[second_poly_id] = two_magnet_block

    def create_polygon(self, args, **kw):
        return self.canvas.create_polygon(args, kw)

    def on_token_button_press(self, event):
        active = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if len(active) != 0 and self.movable_blocks[active[-1]] != 'bin':
            peale = active[-1]
            self.drag_data["item"] = peale
            self.canvas.tag_raise(peale)
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
            # when block is moved and upper isn't None, then disconnect
            # to disconnect blocks which are connected
            if self.movable_blocks[peale].connected[0] is not None:
                if not isinstance(self.movable_blocks[peale], ControlBlockLower):
                    self.movable_blocks[peale].disconnect_magnet(self.movable_blocks)

    def on_token_button_release(self, event):
        if self.drag_data["item"] is not None and self.movable_blocks[self.drag_data["item"]] != 'bin':
            class_instance = self.movable_blocks[self.drag_data["item"]]
            if not isinstance(class_instance, ControlBlockLower):
                class_instance.move_to_magnet(self.movable_blocks)
            if (isinstance(class_instance, TypeBlock) and
                    (class_instance.inside_type == 'number' or class_instance.inside_type=='string'
                     or class_instance.inside_type == 'variable')) \
                    or (isinstance(class_instance, VariableBlock)):
                class_instance.check_if_frame_needed(self.drag_data["item"], self.movable_blocks)

        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0

    def on_token_motion(self, event):
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]
        if self.drag_data["item"] is not None and self.movable_blocks[self.drag_data["item"]] != 'bin':
            class_instance = self.movable_blocks[self.drag_data["item"]]
            # changes coordinates and moves blocks
            class_instance.move_connected(delta_x, delta_y)
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
            class_instance.check_magnets_during_move(self.movable_blocks)
        return [event.x, event.y]

    def binding(self):
        self.canvas.bind("<ButtonPress-1>", self.on_token_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_token_button_release)
        self.canvas.bind("<B1-Motion>", self.on_token_motion)

    def to_code(self):
        all_blocks = []
        first_blocks = []
        for block in self.movable_blocks.values():
            if block not in all_blocks and block != 'bin' and not isinstance(block, ControlBlockLower):
                all_blocks.append(block)
                if block.connected[0] is None and not isinstance(block, (OneMagnetBlock, TwoMagnetBlock, TypeBlock)):
                    first_blocks.append(block)

        file = open("generated.py", "w")
        for block in first_blocks:
            tabs = 0
            self.into_file(file, block, tabs)
        file.close()

    def into_file(self, file, block, tabs):
        if isinstance(block, TwoTextCommandBlock):
            self.make_tabs(file, tabs)
            file.write(block.string)
            if block.connected[2] is not None:
                self.into_file(file, block.connected[2], tabs)
            file.write(block.string2 + '\n')
            if block.connected[1] is not None:
                self.into_file(file, block.connected[1], tabs)
        elif isinstance(block, VariableBlock):
            self.make_tabs(file, tabs)
            file.write(block.variable_name + ' = ')
            if block.connected[2] is not None:
                self.into_file(file, block.connected[2], tabs)
                file.write('\n')
            if block.connected[1] is not None:
                self.into_file(file, block.connected[1], tabs)
        elif isinstance(block, ControlBlock):
            self.make_tabs(file, tabs)
            file.write(block.string)
            if block.connected[2] is not None:
                self.into_file(file, block.connected[2], tabs)
            file.write(': \n')
            if block.connected[1] is not None:
                self.into_file(file, block.connected[1], tabs+1)
            if block.connected[3].connected[1] is not None:
                self.into_file(file, block.connected[3].connected[1], tabs)
        elif isinstance(block, TypeBlock):
            file.write(block.string_on_block)
        elif isinstance(block, OneMagnetBlock):
            file.write(block.text)
            if block.connected[1] is not None:
                self.into_file(file, block.connected[1], tabs)
        else:
            print("error", block)

    def make_tabs(self, file, tabs):
        for i in range(0, tabs):
            file.write('    ')


class Block:
    def __init__(self, coords, canvas, poly_cords):
        self.coords = coords
        self.canvas = canvas
        self.poly_cords = poly_cords
        self.obj_id = None
        self.default_items_on_block = None
        self.default_items_id = []
        self.connected = [None]

    def get_closest(self, movable_blocks):
        magnet_x = movable_blocks[self.obj_id].renew_magnets()[0][0]
        magnet_y = movable_blocks[self.obj_id].renew_magnets()[0][1]
        # finds closest object to magnet
        closest_object = self.canvas.find_overlapping(magnet_x-10, magnet_y-10, magnet_x+10, magnet_y+10)
        closest_objects = list(closest_object)
        closest_objects.remove(self.obj_id)
        for el in self.default_items_id:
            if el in closest_objects:
                closest_objects.remove(el)
        # Blocks can't connect with InsideBlocks
        temp = []
        for elem in closest_objects:
            if isinstance(movable_blocks[elem], InsideBlock):
                temp.append(elem)
        for elem in temp:
            closest_objects.remove(elem)
        # if there is "line" in dictionary then deletes it
        if "line" in movable_blocks.values():
            self.line_delete(movable_blocks)
        return closest_objects

    def check_magnets_during_move(self, movable_blocks):
        # moves magnets also checks other blocks and marks them
        closest_object = self.get_closest(movable_blocks)
        if closest_object != [] and closest_object[0] in movable_blocks and movable_blocks[closest_object[0]] != "line":
            if movable_blocks[closest_object[0]] != 'bin':
                stable_instance = movable_blocks[closest_object[0]]
                stable_coords = stable_instance.renew_magnets()
                line_x = stable_coords[1][0]
                line_y = stable_coords[1][1]
                # draws "line" mark to the block
                line_id = self.canvas.create_line(line_x - 15, line_y - 5, line_x-10, line_y, line_x+5, line_y,
                                                  line_x + 10, line_y - 5, fill="green", width=3)
                movable_blocks[line_id] = "line"

    # deletes "line" mark
    def line_delete(self, movable_blocks):
        line_key = None
        for key in movable_blocks:
            if movable_blocks[key] == "line":
                self.canvas.delete(key)
                line_key = key
        if line_key is not None:
            del movable_blocks[line_key]

    def use_bin(self, movable_blocks):
        self.canvas.delete(self.obj_id)
        for el in self.default_items_id:
            self.canvas.delete(el)
        for i in self.connected[1:]:
            if i is not None:
                i.use_bin(movable_blocks)
        del movable_blocks[self.obj_id]

    def raise_tags(self):
        for el in self.default_items_id:
            self.canvas.tag_raise(el)
        if self.connected[2] is not None:
            self.connected[2].raise_tags()


class CommandBlock(Block):
    def __init__(self, coords, canvas, stableCanvas, poly_cords, color, outline):
        super().__init__(coords, canvas, poly_cords)
        # upper connection, lower connection, inside_poly connection
        self.connected = [None, None, None]
        self.color = color
        self.outline = outline
        self.stableCanvas = stableCanvas
        self.inside_poly_coords = [None, None, None, None]
        self.poly_id = None

    def create_polygon(self):
        self.obj_id = self.canvas.create_polygon(self.poly_cords, fill=self.color, outline=self.outline)
        return self.obj_id

    def renew_magnets(self):
        upper_magnet = [self.coords[0] + 35, self.coords[1] + 5]
        lower_magnet = [self.coords[0] + 35, self.coords[1] + self.coords[2] + 5]
        return [upper_magnet, lower_magnet]

    def change_coords(self, delta_x, delta_y):
        old_coords = self.coords
        self.coords = [old_coords[0] + delta_x, old_coords[1] + delta_y, old_coords[2], old_coords[3]]
        self.canvas.move(self.obj_id, delta_x, delta_y)
        self.renew_magnets()

    def move_connected(self, delta_x, delta_y):
        self.change_coords(delta_x, delta_y)
        if self.connected[1] is not None:
            self.connected[1].move_connected(delta_x, delta_y)
        if self.default_items_on_block is not None:
            self.default_items_on_block.change_inside_coords(delta_x, delta_y)
        if self.connected[2] is not None:
            self.connected[2].move_connected(delta_x, delta_y)
            for i in self.connected[2].default_items_id:
                self.canvas.tag_raise(i)

    def move_to_magnet(self, movable_blocks):
        # when mouse press is let go, puts the block in right place
        magnets = self.renew_magnets()
        magnet_x = magnets[0][0]
        magnet_y = magnets[0][1]
        closest_object = self.get_closest(movable_blocks)
        if closest_object:
            if movable_blocks[closest_object[0]] == 'bin':
                self.use_bin(movable_blocks)
            else:
                stable_instance = movable_blocks[closest_object[0]]
                stable_magnet = stable_instance.renew_magnets()
                delta_x = stable_magnet[1][0] - magnet_x
                delta_y = stable_magnet[1][1] - magnet_y
                self.move_connected(delta_x, delta_y)
                # if user wants to put a block between blocks
                if stable_instance.connected[1] is not None:
                    under_block = stable_instance.connected[1]
                    under_delta_y = self.get_height()
                    under_block.move_connected(0, under_delta_y)
                    last_connected = self.get_last_connection()
                    last_connected.connected[1] = under_block
                    under_block.connected[0] = last_connected
                self.connected[0] = stable_instance
                stable_instance.connected[1] = self
                self.check_control_block(movable_blocks)

    def get_last_connection(self):
        if self.connected[1] is None:
            return self
        else:
            return self.connected[1].get_last_connection()

    def disconnect_magnet(self, movable_blocks):
        self.connected[0].connected[1] = None
        self.check_control_block(movable_blocks)
        self.connected[0] = None

    def get_height(self):
        blo_height = self.coords[2]
        if self.connected[1] is not None:
            blo_height += self.connected[1].get_height()
        return blo_height

    def check_control_block(self, movable_blocks):
        if self.connected[0].connected[0] is not None:
            self.connected[0].check_control_block(movable_blocks)
        if isinstance(self.connected[0], ControlBlock):
            self.connected[0].redraw_length(movable_blocks)

    def redraw_base(self, movable_blocks):
        old_height = self.coords[2]
        if self.connected[2] is not None:
            blo_height = self.connected[2].get_height()
            self.coords[2] = blo_height + self.inside_poly_coords[2] - 4
            self.resize_coords(movable_blocks, old_height)
            blo_width = self.connected[2].get_width()
            self.coords[3] = blo_width + self.inside_poly_coords[3] + 25
        else:
            self.coords[2] = 30
            self.coords[3] = 120
            self.resize_coords(movable_blocks, old_height)
        self.change_poly_coords()
        del movable_blocks[self.obj_id]
        self.canvas.delete(self.obj_id)
        self.obj_id = self.create_polygon()
        movable_blocks[self.obj_id] = self
        if self.connected[2] is not None:
            self.raise_tags()
        else:
            for el in self.default_items_id:
                self.canvas.tag_raise(el)

    def resize_coords(self, movable_blocks, old_height):
        if self.connected[1] is not None:
            self.connected[1].move_connected(0, self.coords[2] - old_height)
        if self.connected[0] is not None:
            self.check_control_block(movable_blocks)

    def change_poly_coords(self):
        self.poly_cords = self.stableCanvas.command_block_coords(self.coords[0], self.coords[1],
                                                                 self.coords[2], self.coords[3])


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


class VariableBlock(CommandBlock):
    def __init__(self, coords, canvas, stableCanvas, poly_cords, color, outline, variable_name, len):
        super().__init__(coords, canvas, stableCanvas, poly_cords, color, outline)
        self.string = '='
        self.variable_name = variable_name
        self.variable_name_block_len = len
        self.variable_name_poly_id = None
        self.variable_name_id = None
        self.text_id = None
        self.poly_id = None
        self.variable_poly_coords = [self.coords[0] + 10, self.coords[1] + 9, 16, len]
        self.name_text_coords = [self.coords[0] + 20, self.coords[1] + 9]
        self.text_coords = [self.coords[0]+self.variable_name_block_len + 22, self.coords[1]+5]
        self.inside_poly_coords = [self.coords[0] + self.variable_name_block_len + 40, self.coords[1]+7, 16, 50]
        self.inside_color = 'light pink'
        self.variable_color = 'dodger blue'

    def create_polygon(self):
        self.coords[3] += self.variable_name_block_len
        self.poly_cords = self.stableCanvas.command_block_coords(self.coords[0], self.coords[1], self.coords[2],
                                                                 self.coords[3])
        self.obj_id = self.canvas.create_polygon(self.poly_cords, fill=self.color, outline=self.outline)
        return self.obj_id

    def create_variable_polygon(self):
        poly_coords = self.stableCanvas.inside_block_coords(self.coords[0] + 10, self.coords[1] + 9, 16, self.variable_name_block_len)
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
        poly_coords = self.stableCanvas.inside_block_coords(self.inside_poly_coords[0], self.inside_poly_coords[1],
                                                            self.inside_poly_coords[2], self.inside_poly_coords[3])
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
        self.inside_poly_coords = [old_poly_coords[0] + delta_x, old_poly_coords[1]+delta_y, old_poly_coords[2],
                                   old_poly_coords[3]]

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
        self.coords[3] = 110
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


class ListBlock(VariableBlock):
    def __init__(self, coords, canvas, stableCanvas, poly_cords, color, outline, variable_name, len):
        super().__init__(coords, canvas, stableCanvas, poly_cords, color, outline, variable_name, len)
        self.text2_id = None
        self.string = ' = ['
        self.string2 = '] '
        self.text2_coords = []
        self.inside_poly_coords = [self.coords[0] + self.variable_name_block_len + 50, self.coords[1]+7, 16, 50]

    def create_polygon(self):
        self.coords[3] += self.variable_name_block_len + 15
        self.poly_cords = self.stableCanvas.command_block_coords(self.coords[0], self.coords[1], self.coords[2],
                                                                 self.coords[3])
        self.obj_id = self.canvas.create_polygon(self.poly_cords, fill=self.color, outline=self.outline)
        return self.obj_id

    def create_text(self):
        self.text_coords = [self.coords[0] + self.variable_name_block_len + 17, self.coords[1] + 5]
        self.text_id = self.canvas.create_text(self.text_coords, anchor=NW, text=self.string, font='bold')
        self.default_items_on_block = self
        self.default_items_id.append(self.text_id)
        return self.text_id

    def create_text2(self):
        self.text2_coords = [self.coords[0] + self.coords[3] - 15, self.coords[1] + 5]
        self.text2_id = self.canvas.create_text(self.text2_coords, anchor=NW, text=self.string2, font='bold')
        self.default_items_on_block = self
        self.default_items_id.append(self.text2_id)
        return self.text2_id

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

        old_text2_coords = self.text2_coords
        self.text2_coords = [old_text2_coords[0] + delta_x, old_text2_coords[1] + delta_y]
        self.canvas.move(self.text2_id, delta_x, delta_y)

        old_poly_coords = self.inside_poly_coords
        self.inside_poly_coords = [old_poly_coords[0] + delta_x, old_poly_coords[1]+delta_y, old_poly_coords[2],
                                   old_poly_coords[3]]

        self.canvas.tag_raise(self.text_id)
        self.canvas.tag_raise(self.text2_id)
        self.canvas.tag_raise(self.variable_name_poly_id)
        self.canvas.tag_raise(self.variable_name_id)

        if self.connected[2] is None:
            self.canvas.tag_raise(self.poly_id)
            self.canvas.move(self.poly_id, delta_x, delta_y)

    def change_type_block(self, s, frame, times, movable_blocks):
        self.variable_name = s
        w = len(s) * times + 15
        delta_x = w - self.variable_name_block_len
        self.variable_name_block_len = w
        # changes CommandBlock size
        del movable_blocks[self.obj_id]
        self.canvas.delete(self.obj_id)
        self.coords[3] = 110
        self.create_polygon()
        movable_blocks[self.obj_id] = self
        # changes variable block size
        del movable_blocks[self.variable_name_poly_id]
        self.canvas.delete(self.variable_name_poly_id)
        self.create_variable_polygon()
        movable_blocks[self.variable_name_poly_id] = self
        # changes variable name
        self.canvas.itemconfig(self.variable_name_id, text=s)
        # changes '= [' position
        self.canvas.move(self.text_id, delta_x, 0)
        # changes ']' position
        self.canvas.move(self.text2_id, delta_x, 0)
        # changes inside block position
        self.canvas.move(self.poly_id, delta_x, 0)
        # raises texts and inside polygon
        self.canvas.tag_raise(self.text_id)
        self.canvas.tag_raise(self.text2_id)
        self.canvas.tag_raise(self.variable_name_id)
        self.canvas.tag_raise(self.poly_id)

        if frame is not None:
            self.canvas.delete(frame)


class ControlBlock(OneTextCommandBlock):
    def __init__(self, coords, canvas, stableCanvas, poly_cords, color, outline, string, inside_color):
        super().__init__(coords, canvas, stableCanvas, poly_cords, color, outline, string, inside_color)
        # upper connection, main lower connection, main inside connection, ControlBlockLower instance
        self.stableCanvas = stableCanvas
        self.connected = [None, None, None, None]
        self.color = color
        self.outline = outline
        self.inside_color = inside_color
        self.string = string
        self.empty_block_height = self.coords[4]
        self.text_coords = [self.coords[0]+20, self.coords[1]+10]
        self.inside_poly_coords = [self.coords[0]+40, self.coords[1]+7, 16, 50]

    def renew_magnets(self):
        upper_magnet = [self.coords[0] + 35, self.coords[1] + 5]
        lower_magnet = [self.coords[0] + 45, self.coords[1] + self.coords[2] + 5]
        return [upper_magnet, lower_magnet]

    def change_coords(self, delta_x, delta_y):
        old_coords = self.coords
        self.coords = [old_coords[0] + delta_x, old_coords[1] + delta_y, old_coords[2], old_coords[3], old_coords[4]]
        self.canvas.move(self.obj_id, delta_x, delta_y)
        self.renew_magnets()

    def move_connected(self, delta_x, delta_y):
        self.change_coords(delta_x, delta_y)
        self.connected[3].move_connected(delta_x, delta_y)
        if self.connected[1] is not None:
            self.connected[1].move_connected(delta_x, delta_y)
        if self.default_items_on_block is not None:
            self.default_items_on_block.change_inside_coords(delta_x, delta_y)
        if self.connected[2] is not None:
            self.connected[2].move_connected(delta_x, delta_y)
            for i in self.connected[2].default_items_id:
                self.canvas.tag_raise(i)

    def move_to_magnet(self, movable_blocks):
        # when mouse press is let go, puts the block in right place
        magnet_x = self.renew_magnets()[0][0]
        magnet_y = self.renew_magnets()[0][1]
        closest_object = self.get_closest(movable_blocks)
        if closest_object:
            if movable_blocks[closest_object[0]] == 'bin':
                self.use_bin(movable_blocks)
            else:
                stable_instance = movable_blocks[closest_object[0]]
                stable_magnet = stable_instance.renew_magnets()
                delta_x = stable_magnet[1][0] - magnet_x
                delta_y = stable_magnet[1][1] - magnet_y
                self.move_connected(delta_x, delta_y)
                if stable_instance.connected[1] is not None:
                    under_block = stable_instance.connected[1]
                    # Don't know why it needs 4 pixels, need to get real height somehow
                    under_delta_y = self.coords[2] + self.coords[4] + self.connected[3].coords[2] - 4
                    under_block.move_connected(0, under_delta_y)
                    self.connected[3].connected[1] = stable_instance.connected[1]
                    stable_instance.connected[1].connected[0] = self.connected[2]
                stable_instance.connected[1] = self
                self.connected[0] = stable_instance
                self.check_control_block(movable_blocks)

    def get_last_connection(self):
        if self.connected[1] is None:
            return self
        else:
            return self.connected[1].get_last_connection()

    def disconnect_magnet(self, movable_blocks):
        self.connected[0].connected[1] = None
        self.check_control_block(movable_blocks)
        self.connected[0] = None

    def get_height(self):
        blo_height = self.coords[2] + self.coords[4] + self.connected[3].get_height()
        if self.connected[0] is not None:
            return blo_height
        elif not isinstance(self.connected[1], ControlBlock):
            blo_height += self.connected[1].get_height()
        if not isinstance(self.connected[0], ControlBlock):
            self.connected[0].get_height()
        return blo_height

    def redraw_length(self, movable_blocks):
        old_height = self.coords[4]
        # if direct block from ControlBlock is disconnected
        if self.connected[1] is None:
            blo_height = self.empty_block_height
        # if something is connecting or something is not directly disconnecting from ControlBlock
        else:
            blo_height = self.connected[1].get_height()
        self.coords[4] = blo_height
        self.poly_cords = self.stableCanvas.control_block_coords(self.coords[0], self.coords[1],
                                                                 self.coords[2], self.coords[3], self.coords[4])[0]
        del movable_blocks[self.obj_id]
        self.canvas.delete(self.obj_id)
        self.obj_id = self.create_polygon()
        movable_blocks[self.obj_id] = self
        self.connected[3].move_connected(0, blo_height - old_height)
        if self.connected[0] is not None:
            self.check_control_block(movable_blocks)
        for i in self.default_items_id:
            self.canvas.tag_raise(i)
        if self.connected[2] is not None:
            self.connected[2].raise_tags()

    def check_control_block(self, movable_blocks):
        if self.connected[0].connected[0] is not None:
            self.connected[0].check_control_block(movable_blocks)
        if isinstance(self.connected[0], ControlBlock):
            self.connected[0].redraw_length(movable_blocks)

    def resize_coords(self, movable_blocks, old_height):
        if self.connected[1] is not None:
            self.connected[1].move_connected(0, self.coords[2] - old_height)
        delta = self.coords[2] - old_height
        self.coords[4] += delta
        self.connected[3].move_connected(0, delta)
        if self.connected[0] is not None:
            self.check_control_block(movable_blocks)

    def change_poly_coords(self):
        self.poly_cords = self.stableCanvas.control_block_coords(self.coords[0], self.coords[1],
                                                                 self.coords[2], self.coords[3], self.coords[4])[0]
        self.connected[3].poly_cords = self.stableCanvas.control_block_coords(self.coords[0], self.coords[1],
                                                                 self.coords[2], self.coords[3], self.coords[4])[1]


class ControlBlockLower(Block):
    def __init__(self, coords, canvas, poly_cords):
        super().__init__(coords, canvas, poly_cords)
        # ControlBlock, lower connection
        self.connected = [None, None]
        self.color = 'orange'
        self.outline = 'chocolate'

    def create_polygon(self):
        self.obj_id = self.canvas.create_polygon(self.poly_cords, fill=self.color, outline=self.outline)
        return self.obj_id

    def renew_magnets(self):
        upper_magnet = [self.coords[0] + 40, self.coords[1] + 5]
        lower_magnet = [self.coords[0] + 35, self.coords[1] + 25]
        return [upper_magnet, lower_magnet]

    def change_coords(self, delta_x, delta_y):
        old_coords = self.coords
        self.coords = [old_coords[0] + delta_x, old_coords[1] + delta_y, old_coords[2], old_coords[3], old_coords[4]]
        self.canvas.move(self.obj_id, delta_x, delta_y)
        self.renew_magnets()

    def move_connected(self, delta_x, delta_y):
        self.change_coords(delta_x, delta_y)
        if self.connected[1] is not None:
            self.connected[1].move_connected(delta_x, delta_y)

    def check_control_block(self, movable_blocks):
        if self.connected[0].connected[0] is not None:
            self.connected[0].check_control_block(movable_blocks)

    def get_height(self):
        blo_height = 25
        if self.connected[1] is not None:
            blo_height += self.connected[1].get_height()
        return blo_height


class InsideBlock:
    def __init__(self, coords, canvas, stableCanvas, poly_cords, color, outline):
        # inside the block
        self.default_items_id = []
        self.coords = coords
        self.canvas = canvas
        self.poly_cords = poly_cords
        # connection to "under" block
        self.connected = [None]
        self.color = color
        self.outline = outline
        self.obj_id = None
        self.default_items_on_block = None
        self.stableCanvas = stableCanvas

    def create_polygon(self):
        self.obj_id = self.canvas.create_polygon(self.poly_cords, fill=self.color, outline=self.outline)
        return self.obj_id

    def renew_magnets(self):
        magnet = [self.coords[0], self.coords[1] + 5]
        return magnet

    def change_coords(self, delta_x, delta_y):
        old_coords = self.coords
        self.coords = [old_coords[0] + delta_x, old_coords[1] + delta_y, old_coords[2], old_coords[3]]
        self.canvas.move(self.obj_id, delta_x, delta_y)
        self.renew_magnets()

    def get_closest(self, movable_blocks):
        magnet_x = movable_blocks[self.obj_id].renew_magnets()[0]
        magnet_y = movable_blocks[self.obj_id].renew_magnets()[1]
        # finds closest object to magnet
        closest_object = self.canvas.find_overlapping(magnet_x-5, magnet_y-5, magnet_x+5, magnet_y+5)
        closest_objects = list(closest_object)
        if self.obj_id in closest_objects:
            closest_objects.remove(self.obj_id)
        for el in self.default_items_id:
            if el in closest_objects:
                closest_objects.remove(el)
        # if there is "line" in dictionary then deletes it
        if "line" in movable_blocks.values():
            self.line_delete(movable_blocks)
        return closest_objects

    def check_magnets_during_move(self, movable_blocks):
        # moves magnets also checks other blocks and marks them
        closest_object = self.get_closest(movable_blocks)
        if closest_object != [] and movable_blocks[closest_object[0]] != "line":
            if movable_blocks[closest_object[0]] != 'bin':
                stable_instance = movable_blocks[closest_object[0]]
                if isinstance(stable_instance, TwoMagnetBlock):
                    first = self.canvas.find_withtag('first')
                    second = self.canvas.find_withtag('second')
                    magnet = None
                    for item in closest_object:
                        if item in first:
                            magnet = 'first'
                            break
                        elif item in second:
                            magnet = 'second'
                            break
                    if magnet is not None:
                        if magnet == 'first':
                            # gets poly_coords
                            stable_coords = stable_instance.inside_poly_coords
                        elif magnet == 'second':
                            # gets poly_coords
                            stable_coords = stable_instance.second_poly_coords
                        line_coords = self.stableCanvas.inside_block_coords(stable_coords[0], stable_coords[1],
                                                                            stable_coords[2], stable_coords[3])
                        # draws "line" mark to the block
                        line_id = self.canvas.create_line(line_coords, fill="green", width=3)
                        movable_blocks[line_id] = "line"
                elif ((isinstance(stable_instance, CommandBlock) or isinstance(stable_instance, ControlBlock))
                    and stable_instance.connected[2] is None) or \
                    (isinstance(stable_instance, OneMagnetBlock) and stable_instance.connected[1] is None):
                    # gets poly_coords
                    stable_coords = stable_instance.inside_poly_coords
                    line_coords = self.stableCanvas.inside_block_coords(stable_coords[0], stable_coords[1],
                                                                    stable_coords[2], stable_coords[3])
                    # draws "line" mark to the block
                    line_id = self.canvas.create_line(line_coords, fill="green", width=3)
                    movable_blocks[line_id] = "line"

    # deletes "line" mark
    def line_delete(self, movable_blocks):
        line_key = None
        for key in movable_blocks:
            if movable_blocks[key] == "line":
                self.canvas.delete(key)
                line_key = key
        if line_key is not None:
            del movable_blocks[line_key]

    def use_bin(self, movable_blocks):
        self.canvas.delete(self.obj_id)
        for el in self.default_items_id:
            self.canvas.delete(el)
        for i in self.connected[1:]:
            if i is not None:
                i.use_bin(movable_blocks)
        del movable_blocks[self.obj_id]

    def move_to_magnet(self, movable_blocks):
        # when mouse press is let go, puts the block in right place
        magnet_x = self.renew_magnets()[0]
        magnet_y = self.renew_magnets()[1]

        closest_object = self.get_closest(movable_blocks)
        if closest_object:
            if movable_blocks[closest_object[0]] == 'bin':
                self.use_bin(movable_blocks)
            else:
                stable_instance = movable_blocks[closest_object[0]]
                if ((isinstance(stable_instance, CommandBlock) or isinstance(stable_instance, ControlBlock))
                    and stable_instance.connected[2] is None) or \
                        (isinstance(stable_instance, OneMagnetBlock) and stable_instance.connected[1] is None):
                    stable_magnet = [stable_instance.inside_poly_coords[0], stable_instance.inside_poly_coords[1]+5]
                    stable_instance.delete_inside_poly(movable_blocks)
                    delta_x = stable_magnet[0] - magnet_x
                    delta_y = stable_magnet[1] - magnet_y
                    self.move_connected(delta_x, delta_y)
                    self.connected[0] = stable_instance
                    if isinstance(stable_instance, TwoMagnetBlock):
                        pass
                    elif isinstance(stable_instance, OneMagnetBlock):
                        stable_instance.connected[1] = self
                        stable_instance.coords_connected(movable_blocks)
                    elif isinstance(stable_instance, CommandBlock):
                        stable_instance.connected[2] = self
                        stable_instance.redraw_base(movable_blocks)

    def disconnect_magnet(self, movable_blocks):
        if isinstance(self.connected[0], CommandBlock):
            self.connected[0].connected[2] = None
            poly_id = self.connected[0].create_inside_polygon()
            self.connected[0].redraw_base(movable_blocks)
        elif isinstance(self.connected[0], OneMagnetBlock):
            self.connected[0].connected[1] = None
            poly_id = self.connected[0].create_first_polygon()
            self.connected[0].coords_disconnected(movable_blocks)
        movable_blocks[poly_id] = self.connected[0]
        self.connected[0] = None

    def move_connected(self, delta_x, delta_y):
        self.change_coords(delta_x, delta_y)
        if self.connected[0] is not None:
            self.connected[0].move_connected()

    def get_width(self):
        return self.coords[3]

    def get_height(self):
        return self.coords[2] + 4

    def raise_tags(self):
        self.canvas.tag_raise(self.obj_id)
        for el in self.default_items_id:
            self.canvas.tag_raise(el)


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
        self.poly_cords = self.stableCanvas.inside_block_coords(self.coords[0], self.coords[1], 16, w)
        del movable_blocks[self.obj_id]
        self.canvas.delete(self.obj_id)
        self.obj_id = self.create_polygon()
        movable_blocks[self.obj_id] = self
        self.canvas.itemconfig(self.text_id, text=s)
        self.canvas.tag_raise(self.text_id)
        if frame is not None:
            self.canvas.delete(frame)


class OneMagnetBlock(InsideBlock):
    def __init__(self, coords, canvas, stableCanvas, poly_cords, text, text_len, color, outline, inside_color):
        super().__init__(coords, canvas, stableCanvas, poly_cords, color, outline)
        self.text = text
        # connection to "under" block, first inside block
        self.connected = [None, None]

        self.obj_id = None
        self.first_poly_id = None
        self.text_id = None
        self.inside_color = inside_color

        # inside the block
        self.default_items_id = []
        self.default_items_on_block = None

        self.first_inside_length = 40
        self.first_inside_height = 16
        self.block_length = self.coords[2]
        self.block_height = self.coords[3]
        self.text_len = text_len
        self.inside_poly_coords = [self.text_len + 30, self.coords[1] + 2, self.first_inside_height, self.first_inside_length]
        self.text_coords = [self.coords[0] + 15, self.coords[1]+2]

    def create_text(self):
        self.text_id = self.canvas.create_text(self.text_coords, anchor=NW, text=self.text)
        self.default_items_on_block = self
        self.default_items_id.append(self.text_id)
        return self.text_id

    def create_first_polygon(self):
        poly_coords = self.stableCanvas.inside_block_coords(self.inside_poly_coords[0], self.inside_poly_coords[1],
                                                            self.inside_poly_coords[2], self.inside_poly_coords[3])
        self.first_poly_id = self.canvas.create_polygon(poly_coords, fill=self.inside_color)
        self.default_items_on_block = self
        self.default_items_id.append(self.first_poly_id)
        return self.first_poly_id

    def move_connected(self, delta_x, delta_y):
        self.change_coords(delta_x, delta_y)
        if self.default_items_on_block is not None:
            self.default_items_on_block.change_inside_coords(delta_x, delta_y)
        if self.connected[1] is not None:
            self.connected[1].move_connected(delta_x, delta_y)
            for i in self.connected[1].default_items_id:
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

        self.canvas.tag_raise(self.obj_id)
        # leaves the text on top always
        self.canvas.tag_raise(self.text_id)

        if self.connected[1] is None:
            self.canvas.tag_raise(self.first_poly_id)
            self.canvas.move(self.first_poly_id, delta_x, delta_y)

    def delete_inside_poly(self, movable_blocks):
        if self.first_poly_id:
            del movable_blocks[self.first_poly_id]
            self.canvas.delete(self.first_poly_id)
            self.default_items_id.remove(self.first_poly_id)
            self.first_poly_id = None

    def redraw_base(self, movable_blocks):
        self.poly_cords = self.stableCanvas.inside_block_coords(self.coords[0], self.coords[1], self.coords[2],
                                                                self.coords[3])
        del movable_blocks[self.obj_id]
        self.canvas.delete(self.obj_id)
        self.obj_id = self.create_polygon()
        movable_blocks[self.obj_id] = self
        if self.connected[1] is not None:
            self.raise_tags()
        else:
            for el in self.default_items_id:
                self.canvas.tag_raise(el)

    def coords_connected(self, movable_blocks):
        if self.connected[1] is not None:
            self.coords[2] = self.connected[1].get_height()
            blo_width = self.connected[1].get_width()
            self.coords[3] = blo_width + self.inside_poly_coords[3] + 10
        self.redraw_base(movable_blocks)

    def coords_disconnected(self, movable_blocks):
        if self.connected[1] is not None:
            self.coords[2] = self.connected[1].get_height()
            blo_width = self.connected[1].get_width()
            self.coords[3] = blo_width + self.inside_poly_coords[3] + 10
        else:
            self.coords[2] = 20
            self.coords[3] = 90
        if self.connected[0] is not None:
            if isinstance(self.connected[0], CommandBlock):
                self.connected[0].redraw_base(movable_blocks)
            else:
                self.connected[0].coords_disconnected(movable_blocks)
        self.redraw_base(movable_blocks)

    def raise_tags(self):
        self.canvas.tag_raise(self.obj_id)
        for el in self.default_items_id:
            self.canvas.tag_raise(el)
        if self.connected[1] is not None:
            self.connected[1].raise_tags()

    def get_height(self):
        blo_height = self.coords[2]
        if self.connected[1] is not None:
            blo_height = 4 + self.connected[1].get_height()
        else:
            blo_height += 4
        return blo_height


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
                                   self.first_inside_height, self.first_inside_length]
        first_poly_coords = self.stableCanvas.inside_block_coords(self.coords[0] + 10, self.coords[1]+2,
                                                                  self.first_inside_height, self.first_inside_length)
        self.first_poly_id = self.canvas.create_polygon(first_poly_coords, fill=self.inside_color, tag='first')
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
                                   self.coords[1] + 2, self.second_inside_height, self.second_inside_length]
        second_poly_coords = self.stableCanvas.inside_block_coords(
            self.coords[0] + 10 + self.first_inside_length + 10 + self.text_len + 10,
            self.coords[1] + 2, self.second_inside_height, self.second_inside_length)
        self.second_poly_id = self.canvas.create_polygon(second_poly_coords, fill=self.inside_color, tag='second')
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

    def redraw_base(self, movable_blocks):
        pass

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

    def raise_tags(self):
        self.canvas.tag_raise(self.obj_id)
        for el in self.default_items_id:
            self.canvas.tag_raise(el)
        if self.connected[1] is not None:
            self.connected[1].raise_tags()
        if self.connected[2] is not None:
            self.connected[2].raise_tags()
