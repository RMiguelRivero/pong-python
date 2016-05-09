__author__ = 'Miguel Rivero'

class Paddle(object):
    """
    Paddle class
    """
    version = "0.1"
    PADDLE_VELOCITY = 3
    def __init__(self, position, pad_size=[8, 80], velocity=[0,0], color="White"):
        self.width = pad_size[0]
        self.height = pad_size[1]
        self.position = position
        self.velocity = velocity
        self.color = color

    @property
    def half_width(self):
        return self.width / 2

    @property
    def half_height(self):
        return self.height / 2

    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
    def draw(self, canvas):
        canvas.draw_polygon([[self.position[0] - self.half_width, self.position[1] - self.half_height],
                             [self.position[0] - self.half_width, self.position[1] + self.half_height],
                             [self.position[0] + self.half_width, self.position[1] + self.half_height],
                             [self.position[0] + self.half_width, self.position[1] - self.half_height]],
                            1, line_color=self.color, fill_color=self.color)

    def up(self):
        self.velocity[0] = 0
        self.velocity[1] -= self.PADDLE_VELOCITY

    def down(self):
        self.velocity[0] = 0
        self.velocity[1] +=  self.PADDLE_VELOCITY