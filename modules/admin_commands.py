class Admin_Commands:
    def run_admin_commands(self):
        c = self.connection
        message = self.chatmessage[:]
        if '!streamer' != message[0]:
            return 0
        option = message[1].lower()
        options = { 'multi','raid','sub','resub','giftsub','bits' }
        sub_options = {'message','status'}
        category = message[2].lower()
        if option not in options:
            c.privmsg(self.channel,self.username() + ', for more info about how to setup the settings, visit https://goo.gl/o1Otwc.')
        elif option == 'multi':
            if category == 'message':
                self.settings['multi']['message'] = message[3:]
                c.privmsg(self.channel, 'The multi command message has  been set.')
        elif option == 'raid':
            if category == 'message':
                self.settings['raid']['message'] = message[3:]
                c.privmsg(self.channel,'The raid command message has been set.')
        elif option == 'sub':
            if category not in sub_options:
                c.privmsg(self.channel,self.username() + ', for more info about how to setup the settings, visit https://goo.gl/o1Otwc.')            
            if category == 'message':
                self.settings['sub']['message'] = message[3:]
                c.privmsg(self.channel,'The new sub message has been set.')
            elif category =='status':
                self.settings['sub']['status'] = message[3].lower()
                c.privmsg(self.channel, 'The new sub message has been turned ' + message[3].lower() + '.')               
        elif option == 'giftsub':
            if category not in sub_options:
                c.privmsg(self.channel,self.username() + ', for more info about how to setup the settings, visit https://goo.gl/o1Otwc.')            
            if category == 'message':
                self.settings['giftsub']['message'] = message [3:]
                c.privmsg(self.channel, 'The gift sub message has been set.')
            elif category =='status':
                self.settings['giftsub']['status'] = message[3].lower()
                c.privmsg(self.channel, 'The gift sub message has been turned ' + message[3].lower() + '.')                
        elif option == 'resub':
            if category not in sub_options:
                c.privmsg(self.channel,self.username() + ', for more info about how to setup the settings, visit https://goo.gl/o1Otwc.')            
            if category == 'message':
                self.settings['resub']['message'] = message[3:]
                c.privmsg(self.channel, 'The resub message has been set.')
            elif category =='status':
                self.settings['resub']['status'] = message[3].lower()
                c.privmsg(self.channel, 'The resub message has been turned ' + message[3].lower() + '.')               
        elif option == 'bits':
            sub_options = {'amount','message','status'}
            if category not in sub_options:
                c.privmsg(self.channel,self.username() + ', for more info about how to setup the settings, visit https://goo.gl/o1Otwc.')
            elif category == 'amount':
                amount = message[3]
                if amount.isdigit() == False:
                    c.privmsg(self.channel,self.username() + ', please make sure the amount is an integer.')
                    return 1
                self.settings['bits']['amount'] = int(amount)
                c.privmsg(self.channel, 'The minimum number of bits for message has been set.')
            elif category == 'message':
                self.settings['bits']['message'] = message[3:]
                c.privmsg(self.channel, 'The bits message has been set.')
        return 1
    