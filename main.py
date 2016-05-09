__author__ = 'Miguel Rivero'
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import Pong

def new_game():
    global pong
    pong = Pong.Pong(CANVAS_SIZE, pad_colors=["Darkred", "Blue"])


def draw(canvas):
    pong.draw(canvas)


def keydown(key):
    if key == simplegui.KEY_MAP["w"]:
        pong.paddle_1.up()
    elif key == simplegui.KEY_MAP["s"]:
        pong.paddle_1.down()
    elif key == simplegui.KEY_MAP["up"]:
        pong.paddle_2.up()
    elif key == simplegui.KEY_MAP["down"]:
        pong.paddle_2.down()
    elif key == simplegui.KEY_MAP["p"]:
        pause()



def keyup(key):
    if key == simplegui.KEY_MAP["w"]:
        pong.paddle_1.down()
    elif key == simplegui.KEY_MAP["s"]:
        pong.paddle_1.up()
    elif key == simplegui.KEY_MAP["up"]:
        pong.paddle_2.down()
    elif key == simplegui.KEY_MAP["down"]:
        pong.paddle_2.up()


def add_ball():
    pong.add_ball()


def remove_ball():
    pong.remove_ball()


def edit_player_1(user_input):
    pong.score[0]["Name"] = user_input

def edit_player_2(user_input):
    pong.score[1]["Name"] = user_input

def pause():
    if pong.paused:
        pause_btn.set_text("Pause")
        pong.paused = False
    else:
        pause_btn.set_text("Resume")
        pong.paused = True

if __name__ == "__main__":
    CANVAS_SIZE = (600, 400)
    WIDTH = CANVAS_SIZE[0]
    HEIGHT = CANVAS_SIZE[1]

    #pong = None


    # create frame
    frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
    frame.set_canvas_background("Green")
    frame.set_draw_handler(draw)
    frame.set_keydown_handler(keydown)
    frame.set_keyup_handler(keyup)
    frame.add_button('Reset', new_game, 100)
    pause_btn = frame.add_button('Pause', pause, 100)
    frame.add_button('Add ball', add_ball, 100)
    frame.add_button('Remove ball', remove_ball, 100)
    frame.add_input("Player 1", edit_player_1, 100)
    frame.add_input("Player 2", edit_player_2, 100)

    # start frame
    new_game()
    frame.start()
