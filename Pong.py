__author__ = 'Miguel Rivero'
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import Ball
import Paddle
import random


class Pong(object):
    """
    Pong class. It defines the game and the rules.
    """
    version = "0.1"
    BOUNCE_BALL = simplegui.load_sound("http://sounds/bounce.wav")
    BOUNCE_PADDLE_1 = simplegui.load_sound("http://sounds/paddle1.wav")
    BOUNCE_PADDLE_2 = simplegui.load_sound("http://sounds/paddle2.wav")
    GUTTERS_SEP = 8
    score = [{"Name": "Player 1", "Points": 0}, {"Name": "Player 2", "Points": 0}]
    paused = False

    def __init__(self, canvas_size=[600, 400], pad_size=[8, 80], pad_colors=["DarkOrange", "Yellow"]):
        self.width = canvas_size[0]
        self.height = canvas_size[1]
        self.balls = []
        self.balls_to_add = []
        ball = Ball.Ball([self.width / 2, self.height / 2])
        self.balls.append(ball)
        self.paddle_1 = Paddle.Paddle([pad_size[0] / 2, self.height / 2], pad_size, velocity=[0, 0], color=pad_colors[0])
        self.paddle_2 = Paddle.Paddle([self.width - pad_size[0] / 2, self.height / 2], pad_size, velocity=[0, 0], color=pad_colors[1])
        self.score[0]["Points"] , self.score[1]["Points"] = 0, 0
        self.BOUNCE_BALL.set_volume(0.7)
        self.BOUNCE_PADDLE_1.set_volume(0.7)
        self.BOUNCE_PADDLE_2.set_volume(0.7)


    def reset(self):
        self.score[0]["Points"] , self.score[1]["Points"] = 0, 0
        self.balls = self.balls[:1]
        self.balls[0].spawn([self.width / 2, self.height / 2], random.choice(["LEFT", "RIGHT"]))

    def add_ball(self):
        """
        There can be up to 4 balls
        :return: True if created, False otherwise
        """
        can_spawn = True
        for ball in self.balls:
            if ball.distance_to_point([self.width / 2, self.height / 2]) <= ball.radius * 2:
                can_spawn = False
        if len(self.balls) < 4 and can_spawn:
            ball = Ball.Ball([self.width / 2, self.height / 2], color="White")
            self.balls.append(ball)
            return True
        return False

    def remove_ball(self):
        if len(self.balls) > 1:
            self.balls.pop()

    def draw(self, canvas):
        """
        It handles the behaviour of the playing field
        :param canvas:
        :return:
        """
        # Check the pause flag
        if not self.paused:
            # draw mid line and gutters from left to right
            canvas.draw_line([self.GUTTERS_SEP, 0], [self.GUTTERS_SEP, self.height], 1, "White")
            canvas.draw_line([self.width / 2, 0], [self.width / 2, self.height], 1, "White")
            canvas.draw_circle([self.width / 2, self.height / 2], 20, 1, "White")
            canvas.draw_line([self.width - self.GUTTERS_SEP, 0], [self.width - self.GUTTERS_SEP, self.height], 1, "White")

            # Game's logic
            self._move_balls(canvas)
            self._keep_paddles_inside()

            # Draw scores and paddles
            canvas.draw_text(self.score[0]["Name"], [self.width / 4 - 25, 20], 20, self.paddle_1.color)
            canvas.draw_text(str(self.score[0]["Points"]), [self.width / 4, 50], 25, self.paddle_1.color)
            canvas.draw_text(self.score[1]["Name"], [self.width * 3 / 4 - 25, 20], 20, self.paddle_2.color)
            canvas.draw_text(str(self.score[1]["Points"]), [self.width * 3 / 4, 50], 25, self.paddle_2.color)
            self.paddle_1.draw(canvas)
            self.paddle_2.draw(canvas)

        else:
            text = "PAUSE"
            text_height = 100
            canvas.draw_text(text, [self.width / 2 - len(text)/2 * text_height / 2 , self.height / 2 + text_height / 2 ],
                             text_height, "Black")


    # helper functions
    def _keep_paddles_inside(self):
        """
        Check if the move is possible for each paddle
        :return: None
        """
        # draw paddles
        if self.paddle_1.position[1] + self.paddle_1.velocity[1] >= self.paddle_1.half_height and \
           self.paddle_1.position[1] + self.paddle_1.velocity[1] <= self.height - self.paddle_1.half_height:
            self.paddle_1.move()
        if self.paddle_2.position[1] + self.paddle_2.velocity[1] >= self.paddle_1.half_height and \
           self.paddle_2.position[1] + self.paddle_2.velocity[1] <= self.height - self.paddle_2.half_height:
            self.paddle_2.move()

    def _move_balls(self, canvas):
        """
        Draw ball in a canvas
        :param canvas:
        :return: None
        """
        for ball in self.balls:
            # check if it is in the middle of the canvas that should be the common stage to avoid more computation
            if (self.GUTTERS_SEP + ball.radius) < ball.position[0] < (self.width - 1 - self.GUTTERS_SEP - ball.radius) \
                and ball.radius < ball.position[1] < (self.height - ball.radius):
                self._check_collisions(ball)
                ball.move()
                ball.draw(canvas)
                continue
            # vertical bounce
            # bounce off paddle 1 or scores
            if (ball.position[0] - ball.radius) <= self.GUTTERS_SEP:
                if ball.position[1] >= (self.paddle_1.position[1] - self.paddle_1.half_height) and \
                   ball.position[1] <= (self.paddle_1.position[1] + self.paddle_1.half_height):
                    self.BOUNCE_PADDLE_1.play()
                    ball.velocity[0] = - ball.velocity[0]
                    ball.increment_velocity()
                else:
                    ball.spawn([self.width / 2, self.height / 2], "LEFT")
                    self.score[1]["Points"] += 1
            # bounce off paddle 2 or scores
            elif (ball.position[0] + ball.radius) >= (self.width - 1 - self.GUTTERS_SEP):
                if ball.position[1] >= (self.paddle_2.position[1] - self.paddle_2.half_height) and \
                   ball.position[1] <= (self.paddle_2.position[1] + self.paddle_2.half_height):
                    self.BOUNCE_PADDLE_1.play()
                    ball.velocity[0] = - ball.velocity[0]
                    ball.increment_velocity()
                else:
                    ball.spawn([self.width / 2, self.height / 2], "RIGHT")
                    self.score[0]["Points"] += 1
            # horizontal bounce
            if ball.position[1] <= ball.radius or ball.position[1] >= (self.height - 1) - ball.radius:
                ball.velocity[1] = - ball.velocity[1]
                self.BOUNCE_BALL.play()
            # it has to move an draw at any case
            ball.move()
            ball.draw(canvas)

    def _check_collisions(self, ball):
        for other in self.balls:
            if ball.distance(other) < 0 and ball.position != other.position:
                # elastic collision with ball same mass
                ball.velocity, other.velocity = other.velocity, ball.velocity
