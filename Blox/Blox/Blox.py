#Import sys for system-specific parameters and functions:
import sys
#Load all user modules from the 'modules' folder:
sys.path.append("modules")
#Import loadPrcFileData:
from pandac.PandaModules import loadPrcFileData
#Import TransparencyAttrip:
from pandac.PandaModules import TransparencyAttrib
#Import ShowBase and DirectObject:
from direct.showbase.ShowBase import ShowBase, DirectObject
#Import Actor:
from direct.actor.Actor import Actor
#Imort Task:
from direct.task import Task
#Import OnscreenText:
from direct.gui.OnscreenText import OnscreenText
#Import OnscreenImage:
from direct.gui.OnscreenImage import OnscreenImage
#Import DirectGui:
from direct.gui.DirectGui import *
#Import all PandaModules:
from pandac.PandaModules import *
#Import all bullet modules:
from libpandabullet import *
#Import string:
import string

#PointMath is a module for dealing with... well, point math!
from PointMath import *
#Import gui:
from gui import *
#Import Input:
from Input import *

#Set options:

#Set the GSG to use for rendering:
loadPrcFileData("","load-display pandagl")

#Set the window title:
loadPrcFileData("","window-title Blox")

#Set the windows icon:
loadPrcFileData("","icon-filename gfx/icon.ico")

#Set window size:
loadPrcFileData("","win-size  1024 768")

#Keep the window from being resized:
loadPrcFileData("","win-fixed-size 0")

#Set AA:
loadPrcFileData("","framebuffer-multisample 1")
loadPrcFileData("","multisamples 8")

#Set mouse cursor visibility:
loadPrcFileData("","cursor-hidden #f")

#Set frame rate meter visibility:
loadPrcFileData("","show-frame-rate-meter #t")

#Set anaglyph stereo rendering:
loadPrcFileData("","red-blue-stereo #f")

#Create the window:
main = ShowBase()

#Disable mouse camera controll:
base.disableMouse()

#Set background color:
base.setBackgroundColor(.2,.2,.2,1)

class Controller():

    def StartGame(self):

        main.taskMgr.add(physics.update,'Physics Task')
        self.LoadLevel()
        menu.background.destroy()
        menu.startButton.destroy()
        menu.exitButton.destroy()

    def LoadLevel(self):

        try:
            world.DestroyStage()
        except:
            doNothing = 1

        self.stage = fileopenbox(msg=None,title="Load Level",default='levels/',filetypes=[["*.blxlvl","Blox level files"]])

        if self.stage == None:
            self.stage = 'levels/default.blxlvl'


        player.body.setCenterOfMassPosition((0,0,1))
        player.body.setLinearVelocity((0,0,0))
        player.body.setAngularVelocity((0,0,0))

        world.LoadStage(self.stage)


    def RestartLevel(self):

        player.body.setCenterOfMassPosition((0,0,1))
        player.body.setLinearVelocity((0,0,0))
        player.body.setAngularVelocity((0,0,0))

        world.DestroyStage()
        world.LoadStage(self.stage)


class Menu():

    def __init__(self):

        #Menu background:
        self.background = OnscreenImage(image='gfx/gui/menu.jpg',scale=(1.5,0,1),pos=(0,0,0))

        self.buttonMaps = loader.loadModel('models/gui/buttons.egg')

        #Start button:
        self.startButton = DirectButton(geom = (self.buttonMaps.find('**/startup'),self.buttonMaps.find('**/startdown'),self.buttonMaps.find('**/startdown'),self.buttonMaps.find('**/startdown')),relief = None,command = controller.StartGame)
        self.startButton.setPos(0,0,.5)
        self.startButton.setScale(.6)

        #Exit button:
        self.exitButton = DirectButton(geom = (self.buttonMaps.find('**/exitup'),self.buttonMaps.find('**/exitdown'),self.buttonMaps.find('**/exitdown'),self.buttonMaps.find('**/exitdown')),relief = None,command = sys.exit)
        self.exitButton.setPos(0,0,-.4)
        self.exitButton.setScale(.6)

