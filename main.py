from tkinter import *
import tkinter.messagebox
import re


class Block:
    def __init__(self, coords, canvas, poly_cords):
        self.coords = coords
        self.canvas = canvas
        self.poly_cords = poly_cords
        self.obj_id = None
        self.default_items_on_block = None
        self.default_items_id = []

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
        # if there is "line" in dictionary then deletes it
        if "line" in movable_blocks.values():
            self.line_delete(movable_blocks)
        return closest_objects

    def check_magnets_during_move(self, movable_blocks):
        # moves magnets also checks other blocks and marks them
        closest_object = self.get_closest(movable_blocks)
        if closest_object != [] and movable_blocks[closest_object[0]] != "line":
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
        #elif "line" in movable_blocks.values():
        #    self.line_delete(movable_blocks)

    # deletes "line" mark
    def line_delete(self, movable_blocks):
        line_key = None
        for key in movable_blocks:
            if movable_blocks[key] == "line":
                self.canvas.delete(key)
                line_key = key
        if line_key is not None:
            del movable_blocks[line_key]


class ControlBlock(Block):
    def __init__(self, coords, canvas, stable_canvas, poly_cords):
        super().__init__(coords, canvas, poly_cords)
        # upper connection, main lower connection,  the most lower connection, main inside connection
        self.connected = [None, None, None, None]
        self.color = 'orange'
        self.outline = 'chocolate'
        self.stableCanvas = stable_canvas
        self.default_items_on_block = None

    def create_polygon(self):
        self.obj_id = self.canvas.create_polygon(self.poly_cords, fill=self.color, outline=self.outline)
        return self.obj_id

    def renew_magnets(self):
        upper_magnet = [self.coords[0] + 40, self.coords[1] + 5]
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
            stable_instance = movable_blocks[closest_object[0]]
            stable_magnet = stable_instance.renew_magnets()
            delta_x = stable_magnet[1][0] - magnet_x
            delta_y = stable_magnet[1][1] - magnet_y
            self.move_connected(delta_x, delta_y)
            stable_instance.connected[1] = self
            self.connected[0] = stable_instance
            self.check_control_block(movable_blocks)

    def disconnect_magnet(self):
        self.connected[0].connected[1] = None
        self.connected[0] = None

    def get_length(self):
        blo_len = self.coords[2] + self.coords[3] + self.connected[2].get_length()
        if self.connected[0] is not None:
            return blo_len
        elif not isinstance(self.connected[1], ControlBlock):
            blo_len += self.connected[1].get_length()
        if not isinstance(self.connected[0], ControlBlock):
            self.connected[0].get_length()
        return blo_len

    def redraw(self, movable_blocks):
        blo_len = self.connected[1].get_length()
        old_length = self.coords[3]
        self.coords[3] = blo_len
        self.poly_cords = self.stableCanvas.control_block_coords(self.coords[0], self.coords[1],
                                                                 self.coords[2], blo_len)[0]
        del movable_blocks[self.obj_id]
        self.canvas.delete(self.obj_id)
        self.obj_id = self.create_polygon()
        movable_blocks[self.obj_id] = self
        self.connected[2].move_connected(0, blo_len - old_length)
        if self.connected[0] is not None:
            self.check_control_block(movable_blocks)

    def check_control_block(self, movable_blocks):
        if self.connected[0].connected[0] is not None:
            self.connected[0].check_control_block(movable_blocks)
        if isinstance(self.connected[0], ControlBlock):
            self.connected[0].redraw(movable_blocks)


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
        lower_magnet = [self.coords[0] + 40, self.coords[1] + 25]
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

    def get_length(self):
        blo_len = 25
        if self.connected[1] is not None:
            blo_len += self.connected[1].get_length()
        return blo_len


