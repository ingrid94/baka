from tkinter import *
import tkinter.messagebox


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
                line_id = self.canvas.create_line(line_x - 15, line_y - 5, line_x-10, line_y,
                                              line_x+5, line_y, line_x + 10, line_y - 5,
                                              fill="green", width=3)
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
        for i in self.connected:
            if i is not None:
                if self.connected[0] is not None:
                    pass
                else:
                    i.use_bin(movable_blocks)
        del movable_blocks[self.obj_id]


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
        lower_magnet = [self.coords[0] + 35, self.coords[1] + 35]
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
        old_width = self.coords[3]
        if self.connected[2] is not None:
            blo_width = self.connected[2].get_width()
            other_width = old_width - self.inside_poly_coords[3]
            self.coords[3] = other_width + blo_width
        else:
            self.coords[3] = 120
        self.poly_cords = self.stableCanvas.command_block_coords(self.coords[0], self.coords[1],
                                                                 self.coords[2], self.coords[3])
        del movable_blocks[self.obj_id]
        self.canvas.delete(self.obj_id)
        self.obj_id = self.create_polygon()
        movable_blocks[self.obj_id] = self
        if self.connected[2] is not None:
            self.raise_tags(self.connected[2])
        else:
            for el in self.default_items_id:
                self.canvas.tag_raise(el)

    def raise_tags(self, item):
        for el in self.default_items_id:
            self.canvas.tag_raise(el)
        inside_id = item.obj_id
        self.canvas.tag_raise(inside_id)
        item.raise_tags()


class ControlBlock(Block):
    def __init__(self, coords, canvas, stable_canvas, poly_cords):
        super().__init__(coords, canvas, poly_cords)
        # upper connection, main lower connection,  ControlBlockLower instance, main inside connection
        self.connected = [None, None, None, None]
        self.color = 'orange'
        self.outline = 'chocolate'
        self.stableCanvas = stable_canvas
        self.default_items_on_block = None
        self.empty_block_height = self.coords[3]

    def create_polygon(self):
        self.obj_id = self.canvas.create_polygon(self.poly_cords, fill=self.color, outline=self.outline)
        return self.obj_id

    def renew_magnets(self):
        upper_magnet = [self.coords[0] + 35, self.coords[1] + 5]
        lower_magnet = [self.coords[0] + 45, self.coords[1] + 35]
        return [upper_magnet, lower_magnet]

    def change_coords(self, delta_x, delta_y):
        old_coords = self.coords
        self.coords = [old_coords[0] + delta_x, old_coords[1] + delta_y, old_coords[2], old_coords[3]]
        self.canvas.move(self.obj_id, delta_x, delta_y)
        self.renew_magnets()

    def move_connected(self, delta_x, delta_y):
        self.change_coords(delta_x, delta_y)
        self.connected[2].move_connected(delta_x, delta_y)
        if self.connected[1] is not None:
            self.connected[1].move_connected(delta_x, delta_y)

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
                    under_delta_y = self.coords[2] + self.coords[3] + self.connected[2].coords[2] - 4
                    under_block.move_connected(0, under_delta_y)
                    self.connected[2].connected[1] = stable_instance.connected[1]
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
        blo_height = self.coords[2] + self.coords[3] + self.connected[2].get_height()
        if self.connected[0] is not None:
            return blo_height
        elif not isinstance(self.connected[1], ControlBlock):
            blo_height += self.connected[1].get_height()
        if not isinstance(self.connected[0], ControlBlock):
            self.connected[0].get_height()
        return blo_height

    def redraw_length(self, movable_blocks):
        old_height = self.coords[3]
        # if direct block from ControlBlock is disconnected
        if self.connected[1] is None:
            blo_height = self.empty_block_height
        # if something is connecting or something is not directly disconnecting from ControlBlock
        else:
            blo_height = self.connected[1].get_height()
        self.coords[3] = blo_height
        self.poly_cords = self.stableCanvas.control_block_coords(self.coords[0], self.coords[1],
                                                                 self.coords[2], self.coords[3])[0]
        del movable_blocks[self.obj_id]
        self.canvas.delete(self.obj_id)
        self.obj_id = self.create_polygon()
        movable_blocks[self.obj_id] = self
        self.connected[2].move_connected(0, blo_height - old_height)
        if self.connected[0] is not None:
            self.check_control_block(movable_blocks)

    def check_control_block(self, movable_blocks):
        if self.connected[0].connected[0] is not None:
            self.connected[0].check_control_block(movable_blocks)
        if isinstance(self.connected[0], ControlBlock):
            self.connected[0].redraw_length(movable_blocks)


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
        self.coords = [old_coords[0] + delta_x, old_coords[1] + delta_y, old_coords[2], old_coords[3]]
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
                # When ControlBlock has inside_poly, remove the first condition
                if (isinstance(stable_instance, CommandBlock) and stable_instance.connected[2] is None) or \
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
        for i in self.connected:
            if i is not None:
                if self.connected[0] is not None:
                    pass
                else:
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
                if (isinstance(stable_instance, CommandBlock) and stable_instance.connected[2] is None) or \
                    (isinstance(stable_instance, OneMagnetBlock) and stable_instance.connected[1] is None):
                    stable_magnet = [stable_instance.inside_poly_coords[0], stable_instance.inside_poly_coords[1]+5]
                    stable_instance.delete_inside_poly(movable_blocks)
                    delta_x = stable_magnet[0] - magnet_x
                    delta_y = stable_magnet[1] - magnet_y
                    self.move_connected(delta_x, delta_y)
                    self.connected[0] = stable_instance
                    if isinstance(stable_instance, OneMagnetBlock):
                        stable_instance.connected[1] = self
                    elif isinstance(stable_instance, CommandBlock):
                        stable_instance.connected[2] = self
                    stable_instance.redraw_base(movable_blocks)

    def disconnect_magnet(self, movable_blocks):
        if isinstance(self.connected[0], CommandBlock):
            self.connected[0].connected[2] = None
            poly_id = self.connected[0].create_inside_polygon()
        elif isinstance(self.connected[0], OneMagnetBlock):
            self.connected[0].connected[1] = None
            poly_id = self.connected[0].create_first_polygon()
        movable_blocks[poly_id] = self.connected[0]
        self.connected[0].redraw_base(movable_blocks)
        self.connected[0] = None

    def move_connected(self, delta_x, delta_y):
        self.change_coords(delta_x, delta_y)
        if self.connected[0] is not None:
            self.connected[0].move_connected()

    def get_width(self):
        return self.coords[3]

    def raise_tags(self):
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
        old_width = self.coords[3]
        if self.connected[1] is not None:
            blo_width = self.connected[1].get_width()
            other_width = old_width - self.inside_poly_coords[3]
            self.coords[3] = other_width + blo_width
        else:
            self.coords[3] = 90
        self.poly_cords = self.stableCanvas.inside_block_coords(self.coords[0], self.coords[1], self.coords[2],
                                                                self.coords[3])
        del movable_blocks[self.obj_id]
        self.canvas.delete(self.obj_id)
        self.obj_id = self.create_polygon()
        movable_blocks[self.obj_id] = self
        if self.connected[1] is not None:
            self.raise_tags_item(self.connected[1])
        else:
            for el in self.default_items_id:
                self.canvas.tag_raise(el)

    def raise_tags_item(self, item):
        for el in self.default_items_id:
            self.canvas.tag_raise(el)
        inside_id = item.obj_id
        self.canvas.tag_raise(inside_id)
        item.raise_tags()

