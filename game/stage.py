class Stage:
    def __init__(self):
        self.floor_rects = []
        pass

    def get_width(self):
        return 0

    def update(self, game_speed):
        pass

    def draw_background(self, surface, window_x, window_y):
        pass

    def draw_foreground(self, surface, window_x, window_y):
        pass

    def entity_pos(self, entity_name):
        return 0, 0
