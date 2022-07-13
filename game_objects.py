"""
Definition and logic for the objects and their lifecycle
"""
import random
import models


class Obstacle:
    x = 0
    y = 0
    model = None
    width = 0


class Man:
    x = 2
    y = 0
    state = "run"
    model = models.man["run"][0]
    jump_steps = [1, 2, 3, 3, 3, 2, 1, 0]
    jump_seq = -1

    def jump(self):
        # only start jumping when not in the air (counter at -1)
        if self.jump_seq == -1:
            self.jump_seq = 0
        self.state = "jump"

    def duck(self):
        self.state = "duck"

    def run(self):
        self.state = "run"

    def move(self):
        self.y = 0
        if self.jump_seq >= 0:
            self.y += self.jump_steps[self.jump_seq]
        if 0 <= self.jump_seq < len(self.jump_steps) - 1:
            self.jump_seq += 1
        else:
            self.jump_seq = -1

    def reset(self):
        self.y = 0
        self.jump_seq = -1


objects = {
    "clouds": [],
    "blocks": []
}

difficulty = 1
diff_levels = [
    {"timer": 0.13, "color": [0, 0, 155]},
    {"timer": 0.10, "color": [155, 155, 0]},
    {"timer": 0.06, "color": [155, 0, 0]}
]


def toggle_difficulty():
    global difficulty
    difficulty = (difficulty + 1) % len(diff_levels)


def get_difficulty():
    return diff_levels[difficulty]


def handle_objects(game_seq, screen_w):
    global objects
    """
    Handles the creation, destruction and movement of obstacles and clouds
    """
    objects = add_obstacle(screen_w, 6 + random.randint(0, 3))
    objects = move_obstacles()
    objects = add_cloud(screen_w)
    objects = move_clouds(game_seq)
    return objects


def add_cloud(screen_w):
    objects["clouds"] = add_object(objects["clouds"], models.cloud, screen_w, 3, 4 + random.randint(1, 6))
    return objects


def move_clouds(game_seq):
    # move clouds every 3 frames for parallax effect
    if game_seq % 3 > 0:
        return objects
    objects["clouds"] = move_objects(objects["clouds"])
    return objects


def add_obstacle(screen_w, min_distance=10):
    if random.randint(1, 3) == 1:
        # add floating block
        objects["blocks"] = add_object(objects["blocks"], models.block, screen_w, 3, min_distance)
    else:
        # add stone
        objects["blocks"] = add_object(objects["blocks"], models.stone, screen_w, 0, min_distance)
    return objects


def move_obstacles():
    objects["blocks"] = move_objects(objects["blocks"])
    return objects


def add_object(arr_objects, arr_model, screen_w, y, distance):
    if len(arr_objects) > 0:
        last_object = arr_objects[-1]
        if screen_w - (last_object.x + last_object.width) < distance:
            return arr_objects
    o = Obstacle()
    o.x = screen_w
    o.y = y
    o.model = arr_model[random.randint(0, len(arr_model) - 1)]
    o.width = len(o.model[0])
    arr_objects.append(o)
    return arr_objects


def move_objects(arr_objects):
    for o in arr_objects:
        o.x -= 1
    # only keep objects that are still visible
    arr_objects = [e for e in arr_objects if e.x > -e.width]
    return arr_objects
