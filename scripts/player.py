import pygame, os
from pygame import image as img

class Player():
    def __init__(self):
        self.rect = pygame.Rect(300, 20, 8, 16)
        self.size = 16
        self.false_pos = [300, 0]
        self.ACCEL = 0.2
        self.FRICTION = 0.15
        self.MAX = 2
        self.falling_y = 0
        self.vels = [0, 0]
        self.was_dirs = 'wright'

        self.image_dir = 'images/player'
        all_images = os.listdir(self.image_dir)
        self.right = [img.load(f'{self.image_dir}/run_right1.png'), img.load(f'{self.image_dir}/run_right2.png'),
            img.load(f'{self.image_dir}/run_right3.png'), img.load(f'{self.image_dir}/run_right4.png'),
            img.load(f'{self.image_dir}/run_right5.png'), img.load(f'{self.image_dir}/run_right6.png'), 
            img.load(f'{self.image_dir}/run_right7.png')]
        self.run_len = len(self.right)-1
        self.left = [pygame.transform.flip(image, True, False) for image in self.right]

        self.idle_right = [img.load(f'{self.image_dir}/idle_right1.png'), img.load(f'{self.image_dir}/idle_right2.png'),
            img.load(f'{self.image_dir}/idle_right3.png'), img.load(f'{self.image_dir}/idle_right4.png')]
        self.idle_len = len(self.idle_right)-1
        self.idle_left = [pygame.transform.flip(image, True, False) for image in self.idle_right]
        
        self.jump_right = img.load(f'{self.image_dir}/jump_right1.png')
        self.jump_left = pygame.transform.flip(self.jump_right, True, False)
        
        self.hitg_right = img.load(f'{self.image_dir}/hitground_right1.png')
        self.hitg_left = pygame.transform.flip(self.hitg_right, True, False)

        self.image_id = 0
        self.animation_speed = 0.2

        self.animations = {
            'right':self.move_right, 
            'left':self.move_left,
            'wright':self.ani_idle_right,
            'wleft':self.ani_idle_left,
            'space':self.jump,
            'hitgr':self.hit_ground_right,
            'hitgl':self.hit_ground_left
            }

    def move_right(self, dt):
        self.image_id += self.animation_speed * dt
        if self.run_len < self.image_id:
            self.image_id = 0
        curr_image = self.right[int(self.image_id)]
        return curr_image
    def move_left(self, dt):
        self.image_id += self.animation_speed * dt
        if self.run_len < self.image_id:
            self.image_id = 0
        curr_image = self.left[int(self.image_id)]
        return curr_image

    def ani_idle_right(self, dt):
        self.image_id += self.animation_speed * dt
        if self.idle_len < self.image_id:
            self.image_id = 0
        curr_image = self.idle_right[int(self.image_id)]
        return curr_image
    def ani_idle_left(self, dt):
        self.image_id += self.animation_speed * dt
        if self.idle_len < self.image_id:
            self.image_id = 0
        curr_image = self.idle_left[int(self.image_id)]
        return curr_image

    def jump(self, dt):
        if self.was_dirs == 'wright':
            curr_image = self.jump_right
        else:
            curr_image = self.jump_left
        self.image_id = 0
        return curr_image

    def hit_ground_right(self):
        curr_image = self.hitg_right
        self.image_id = 0
        return curr_image
    def hit_ground_left(self):
        curr_image = self.hitg_left
        self.image_id = 0
        return curr_image

    def render(self, surf, scroll, dt, key, hit_ground):
        if not hit_ground:
            try: curr_image = self.animations[key](dt)
            except: curr_image = self.animations[self.was_dirs](dt)
        else:
            if self.was_dirs == 'wright':
                curr_image = self.animations['hitgr']()
            else:
                curr_image = self.animations['hitgl']()
        
        surf.blit(curr_image, ((self.rect.x-4)-scroll[0], self.rect.y-scroll[1]))

        #pygame.draw.rect(surf, (255, 0, 0), (self.rect.x-scroll[0],
         #   self.rect.y-scroll[1], self.size-8, self.size), 1)

    def update_vels(self, key, dt):
        self.vels[1] = 0
        if key['right']:
            if self.vels[0] < self.MAX:
                self.vels[0] += self.ACCEL * dt
        elif key['left']:
            if self.vels[0] > -self.MAX:
                self.vels[0] -= self.ACCEL * dt
        else:
            if self.vels[0] > 0:
                self.vels[0] -= self.FRICTION * dt
                if abs(self.vels[0] - 0.05) < 0.06:
                    self.vels[0] = 0
            elif self.vels[0] < 0:
                self.vels[0] += self.FRICTION * dt
                if (self.vels[0] + 0.05) > -0.06:
                    self.vels[0] = 0

        self.falling_y += 0.3 * dt
        self.vels[1] += self.falling_y
        if self.vels[1] >= 6:
            self.vels[1] = 6

    def test_collision(self, rect_list):
        hit_list = []
        for rect in rect_list:
            if rect.colliderect(self.rect):
                hit_list.append(rect)
        return hit_list

    def physics(self, rect_list, dt):
        colli = {'right':False, 'left':False, 'top':False, 'bottom':False}
        self.false_pos[0] += self.vels[0] * dt
        self.rect.x = self.false_pos[0]
        hit_list = self.test_collision(rect_list)
        for rect in hit_list:
            if self.vels[0] > 0:
                self.rect.right = rect.left
                self.false_pos[0] = self.rect.x
                self.vels[0] = 0
                colli['right'] = True
            elif self.vels[0] < 0:
                self.rect.left = rect.right
                self.false_pos[0] = self.rect.x
                self.vels[0] = 0
                colli['left'] = True
        self.false_pos[1] += self.vels[1] * dt
        self.rect.y = self.false_pos[1]
        hit_list = self.test_collision(rect_list)
        for rect in hit_list:
            if self.vels[1] > 0:
                self.rect.bottom = rect.top
                self.false_pos[1] = self.rect.y
                self.vels[1] = 0
                colli['bottom'] = True
            elif self.vels[1] < 0:
                self.falling_y = 1
                self.rect.top = rect.bottom
                self.false_pos[1] = self.rect.y
                self.vels[1] = 0
                colli['top'] = True

        return colli