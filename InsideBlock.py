from CommandBlock import CommandBlock
from ControlBlock import ControlBlock, ControlBlockLower


class InsideBlock:
    def __init__(self, coords, canvas, stableCanvas, poly_cords, color, outline):
        # inside the block
        self.default_items_id = []
        self.coords = coords
        self.canvas = canvas
        self.poly_cords = poly_cords
        self.connected = []
        self.connected_to_bigger_block = None
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
                   or isinstance(stable_instance, InsideBlock)):
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
            stable_magnet = [stable_instance.inside_poly_coords[0], stable_instance.inside_poly_coords[1]]
            stable_instance.delete_inside_poly(movable_blocks)
            delta_x = stable_magnet[0] - magnet_x
            delta_y = stable_magnet[1] - magnet_y
            self.move_connected(delta_x, delta_y)
            stable_instance.connected[2] = self
            self.connected_to_bigger_block = stable_instance
            if isinstance(stable_instance, CommandBlock):
               stable_instance.redraw(movable_blocks)

    def disconnect_magnet(self):
        self.connected_to_bigger_block = None

    def move_connected(self, delta_x, delta_y):
        self.change_coords(delta_x, delta_y)

    def get_width(self):
        return self.coords[2]

    def raise_tags(self):
        for el in self.default_items_id:
            self.canvas.tag_raise(el)