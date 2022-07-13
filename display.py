"""
Rendering objects into the scene
Handling of collisions
"""
import picounicorn

import game_objects
import models


def clear(w, h, color):
    return [[color for _ in range(h)] for _ in range(w)]


def set_model(matrix, model, x, y, check_collision):
    collision = False
    model_h = len(model)
    model_w = len(model[0])
    for my in range(model_h):
        for mx in range(model_w):
            if model[my][mx][0] + model[my][mx][1] + model[my][mx][2] > 0:
                if 0 <= x + mx < 16:
                    p = matrix[x + mx][y + my]
                    # detect collision when there is a red pixel
                    if check_collision and p[0] == 175 and p[1] == 0 and p[1] == 0:
                        collision = True
                    matrix[x + mx][y + my] = model[my][mx]
    return matrix, collision


def render_scene(matrix, man, game_seq):
    matrix, collision = show_objects(matrix, man, game_seq)
    matrix = show_difficulty(matrix)
    plot(matrix)
    return collision


def show_difficulty(matrix):
    difficulty = game_objects.get_difficulty()
    height = len(matrix)
    width = len(matrix[0])
    matrix[height-1][width-1] = difficulty["color"]
    return matrix


def plot(matrix):
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            # flip y-axis to set 0,0 to bottom left
            y2 = len(matrix[0]) - 1 - y
            picounicorn.set_pixel(x, y2, matrix[x][y][0], matrix[x][y][1], matrix[x][y][2])
    return matrix


def show_objects(matrix, man, game_seq):
    matrix, _ = set_model(matrix, models.sky, 0, 3, False)
    for cloud in game_objects.objects["clouds"]:
        matrix, _ = set_model(matrix, cloud.model, cloud.x, cloud.y, False)
    for block in game_objects.objects["blocks"]:
        matrix, _ = set_model(matrix, block.model, block.x, block.y, False)
    man_model = man.model = models.man[man.state][game_seq % len(models.man[man.state])]
    matrix, collision = set_model(matrix, man.model, man.x, man.y, True)
    return matrix, collision


def score(matrix, game_seq):
    x = 1
    game_seq = game_seq % 10000  # can't show more than four digits
    for i in str(game_seq):
        matrix, _ = set_model(matrix, models.letters[i], x, 1, False)
        x += len(models.letters[i][0]) + 1
    plot(matrix)


def marquee(text):
    stack = []
    for letter in text:
        stack.append(models.letters[letter])
