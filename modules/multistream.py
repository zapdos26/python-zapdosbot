from threading import Timer
import logging
class Multistream:
    def multi_set(self):
        c = self.connection
        if self.check_mod() == 0:
            print("Setting multitwitch failed. User is not a mod.")
            return
        multi_targets = '/'.join(self.chatmessage[2:])
        message = "".join(self.settings['multi']['message'][:])
        message = message.replace('@multitarget@',multi_targets)
        message = message.replace('@channel@',self.channel)
        self.multi = list()
        self.multi.append(message)
        self.multi.append(0)
        self.multi_start_timer()
        logging.info("Starting multistream timer")
        c.privmsg(self.channel, "Multistream has been turned on.")
        
            
    def multi_run(self):
        c = self.connection
        if self.multi == None:
            return
        if self.number_of_messages - self.multi[1] > 1:
            self.multi[1] = self.number_of_messages
            print("Sending multistream message")
            c.privmsg(self.channel, self.multi[0])
            print(self.multi[1])
            if len(self.multi)  ==3:
                self.multi_stop_timer()
            self.multi_start_timer()
    
    def multi_off(self):    
        c = self.connection
        if self.check_mod() == 0:
            print("Turning off multitwitch failed. User is not a mod.")
            return
        self.multi_stop_timer()
        self.multi = None
        print('Multistream has been turned off.')
        c.privmsg(self.channel, 'Multistream has been turn off.')
        return
    def multi_start_timer(self):
        t = Timer(5,self.multi_run)
        self.multi.append(t)
        t.start()
        return
    def multi_stop_timer(self):
        t = self.multi.pop()
        t.cancel()
        return