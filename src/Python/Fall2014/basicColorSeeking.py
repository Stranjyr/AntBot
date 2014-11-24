import ColorTracker
import movement
import math

##Todo: add way to stop movement from another thread
#This will let us actually read tags...
class BasicColorSeeking():
    def __init__(self, port, low, high, r):
        self.tracker = ColorTracker.Tracker(low, high, r)
        self.mover = movement.Movement(port)
    def basicMovement():
        while(True):
            self.mover.sensors() #Check for walls first
            rot = self.tracker.getTurn()
            self.mover.rotate(rot)
    def basicNoVision()
        while(True):
            self.mover.sensors()
            self.mover.bot.go(10, 0)
    ##Experimental method. Call inner attributes from mover and tracker, to see if
    ##there are better ways of handling movement. Do not call this, except for code tests.
    ##This is not a production method, and will change whenever I feel like it
    ##Note: this is a terrible anti-pattern, but whatever, I'm done
    def advTestingMove():
        _, t = self.tracker.cap.read()
        width = t.shape[0:2]
        while(True):
            tags = self.tracker.getTag()
            next = min(tags, key = lambda x:(math.abs(x)-width/2.0)
            while(math.abs(next)<=self.tracker.r):
                self.mover.bot.go(10, 0)
                past = next
                tags = self.tracker.getTag()
                next = min(tags, key = lambda x:(math.abs(x)-width/2.0)
            if(math.abs(past) <=self.tracker.r and math.abs(next) >=width/6.0):
                ##check if the next value is way off. 
                ##This is a sign that we are almost at our target tag, and just lost sight of it
                self.mover.bot.go(10, 0)
                time.sleep(5)
            ##Turn until facing a tag
            else:
                while(math.abs(next) >=self.tracker.r):
                    self.mover.bot.go(0, 5*math.abs(next)/next)
                    past = next
                    tags = self.tracker.getTag()
                    next = min(tags, key = lambda x:(math.abs(x)-width/2.0)
                
                
            
            
        