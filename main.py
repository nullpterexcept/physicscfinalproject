Web VPython 3.2
# messing around to get familar with coordinate system and mechanics
scene.background = color.white
scene.autoscale = False # manually control scene.camera.pos
fps = 60

mainGroup = group()
box(length=3,height=3,width=0.01,color=color.black,group=mainGroup)
box(length=3-0.5,height=3-0.5,width=1,color=color.white,group=mainGroup)

class Spring:
    pass

bg = box(length=20,height=20,width=1e-3,texture="https://i.imgur.com/YknYWNh.jpeg")

# load textures
scene.visible = False
scene.waitfor("textures")
scene.visible = True

ticks = 0
while True:
    rate(fps)
    ticks+=1
    sec = ticks/fps
    displacement = vec(5*cos(sec),0,0)/fps
    mainGroup.pos += displacement
