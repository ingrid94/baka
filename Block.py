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


class CommandBlock(Block):
    def __init__(self, coords, canvas, stableCanvas, poly_cords):
        super().__init__(coords, canvas, poly_cords)
        # upper connection, lower connection, inside_poly connection
        self.connected = [None, None, None]
        self.color = 'violet red'
        self.outline = 'purple'
        self.stableCanvas = stableCanvas
        self.inside_poly_coords = [None, None, None, None]
        self.text_id = None
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
            self.connected[0].redraw(movable_blocks)
            # self.canvas.tag_raise(self.obj_id)

    def redraw(self, movable_blocks):
        old_width = self.coords[3]
        if self.connected[2] is not None:
            blo_width = self.connected[2].get_width()
            other_width = old_width - self.inside_poly_coords[2]
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
            stable_instance = movable_blocks[closest_object[0]]
            stable_magnet = stable_instance.renew_magnets()
            delta_x = stable_magnet[1][0] - magnet_x
            delta_y = stable_magnet[1][1] - magnet_y
            self.move_connected(delta_x, delta_y)
            if stable_instance.connected[1] is not None:
                under_block = stable_instance.connected[1]
                # Don't know ehy it needs 4 pixels, need to get real height somehow
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

    def redraw(self, movable_blocks):
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
            stable_instance = movable_blocks[closest_object[0]]
            # When ControlBlock has inside_poly, remove the first condition
            if not(isinstance(stable_instance, ControlBlock) or isinstance(stable_instance, ControlBlockLower)
                   or isinstance(stable_instance, InsideBlock)) and stable_instance.connected[2] is None:
                # gets poly_coords
                stable_coords = stable_instance.inside_poly_coords
                line_coords = self.stableCanvas.inside_block_coords(stable_coords[0], stable_coords[1], stable_coords[2], stable_coords[3])
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

    def move_to_magnet(self, movable_blocks):
        # when mouse press is let go, puts the block in right place
        magnet_x = self.renew_magnets()[0]
        magnet_y = self.renew_magnets()[1]

        closest_object = self.get_closest(movable_blocks)
        if closest_object:
            stable_instance = movable_blocks[closest_object[0]]
            if stable_instance.connected[2] is None:
                stable_magnet = [stable_instance.inside_poly_coords[0], stable_instance.inside_poly_coords[1]]
                stable_instance.delete_inside_poly(movable_blocks)
                delta_x = stable_magnet[0] - magnet_x
                delta_y = stable_magnet[1] - magnet_y
                self.move_connected(delta_x, delta_y)
                stable_instance.connected[2] = self
                self.connected[0] = stable_instance
                if isinstance(stable_instance, CommandBlock):
                    stable_instance.redraw(movable_blocks)

    def disconnect_magnet(self, movable_blocks):
        self.connected[0].connected[2] = None
        poly_id = self.connected[0].create_inside_polygon()
        movable_blocks[poly_id] = self.connected[0]
        self.connected[0].redraw(movable_blocks)
        self.connected[0] = None

    def move_connected(self, delta_x, delta_y):
        self.change_coords(delta_x, delta_y)
        if self.connected[0] is not None:
            self.connected[0].move_connected()

    def get_width(self):
        return self.coords[2]

    def raise_tags(self):
        for el in self.default_items_id:
            self.canvas.tag_raise(el)