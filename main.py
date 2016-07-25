from tkinter import *


class Block:
    def __init__(self, coords, canvas, poly_cords):
        self.coords = coords
        self.canvas = canvas
        self.poly_cords = poly_cords
        self.obj_id = None

    def get_closest(self, movable_blocks):
        magnet_x = movable_blocks[self.obj_id].renew_magnets()[0][0]
        magnet_y = movable_blocks[self.obj_id].renew_magnets()[0][1]
        # finds closest object to magnet
        closest_object = self.canvas.find_closest(magnet_x, magnet_y, halo=20, start=self.obj_id)
        # if there is "line" in dictionary then deletes it
        if "line" in movable_blocks.values():
            self.line_delete(movable_blocks)
        return closest_object

    def check_magnets_during_move(self, movable_blocks):
        # moves magnets also checks other blocks and marks them
        closest_object = self.get_closest(movable_blocks)
        if closest_object[0] != self.obj_id and movable_blocks[closest_object[0]] != "line":
            stable_instance = movable_blocks[closest_object[0]]
            stable_coords = stable_instance.renew_magnets()
            line_x = stable_coords[1][0]
            line_y = stable_coords[1][1]
            # draws "line" mark to the block
            line_id = self.canvas.create_line(line_x - 20, line_y - 5, line_x - 15, line_y,
                                              line_x, line_y, line_x + 5, line_y - 5,
                                              fill="green", width=3)
            movable_blocks[line_id] = "line"
        # deletes "line" mark
        elif closest_object[0] == self.obj_id and "line" in movable_blocks.values():
            self.line_delete(movable_blocks)

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

    def create_polygon(self):
        self.obj_id = self.canvas.create_polygon(self.poly_cords, fill=self.color, outline=self.outline)
        return self.obj_id

    def renew_magnets(self):
        upper_magnet = [self.coords[0] + 40, self.coords[1] + 5]
        lower_magnet = [self.coords[0] + 50, self.coords[1] + 35]
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
        if closest_object[0] != self.obj_id:
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
        upper_magnet = [self.coords[0] + 40, self.coords[1] + 5]
        lower_magnet = [self.coords[0] + 40, self.coords[1] + 40]
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

    def move_to_magnet(self, movable_blocks):
        # when mouse press is let go, puts the block in right place
        magnet_x = self.renew_magnets()[0][0]
        magnet_y = self.renew_magnets()[0][1]
        closest_object = self.get_closest(movable_blocks)
        if closest_object[0] != self.obj_id:
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
    def __init__(self, coords, canvas, poly_cords, color, outline):
        super().__init__(coords, canvas, poly_cords, color, outline)

    def move_connected(self, delta_x, delta_y):
        self.change_coords(delta_x, delta_y)


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
    def command_block_coords(x, y, z):
        points = [x, y + 5, x + 5, y,
                  x + 20, y, x + 25, y + 5,
                  x + 40, y + 5, x + 45, y,
                  x + 175, y, x + 180, y + 5,
                  x + 180, y + z-5, x + 175, y + z,
                  x + 45, y + z, x + 40, y + z+5,
                  x + 25, y + z+5, x + 20, y + z,
                  x + 5, y + z, x, y + z-5,
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
                  x + 180, y + z-5, x + 175, y + z,
                  x + 55, y + z, x + 50, y + z+5,
                  x + 35, y + z+5, x + 30, y + z,
                  x + 15, y + z, x + 10, y + z+5,
                  x + 10, y + w+35,
                  x, y + w+35, x, y + 5]
        points_lower = [x + 10, y + w+35, x + 15, y + w+40,
                  x + 85, y + w+40, x + 90, y + w+45,
                  x + 90, y + w+50,
                  x + 85, y + w+55, x + 45, y + w+55,
                  x + 40, y + w+60, x + 25, y + w+60,
                  x + 20, y + w+55, x + 5, y + w+55,
                  x, y + w+50, x, y + w+35]
        return [points, points_lower]

    @staticmethod
    def inside_block_coords(x, y, w, h):
        a = (h/2)
        points = [x, y + a, x + a, y,
                  x + w, y, x + w + a, y + a,
                  x + w, y + h, x + a, y + h,
                  x, y + a]
        return points

    @staticmethod
    def type_block_coords(x, y, w, h):
        points = [x, y,
                  x+w, y,
                  x+w, y+h,
                  x, y+h,
                  x, y]
        return points

    def create_blocks_fst(self):
        self.canvas.create_polygon(self.command_block_coords(50, 100, 35), fill='violet red', outline='purple', tags='command_block')
        self.canvas.create_polygon(self.inside_block_coords(50, 200, 130, 20), fill='dodger blue', outline='steel blue',tags='inside_block')
        # self.canvas.create_polygon(self.inside_block_coords(50, 250, 65, 20), fill='limegreen', outline='green')
        self.canvas.create_polygon(self.control_block_coords(50, 300, 30, 35)[0], fill='orange', outline='chocolate', tags='control_block')
        self.canvas.create_polygon(self.control_block_coords(50, 300, 30, 35)[1], fill='orange', outline='chocolate', tags='control_block')
        self.canvas.create_polygon(self.type_block_coords(50, 420, 63, 15), fill='limegreen', outline='green', tags='variable')
        self.canvas.create_text(57, 420, anchor=NW, text="variable", tags='variable')
        self.canvas.create_polygon(self.type_block_coords(50, 445, 63, 15), fill='limegreen', outline='green', tags='number')
        self.canvas.create_text(57, 445, anchor=NW, text="number", tags='number')
        self.canvas.create_polygon(self.type_block_coords(50, 470, 63, 15), fill='limegreen', outline='green', tags='string')
        self.canvas.create_text(63, 470, anchor=NW, text="string", tags='string')

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
            if tag == 'command_block':
                cords = self.stableCanvas.command_block_coords(0, 0, 35)
                assign_block = CommandBlock([0, 0, 35], self.canvas, cords)
                obj_id = assign_block.create_polygon()
                self.movable_blocks[obj_id] = assign_block
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
                cords = self.stableCanvas.type_block_coords(0, 0, 65, 20)
                type_block = TypeBlock([0, 0, 65, 20], self.canvas, cords, 'limegreen', 'green')
                obj_id = type_block.create_polygon()
                self.movable_blocks[obj_id] = type_block
                self.create_frame('number', obj_id)
            elif tag == 'variable':
                cords = self.stableCanvas.type_block_coords(0, 0, 65, 20)
                type_block = TypeBlock([0, 0, 65, 20], self.canvas, cords, 'limegreen', 'green')
                obj_id = type_block.create_polygon()
                self.movable_blocks[obj_id] = type_block
                self.create_frame('variable', obj_id)
            elif tag == 'string':
                cords = self.stableCanvas.type_block_coords(0, 0, 65, 20)
                type_block = TypeBlock([0, 0, 65, 20], self.canvas, cords, 'limegreen', 'green')
                obj_id = type_block.create_polygon()
                self.movable_blocks[obj_id] = type_block
                self.create_frame('string', obj_id)

    def create_frame(self, inside_type, obj_id):

        text = ""
        if inside_type == 'variable':
            text = "Variables must begin with a letter (a - z, A - B) or underscore (_). \n" \
                   "Other characters can be letters, numbers or _"
        elif inside_type == 'number':
            text = "Numbers consist of digits (0-9). \n To get floating point number use point (.)"
        elif inside_type == 'string':
            text = "String literals are written in single or double quotes. "

        frame = Frame(self.canvas)
        can = self.canvas.create_window(250, 200, window=frame)

        introduction = Label(frame, text=text)
        introduction.pack(pady=10)

        e = Entry(frame)
        e.pack()

        cancel = Button(frame, text="Cancel", command=lambda: self.delete_item(obj_id, can))
        cancel.pack(side=LEFT, padx=30, pady=10)

        confirm = Button(frame, text="Confirm")
        confirm.pack(side=RIGHT, padx=30, pady=10, command=lambda: self.create_type(obj_id, can))

    def delete_item(self, obj_id, frame):
        self.canvas.delete(obj_id)
        self.canvas.delete(frame)
        del self.movable_blocks[obj_id]

    def create_type(self, obj_id, can):
        pass

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
