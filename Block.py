
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
        # elif "line" in movable_blocks.values():
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