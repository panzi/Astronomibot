import imp
import milight
import webcolors
baseFile = "astronomibot.py"
if __name__ == "__main__":
    baseFile = "../"+baseFile
    
c = imp.load_source('Command',baseFile)

class MiLight(c.Command):

    def __init__(self,bot,name):
        super(MiLight,self).__init__(bot,name)

        self.lightgroup=3
        self.lastState = "               "
        
        if not self.bot.isCmdRegistered("!light"):
            self.bot.regCmd("!light",self)
        else:
            print("!light is already registered to ",self.bot.getCmdOwner("!light"))
            
        if not self.bot.isCmdRegistered("!disco"):
            self.bot.regCmd("!disco",self)
        else:
            print("!disco is already registered to ",self.bot.getCmdOwner("!disco"))
            
        if not self.bot.isCmdRegistered("!swirl"):
            self.bot.regCmd("!swirl",self)
        else:
            print("!swirl is already registered to ",self.bot.getCmdOwner("!swirl"))

            
        self.cont = milight.MiLight({'host':'192.168.1.10','port':8899},wait_duration=0)
        self.light = milight.LightBulb(['rgbw'])
        self.cont.send(self.light.on(self.lightgroup))

    def getState(self):
        tables = []

        state=[]
        state.append(("",""))
        state.append(("Last State",self.lastState))
        state.append(("",""))

        cmds = []
        cmds.append(("Command","Description","Example"))
        cmds.append(("!light <r> <g> <b>","Specify an exact colour with RGB values for the light.  Values are between 0 and 255","!light 255 0 128"))
        cmds.append(("!disco","Makes the light flash between various colours","!disco"))
        cmds.append(("!swirl","Makes the light gently swirl between all the colours","!swirl"))

        tables.append(state)
        tables.append(cmds)

        return tables
    
    def getDescription(self, full=False):
        if full:
            return "Users can use various commands to mess with an RGB light in the room!  Uses cheap MiLight light bulbs."
        else:
            return "Control an RGB light bulb!"
        

    def getParams(self):
        params = []
        return params

    def setParam(self, param, val):
        pass
    
    def shouldRespond(self, msg, userLevel):
        if msg.messageType == 'PRIVMSG' and len(msg.msg)!=0:
            splitMsg = msg.msg.split()
            if splitMsg[0]=='!light' and len(splitMsg)==4:
                if splitMsg[1].isdigit() and splitMsg[2].isdigit() and splitMsg[3].isdigit():
                    return True
            if splitMsg[0]=='!disco':
                return True
            if splitMsg[0]=='!swirl':
                return True
        return False


    def respond(self,msg,sock):
        splitMsg = msg.msg.split()
        response=""
        
        if splitMsg[0]=='!light':
            red = int(splitMsg[1])
            if red<0:
                red=0
            elif red>255:
                red=255
                
            green = int(splitMsg[2])
            if green<0:
                green=0
            elif green>255:
                green=255
                
            blue = int(splitMsg[3])
            if blue<0:
                blue=0
            elif blue>255:
                blue=255
                
            self.cont.send(self.light.color(milight.color_from_rgb(red,green,blue),self.lightgroup))
            self.lastState = "R"+str(red)+" G"+str(green)+" B"+str(blue)
            response = "Light changed to R"+str(red)+" G"+str(green)+" B"+str(blue)
        elif splitMsg[0]=='!disco':
            self.cont.send(self.light.party('rainbow_jump',self.lightgroup))
            self.lastState="Disco Mode"
            response = "Light switched to disco mode"
            
        elif splitMsg[0]=='!swirl':
            self.cont.send(self.light.party('rainbow_swirl',self.lightgroup))
            self.lastState="Rainbow Swirl Mode"
            response = "Light switched to rainbow swirl mode"

            
        ircResponse = "PRIVMSG "+channel+" :"+response+"\n"
        sock.sendall(ircResponse.encode('utf-8'))
        return response
        