import requests
class Regular:
    def regular(self):
        command = self.chatmessage[0]
        if command == '!regular':
            if self.chatmessage[1] == 'add':
                self.add_regular()
                return
            elif self.chatmessage[1] in { 'del','delete','remove' }:
                self.delete_regular()
                return 1
        return 0
    def add_regular(self):
        c = self.connection
        message = self.chatmessage[:]
        regular_name = message[2]
        url = 'https://api.twitch.tv/helix/users?login=' + regular_name
        headers = {'Client-ID': self.client_id}
        r = requests.get(url, headers=headers).json()
        if 'data' not in r:
            print('Adding regular failed. ' + regular_name + ' is not a real username.')
            c.privmsg(self.channel, regular_name + 'is not a real username.')
            return
        regular_id = r['data'][0]['id']
        if regular_id in self.regulars:
            print('Adding regular failed. ' + regular_name + ' is already a regular.')
            c.privmsg(self.channel, regular_name + ' is already a regular.')
            return 
        self.regulars.add(regular_id)
        print('Regular Added: ' + regular_name)
        c.privmsg(self.channel, regular_name + ' has been added a regular.')    
        return
    
    def delete_regular(self):
        c = self.connection
        message = self.chatmessage[:]
        regular_name = message[2]
        url = 'https://api.twitch.tv/helix/users?login=' + regular_name
        headers = {'Client-ID': self.client_id}
        r = requests.get(url, headers=headers).json()
        if 'data' not in r:
            print('Removing regular failed. ' + regular_name + ' is not a real username.')
            c.privmsg(self.channel, regular_name + 'is not a real username.')
            return
        regular_id = r['data'][0]['id']
        if regular_id not in self.regulars:
            print('Removing regular failed. ' + regular_name + ' is not a regular.')
            c.privmsg(self.channel, regular_name + ' is not a regular.')
            return
        self.regulars.remove(regular_id)
        print('Regular Removed: ' + regular_name)
        c.privmsg(self.channel, regular_name + ' is no longer a regular.')
        return    