class Checks:
    def check_mod(self):
        if self.check_owner():
            return True
        if self.tags['mod'] == '1':
            return True
        return False
    
    
    def check_owner(self):
        if self.tags['user-id'] == self.channel_id:
            return True
        return False
    
    def check_regular(self):
        if self.tags['user-id'] in self.regulars:
            return 1
        return 0
    
    def check_subscriber(self):
        if self.tags['subscriber'] == '1':
            return 1
        return 0
    def username(self):
        if self.tags['display-name'] != None:
            return self.tags['display-name']
        return self.tags['login']
        
    def check_tags(self,e):
        for tag in e.tags:
            tag_key = tag["key"]
            tag_value = tag["value"]
            self.tags[tag_key] = tag_value    