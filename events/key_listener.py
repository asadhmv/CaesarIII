class KeyListener:
    def __init__(self, func, key, continuous_press: bool = False, params = []):
        self.func = func
        self.key = key
        self.continuous_press = continuous_press
        self.being_pressed = False
        self.params = params

    def is_being_pressed(self):
        return self.being_pressed

    def set_being_pressed(self, being_pressed: bool):
        if self.continuous_press:
            self.being_pressed = being_pressed

    def call(self):
        if len(self.params) != 0:
            self.func(self.params)
        else:
            self.func()
