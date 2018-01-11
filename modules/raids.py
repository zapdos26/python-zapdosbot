class Raid:
    def raid(self,username):
        message = " ".join(self.settings['raid']['message'])
        if '@raidtarget@' in message:
            message = message.replace('@raidtarget@',username)
        for x in range(5):
            self.message_channel(message)