class CommandBlock(Block):
    def __init__(self, coords, canvas, poly_cords):
        super().__init__(coords, canvas, poly_cords)
        # upper connection, lower connection
        self.connected = [None, None]
        self.color = 'violet red'
        self.outline = 'purple'

    def create_polygon(self):
        self.obj_id = self.canvas.create_polygon(self.poly_cords, fill=self.color, outline=self.outline)
        return self.obj_id

    def renew_magnets(self):
        upper_magnet = [self.coords[0] + 35, self.coords[1] + 5]
        lower_magnet = [self.coords[0] + 35, self.coords[1] + 35]
        return [upper_magnet, lower_magnet]

    def change_coords(self, delta_x, delta_y):
        old_coords = self.coords
        self.coords = [old_coords[0] + delta_x, old_coords[1] + delta_y, old_coords[2]]
        self.canvas.move(self.obj_id, delta_x, delta_y)
        self.renew_magnets()

    def move_connected(self, delta_x, delta_y):
        self.change_coords(delta_x, delta_y)
        if self.connected[1] is not None:
            self.connected[1].move_connected(delta_x, delta_y)
        if self.default_items_on_block is not None:
            self.default_items_on_block.change_inside_coords(delta_x, delta_y)

    def move_to_magnet(self, movable_blocks):
        # when mouse press is let go, puts the block in right place
        magnet_x = self.renew_magnets()[0][0]
        magnet_y = self.renew_magnets()[0][1]
        closest_object = self.get_closest(movable_blocks)
        if closest_object:
            stable_instance = movable_blocks[closest_object[0]]
            stable_magnet = stable_instance.renew_magnets()
            delta_x = stable_magnet[1][0] - magnet_x
            delta_y = stable_magnet[1][1] - magnet_y
            self.move_connected(delta_x, delta_y)
            stable_instance.connected[1] = self
            self.connected[0] = stable_instance
            self.check_control_block(movable_blocks)

    def disconnect_magnet(self):
        self.connected[0].connected[1] = None
        self.connected[0] = None

    def get_length(self):
        blo_len = self.coords[2]
        if self.connected[1] is not None:
            blo_len += self.connected[1].get_length()
        return blo_len

    def check_control_block(self, movable_blocks):
        if self.connected[0].connected[0] is not None:
            self.connected[0].check_control_block(movable_blocks)
        if isinstance(self.connected[0], ControlBlock):
            self.connected[0].redraw(movable_blocks)
            # self.canvas.tag_raise(self.obj_id)


class ReturnBlock(CommandBlock):
    def __init__(self, coords, canvas, poly_cords, inside_poly_coords, text_coords):
        super().__init__(coords, canvas, poly_cords)
        self.string = 'return'
        self.text_id = None
        self.poly_id = None
        self.text_coords = text_coords
        self.inside_magnet_coords = None
        self.inside_poly_coords = inside_poly_coords
        self.inside_color = 'light pink'

    def create_text(self):
        self.text_id = self.canvas.create_text(self.text_coords, anchor=NW, text=self.string)
        self.default_items_on_block = self
        self.default_items_id.append(self.text_id)
        return self.text_id

    def create_inside_polygon(self):
        self.poly_id = self.canvas.create_polygon(self.inside_poly_coords, fill=self.inside_color)
        self.default_items_id.append(self.poly_id)
        return self.poly_id

    def change_inside_coords(self, delta_x, delta_y):
        old_text_coords = self.text_coords
        self.text_coords = [old_text_coords[0] + delta_x, old_text_coords[1] + delta_y]
        self.canvas.move(self.text_id, delta_x, delta_y)
        old_poly_coords = self.inside_poly_coords
        self.inside_poly_coords = [old_poly_coords[0] + delta_x, old_poly_coords[1]+delta_y, old_poly_coords[2], old_poly_coords[3]]
        self.canvas.move(self.poly_id, delta_x, delta_y)
        self.canvas.tag_raise(self.text_id)
        self.canvas.tag_raise(self.poly_id)
        # self.canvas.move_connected(self.obj_id, delta_x, delta_y)


class InsideBlock:
    def __init__(self, coords, canvas, poly_cords, color, outline):
        # inside the block
        self.coords = coords
        self.canvas = canvas
        self.poly_cords = poly_cords
        self.connected = []
        self.connected_to_bigger_block = None
        self.color = color
        self.outline = outline
        self.obj_id = None
        self.default_items_on_block = None

    def create_polygon(self):
        self.obj_id = self.canvas.create_polygon(self.poly_cords, fill=self.color, outline=self.outline)
        return self.obj_id

    def renew_magnet(self):
        magnet = [self.coords[0], self.coords[1] + 5]
        return magnet

    def change_coords(self, delta_x, delta_y):
        old_coords = self.coords
        self.coords = [old_coords[0] + delta_x, old_coords[1] + delta_y]
        self.canvas.move(self.obj_id, delta_x, delta_y)
        self.renew_magnet()

    def move_to_magnet(self, movable_blocks):
        # when mouse press is let go, puts the block in right place
        magnet_x = self.renew_magnet()[0]
        magnet_y = self.renew_magnet()[1]

    #    closest_object = self.get_closest(movable_blocks)
    #    if closest_object[0] != self.obj_id:
    #        stable_instance = movable_blocks[closest_object[0]]
    #        stable_magnet = stable_instance.renew_magnets()
    #        delta_x = stable_magnet[1][0] - magnet_x
    #        delta_y = stable_magnet[1][1] - magnet_y
    #        self.move_connected(delta_x, delta_y)
    #        stable_instance.connected[1] = self
    #        self.connected[0] = stable_instance

    def disconnect_magnet(self):
        self.connected_to_bigger_block = None


