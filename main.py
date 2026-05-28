Web VPython 3.2
# messing around to get familar with coordinate system and mechanics
scene.background = color.white
scene.autoscale = False # manually control scene.camera.pos
fps = 60

box_L = 3
box_H = 3
wall_thickness = 0.5
mass_box = 1
mass_pendulum = 1

myBox = compound([box(length=box_L,height=box_H,width=0.01,color=color.black), box(length=box_L-wall_thickness,height=box_H-wall_thickness,width=0.01,color=color.white)])

L = 1
R = 0.25

myPendulum = compound([sphere(radius=R,pos=vec(0,0,0)), box(length=0.1,height=L,width=0.01,color=color.black,pos=vec(0,L/2+R,0))])

myPendulum.pos = -myPendulum.size + vec(box_L/2-2*wall_thickness,box_H-2*wall_thickness, 1)
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
v_box = vec(0,0,0)
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
    
    v_box += vec(-a*mass_pendulum/mass_box/fps,0,0)
    
    displacement = v*1/fps
    ang_displacement = omega*1/fps
    
    theta += ang_displacement
    
    displacement_box = v_box*1/fps
    
    myPendulum.pos += displacement + displacement_box
    myBox.pos += displacement_box
    myPendulum.rotate(axis=vec(0,0,1),angle=ang_displacement,origin=vec(0,0,0))
