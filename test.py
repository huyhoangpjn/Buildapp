# start = time.time()
# G = load_graph_gpickle("Graph.gpickle")
# end = time.time()

# x_coor, y_coor = get_coordinate('Q10.pycgr')

# # print(astar(G,4,100,x_coor,y_coor))
# print(nx.shortest_path(G,4,100,weight="weight"))

# print('Completed in: ',end-start)


# x_coor, y_coor = get_coordinate('Q10.pycgr')
# G = load_graph_gpickle("Graph.gpickle")
# start = time.time()
# path = nx.shortest_path(G,4,4200,weight="weight")
# end = time.time()
# print(path)
# draw_shortest_path("Map.png",path,x_coor,y_coor)
# print('Completed in: ',end-start)

# import networkx as nx
# import matplotlib.pyplot as plt
# G = nx.MultiDiGraph()
# edge = [(1,2,3),(2,1,3),(4,5,6)]
# G.add_weighted_edges_from(edge)
# print(G[0])
# nx.draw(G,with_labels=True)
# plt.show()

# import pygame
# import os

# window = pygame.display.set_mode((1700, 1000), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
# map =  pygame.image.load('HCM_map.png')
# maprect = pygame.Rect(1,1,1378,999)
# mapsurface = map
# run = True
# while run:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
        
#         elif event.type == pygame.VIDEORESIZE:
#             window = pygame.display.set_mode(event.dict['size'], pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
#             mapsurface = pygame.transform.smoothscale(map, maprect.size)
        
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             if event.button == 4 or event.button == 5:
#                 zoom = 2.5 if event.button == 4 else 0.8
#                 mx, my = event.pos
#                 left   = mx + (maprect.left - mx) * zoom
#                 right  = mx + (maprect.right - mx) * zoom
#                 top    = my + (maprect.top - my) * zoom
#                 bottom = my + (maprect.bottom - my) * zoom
#                 maprect = pygame.Rect(left, top, right-left, bottom-top)

#                 mapsurface = pygame.transform.smoothscale(map, (right-left, bottom-top))
                
#     window.fill(0)
#     window.blit(mapsurface, maprect,(1378,999))
#     pygame.display.flip()

# pygame.quit()
# exit()

# import os
# import pygame

# class ScaleSprite(pygame.sprite.Sprite):
#     def __init__(self, center, image):
#         super().__init__()
#         self.original_image = image
#         self.image = image
#         self.rect = self.image.get_rect(center = center)
#         self.mode = 1
#         self.grow = 0

#     def update(self):
#         if self.grow > 100:
#             self.mode = -1
#         if self.grow < 1:
#             self.mode = 1
#         self.grow += 1 * self.mode 

#         orig_x, orig_y = self.original_image.get_size()
#         size_x = orig_x + round(self.grow)
#         size_y = orig_y + round(self.grow)
#         self.image = pygame.transform.scale(self.original_image, (size_x, size_y))
#         self.rect = self.image.get_rect(center = self.rect.center)

# pygame.init()
# window = pygame.display.set_mode((1600, 1000))
# clock = pygame.time.Clock()
# img = pygame.image.load("HCM_map.png")
# sprite = ScaleSprite(img.get_rect().center, img)
# group = pygame.sprite.Group(sprite)

# run = True
# while run:
#     clock.tick(60)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False

#     group.update()

#     window.fill(0)
#     group.draw(img)
#     pygame.display.flip()

# pygame.quit()
# exit()

# import pygame

# class OptionBox():

#     def __init__(self, x, y, w, h, color, highlight_color, font, option_list, selected = 0):
#         self.color = color
#         self.highlight_color = highlight_color
#         self.rect = pygame.Rect(x, y, w, h)
#         self.font = font
#         self.option_list = option_list
#         self.selected = selected
#         self.draw_menu = False
#         self.menu_active = False
#         self.active_option = -1

#     def draw(self, surf):
#         pygame.draw.rect(surf, self.highlight_color if self.menu_active else self.color, self.rect)
#         pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
#         msg = self.font.render(self.option_list[self.selected], 1, (0, 0, 0))
#         surf.blit(msg, msg.get_rect(center = self.rect.center))

#         if self.draw_menu:
#             for i, text in enumerate(self.option_list):
#                 rect = self.rect.copy()
#                 rect.y += (i+1) * self.rect.height
#                 pygame.draw.rect(surf, self.highlight_color if i == self.active_option else self.color, rect)
#                 msg = self.font.render(text, 1, (0, 0, 0))
#                 surf.blit(msg, msg.get_rect(center = rect.center))
#             outer_rect = (self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
#             pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)

#     def update(self, event_list):
#         mpos = pygame.mouse.get_pos()
#         self.menu_active = self.rect.collidepoint(mpos)
        
#         self.active_option = -1
#         for i in range(len(self.option_list)):
#             rect = self.rect.copy()
#             rect.y += (i+1) * self.rect.height
#             if rect.collidepoint(mpos):
#                 self.active_option = i
#                 break

#         if not self.menu_active and self.active_option == -1:
#             self.draw_menu = False

#         for event in event_list:
#             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                 if self.menu_active:
#                     self.draw_menu = not self.draw_menu
#                 elif self.draw_menu and self.active_option >= 0:
#                     self.selected = self.active_option
#                     self.draw_menu = False
#                     return self.active_option
#         return -1

# pygame.init()
# clock = pygame.time.Clock()
# window = pygame.display.set_mode((640, 480))

# list1 = OptionBox(
#     40, 40, 160, 40, (150, 150, 150), (100, 200, 255), pygame.font.SysFont(None, 30), 
#     ["option 1", "2nd option", "another option"])

# run = True
# while run:
#     clock.tick(60)
#     event_list = pygame.event.get()
#     for event in event_list:
#         if event.type == pygame.QUIT:
#             run = False

#     selected_option = list1.update(event_list)
#     if selected_option >= 0:
#         print(selected_option)

#     window.fill((255, 255, 255))
#     list1.draw(window)
#     pygame.display.flip()
    
# pygame.quit()
# exit()
import os
root = os.path.dirname(os.path.realpath(__file__))
print(root)