class FunctionBlock(InsideBlock):
    def __init__(self, coords, canvas, poly_cords, color, outline):
        super().__init__(coords, canvas, poly_cords, color, outline)
        # upper connection, lower connection
        self.connected = []

    def move_connected(self, delta_x, delta_y):
        self.change_coords(delta_x, delta_y)
        if self.connected:
            for i in self.connected:
                i.move_connected(delta_x, delta_y)


class TypeBlock(InsideBlock):
    def __init__(self, coords, canvas, stableCanvas, poly_cords, color, outline, string, inside_type):
        super().__init__(coords, canvas, poly_cords, color, outline)
        self.string_on_block = string
        self.text_id = None
        self.text_coords = [self.coords[0] + 12, self.coords[1] + 1]
        self.inside_type = inside_type
        self.stableCanvas = stableCanvas
        self.connected = [None]

    def create_text(self):
        self.text_id = self.canvas.create_text(self.text_coords, anchor=NW, text=self.string_on_block)
        return self.text_id

    def move_connected(self, delta_x, delta_y):
        self.change_coords(delta_x, delta_y)
        # moves text
        old_text_coords = self.text_coords
        self.text_coords = [old_text_coords[0] + delta_x, old_text_coords[1] + delta_y]
        self.canvas.move(self.text_id, delta_x, delta_y)
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
            else:
                tkinter.messagebox.showerror("Error", "It's not a number. Try again. ")
        elif inside_type == 'string':
            p = re.match(r'^(\"|\')(.)*(\"|\')$', s, re.S)
            if p:
                self.change_type_block(s, frame, 6, movable_blocks)
            else:
                tkinter.messagebox.showerror("Error", "It's not a string. Try again. ")
        elif inside_type == 'variable':
            p = re.match(r'^[a-zA-Z_][\w0-9_]*$', s, re.S)
            if p:
                self.change_type_block(s, frame, 6.5, movable_blocks)
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