class Camera():

    def __init__(self):

        main.taskMgr.add(self.update,'Camera Task',20)

        #Set the camera's position and rotation:
        main.camera.setPos(0,-10,6)
        main.camera.setHpr(0,-22,0)

    def update(self,task):

        main.camera.setPos(player.np.getX(),-10,player.np.getZ()+5)

        return Task.cont


class Player():

    def __init__(self):

        main.taskMgr.add(self.update,'Player Task',20)

        #Load the player model:
        self.model = main.loader.loadModel("models/player.egg")
        self.model.reparentTo(render)

        self.tex = loader.loadTexture('gfx/balls/ball.jpg')
        self.model.setTexture(self.tex)

        #Physics:
        self.node = BulletMotionNode('sphere')
        self.node.setTransform(TransformState.makePos((0,0,1)))

        self.shape = BulletSphereShape(0.25)

        self.body = BulletRigidBody(1,self.node,self.shape)
        self.body.setActivationState(BulletRigidBody.ASDisableDeactivation)
        self.body.setFriction(1)
        self.body.setDamping(0,.9)

        physics.world.addRigidBody(self.body)

        self.np = render.attachNewNode(self.node)
        self.model.reparentTo(self.np)

        #Shadow:
        self.shadowLight = Spotlight('slight')
        self.shadowLight.setColor(VBase4(-.75,-.75,-.75,1))
        self.shadowLight.setAttenuation(Point3(0,0,.5))
        self.shadowLens = PerspectiveLens()
        self.shadowLens.setFov(180)
        self.shadowLight.setLens(self.shadowLens)
        self.shadowNp = render.attachNewNode(self.shadowLight)
        self.shadowNp.setHpr(0,-90,0)


    def update(self,task):

        self.shadowNp.setPos((self.np.getX(),self.np.getY(),self.np.getZ()+1))

        self.linearVelocity = self.body.getLinearVelocity()

        if keyboard.getKey("up"):

            if self.linearVelocity[2] < .015 and self.linearVelocity[2] > -.015:

                self.body.applyCentralImpulse((0,0,5))

        if keyboard.getKey("left"):

            self.body.applyCentralForce((-10,0,0))

        if keyboard.getKey("right"):

            self.body.applyCentralForce((10,0,0))

        if keyboard.getKey("r"):

            controller.RestartLevel()


        if self.np.getZ() < -20:

            controller.RestartLevel()

        return Task.cont


class Block():

    def __init__(self,Type,mass,x,y,z,h,p,r):

        #Load a model:
        self.model = main.loader.loadModel("models/block.egg")

        self.model.setLight(player.shadowNp)

        if str(Type) == "clear":
            self.model.setTransparency(TransparencyAttrib.MAlpha)
            self.model.setAlphaScale(0)
        else:
            self.tex = loader.loadTexture('gfx/blocks/'+str(Type)+'.jpg')
            self.model.setTexture(self.tex)

        if str(Type) == "finish":

            self.task = main.taskMgr.add(self.updateFinish,"Block Task")

        #Reparent the model to render:
        self.model.reparentTo(render)

        if mass != 0 and str(Type) != "finish":
            self.model.setColorScale(.8,.8,.8,1)

        #Physics:
        self.node = BulletMotionNode('box')
        self.node.setTransform(TransformState.makePosHpr((x,y,z),(h,p,r)))

        self.shape = BulletBoxShape(0.5)

        self.body = BulletRigidBody(mass,self.node,self.shape)
        physics.world.addRigidBody(self.body)

        self.np = render.attachNewNode(self.node)
        self.model.reparentTo(self.np)

    def updateFinish(self,task):

        if PointDistance(self.np.getX(),self.np.getZ(),player.np.getX(),player.np.getZ()) < 1:

            if ynbox(msg='You win!!! Would you like to keep playing?',title='',choices=('Yes','No'),image=None) == 1:

                main.taskMgr.remove(self.task)
                controller.LoadLevel()
            else:
                sys.exit()

        return Task.cont


