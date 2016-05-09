__author__ = 'Miguel Rivero'
import random
import math


class Ball(object):
    """
    Ball class
    """
    version = "0.1"
    DEFAULT_RADIUS = 15
    INCREMENT_VELOCITY = 1.1
    def __init__(self,
                 position,
                 radius=DEFAULT_RADIUS,
                 color="White"):
        self.position = position
        self.radius =  radius
        self.velocity = [random.randrange(120.0 / 60.0, 240.0 / 60.0), random.randrange(60.0 / 60.0, 180.0 / 60.0)]
        self.color = color

    def move(self):
        """
        update de ball's position
        """
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def change_direction(self, direction):
        """[int, int] -> None

        :param direction: Velocity
        :return:
        """
        self.velocity[0], self.velocity[1] = direction[0], direction[1]

    def increment_velocity(self, increment=INCREMENT_VELOCITY):
        """(int) -> None

        :param increment: Amount that increments the ball's velocity
        :return:
        """
        self.velocity[0] *= increment
        self.velocity[1] *= increment

    def spawn(self, position, direction):
        self.position = position
        if direction == "LEFT":
            self.velocity[0] = - random.randrange(120.0 / 60.0, 240.0 / 60.0)
            self.velocity[1] = - random.randrange(60.0 / 60.0, 180.0 / 60.0)
        elif direction == "RIGHT":
            self.velocity[0] = random.randrange(120.0 / 60.0, 240.0 / 60.0)
            self.velocity[1] = - random.randrange(60.0 / 60.0, 180.0 / 60.0)

    def draw(self, canvas):
        canvas.draw_circle(self.position, self.radius, 2, self.color, self.color)

    def distance(self, other):
        center_distance = math.sqrt((self.position[0] - other.position[0]) ** 2 + (self.position[1] - other.position[1]) ** 2 )
        radius_sum  = self.radius + other.radius
        return  center_distance - radius_sum

    def distance_to_point(self, point):
        '''(list(double)) -> double

        :param point: list of 2 double
        :return: double
        '''
        return math.sqrt((self.position[0] - point[0]) ** 2 + (self.position[1] - point[1]) ** 2)