class ChooseBlocksCanvas:
    def __init__(self, root):
        self.top = Toplevel(root)
        self.canvas = Canvas(self.top, width=500, height=500, bg="white", highlightthickness=0)
        self.canvas.pack()

    def get_focus_set(self):
        return self.canvas.focus_set()

    def gettags(self, int):
        return self.canvas.gettags(int)

    @staticmethod
    def command_block_coords(x, y, h, w):
        points = [x, y + 5, x + 5, y,
                  x + 20, y, x + 25, y + 5,
                  x + 40, y + 5, x + 45, y,
                  x + w - 5, y, x + w, y + 5,
                  x + w, y + h - 5, x + w - 5, y + h,
                  x + 45, y + h, x + 40, y + h + 5,
                  x + 25, y + h + 5, x + 20, y + h,
                  x + 5, y + h, x, y + h - 5,
                  x, y + 5]
        return points

    @staticmethod
    # x,y are upper left side corner coordinates, z is height of main block,
    # w is length of commands (when condition true) and lower block part to connect with other blocks
    def control_block_coords(x, y, z, w):
        points = [x, y + 5, x + 5, y,
                  x + 20, y, x + 25, y + 5,
                  x + 40, y + 5, x + 45, y,
                  x + 175, y, x + 180, y + 5,
                  x + 180, y + z - 5, x + 175, y + z,
                  x + 55, y + z, x + 50, y + z + 5,
                  x + 35, y + z + 5, x + 30, y + z,
                  x + 15, y + z, x + 10, y + z + 5,
                  x + 10, y + w + 35,
                  x, y + w + 35, x, y + 5]
        points_lower = [x + 10, y + w + 35, x + 15, y + w + 40,
                        x + 85, y + w + 40, x + 90, y + w + 45,
                        x + 90, y + w + 50,
                        x + 85, y + w + 55, x + 45, y + w + 55,
                        x + 40, y + w + 60, x + 25, y + w + 60,
                        x + 20, y + w + 55, x + 5, y + w + 55,
                        x, y + w + 50, x, y + w + 35]
        return [points, points_lower]

    @staticmethod
    def inside_block_coords(x, y, w, h):
        a = (h / 2)
        points = [x, y + a, x + a, y,
                  x + w, y, x + w + a, y + a,
                  x + w, y + h, x + a, y + h,
                  x, y + a]
        return points

    @staticmethod
    def type_block_coords(x, y, w, h):
        points = [x, y,
                  x + w, y,
                  x + w, y + h,
                  x, y + h,
                  x, y]
        return points

    def create_blocks_fst(self):
        self.canvas.create_polygon(self.command_block_coords(50, 20, 30, 120), fill='violet red', outline='purple',
                                   tags='print_block')
        self.canvas.create_text(60, 30, anchor=NW, text='print(', tags='print_block')
        self.canvas.create_polygon(self.inside_block_coords(97, 30, 40, 15), fill='light pink', tags='print_block')
        self.canvas.create_text(150, 30, anchor=NW, text=')', tags='print_block')

        self.canvas.create_polygon(self.command_block_coords(50, 60, 30, 120), fill='violet red', outline='purple',
                                   tags='return_block')
        self.canvas.create_text(60, 70, anchor=NW, text='return', tags='return_block')
        self.canvas.create_polygon(self.inside_block_coords(105, 70, 40, 15), fill='light pink', tags='return_block')

        self.canvas.create_polygon(self.inside_block_coords(50, 110, 130, 20), fill='dodger blue', outline='steel blue',
                                   tags='inside_block')
        # self.canvas.create_polygon(self.inside_block_coords(50, 250, 65, 20), fill='limegreen', outline='green')
        self.canvas.create_polygon(self.control_block_coords(50, 150, 30, 35)[0], fill='orange', outline='chocolate',
                                   tags='control_block')
        self.canvas.create_polygon(self.control_block_coords(50, 150, 30, 35)[1], fill='orange', outline='chocolate',
                                   tags='control_block')

        self.canvas.create_polygon(self.inside_block_coords(50, 260, 63, 15), fill='limegreen', outline='green',
                                   tags='variable')
        self.canvas.create_text(62, 260, anchor=NW, text="variable", tags='variable')

        self.canvas.create_polygon(self.inside_block_coords(50, 290, 63, 15), fill='limegreen', outline='green',
                                   tags='number')
        self.canvas.create_text(62, 290, anchor=NW, text="number", tags='number')

        self.canvas.create_polygon(self.inside_block_coords(50, 320, 63, 15), fill='limegreen', outline='green',
                                   tags='string')
        self.canvas.create_text(65, 320, anchor=NW, text="string", tags='string')

        self.canvas.create_polygon(self.inside_block_coords(50, 350, 63, 15), fill='limegreen', outline='green',
                                   tags='none')
        self.canvas.create_text(65, 350, anchor=NW, text="None", tags='none')

        self.canvas.create_polygon(self.inside_block_coords(50, 380, 63, 15), fill='limegreen', outline='green',
                                   tags='true')
        self.canvas.create_text(65, 380, anchor=NW, text="True", tags='true')

        self.canvas.create_polygon(self.inside_block_coords(50, 410, 63, 15), fill='limegreen', outline='green',
                                   tags='false')
        self.canvas.create_text(65, 410, anchor=NW, text="False", tags='false')

    def bind(self, function):
        self.canvas.bind("<ButtonPress-1>", function)


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
                assign_block = CommandBlock([0, 0, 30, 120], self.canvas, cords)
                obj_id = assign_block.create_polygon()
                self.movable_blocks[obj_id] = assign_block
            elif tag == 'return_block':
                cords = self.stableCanvas.command_block_coords(0, 0, 30, 120)
                inside_poly_coords = self.stableCanvas.inside_block_coords(52, 10, 40, 15)
                text_coords = [7, 10]
                assign_block = ReturnBlock([0, 0, 30, 120], self.canvas, cords, inside_poly_coords, text_coords)
                obj_id = assign_block.create_polygon()
                poly_id = assign_block.create_inside_polygon()
                text_id = assign_block.create_text()
                self.movable_blocks[obj_id] = assign_block
                self.movable_blocks[poly_id] = assign_block
                self.movable_blocks[text_id] = assign_block
            elif tag == 'inside_block':
                cords = self.stableCanvas.inside_block_coords(0, 0, 130, 20)
                bool_op_block = FunctionBlock([0, 0, 130, 20], self.canvas, cords, 'dodger blue', 'steel blue')
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
                    self.movable_blocks[peale].disconnect_magnet()

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


def main():
    root = Tk()
    root.geometry("+1+1")
    Button(command=root.quit, text="Quit").pack()
    t1 = ChooseBlocksCanvas(root)
    t1.top.geometry("+10+100")
    ChooseBlocksCanvas.create_blocks_fst(t1)
    t2 = MoveBlocksCanvas(root, t1)
    t2.top.geometry("+520+100")
    root.mainloop()


main()
