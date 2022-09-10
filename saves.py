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

        self.image_dir = 'images/player/'
        self.image_id = 0

        self.image = {
            'run_right':[], 'run_left':[], 'idle_right':[],
            'idle_left':[], 'jump_right':[], 'jump_left':[],
            'hitground_right':[], 'hitground_left':[]
        }
        self.curr_mov = 'idle_right'
        self.pre_direction = 'right'
        for name in os.listdir(self.image_dir):
            image = pygame.image.load((self.image_dir + name))
            mov_name = ''
            for char in name:
                if char.isdigit():
                    break
                mov_name += char
            self.image[mov_name].append(image)
            left_mov_name = mov_name.replace('right', 'left')
            left_image = pygame.transform.flip(image, True, False)
            self.image[left_mov_name].append(left_image)
        self.image['idle_jump_right'] = [self.image['jump_right']]
        self.image['idle_jump_left'] = [self.image['jump_left']]
        self.image['idle_hitg_right'] = self.image['hitground_right']
        self.image['idle_hitg_left'] = self.image['hitground_left']
    
    def movement(self, dt, jump_timer, hit_ground, ground_touches):
        keys = pygame.key.get_pressed()
        #If previous dir was jumping, this resets the value so the animation stops
        if hit_ground:
            if 'right' in self.pre_direction: self.pre_direction = 'right'
            else: self.pre_direction = 'left'
        self.curr_mov = self.pre_direction
        self.vels[1] = 0

        #print(ground_touches)

        print(self.pre_direction, self.curr_mov)

        if keys[pygame.K_d]:
            if ground_touches >= 3:
                self.curr_mov = 'run_right'
                self.pre_direction = 'right'
            if self.vels[0] < self.MAX:
                self.vels[0] += self.ACCEL * dt
        elif keys[pygame.K_a]:
            if ground_touches >= 3:
                self.curr_mov = 'run_left'
                self.pre_direction = 'left'
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

        if keys[pygame.K_SPACE]:
            if self.pre_direction == 'right':
                self.curr_mov = 'jump_right'
                self.pre_direction = 'jump_right'
            elif self.pre_direction == 'left':
                self.curr_mov = 'jump_left'
                self.pre_direction = 'jump_left'
            if jump_timer < 6:
                self.falling_y = -6
                hit_ground = False
                ground_touches = 0

        self.falling_y += 0.3 * dt
        self.vels[1] += self.falling_y
        if self.vels[1] >= 6:
            self.vels[1] = 6

        if ground_touches < 3:
            if self.pre_direction == 'right':
                self.pre_direction = 'hitg_right'
                self.curr_mov = 'hitground_right'
            elif self.pre_direction == 'left':
                self.pre_direction = 'hitg_left'
                self.curr_mov = 'hitground_left'

        return hit_ground, ground_touches

    def animate(self, surf, dt, scroll):
        try: 
            if self.image_id >= len(self.image[self.curr_mov])-.3:
                self.image_id = 0
            player_image = self.image[self.curr_mov][int(self.image_id)]
        except: 
            if self.image_id >= len(self.image['idle_' + self.curr_mov])-.3:
                self.image_id = 0
            player_image = self.image['idle_' + self.curr_mov][int(self.image_id)]
            #print(self.curr_mov)
        self.image_id += 0.2 * dt
        surf.blit(player_image, (
            (self.rect.x-4)-scroll[0], self.rect.y-scroll[1])
        )

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












import pygame, sys, os
from pygame.locals import *
import worldProcess
import player
import menu_ui as menu
pygame.init()

