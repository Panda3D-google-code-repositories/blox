#Import ShowBase and DirectObject:
from direct.showbase.ShowBase import DirectObject

class Keyboard(DirectObject.DirectObject):

    def __init__(self):

        #The key events update this list, and our task will query it as input
        self.keys = {}

        #Other keys events set the appropriate value in our key dictionary
        self.accept("arrow_left",     self.setKey, ["left", 1])
        self.accept("arrow_left-up",  self.setKey, ["left", 0])
        self.accept("arrow_right",    self.setKey, ["right", 1])
        self.accept("arrow_right-up", self.setKey, ["right", 0])
        self.accept("arrow_up",       self.setKey, ["up", 1])
        self.accept("arrow_up-up",    self.setKey, ["up", 0])
        self.accept("arrow_down",     self.setKey, ["down", 1])
        self.accept("arrow_down-up",  self.setKey, ["down", 0])
        self.accept("a",     self.setKey, ["a", 1])
        self.accept("a-up",  self.setKey, ["a", 0])
        self.accept("b",     self.setKey, ["b", 1])
        self.accept("b-up",  self.setKey, ["b", 0])
        self.accept("c",     self.setKey, ["c", 1])
        self.accept("c-up",  self.setKey, ["c", 0])
        self.accept("d",     self.setKey, ["d", 1])
        self.accept("d-up",  self.setKey, ["d", 0])
        self.accept("e",     self.setKey, ["e", 1])
        self.accept("e-up",  self.setKey, ["e", 0])
        self.accept("f",     self.setKey, ["f", 1])
        self.accept("f-up",  self.setKey, ["f", 0])
        self.accept("g",     self.setKey, ["g", 1])
        self.accept("g-up",  self.setKey, ["g", 0])
        self.accept("h",     self.setKey, ["h", 1])
        self.accept("h-up",  self.setKey, ["h", 0])
        self.accept("i",     self.setKey, ["i", 1])
        self.accept("i-up",  self.setKey, ["i", 0])
        self.accept("j",     self.setKey, ["j", 1])
        self.accept("j-up",  self.setKey, ["r", 0])
        self.accept("k",     self.setKey, ["k", 1])
        self.accept("k-up",  self.setKey, ["k", 0])
        self.accept("l",     self.setKey, ["l", 1])
        self.accept("l-up",  self.setKey, ["l", 0])
        self.accept("m",     self.setKey, ["m", 1])
        self.accept("m-up",  self.setKey, ["m", 0])
        self.accept("n",     self.setKey, ["n", 1])
        self.accept("n-up",  self.setKey, ["n", 0])
        self.accept("o",     self.setKey, ["o", 1])
        self.accept("o-up",  self.setKey, ["o", 0])
        self.accept("p",     self.setKey, ["p", 1])
        self.accept("p-up",  self.setKey, ["p", 0])
        self.accept("q",     self.setKey, ["q", 1])
        self.accept("q-up",  self.setKey, ["q", 0])
        self.accept("r",     self.setKey, ["r", 1])
        self.accept("r-up",  self.setKey, ["r", 0])
        self.accept("s",     self.setKey, ["s", 1])
        self.accept("s-up",  self.setKey, ["s", 0])
        self.accept("t",     self.setKey, ["t", 1])
        self.accept("t-up",  self.setKey, ["t", 0])
        self.accept("u",     self.setKey, ["u", 1])
        self.accept("u-up",  self.setKey, ["u", 0])
        self.accept("v",     self.setKey, ["v", 1])
        self.accept("v-up",  self.setKey, ["v", 0])
        self.accept("w",     self.setKey, ["w", 1])
        self.accept("w-up",  self.setKey, ["w", 0])
        self.accept("x",     self.setKey, ["x", 1])
        self.accept("x-up",  self.setKey, ["x", 0])
        self.accept("y",     self.setKey, ["y", 1])
        self.accept("y-up",  self.setKey, ["y", 0])
        self.accept("z",     self.setKey, ["z", 1])
        self.accept("z-up",  self.setKey, ["z", 0])

    def setKey(self, key, val):

        self.keys[key] = val

    def getKey(self,key):

        return self.keys.get(key)


class Mouse(DirectObject.DirectObject):

    def __init__(self):

        #The button events update this list, and our task will query it as input
        self.buttons = {}

        #Other keys events set the appropriate value in our key dictionary
        self.accept("mouse1",     self.setButton, ["mouse1", 1])
        self.accept("mouse1-up",  self.setButton, ["mouse1", 0])
        self.accept("mouse2",     self.setButton, ["mouse2", 1])
        self.accept("mouse2-up",  self.setButton, ["mouse2", 0])

    def setButton(self,button,val):

        self.buttons[button] = val

    def getButton(self,key):

        return self.buttons.get(key)
