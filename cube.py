import math
import random
import csv
screenscale=12
edge_char="*"
corner_char="#"
def save_csv(vert, edges, filename="custom_shape.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "a", "b", "c"])    
        for x, y, z in vert:
            writer.writerow(["v", x, y, z])         
        for s, e in edges:
            writer.writerow(["e", s, e, ""])
    print("Saved to", filename)
def cube_draw():
    vert=[(x,y,z) for x in (-1,1) for y in (-1,1) for z in (-1,1)]
    edges = {(0,1), (0,2), (0,4), (1,3), (1,5), (2,3),
             (2,6), (3,7), (4,5), (4,6), (5,7), (6,7)}
    return vert,edges
def custom_draw():
    vert=[]
    a=int(input("number of points"))
    i=0
    while(i<a):
        x=int(input("Enter x cordinate"))
        y=int(input("Enter y cordinate"))
        z=int(input("Enter z cordinate"))
        vert.append((x,y,z))
        i+=1
    edges = []#1.List
    e = int(input("Number of edges: "))
    for i in range(e):
        start = int(input(f"Edge {i} - start vertex "))
        end = int(input(f"Edge {i} "))
        if 0 <= start < a and 0 <= end < a and start != end:
            edges.append((start, end))
        else:
            print("Invalid edge, skipped.")
    if input("Save this shape to CSV? y/n ")=="y":
        save_csv(vert, edges)
    return vert, edges
def load_csv(filename="custom_shape.csv"):
    vert, edges = [], []
    with open(filename, newline="") as f:
        for row in csv.reader(f):
            if row[0] == "v":
                vert.append((float(row[1]), float(row[2]), float(row[3])))
            elif row[0] == "e":
                edges.append((int(row[1]), int(row[2])))
    return vert, edges    
def sphere_draw(rings=4,points=10):
    verts=[]
    edges=set()
    for r in range(rings):
        lat=math.radians(-90+180*(r+1)/(rings+1)) 
        for k in range(points):
            lon=2*math.pi*k/points
            verts.append((math.cos(lat)*math.cos(lon),math.sin(lat),math.cos(lat)*math.sin(lon)))
    for r in range(rings):
        for k in range(points):
            here=r*points+k
            edges.add((here,r*points+(k+1)%points))
            if r<rings-1:
                edges.add((here,here+points))
    south=len(verts); verts.append((0,-1,0))
    north=len(verts); verts.append((0,1,0))
    for k in range(points):
        edges.add((south,k))
        edges.add((north,(rings-1)*points+k))
    return verts,edges
W,H,DIST=80,30,10
SHAPES={"cube":cube_draw,"sphere":sphere_draw,"custom":custom_draw,"load":load_csv}
def projection(points):
    scale=DIST/(points[2]+DIST)
    return int(W/2+points[0]*scale*screenscale),int(H/2-points[1]*scale*(screenscale/2))
def render_screen(verts,edges):
    screen=[[" "]*W for _ in range(H)]
    points=[projection(vert) for vert in verts
    for i,j in edges:
        c1,r1=points[i]
        c2,r2=points[j]
        n=max(abs(c2-c1),abs(r2-r1),1)
        for k in range(n+1):
            c=round(c1+(c2-c1)*k/n)
            r=round(r1+(r2-r1)*k/n)
            if 0<=c<W and 0<=r<H:
                screen[r][c]=edge_char
        if 0<=c1<W and 0<=r1<H: 
            screen[r1][c1]=corner_char
        if 0<=c2<W and 0<=r2<H: 
            screen[r2][c2]=corner_char               
    for row in screen:
        print("".join(row))
def rotate_points(verts,angles):
    to_radians=lambda deg:math.radians(deg)
    spin=lambda pt1,pt2,angle:(pt1*math.cos(angle)-pt2*math.sin(angle),pt2*math.cos(angle)+pt1*math.sin(angle))
    ax,ay,az=to_radians(angles["x"]),to_radians(angles["y"]),to_radians(angles["z"])
    rotated_points=[]
    for x,y,z in verts:
        y, z = spin(y, z, ax) 
        z, x = spin(z, x, ay)
        x, y = spin(x, y, az)
        rotated_points.append((x, y, z))
    return rotated_points       
class Main:
    def __init__(self):
        self._state = {}
    def __choose_state(self):
        random_generation = bool("y" == input("Generate randomly or choose y for yes"))
        if not random_generation:
            self._state = {"shape": input("Enter the shape cube/sphere/custom/load"),
                           "angles": {"x": int(input("Enter angle about x")),
                                      "y": int(input("Enter angle about y")),
                                      "z": int(input("Enter angle about z"))}}
        elif random_generation:
            self._state = {"shape": random.choice(["cube", "sphere"]),
                           "angles": {axis: random.randint(0, 359) for axis in "xyz"}}
        else:
             print("Unknown error")
        print(self._state)     
    def run(self): 
        self.__choose_state()
        verts, edges = SHAPES[self._state["shape"]]()
        biggest = max(max(abs(c) for c in v) for v in verts) or 1  
        verts = [(x/biggest, y/biggest, z/biggest) for x, y, z in verts]
        render_screen(rotate_points(verts, self._state["angles"]), edges)
app = Main() 
app.run()