def main():
	WINDOW_SIZE = (800, 500)
	window = pygame.display.set_mode(WINDOW_SIZE)
	res_sizex = 200
	res_sizey = 125
	RES = (res_sizex, res_sizey)
	res = pygame.Surface(RES)
	clock = pygame.time.Clock()
	fps_cap = 10_000
	rel_fps = 60

	world_image_dir = 'images/world'
	sim_dis, x_dis, y_dis = 25, 170, 150
	mapc = worldProcess.MapC(
		'data/world/worldData', f'{world_image_dir}/tiles', [sim_dis, x_dis, y_dis]
	)
	mapc.convert_tile_size(16)
	sliced = False

	plyer = player.Player()

	jump_timer = 0
	tscroll = [0, 0]
	hit_ground = False
	ground_touches = 0

	ticks = 0
	time = 0

	#MENU VARIABLES#
	starts = {
		'game':False,
		'menu':True
	}
	mu = menu.Menu(RES, WINDOW_SIZE)
	mouse_button_up = False
	#MENU VARIABLES#

	#BACKGROUND#
	bg = pygame.image.load('images/world/background/bg.png')
	bgx, bgy = 0, 0
	#BACKGROUND#

	while 1:
		dt = clock.tick(fps_cap) * .001 * rel_fps

		ticks += 1
		time += 1 * dt
		if time >= rel_fps:
			time = 0
			print(f'fps: {ticks}')
			ticks = 0

		size_diffx = (WINDOW_SIZE[0]/RES[0]*2)+1
		size_diffy = (WINDOW_SIZE[1]/RES[1]*2)+1
		tscroll[0] += (((plyer.rect.x-plyer.size/2 - tscroll[0]) - (WINDOW_SIZE[0]/size_diffx)))/20 * dt
		tscroll[1] += (((plyer.rect.y-plyer.size/2 - tscroll[1]) - (WINDOW_SIZE[1]/size_diffy)))/20 * dt
		scroll = tscroll.copy()
		scroll[0] = int(scroll[0])
		scroll[1] = int(scroll[1])

		mouse_button_up = False
		for event in pygame.event.get():
			match event.type:
				case pygame.QUIT:
					pygame.quit()
					sys.exit()
				case pygame.MOUSEBUTTONDOWN:
					match event.button:
						case 4:
							res_sizex -= 12.5
							res_sizey -= 7.8
							x_dis -= 12.5
							y_dis -= 7.8125
							RES = (res_sizex, res_sizey)
							res = pygame.Surface(RES)
							x_dis, y_dis = mapc.convert_render_dis(x_dis, y_dis)
						case 5:
							res_sizex += 12.5
							res_sizey += 7.8125
							x_dis += 12.5
							y_dis += 7.8125
							RES = (res_sizex, res_sizey)
							res = pygame.Surface(RES)
							x_dis, y_dis = mapc.convert_render_dis(x_dis, y_dis)
						case 1:
							mouse_button_down = True
							mouse_button_up = False
				case pygame.MOUSEBUTTONUP:
					match event.button:
						case 1:
							mouse_button_up = True

		res.fill((200, 200, 200))

		if starts['game']:
			rect_list = mapc.show_map(res, [plyer.rect.x, plyer.rect.y], scroll)
			if not sliced:
				map_rect, tx, ty, width, height = mapc.slice_chunks()
				sliced = True

			hit_ground, ground_touches = plyer.movement(dt, jump_timer, hit_ground, ground_touches)

			jump_timer += 2 * dt
			colli = plyer.physics(rect_list, dt)
			if plyer.falling_y > 1:
				ground_touches = 0
				hit_ground = False
			if colli['bottom']:
				if ground_touches < 3:
					hit_ground = True
				else:
					hit_ground = False
					ground_touches -= 1
				jump_timer = 0
				plyer.falling_y = 0
				ground_touches += 1

			plyer.animate(res, dt, scroll)
			for rect in rect_list:
				pygame.draw.rect(res, (255, 0, 0), (rect[0]-scroll[0],
					rect[1]-scroll[1], rect[2], rect[3]), 1)
			
		elif starts['menu']:
			mpos = pygame.mouse.get_pos()
			starts = mu.render_buttons(res, mpos, starts, mouse_button_up)

		new_surf = pygame.transform.scale(res, WINDOW_SIZE)
		window.blit(new_surf, (0, 0))

		pygame.display.update()

if __name__ == '__main__':
	main()