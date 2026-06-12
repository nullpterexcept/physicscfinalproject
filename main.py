Web VPython 3.2
scene.background = color.white
scene.autoscale = False # manually control scene.camera.pos
scene.userzoom = False
scene.range /= 3

wheel_image = textures.granite
fps = 60

box_L = 3
box_H = 3
wall_thickness = 0.5
mass_box = 1
mass_bob = 1
L = 1
R = 0.25
g = 9.81
lastPick = None

def modifyL(evt):
    global L, paramWidgets
    L = evt.value
    paramWidgets["Llabel"].text = f"L = {L}m"
    createPendulum()

def modifyR(evt):
    global R, paramWidgets
    R = evt.value
    paramWidgets["Rlabel"].text = f"R = {R}m"
    createPendulum()

def modifyMassBob(evt):
    global mass_bob, paramWidgets
    mass_bob = evt.value
    paramWidgets["MBobLabel"].text = f"mass_bob = {mass_bob}kg"

def modifyMassBox(evt):
    global mass_box, paramWidgets
    mass_box = evt.value
    paramWidgets["MBoxLabel"].text = f"mass_box = {mass_box}kg"

def createPendulum():
    global myPendulum, myBox, theta
    if myPendulum:
        myPendulum.visible = False
    myPendulum = compound([sphere(radius=R,pos=vec(0,0,0)), box(length=0.1,height=L,width=0.01,color=color.black,pos=vec(0,L/2+R,0))])
    myPendulum.pos = myBox.pos + vec(wall_thickness/2,box_H/2-wall_thickness/2,0) - myPendulum.size/2
    # Default is good for 2x zoom, adding line below for 3x zoom
    myPendulum.pos.y -= wall_thickness/3
    myPendulum.pos.z = 1
    
    myPendulum.rotate(axis=vec(0,0,1),angle=theta,origin=myPendulum.pos+vec(0, L/2 + R, 0))
paramWidgets = {}
sysParamWidgets = {}
graphs = {}
resetButton = button(bind=setup,text='reset')

def setup():
    global myPendulum, myBox, leftWheel, rightWheel, scene
    global paramWidgets, graphs, sysParamWidgets
    global ticks, v, v_box, omega, theta
    
    ticks = 0
    v = vec(0,0,0)
    v_box = vec(0,0,0)
    omega = 0
    theta=0.2

    for obj in scene.objects:
        obj.visible = False

    for g in graphs.values():
        g.delete()

    for widget in sysParamWidgets.values():
        widget.delete()
    
    for widget in paramWidgets.values():
        widget.delete()

    myBox = compound([box(length=box_L,height=box_H,width=0.01,color=color.black), box(length=box_L-wall_thickness,height=box_H-wall_thickness,width=0.01,color=color.white)])
    leftWheel = cylinder(radius=box_L/12,axis=vec(0,0,1),length=0.01,pos=vec(-box_L/2+box_L/12,-box_H/2-box_L/12,0),texture=wheel_image)
    rightWheel = cylinder(radius=box_L/12,axis=vec(0,0,1),length=0.01,pos=vec(box_L/2-box_L/12,-box_H/2-box_L/12,0),texture=wheel_image)
    
    myBox.pos = vec(0,0,0)
    myGround = box(length=scene.width,height=0.1,color=color.black)
    myGround.pos.y = -box_H/2-box_L/12*2-0.1

    createPendulum()

    # For spring use helix()
    
    #bg = box(length=20,height=20,width=1e-3,texture="https://i.imgur.com/YknYWNh.jpeg")
    
    # load textures
    scene.visible = False
    scene.waitfor("textures")
    scene.visible = True

    scene.bind('click',onClick)
    #graphs["xVelocityBoxGraph"] = graph(title='x velocity Box', ytitle='m/s', xtitle='s', xmin=0, ymin=-20, align='left')
    #graphs["xVelocityBoxCurve"] = gcurve()

    #graphs["xVelocityPendulumGraph"] = graph(title='x velocity Pendulum' , ytitle='m/s', xtitle='t', xmin=0, ymin=-20, align='right')
    #graphs["xVelocityPendulumCurve"] = gcurve()
    
    # TODO: Figure out how to better control graph pos besides alignment...
    graphs["xVelocityCOMGraph"] = graph(title='x velocity COM' , ytitle='m/s', xtitle='t', xmin=0, ymin=-20, align='left')
    graphs["xVelocityCOMCurve"] = gcurve()
    
    graphs["yVelocityCOMGraph"] = graph(title='y velocity COM' , ytitle='m/s', xtitle='t', xmin=0, ymin=-20, align='right')
    graphs["yVelocityCOMCurve"] = gcurve()

def onClick():
    global myPendulum, myBox, scene
    global paramWidgets, lastPick
    if scene.mouse.pick == myPendulum:
        for widget in paramWidgets.values():
            widget.delete()
        paramWidgets = {}
        paramWidgets["Lslider"] = slider(bind=modifyL,min=0.5,max=2,value=L)
        paramWidgets["Llabel"] = wtext(text=f"L = {L}m")
        paramWidgets["Rslider"] = slider(bind=modifyR,min=0.1,max=0.5,value=R)
        paramWidgets["Rlabel"] = wtext(text=f"R = {R}m")
        paramWidgets["MBobSlider"] = slider(bind=modifyMassBob,min=0.5,max=10,value=mass_bob)
        paramWidgets["MBobLabel"] = wtext(text=f"mass_bob = {mass_bob}kg")
    elif scene.mouse.pick == myBox:
        for widget in paramWidgets.values():
            widget.delete()
        paramWidgets = {}
        paramWidgets["MBoxSlider"] = slider(bind=modifyMassBox,min=0.5,max=10,value=mass_box)
        paramWidgets["MBoxLabel"] = wtext(text=f"mass_box = {mass_box}kg")
    else:
        for widget in paramWidgets.values():
            widget.delete()
    lastPick = scene.mouse.pick
setup()

while True:
    rate(fps)
    ticks+=1
    sec = ticks/fps
    
    a = -g*sin(theta)
    alpha = a/(L+R)
    
    omega += alpha/fps
    
    force_pendulum_on_box = -mass_box * mass_bob / (mass_box + mass_bob) * a * cos(theta)
    
    v_box += vec(force_pendulum_on_box/mass_box/fps, 0, 0)
    #graphs["xVelocityBoxCurve"].plot(sec,v_box.x)
    
    v_bob_rel = (L+R)*omega*vec(cos(theta),sin(theta),0)
    v_bob = v_box + v_bob_rel
    #graphs["xVelocityPendulumCurve"].plot(sec, v_bob.x)
    
    v_com = (mass_box*v_box + mass_bob*v_bob)/(mass_box+mass_bob)
    graphs["xVelocityCOMCurve"].plot(sec, v_com.x)
    graphs["yVelocityCOMCurve"].plot(sec, v_com.y)
    
    #print(v_com)
    
    ang_displacement = omega*1/fps
    theta += ang_displacement
    
    displacement_box = v_box*1/fps
    ang_displacement_wheel = -displacement_box.x / (box_L/12)
    
    myPendulum.pos += displacement_box
    myBox.pos += displacement_box
    leftWheel.pos += displacement_box
    rightWheel.pos += displacement_box
    myPendulum.rotate(axis=vec(0,0,1),angle=ang_displacement,origin=myPendulum.pos+vec(0, L/2 + R, 0))
    leftWheel.rotate(axis=vec(0,0,1),angle=ang_displacement_wheel)
    rightWheel.rotate(axis=vec(0,0,1),angle=ang_displacement_wheel)
