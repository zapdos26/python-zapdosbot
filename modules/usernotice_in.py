class Usernotice_Messages:
    def usernotice_in(self):    
        msg_id = self.tags['msg-id']
        if msg_id == 'sub':
            self.new_subscriber()
        elif msg_id == 'resub':
            self.resubscription()
        elif msg_id == 'subgift':
            self.gift_subscription()
        return
    def new_subscriber(self):
        if self.settings['sub']['status'] == 'off':
            return
        tier = self.tags['msg-param-sub-plan']
        if tier.isdigit():
            tier = int(tier) //1000
        else:
            tier == 1
        username = self.username()
        message = self.settings['sub']['message']
        if '@tier@' in message:
            message = message.replace('@tier@',tier)
        if '@user@' in message:
            message = message.replace('@user@',username)
        self.message_channel(message)
        return
    def resubscription(self):
        if self.settings['resub']['status'] == 'off':
            return        
        tier = self.tags['msg-param-sub-plan']
        if tier.isdigit():
            tier = int(tier) //1000
        else:
            tier == 1
        username = self.username()
        msg = self.tags['system-msg']
        months = self.tags['msg-param-months']
        message = self.settings['sub']['message']
        if '@tier@' in message:
            message = message.replace('@tier@',tier)
        if '@user@' in message:
            message = message.replace('@user@',username)
        if '@message@' in message:
            message = message.replace('@message@',msg)
        if '@months@' in message:
            message = message.replace('@months@',months)
        self.message_channel(message)
        return
    def gift_subscription(self):
        if self.settings['giftsub']['status'] == 'off':
            return        
        tier = self.tags['msg-param-sub-plan']
        if tier.isdigit():
            tier = int(tier) //1000
        else:
            tier == 1
        giver = self.username()
        message = self.settings['sub']['message']
        recipient = self.tags['msg-param-recipient-display-name']
        if recipient == '':
            recipient = self.tags['msg-param-recipient-user-name']
        if '@tier@' in message:
            message = message.replace('@tier@',tier)
        if '@user@' in message:
            message = message.replace('@user@',recipient)
        if '@gifter@' in message:
            message = message.replace('@gifter@',gifter)
        self.message_channel(message)
        return
    