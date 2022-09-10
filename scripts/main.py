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
	key = None
	move_keys = {
		'right':False, 
		'left':False
		}
	presses = [False, False]
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
				case pygame.KEYDOWN:
					match event.key:
						case pygame.K_d:
							if key != 'space':
								key = 'right'
							move_keys['right'] = True
							presses[0] = True
							plyer.was_dirs = 'wright'
						case pygame.K_a:
							if key != 'space':
								key = 'left'
							move_keys['left'] = True
							presses[1] = True
							plyer.was_dirs = 'wleft'
						case pygame.K_SPACE:
							if jump_timer < 6:
								plyer.falling_y = -6
								key = 'space'
								hit_ground = False
								ground_touches = 0
				case pygame.KEYUP:
					match event.key:
						case pygame.K_d:
							if key != 'space':
								key = None
							move_keys['right'] = False
							presses[0] = False
						case pygame.K_a:
							if key != 'space':
								key = None
							move_keys['left'] = False
							presses[1] = False
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
			plyer.update_vels(move_keys, dt)
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
				if key == 'space': 
					if presses[0]: key = 'right'
					elif presses[1]: key = 'left'
					else: key = None
			
			if key == None:
				if presses[0]: key = 'right'
				elif presses[1]: key = 'left'


			plyer.render(res, scroll, dt, key, hit_ground)
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