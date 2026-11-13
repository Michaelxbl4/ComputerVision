"""
Concepts   
 1. List, Tuple, Random number generation
 2. Tuple, Set, Dictionary, Strings
 3. Classes and Objects, access modifiers
 4. Lambda, for, while, if, elif
 6. Files and CSV
"""
import math
import random
import csv
screenscale=12
edge_char="*"#2.Strings
corner_char="#"
def save_csv(vert, edges, filename="custom_shape.csv"):#6. Files and CSV
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "a", "b", "c"])    
        for x, y, z in vert:
            writer.writerow(["v", x, y, z])         
        for s, e in edges:
            writer.writerow(["e", s, e, ""])
    print("Saved to", filename)
def cube_draw():
    vert=[(x,y,z) for x in (-1,1) for y in (-1,1) for z in (-1,1)]#list of tupples
    edges = {(0,1), (0,2), (0,4), (1,3), (1,5), (2,3),
             (2,6), (3,7), (4,5), (4,6), (5,7), (6,7)}#set
    return vert,edges
def custom_draw():
    vert=[]#1.List
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
def load_csv(filename="custom_shape.csv"):#4. for, while, if, elif
    vert, edges = [], []
    with open(filename, newline="") as f:
        for row in csv.reader(f):
            if row[0] == "v":
                vert.append((float(row[1]), float(row[2]), float(row[3])))
            elif row[0] == "e":
                edges.append((int(row[1]), int(row[2])))
    return vert, edges    #1.List
def sphere_draw(rings=4,points=10):
    verts=[]#list of tuples
    edges=set()#set of index pairs
    for r in range(rings):#one latitude ring at a time
        lat=math.radians(-90+180*(r+1)/(rings+1))#evenly spaced, never exactly at a pole Logic:-90 is south pole +90 is north pole so we have dist of 180 degree so if we divide it into n+1 parts using n latgitude or rings its like 1 to n180/n+1 + -90 or -1 to n180/n+1 + 90 
        for k in range(points):
            lon=2*math.pi*k/points#evenly spaced around the ring
            verts.append((math.cos(lat)*math.cos(lon),math.sin(lat),math.cos(lat)*math.sin(lon)))
    for r in range(rings):
        for k in range(points):
            here=r*points+k#index of ring r, point k
            edges.add((here,r*points+(k+1)%points))#to the next point on the ring (% wraps around)
            if r<rings-1:
                edges.add((here,here+points))#up to the same point on the next ring
    south=len(verts); verts.append((0,-1,0))#bottom pole
    north=len(verts); verts.append((0,1,0))#top pole
    for k in range(points):
        edges.add((south,k))#south pole to the bottom ring
        edges.add((north,(rings-1)*points+k))#north pole to the top ring
    return verts,edges
W,H,DIST=80,30,10
SHAPES={"cube":cube_draw,"sphere":sphere_draw,"custom":custom_draw,"load":load_csv}#dictionary
def projection(points):
    scale=DIST/(points[2]+DIST)# farther points appear small we will first get what point should be where for a normal cube then rotate it
    return int(W/2+points[0]*scale*screenscale),int(H/2-points[1]*scale*(screenscale/2))
def render_screen(verts,edges):#2.Strings
    screen=[[" "]*W for _ in range(H)]#list of lists _ means repeatin [" "]*W number of times of screen heght so right now screen is just with " "" "...for height of screen
    points=[projection(vert) for vert in verts]#points have every corner to be plotted
    for i,j in edges:#joining edges
        c1,r1=points[i]
        c2,r2=points[j]
        n=max(abs(c2-c1),abs(r2-r1),1)#1 is to avoid divide by zero
        for k in range(n+1):
            c=round(c1+(c2-c1)*k/n)
            r=round(r1+(r2-r1)*k/n)
            if 0<=c<W and 0<=r<H:
                screen[r][c]=edge_char
        if 0<=c1<W and 0<=r1<H: 
            screen[r1][c1]=corner_char
        if 0<=c2<W and 0<=r2<H: 
            screen[r2][c2]=corner_char               
    for row in screen:#4.for, while, if, elif
        print("".join(row))
def rotate_points(verts,angles):
    to_radians=lambda deg:math.radians(deg)#4.Lambda
    spin=lambda pt1,pt2,angle:(pt1*math.cos(angle)-pt2*math.sin(angle),pt2*math.cos(angle)+pt1*math.sin(angle))#4. Lambda
    ax,ay,az=to_radians(angles["x"]),to_radians(angles["y"]),to_radians(angles["z"])
    rotated_points=[]
    for x,y,z in verts:
        y, z = spin(y, z, ax) 
        z, x = spin(z, x, ay)
        x, y = spin(x, y, az)
        rotated_points.append((x, y, z))
    return rotated_points       
class Main:#3.Classes and objects
    def __init__(self):
        self._state = {}#protected variable
    def __choose_state(self):#private method
        random_generation = bool("y" == input("Generate randomly or choose y for yes"))
        if not random_generation:
            self._state = {"shape": input("Enter the shape cube/sphere/custom/load"),
                           "angles": {"x": int(input("Enter angle about x")),
                                      "y": int(input("Enter angle about y")),
                                      "z": int(input("Enter angle about z"))}}
        elif random_generation:
            self._state = {"shape": random.choice(["cube", "sphere"]),
                           "angles": {axis: random.randint(0, 359) for axis in "xyz"}}#1.Random
        else:
             print("Unknown error")
        print(self._state)     
    def run(self): #public method
        self.__choose_state()
        verts, edges = SHAPES[self._state["shape"]]()
        biggest = max(max(abs(c) for c in v) for v in verts) or 1   # prolem was some shapes were too big in custom so scales tjem down
        verts = [(x/biggest, y/biggest, z/biggest) for x, y, z in verts]
        render_screen(rotate_points(verts, self._state["angles"]), edges)
app = Main() #create the object
app.run()#call it