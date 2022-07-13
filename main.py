import picounicorn
import time
import game_objects
import display

picounicorn.init()

screen_w = picounicorn.get_width()
screen_h = picounicorn.get_height()
man = game_objects.Man()
game_seq = 0
difficulty = 0
pressed_x = False


def game_controls():
    global man, pressed_x
    if picounicorn.is_pressed(picounicorn.BUTTON_Y):
        man.jump()
    if picounicorn.is_pressed(picounicorn.BUTTON_B):
        man.duck()
    if picounicorn.is_pressed(picounicorn.BUTTON_X):
        if not pressed_x:
            game_objects.toggle_difficulty()
            pressed_x = True
        else:
            pressed_x = False


while True:
    # clear scene
    matrix = display.clear(screen_w, screen_h, [0, 40, 0])
    man.run()
    # read buttons and move
    game_controls()
    man.move()
    # draw and move objects (obstacles, clouds)
    objects = game_objects.handle_objects(game_seq, screen_w)
    # plot objects to matrix and detect collision
    collision = display.render_scene(matrix, man, game_seq)

    if collision:
        matrix = display.clear(screen_w, screen_h, [0, 0, 0])
        display.score(matrix, game_seq)
        # wait for button A to reset game
        while not picounicorn.is_pressed(picounicorn.BUTTON_A):
            pass
        game_seq = 0
        objects["blocks"] = []
        man.reset()
        continue

    game_seq += 1
    difficulty = game_objects.get_difficulty()
    time.sleep(difficulty["timer"])
