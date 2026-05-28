Web VPython 3.2
# messing around to get familar with coordinate system and mechanics
scene.background = color.white
scene.autoscale = False # manually control scene.camera.pos
fps = 60

# This is probably what we are going to use for the pendulum stuffs
box_L = 3
box_H = 3
wall_thickness = 0.5

myBox = compound([box(length=box_L,height=box_H,width=0.01,color=color.black), box(length=box_L-wall_thickness,height=box_H-wall_thickness,width=0.01,color=color.white)])

L = 2
R = 0.25

myPendulum = compound([sphere(radius=R,pos=vec(0,0,0)), box(length=0.1,height=L,width=0.01,color=color.black,pos=vec(0,L/2+R,0))])
print(myPendulum.size)
myPendulum.pos = vec(0,0,0.02)
# Maybe implement by changing the space between the spring wraps instead of trying to texture a box to somehow do this
class Spring:
    pass

bg = box(length=20,height=20,width=1e-3,texture="https://i.imgur.com/YknYWNh.jpeg")

# load textures
scene.visible = False
scene.waitfor("textures")
scene.visible = True

ticks = 0
v = vec(0,0,0)
omega = 0
g=9.81
theta=0.1

myPendulum.rotate(axis=vec(0,0,1),angle=theta,origin=vec(0,0,0))

while True:
    rate(fps)
    ticks+=1
    sec = ticks/fps
    
    a=-g*sin(theta)
    alpha=a/L
    
    v += vec(a/fps,0,0)
    omega += alpha/fps
    
    displacement = v*1/fps
    ang_displacement = omega*1/fps
    theta += ang_displacement
    
    myPendulum.pos += displacement
    myBox.pos += displacement
    myPendulum.rotate(axis=vec(0,0,1),angle=ang_displacement,origin=vec(0,0,0))
