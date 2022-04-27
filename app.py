from pickletools import optimize
from Astar_algo import *
from Dijkstra_algo_C import *
from Gif_Image import *
from TextInput import *
import pygame
import sys
import utm
import os
import time


def Pixel_to_utm(x, y, min_x, min_y, den_x, den_y):
    x_graph = x * den_x + min_x
    y_graph = - y * den_y - min_y
    return x_graph, y_graph

def utm_to_Pixel(x,y, min_x,min_y,den_x,den_y):
    x_graph=(x-min_x)/den_x
    y_graph=(-y-min_y)/den_y
    return x_graph, y_graph

def get_cache_map_gps(west, east, south, north, width, height):
    min_x, max_y, _, _ = utm.from_latlon(south, west)
    max_x, min_y, _, _ = utm.from_latlon(north, east)
    min_y, max_y = - min_y, - max_y
    den_x = (max_x - min_x) / width
    den_y = (max_y - min_y) / height
    return min_x, min_y, den_x, den_y

def draw_src(surface, x, y):
    icon = pygame.image.load('src-pin.png')
    surface.blit(icon, (x - 6, y - 19))


def draw_des(surface, x, y):
    icon = pygame.image.load('des-pin.png')
    surface.blit(icon, (x - 6, y - 19))


def draw_traffic_point(surface, x, y):
    color = '#FF9300'
    pygame.draw.circle(surface, color, (x, y), 2)


def draw_path(surface, network_type, path, x_coor, y_coor, min_x, min_y, den_x, den_y, start_pos_pix):
    if network_type == 0:
        color = '#004DFE'
    elif network_type == 1:
        color = '#00C1FF'
    elif network_type == 2:
        color = '#FF9300'
    elif network_type == 3:
        color = '#00FF70'
    for i in range(0, len(path) - 1):
        sx = (x_coor[path[i]] - min_x) / den_x
        tx = (x_coor[path[i + 1]] - min_x) / den_x

        sy = (- y_coor[path[i]] - min_y) / den_y
        ty = (- y_coor[path[i + 1]] - min_y) / den_y
        if network_type == 2:
            pygame.draw.line(surface, color, (sx + start_pos_pix, sy + start_pos_pix),
                             (tx + start_pos_pix, ty + start_pos_pix), width=5)
        else:
            pygame.draw.line(surface, color, (sx + start_pos_pix, sy + start_pos_pix),
                             (tx + start_pos_pix, ty + start_pos_pix), width=3)


def display_text(screen, text, font, color, pos, width, height):
    text = font.render(text, True, color)
    text_rect = text.get_rect(center=pygame.Rect(pos, (width, height)).center)
    screen.blit(text, text_rect)
    pygame.display.update()


def get_index_point(screen, x_click, y_click, x_coor, y_coor, min_x, min_y, den_x, den_y):
    screen.fill('#FFFFFF', rect=pygame.Rect((1381, 720), (320, 60)))
    x_src, y_src = Pixel_to_utm(x_click - 1, y_click - 1, min_x, min_y, den_x, den_y)
    index = get_nearest_node(x_coor, y_coor, [x_src, y_src])
    pygame.display.update()
    return index