class Physics():

    def __init__(self):


        #Physics:
        self.world = BulletWorld((-1024,-1024,-1024),(1024,1024,1024),1024)
        self.world.setGravity(Vec3(0,0,-9.81))

        #Create two planes to keep objects from rolling off the Y edges:
        self.node = BulletMotionNode('plane')
        self.node.setTransform(TransformState.makePosHpr((0,-.5,0),(0,90,0)))

        self.shape = BulletPlaneShape(Vec3(0,0,1),-1)

        self.body = BulletRigidBody(0,self.node,self.shape)
        self.body.setFriction(0)
        self.world.addRigidBody(self.body)

        self.node = BulletMotionNode('plane')
        self.node.setTransform(TransformState.makePosHpr((0,.5,0),(0,-90,0)))

        self.shape = BulletPlaneShape(Vec3(0,0,1),-1)

        self.body = BulletRigidBody(0,self.node,self.shape)
        self.body.setFriction(0)
        self.world.addRigidBody(self.body)

    def update(self,task):

        self.world.stepSimulation(globalClock.getDt(),10,1.0/60.0)

        return Task.cont


class World():

    def LoadStage(self,stage):

        #Level path:
        self.inputFile = open(str(stage),'r')
        self.fileString = self.inputFile.read()

        #Set some var's:
        self.currentBlock = 0
        self.blocks = []

        #Check if we are not at the end of the fiel:
        while self.fileString.find(str(self.currentBlock+1)+":") != -1:

            self.currentBlock += 1
            self.block = self.fileString.find(str(self.currentBlock)+":")

            self.blockEnd = self.fileString.find(";",self.block)

            self.blockValue = self.fileString[self.block:self.blockEnd]

            self.blockTypeStart = self.blockValue.find('(')

            self.blockTypeEnd = self.blockValue.find(')')

            self.type = self.blockValue[self.blockTypeStart+1:self.blockTypeEnd]

            self.blockMassStart = self.blockValue.find('(',self.blockTypeEnd)
            self.blockMassEnd = self.blockValue.find(')',self.blockMassStart)

            self.blockMass = self.blockValue[self.blockMassStart+1:self.blockMassEnd]

            self.blockPosStart = self.blockValue.find('(',self.blockMassEnd)
            self.blockPosEnd = self.blockValue.find(')',self.blockPosStart)

            self.blockPos = string.split(self.blockValue[self.blockPosStart+1:self.blockPosEnd],',')

            self.blockHprStart = self.blockValue.find('(',self.blockPosEnd)
            self.blockHprEnd = self.blockValue.find(')',self.blockHprStart)

            self.blockHpr = string.split(self.blockValue[self.blockHprStart+1:self.blockHprEnd],',')

            self.block = Block(self.type,float(self.blockMass),float(self.blockPos[0]),float(self.blockPos[1]),float(self.blockPos[2]),float(self.blockHpr[0]),float(self.blockHpr[1]),float(self.blockHpr[2]))

            self.blocks.append(self.block)

        self.inputFile.close()

    def DestroyStage(self):


        for self.block in self.blocks:
            physics.world.removeRigidBody(self.block.body)
            self.block.model.removeNode()
            try:
                main.taskMgr.remove(self.block.task)
            except:
                doNothing = 0


#Lighting:

#Enable per-pixel lighting:
render.setShaderAuto()

sun = DirectionalLight('Sun')
sun.setColor(Vec4(.7,.7,.7,1))

sun = render.attachNewNode(sun)
sun.setHpr(45,-45,0)
render.setLight(sun)

ambientLight = AmbientLight('AmbientLight')
ambientLight.setColor(VBase4(.5,.5,.5,1))

ambientLight = render.attachNewNode(ambientLight)
render.setLight(ambientLight)


#Create objects:
keyboard = Keyboard()
mouse = Mouse()
physics = Physics()
world = World()
player = Player()
camera = Camera()
controller = Controller()
menu = Menu()


#End program is escape key is pressed:
main.accept("escape",sys.exit)

#Run the engine:
main.run()
