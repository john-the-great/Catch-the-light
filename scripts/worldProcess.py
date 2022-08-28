import chunk
import pygame
import json

class MapC:
    def __init__(self, file_name, image_dir, processed_distances):
        self.data = json.load(open(file_name + '.json'))
        self.world_data = {}
        for key in self.data:
            image = pygame.image.load(image_dir + '/' + self.data[key]).convert()
            image.set_colorkey((0, 0, 0, 0))
            self.world_data[key] = [image, self.data[key]]
        self.itterate_data = {}
        for id, key in enumerate(self.world_data):
            pos = key.split()
            pos1 = int(pos[0])
            pos2 = int(pos[1])
            self.itterate_data[id] = [pos1, pos2]
        self.sim_dis = processed_distances[0]
        self.x_dis = processed_distances[1]
        self.y_dis = processed_distances[2]

    def convert_tile_size(self, TILE_SIZE):
        for key in self.world_data:
            self.world_data[key][0] = pygame.transform.scale(self.world_data[key][0], (TILE_SIZE, TILE_SIZE))
        self.TILE_SIZE = TILE_SIZE

    def convert_render_dis(
        self, x_dis: int, y_dis: int
    ):
        self.x_dis = x_dis
        self.y_dis = y_dis

        return self.x_dis, self.y_dis
    #if self.world_data[key][1] == 'grassShards2.png'

    def slice_chunks(self):
        positions = [[], []]
        for key in self.world_data:
            pos = key.split()
            x = int(pos[0])
            y = int(pos[1])
            positions[0].append(x)
            positions[1].append(y)
        tx = min(positions[0])
        ty = min(positions[1])
        width = abs(max(positions[0]) - tx)+self.TILE_SIZE
        height = abs(max(positions[1]) - ty)+self.TILE_SIZE

        tile_data = {}
        for wlength in range(width):
            x = tx+wlength
            for hlength in range(height):
                y = ty+hlength
                if x % self.TILE_SIZE == 0 and y % self.TILE_SIZE == 0:
                    has_data = False
                    for key in self.world_data:
                        if key == f'{x} {y}':
                            tile_data[key] = self.world_data[key]
                            has_data = True
                            break
                    if not has_data:
                        tile_data[f'{x} {y}'] = [None, None]

        chunk_data = {}
        marked = []
        for key in tile_data:
            try:
                if tile_data[key][0] != None and tile_data[key][1] != 'tile9.png':
                    pos = key.split()
                    x = int(pos[0])
                    y = int(pos[1])
                    markedk = False
                    for marked_key in marked:
                        if marked_key == key:
                            markedk = True
                    if not markedk:
                        tmp_surf = pygame.Surface((self.TILE_SIZE*2, self.TILE_SIZE*2))
                        tmp_surf.blit(tile_data[key][0], (0, 0))
                        tmp_surf.blit(tile_data[f'{x+self.TILE_SIZE} {y}'][0], (self.TILE_SIZE, 0))
                        tmp_surf.blit(tile_data[f'{x} {y+self.TILE_SIZE}'][0], (0, self.TILE_SIZE))
                        tmp_surf.blit(tile_data[f'{x+self.TILE_SIZE} {y+self.TILE_SIZE}'][0], (self.TILE_SIZE, self.TILE_SIZE))
                        marked.append(key)
                        marked.append(f'{x+self.TILE_SIZE} {y}')
                        marked.append(f'{x} {y+self.TILE_SIZE}')
                        marked.append(f'{x+self.TILE_SIZE} {y+self.TILE_SIZE}')
                        chunk_data[key] = [tmp_surf, '4chunk']
                else:
                    if tile_data[key][0] != None:
                        chunk_data[key] = tile_data[key]
            except:
                chunk_data[key] = tile_data[key]

        self.world_data = chunk_data

        return pygame.Rect(x, y, width, height), tx, ty, width, height

    def show_map(self, surf, player_pos, scroll = [0, 0]):
        rect_list = []
        for key in self.world_data:
            pos = key.split()
            x = int(pos[0])
            y = int(pos[1])
            if not self.world_data[key][0] == None:
                if abs(player_pos[0] - x-self.TILE_SIZE/2) < self.x_dis and abs(player_pos[1] - y-self.TILE_SIZE/2) < self.y_dis:
                    surf.blit(self.world_data[key][0], (x-scroll[0], y-scroll[1]))
                if abs(player_pos[0] - x-self.TILE_SIZE/2) < self.sim_dis and abs(player_pos[1] - y-self.TILE_SIZE/2) < self.sim_dis:
                    if not self.world_data[key][1] == 'tile9.png':
                        if self.world_data[key][1] == '4chunk':
                            rect_list.append(pygame.Rect(x, y, self.TILE_SIZE*2, self.TILE_SIZE*2))
                        else:
                            rect_list.append(pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE))
        return rect_list
