import logging
class Bits:
    def bits_exist(self):
        if 'bits' not in self.tags:
            return False
        return True
    def bits_message(self):
        if self.settings['bits']['status'] == 'off':
            return        
        if self.bits_exist():
            if int(self.tags['bits']) >= self.settings['bits']['amount']:
                message = self.settings['bits']['message']
                if message == '':
                    return
                if '@user@' in message:
                    message = message.replace('@user@',self.username())
                if '@bits@' in message:
                    message = message.replace('@bits@',self.tags['bits'])
                if '@dollar@' in message:
                    message = message.replace('@bits@',float(self.tags['bits'])/100)
                self.message_channel(message)
                logging.debug("Bit message sent: " + message)
            return