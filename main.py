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
L = 1
R = 0.25
g=9.81
isPaused = False

def modifyL(evt):
    global L, isPaused
    L = evt.value
    isPaused = True

def modifyR(evt):
    global R, isPaused
    R = evt.value
    isPaused = True

widgets = []

def setup():
    global myPendulum, myBox, scene
    global widgets, isPaused
    global ticks, v, v_box, omega, theta
    for widget in widgets:
        widget.delete()
    widgets = []
    
    scene.delete()
    scene = canvas()
    scene.select()
    scene.background = color.white
    scene.autoscale = False # manually control scene.camera.pos

    myBox = compound([box(length=box_L,height=box_H,width=0.01,color=color.black), box(length=box_L-wall_thickness,height=box_H-wall_thickness,width=0.01,color=color.white)])
    myBox.pos = vec(0,0,0)

    myPendulum = compound([sphere(radius=R,pos=vec(0,0,0)), box(length=0.1,height=L,width=0.01,color=color.black,pos=vec(0,L/2+R,0))])

    myPendulum.pos = myBox.pos + vec(wall_thickness/2,box_H/2-wall_thickness/2,0) - myPendulum.size/2
    myPendulum.pos.z = 1

    # For spring use helix()
    
    #bg = box(length=20,height=20,width=1e-3,texture="https://i.imgur.com/YknYWNh.jpeg")
    
    # load textures
    scene.visible = False
    scene.waitfor("textures")
    scene.visible = True

    ticks = 0
    v = vec(0,0,0)
    v_box = vec(0,0,0)
    omega = 0
    theta=0.2

    myPendulum.rotate(axis=vec(0,0,1),angle=theta,origin=myPendulum.pos+vec(0, L/2 + R, 0))

    resetButton = button(bind=setup,text='reset')
    Lslider = slider(bind=modifyL,min=0.5,max=2,value=L)
    Rslider = slider(bind=modifyR,min=0.1,max=0.5,value=R)
    widgets.append(resetButton)
    widgets.append(Lslider)
    widgets.append(Rslider)
    
    isPaused = False

setup()
while True:
    rate(fps)
    if isPaused:
        continue
    ticks+=1
    sec = ticks/fps
    
    a = -g*sin(theta)
    alpha = a/L
    
    omega += alpha/fps
    
    force_pendulum_on_box = -a * mass_pendulum
    
    v_box += vec(force_pendulum_on_box/mass_box/fps, 0, 0)
    
    ang_displacement = omega*1/fps
    theta += ang_displacement
    
    displacement_box = v_box*1/fps
    
    myPendulum.pos += displacement_box
    myBox.pos += displacement_box
    myPendulum.rotate(axis=vec(0,0,1),angle=ang_displacement,origin=myPendulum.pos+vec(0, L/2 + R, 0))
