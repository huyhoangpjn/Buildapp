from readfile import read_file
import utm
from PIL import Image, ImageDraw, ImageColor

#DRAW_MAP READ PYCGR FILE
def draw_map(filename,width,height,output_cache,output_name):
    nodes, edges = read_file(filename)
    lines = []
    max_x, max_y = float("-inf"), float("-inf")
    min_x, min_y = float("inf"), float("inf")

    for e in edges:
        if (e.source_id not in nodes) or (e.target_id not in nodes):
            print(f"didn't find {e.source_id} or {e.target_id}")
            continue

        s, t = nodes[e.source_id], nodes[e.target_id]
        sx, sy, _, _ = utm.from_latlon(s.lat, s.lon)
        tx, ty, _, _ = utm.from_latlon(t.lat, t.lon)
        sy, ty = -sy, -ty  # need to invert y coordinates
        lines.append(((sx, sy), (tx, ty), e.max_speed))
        max_x, max_y = max(max_x, sx, tx), max(max_y, sy, ty)
        min_x, min_y = min(min_x, sx, tx), min(min_y, sy, ty)

    picture_width = width
    picture_height = height
    denominator_x = (max_x - min_x) / picture_width
    denominator_y = (max_y - min_y) / picture_height
    im = Image.new("RGB", (picture_width, picture_height), "#FFF")
    draw = ImageDraw.Draw(im)
    for line_data in lines:
        # prepare coordinates to draw
        sx = (line_data[0][0] - min_x) / denominator_x
        tx = (line_data[1][0] - min_x) / denominator_x

        sy = (line_data[0][1] - min_y) / denominator_y
        ty = (line_data[1][1] - min_y) / denominator_y

        line = ((sx, sy), (tx, ty))

        # determine color
        max_speed = line_data[2]
        luminosity = max(-8.0 / 5.0 * max_speed + 70.0, 0)
        color = ImageColor.getrgb(f"hsl(233, 74%, {luminosity}%)")

        # draw line
        draw.line(line, fill=color,width=1)
    with open(output_cache,"w") as f:
        f.write(str(min_x)+'\n')
        f.write(str(min_y)+'\n')
        f.write(str(denominator_x)+'\n')
        f.write(str(denominator_y)+'\n')
        f.close()

    del draw
    im.save(output_name, "PNG")

def get_cache_map(filename):
    with open(filename) as f:
        lines = f.readlines()
        min_x = float(lines[0])
        min_y = float(lines[1])
        den_x = float(lines[2])
        den_y = float(lines[3]) 
    return min_x,min_y, den_x, den_y

#DRAW SHORTEST PATH
def draw_shortest_path(filename,path,x_coor,y_coor):
    min_x,min_y,den_x,den_y = get_cache_map("cache.txt")
    im = Image.open(filename)
    draw = ImageDraw.Draw(im)
    for i in range(0,len(path)-1):
        sx = (x_coor[path[i]] - min_x) / den_x
        tx = (x_coor[path[i+1]] - min_x) / den_x

        sy = (-y_coor[path[i]] - min_y) / den_y
        ty = (-y_coor[path[i+1]] - min_y) / den_y
        draw.line(((sx, sy),(tx, ty)),fill="red",width=2)

    del draw
    im.save("Map_with_shortest_path.png", "PNG")

#draw_map("HCM_data_motorbike.pypgr",1378,999,"cache_motorbike.txt","Motorbike_route.png")