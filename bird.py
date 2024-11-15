import random

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT

import game_framework
from state_machine import *
import game_world


# bird Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 1.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

class Idle:
    @staticmethod
    def enter(bird, e):
        if start_event(e):
            bird.action = 2
            bird.face_dir = 1
        elif right_down(e) or left_up(e):
            bird.action = 2
            bird.face_dir = -1
        elif left_down(e) or right_up(e):
            bird.action = 2
            bird.face_dir = 1

        bird.frame = 0
        bird.wait_time = get_time()

    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        if get_time() - bird.wait_time > 2:
            bird.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(bird):
        bird.image.clip_composite_draw(int(bird.frame) * 183, bird.action * 168, 183, 168, 0, '', bird.x, bird.y,30,30)
        # bird x = 183 y = 168

class Run:
    @staticmethod
    def enter(bird, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            bird.dir, bird.face_dir, bird.action = 1, 1, 2
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            bird.dir, bird.face_dir, bird.action = -1, -1, 2

    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time


    @staticmethod
    def draw(bird):
        if bird.face_dir == -1:
            bird.image.clip_composite_draw(int(bird.frame) * 183, bird.action * 168, 183, 168, 0, 'h', bird.x, bird.y,30,30)
        else:
            bird.image.clip_composite_draw(int(bird.frame) * 183, bird.action * 168, 183, 168, 0, '', bird.x, bird.y,30,30)




class Bird:

    def __init__(self):
        self.x, self.y = 400+random.randint(-40,40) , 90+random.randint(-20,20)
        self.face_dir = 1
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Run},
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 여기서 받을 수 있는 것만 걸러야 함. right left  등등..
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