class Button:
    def __init__(self, text, width, height, pos, elevation, top_color, color_temp):
        self.press = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = top_color
        self.color_fixed = top_color
        self.color_temp = color_temp
        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_color = '#06237F'

        self.text_surf = gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(fake_screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(fake_screen, self.top_color, self.top_rect, border_radius=12)
        fake_screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.color_temp
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.press = True
            else:
                if self.press:
                    self.dynamic_elevation = self.elevation
                    self.press = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = self.color_fixed


class OptionBox():
    def __init__(self, x, y, w, h, color, highlight_color, font, option_list, selected=0):
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(surf, self.highlight_color if self.menu_active else self.color, self.rect, border_radius=12)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2, border_radius=12)
        msg = self.font.render(self.option_list[self.selected], 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(surf, self.highlight_color if i == self.active_option else self.color, rect)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))
            outer_rect = (
            self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.selected = self.active_option
                    self.draw_menu = False
                    return self.active_option
        return -1


def jam_state_enable(graph, path_jam):
    max_weight = 605.7  # Founded in Astar_algo.py
    jam_density = 10
    for i in range(0, len(path_jam) - 1):
        graph[path_jam[i]][path_jam[i + 1]][0]['weight'] = jam_density * max_weight


root = os.path.dirname(os.path.realpath(__file__))
image_dir = root + '\map\HCM_map.png'
graph_dir = root + '\graph'
data_dir = root + '\data'
logo_dir = root + '\logo.gif'

pygame.init()
pygame.display.set_caption("HCM map")
screen = pygame.display.set_mode((1700, 1000), RESIZABLE)
fake_screen = screen.copy()

image = pygame.image.load(image_dir)
gui_font = pygame.font.SysFont('cambriamath', 20)
title_font=pygame.font.SysFont('cambriamath', 40)
button_run = Button("FIND PATH", 150, 50, (1465, 800), 6, '#0032FF', '#00AAFF')
button_res = Button("RESTART", 150, 50, (1465, 870), 6, '#FD1414', '#FF5A5A')
net_option = OptionBox(1465, 400, 150, 30, (150, 150, 150), (100, 200, 255), gui_font, ["Car", "Motorbike"])
optimize_option = OptionBox(1465, 300, 150, 30, (150, 150, 150), (100, 200, 255), gui_font, ["Length", "Time"])

G = load_graph_gpickle(graph_dir + '\Graph_car.gpickle')
G_time = load_graph_gpickle(graph_dir + '\Graph_car_time.gpickle')
x_coor, y_coor = get_coordinate(data_dir + '\HCM_data_car.pycgr')
min_x, min_y, den_x, den_y = get_cache_map_gps(west=106.65258982689619, east=106.7185077956462, south=10.733603119492543, north=10.780486386368423, width=1378, height=998)
src_exist = False
des_exist = False
car = True
src_jam = False
length_opt = True
# car -- 0
# motorbike -- 1
# jam -- 2
# time -- 3

fake_screen.fill('#FFFFFF')
display_text(fake_screen, "TYPE:", gui_font, '#000000', (1410, 400), 30, 42)
display_text(fake_screen, "FROM", gui_font, '#000000', (1400, 550), 30, 42)
display_text(fake_screen, "TO", gui_font, '#000000', (1400, 650), 30, 42)
logo = GIFImage(logo_dir)

pygame.draw.rect(fake_screen, (0, 0, 0), (1450, 545, 240, 50), 2)
pygame.draw.rect(fake_screen, (0, 0, 0), (1450, 645, 240, 50), 2)
display_text(fake_screen, "Lat:", gui_font, '#000000', (1465, 550), 10, 21)
display_text(fake_screen, "Long:", gui_font, '#000000', (1475, 570), 10, 21)
display_text(fake_screen, "Lat:", gui_font, '#000000', (1465, 650), 10, 21)
display_text(fake_screen, "Long:", gui_font, '#000000', (1475, 670), 10, 21)
display_text(fake_screen, "Best Routing App", title_font, '#1E90FF', (1530, 220), 10, 21)
input_boxes = CreateInputBox()
coord = [0, 0, 0, 0]

while True:
    # if first_screen not pass
    # else...
    pygame.draw.rect(fake_screen, '#FFFFFF', pygame.Rect((0, 0), (1380, 1000)))
    fake_screen.blit(image, (1, 1))
    logo.render(fake_screen, (1395, 30))
    button_run.draw()
    button_res.draw()
    pygame.display.update()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        for box in input_boxes:
            box.handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                coord[input_boxes.index(box)] = box.ShowValue()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            x_src, y_src, _, _ = utm.from_latlon(float(coord[0]), float(coord[1]))
            x_des, y_des, _, _ = utm.from_latlon(float(coord[2]), float(coord[3]))
            x_src_graph, y_src_graph = utm_to_Pixel(x_src, y_src, min_x, min_y, den_x, den_y)
            x_des_graph, y_des_graph = utm_to_Pixel(x_des, y_des, min_x, min_y, den_x, den_y)

            if not src_exist:
                draw_src(image, x_src_graph, y_src_graph)
                src_exist = True
            else:
                draw_des(image, x_des_graph, y_des_graph)
                des_exist = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                x_click, y_click = pygame.mouse.get_pos()
                if x_click < 1379:
                    if not src_exist:
                        draw_src(image, x_click, y_click)
                        x_src_graph, y_src_graph = x_click, y_click
                        src_exist = True
                    else:
                        draw_des(image, x_click, y_click)
                        x_des_graph, y_des_graph = x_click, y_click
                        des_exist = True

                if button_run.press:
                    if not src_exist:
                        fake_screen.fill('#FFFFFF', rect=pygame.Rect((1381, 720), (320, 70)))
                        display_text(fake_screen, "NO SOURCE!", gui_font, '#FF0000', (1490, 720), 100, 100)
                    elif des_exist:
                        try:
                            index_src = get_index_point(fake_screen, x_src_graph, y_src_graph, x_coor, y_coor, min_x, min_y, den_x,
                                                        den_y)
                            index_des = get_index_point(fake_screen, x_des_graph, y_des_graph, x_coor, y_coor, min_x, min_y, den_x,
                                                        den_y)
                            start = time.time()
                            path = astar(G, index_src, index_des, x_coor, y_coor)
                            end = time.time()
                            path_time = astar(G_time, index_src, index_des, x_coor, y_coor)

                            if car:
                                if length_opt:
                                    draw_path(image, 0, path, x_coor, y_coor, min_x, min_y, den_x, den_y,
                                              start_pos_pix=1)
                                else:
                                    draw_path(image, 3, path_time, x_coor, y_coor, min_x, min_y, den_x, den_y,
                                              start_pos_pix=1)
                            else:
                                if length_opt:
                                    draw_path(image, 1, path, x_coor, y_coor, min_x, min_y, den_x, den_y,
                                              start_pos_pix=1)
                                else:
                                    draw_path(image, 3, path_time, x_coor, y_coor, min_x, min_y, den_x, den_y,
                                              start_pos_pix=1)
                                    # DISPLAY PATH_LENGTH HERE
                            fake_screen.fill('#FFFFFF', rect=pygame.Rect((1381, 690), (50, 70)))
                            display_text(fake_screen, f"Path length is {path_length(G,path):.4f} m",
                                         pygame.font.Font(None, 20), '#000000', (1490, 690), 100, 100)
                            fake_screen.fill('#FFFFFF', rect=pygame.Rect((1381, 720), (50, 70)))
                            display_text(fake_screen, f"Finding path in {(end - start):.4f} s",
                                         pygame.font.Font(None, 20), '#000000', (1490, 720), 100, 100)

                        except:
                            fake_screen.fill('#FFFFFF', rect=pygame.Rect((1381, 720), (320, 70)))
                            display_text(fake_screen, "Can't find path, try again!", gui_font, '#FF0000', (1490, 720),
                                         100, 100)
                    else:
                        fake_screen.fill('#FFFFFF', rect=pygame.Rect((1381, 720), (320, 70)))
                        display_text(fake_screen, "NO DESTINATION!", gui_font, '#FF0000', (1490, 720), 100, 100)
                # Restart button
                if button_res.press:
                    image = pygame.image.load(image_dir)
                    src_exist = False
                    des_exist = False
                    src_jam = False
                    if car:
                        G = load_graph_gpickle(graph_dir + '\Graph_car.gpickle')
                        G_time = load_graph_gpickle(graph_dir + '\Graph_car_time.gpickle')
                    else:
                        G = load_graph_gpickle(graph_dir + '\Graph_motorbike.gpickle')
                        G_time = load_graph_gpickle(graph_dir + '\Graph_motorbike_time.gpickle')
                    fake_screen.fill('#FFFFFF', rect=pygame.Rect((1381, 720), (320, 70)))

            if event.button == 3:
                x_click, y_click = pygame.mouse.get_pos()
                if x_click < 1379:
                    if not src_jam:
                        x_src_jam, y_src_jam = x_click, y_click
                        draw_traffic_point(image, x_click, y_click)
                        src_jam = True
                    else:
                        draw_traffic_point(image, x_click, y_click)
                        index_src_jam = get_index_point(fake_screen, x_src_jam, y_src_jam, x_coor, y_coor, min_x, min_y,
                                                        den_x, den_y)
                        index_des_jam = get_index_point(fake_screen, x_click, y_click, x_coor, y_coor, min_x, min_y,
                                                        den_x, den_y)
                        path_jam = astar(G, index_src_jam, index_des_jam, x_coor, y_coor)
                        # Increase weight
                        jam_state_enable(G, path_jam)
                        draw_path(image, 2, path_jam, x_coor, y_coor, min_x, min_y, den_x, den_y, start_pos_pix=1)
                        src_jam = False
    for box in input_boxes:
        box.update()
    pygame.draw.rect(fake_screen, (255, 255, 255), (1510, 550, 160, 20))
    pygame.draw.rect(fake_screen, (255, 255, 255), (1510, 570, 160, 20))
    pygame.draw.rect(fake_screen, (255, 255, 255), (1510, 650, 160, 20))
    pygame.draw.rect(fake_screen, (255, 255, 255), (1510, 670, 160, 20))

    for box in input_boxes:
        box.draw(fake_screen)

    fake_screen.fill('#FFFFFF', rect=pygame.Rect((1381, 430), (320, 60)))
    graph = net_option.update(events)
    if graph == 0:
        display_text(screen, "LOADING...", gui_font, '#000000', (1535, 490), 20, 20)
        src_jam = False
        G = load_graph_gpickle(graph_dir + '\Graph_car.gpickle')
        G_time = load_graph_gpickle(graph_dir + '\Graph_car_time.gpickle')
        x_coor, y_coor = get_coordinate(data_dir + '\HCM_data_car.pycgr')
        fake_screen.fill('#FFFFFF', rect=pygame.Rect((1381, 490), (320, 20)))
        car = True
    elif graph == 1:
        src_jam = False
        display_text(screen, "LOADING...", gui_font, '#000000', (1535, 490), 20, 20)
        G = load_graph_gpickle(graph_dir + '\Graph_motorbike.gpickle')
        G_time = load_graph_gpickle(graph_dir + '\Graph_motorbike_time.gpickle')
        x_coor, y_coor = get_coordinate(data_dir + '\HCM_data_motorbike.pypgr')
        fake_screen.fill('#FFFFFF', rect=pygame.Rect((1381, 490), (320, 20)))
        car = False
    net_option.draw(fake_screen)

    fake_screen.fill('#FFFFFF', rect=pygame.Rect((1381, 330), (320, 60)))
    opt = optimize_option.update(events)
    if opt == 0:
        length_opt = True
    elif opt == 1:
        length_opt = False
    optimize_option.draw(fake_screen)

    screen.blit(pygame.transform.scale(fake_screen, screen.get_rect().size), (0, 0))
    pygame.display.update()