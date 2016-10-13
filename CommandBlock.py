from Block import Block
from ControlBlock import ControlBlock


class CommandBlock(Block):
    def __init__(self, coords, canvas, stableCanvas, poly_cords):
        super().__init__(coords, canvas, poly_cords)
        # upper connection, lower connection, inside_poly connection
        self.connected = [None, None, None]
        self.color = 'violet red'
        self.outline = 'purple'
        self.stableCanvas = stableCanvas

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