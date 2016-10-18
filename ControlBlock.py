from Block import Block


class ControlBlock(Block):
    def __init__(self, coords, canvas, stable_canvas, poly_cords):
        super().__init__(coords, canvas, poly_cords)
        # upper connection, main lower connection,  ControlBlockLower instance, main inside connection
        self.connected = [None, None, None, None]
        self.color = 'orange'
        self.outline = 'chocolate'
        self.stableCanvas = stable_canvas
        self.default_items_on_block = None

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

    def disconnect_magnet(self):
        self.connected[0].connected[1] = None
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
        blo_height = self.connected[1].get_height()
        old_height = self.coords[3]
        self.coords[3] = blo_height
        self.poly_cords = self.stableCanvas.control_block_coords(self.coords[0], self.coords[1],
                                                                 self.coords[2], blo_height)[0]
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
