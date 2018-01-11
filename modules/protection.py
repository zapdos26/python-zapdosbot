import re
import fnmatch
import emoji
from calendar import timegm 
import time

class Protection:
    def run_protection(self,action):
        self.protection_message = ' '.join(self.chatmessage)
        if self.check_mod():
            return 0
        self.whitelist()
        if self.repeat_protection() == 1:
            return 1
        elif self.emotes_protection() == 1:
            return 1        
        self.whitelist()
        if self.link_protection() == 1:
            return 1
        elif self.caps_protection() ==1 :
            return 1
        elif self.symbols_protection() == 1:
            return 1 
        elif self.blacklist_protection() == 1:
            return 1 
        elif self.spam_protection() ==1:
            return 1
        elif self.fakedeletion_protection() ==1 :
            return 1
        if action:
            if self.fakedonation_protection() ==1:
                return 1
        return 0
    def whitelist(self):
        for word in self.protections['whitelist']['list']:
            self.protection_message = self.protection_message.replace(word, '')
        return
    def repeat_protection(self):
        if self.protections['repeat']['status'] == 'off':
            return 0
        if self.protections['repeat']['regular'] == 'on' and self.tags['user_id'] in self.regulars:
            return 0
        if self.protections['repeat']['subscriber'] == 'on' and self.tags['subscriber'] == 1:
            return 0
        if self.protections['repeat']['bits'] == 'on' and self.bits_exist():
            return 0
        user_id = self.tags['user-id']
        if user_id not in self.repeats.keys():
            self.repeats[user_id] = []
            self.repeats[user_id].append(self.protection_message.lower())
            self.repeats[user_id].append(1)
            return 0
        elif self.repeats[user_id][0] == self.protection_message.lower():
            self.repeats[user_id][1] = self.repeats[user_id][1] + 1
        else: 
            self.repeats[user_id][0] = self.protection_message.lower()
            self.repeats[user_id][1] = 1
            return 0
        if self.repeats[user_id][1] > 5:
            self.timeout('repeats')
            return 1
        
    def link_protection(self):
        if self.protections['links']['status'] == 'off':
            return 0
        if self.protections['links']['regular'] == 'on' and self.tags['user_id'] in self.regulars:
            return 0
        if self.protections['links']['subscriber'] == 'on' and self.tags['subscriber'] == 1:
            return 0
        if self.protections['links']['bits'] == 'on' and self.bits_exist():
            return 0        
        matches = []
        domains = { 'com','edu','gov','mil','net','org','biz','info','name','museum','us','ca','uk','xxx','tv','eu','link','gg','ca','tel','pro','mobi','jobs','asia','arpa','aero','fm','gl','le','ly','png','co','tk','nl','mn','uk','be','ac','me','io','jpg' }
        for domain in domains:
            regex = r"[-a-zA-Z0-9@:%._\+~#=]\." + re.escape(domain) + r"\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
            if re.search(regex, self.protection_message) != None:
                self.timeout('links')
                return 1
        return 0
    
    def caps_protection(self):
        if self.protections['caps']['status'] == 'off':
            return 0
        if self.protections['caps']['regular'] == 'on' and self.tags['user_id'] in self.regulars:
            return 0
        if self.protections['caps']['subscriber'] == 'on' and self.tags['subscriber'] == 1:
            return 0
        if self.protections['caps']['bits'] == 'on' and self.bits_exist():
            return 0        
        message = self.protection_message
        number_caps = sum(1 for c in message if c.isupper())
        if number_caps >= self.protections['caps']['limitamount']:
            number_characters = len(message.strip())
            if number_caps/number_characters * 100 >= self.protections['caps']['limitpercentage']:
                self.timeout('caps')
                return 1
        return 0
    
    def blacklist_protection(self):
        if self.protections['blacklist']['status'] == 'off':
            return 0
        if self.protections['blacklist']['regular'] == 'on' and self.tags['user_id'] in self.regulars:
            return 0
        if self.protections['blacklist']['subscriber'] == 'on' and self.tags['subscriber'] == 1:
            return 0
        if self.protections['blacklist']['bits'] == 'on' and self.bits_exist():
            return 0        
        blacklist = self.protections['blacklist']['list']
        message = self.protection_message.lower()
        message = message.split()
        matches = 0
        for word in blacklist:
            matches = matches + len(fnmatch.filter(message, word))
        if matches > 0:
            self.timeout('blacklist')
            return 1
        return 0
    
    def symbols_protection(self):
        if self.protections['symbols']['status'] == 'off':
            return 0
        if self.protections['symbols']['regular'] == 'on' and self.tags['user_id'] in self.regulars:
            return 0
        if self.protections['symbols']['subscriber'] == 'on' and self.tags['subscriber'] == 1:
            return 0       
        if self.protections['symbols']['bits'] == 'on' and self.bits_exist():
            return 0        
        message = self.protection_message
        emojis = list(c for c in message if c in emoji.UNICODE_EMOJI)
        emoji_matches = len(emojis)
        print(emoji_matches)
        for emoji_ in emojis:
            message = message.strip(emoji_)
        emoji_matches = len(emojis)
        regex_emoji = r"[^\w\s]|_"
        symbol_matches = len(re.findall(regex_emoji,message))   
        matches = emoji_matches + symbol_matches
        if matches >= self.protections['symbols']['limitamount']:
            original = self.protection_message
            if matches/(len(original.strip())) * 100 > self.protections['symbols']['limitpercentage']:
                self.timeout("symbols")
                return 1
        return 0
    
    def emotes_protection(self):
        if self.protections['emotes']['status'] == 'off':
            return 0
        if self.protections['emotes']['regular'] == 'on' and self.tags['user_id'] in self.regulars:
            return 0
        if self.protections['emotes']['subscriber'] == 'on' and self.tags['subscriber'] == 1:
            return 0
        if self.protections['emotes']['bits'] == 'on' and self.bits_exist():
            return 0        
        emotes = self.tags['emotes']
        if emotes == None:
            return 0
        message = list(self.protection_message)
        emote_count = 0
        emote_protection = self.protections['emotes']['ignore']
        emotes = emotes.split('/')
        for emote in emotes:
            emote_id = emote.split(':')
            if emote_id[0] not in emote_protection:
                emote_count = emote_count + emote_id[1].count('-')
            emote_positions = emote_id[1].split(',')
            for emote_individual in emote_positions:
                emote_indexs = emote_individual.split('-')
                for index in range(int(emote_indexs[0]), int(emote_indexs[1])+1):
                    message[index] = ''
        self.protection_message = ''.join(message)
        if emote_count >= self.protections['emotes']['limitamount']:
            self.timeout('emotes')
            return 1
        return 0
    
    def spam_protection(self):
        if self.protections['spam']['status'] == 'off':
            return 0
        if self.protections['spam']['regular'] == 'on' and self.tags['user_id'] in self.regulars:
            return 0
        if self.protections['spam']['subscriber'] == 'on' and self.tags['subscriber'] == 1:
            return 0        
        if self.protections['spam']['bits'] == 'on' and self.bits_exist():
            return 0        
        message = self.protection_message.lower()
        matcher = re.compile(r'(?u)(\w)\1*')
        matches = [ match.group() for match in matcher.finditer(message)]
        length = 0
        for match in matches:
            if length < len(match):
                length = len(match)
        if length > self.protections['spam']['limitamount']:
            self.timeout('spam')
            return 1
        return 0
    def fakedeletion_protection(self):
        if self.protections['fakedeletion']['status'] == 'off':
            return 0
        message = self.protection_message.lower()
        if '<message deleted>' in message:
            self.timeout('fakedeletion')
            return 1
        return 0
    
    def fakedonation_protection(self):
        if self.protections['fakedonation']['status'] == 'off':
            return 0
        message = self.protection_message.lower()
        if '$' in message or 'donate' in message:
            self.timeout('fakedonation')
            return 1
        return 0         
            
    def timeout(self,spam):
        c = self.connection
        message = self.protections[spam]['message']
        username = self.username()
        if '@user@' in message:
            message = message.replace('@user@',username)
        c.privmsg(self.channel, '/timeout ' + username + ' ' + str(self.protections[spam]['timeout']) + ' ' + message)
        if self.protections[spam]['silence'] == 'off' and timegm(time.gmtime()) - self.protections[spam]['last_used'] > 5:
            self.protections[spam]['last_used'] = timegm(time.gmtime())
            c.privmsg(self.channel, message)
        return
    def protection_setup(self):
        c = self.connection
        if '!protection' != self.chatmessage[0]:
            return 0
        protection_options = {'caps', 'emotes', 'repeat', 'spam', 'links','blacklist','symbols','fakedonation','fakedeletion','whitelist'}
        if len(self.chatmessage) < 3:
            c.privmsg(self.channel,self.username() + ', for more info about how to set the protection settings, visit https://goo.gl/o1Otwc.')
            return 1
        if self.chatmessage[1].lower() not in protection_options:
            c.privmsg(self.channel,self.username() + ', for more info about how to set the protection settings, visit https://goo.gl/o1Otwc.')
            return 1
        spam_type = self.chatmessage[1].lower()
        option = self.chatmessage[2].lower()
        if option == 'on' or option == 'off':
            if self.protections[spam_type]['status'] == option:
                c.privmsg(self.channel, spam_type + ' protection is already turned ' + option + '.' )
                return 1
            self.protections[spam_type] ['status'] = option
            c.privmsg(self.channel, spam_type.title() + ' protection has been turned ' + option + '.')
            return 1
        if option == 'message':
            self.protections[spam_type]['message']  = self.chatmessage[3:]
            c.privmsg(self.chanel,spam_type.title() + ' protection message has been set.')
            return 1
        if option == 'timeout':
            timeout = self.chatmessage[3]
            if timeout.isdigit() == False:
                c.privmsg(self.channel,self.username() + ', for more info about how to set the protection settings, visit https://goo.gl/o1Otwc.')
                return 1
            timeout = int(timeout)
            if timeout < 1:
                c.privmsg(self.channel,self.username() + ', the timeout you have chose is too low. Please pick a higher timeout period.')
                return 1
            self.protections[spam_type]['timeout'] = timeout
            c.privmsg(self.channel, spam_type.title() + ' protection timeout period has been set.')
            return 1
        if option == 'limitamount':
            protection_limitamount = {'emotes', 'caps', 'symbols', 'repeat', 'spam'}
            if spam_type not in protection_limitamount:
                c.privmsg(self.channel, 'LimitAmount is not a valid option for ' + spam_type.title() + ' protection.')
                return 1
            limitamount = self.chatmessage[3]
            if limitamount.isdigit() == False:
                c.privmsg(self.channel,self.username() + ', for more info about how to set the protection settings, visit https://goo.gl/o1Otwc.')
                return 1
            limitamount = int(limitamount)
            if limitamount == 0:
                c.privmsg(self.channel,self.username() + ', the amount you picked is too low. Please pick a higher amount.')
                return 1
            self.protections[spam_type]['limitamount'] =  limitamount
            c.privmsg(self.channel, spam_type.title() + ' protection amount required to activate has been set.')
            return 1
        if option == 'limitpercentage':
            if spam_type != 'caps' and spam_type != 'symbols':
                c.privmsg(self.channel, 'Limit Percentage is not a valid option for ' + spam_type.title() + ' protection.')
                return 1
            limitpercentage = self.chatmessage[3]
            if limitpercentage.isdigit() == False:
                c.privmsg(self.channel,self.username() + ', for more info about how to set the protection settings, visit https://goo.gl/o1Otwc.')
                return 1
            limitpercentage = int(limitpercentage)
            if limitpercentage == 0:
                c.privmsg(self.channel,self.username() + ', the percentage you picked is too low. Please pick a higher percentage.')
                return 1
            self.protections[spam_type]['limitpercentage'] = limitpercentage
            c.privmsg(self.channel,spam_type.title() + ' protection percentage required to activate has been set.')
            return 1
        if option == 'regular':
            status == self.chatmessage[3].lower()
            if status != 'on' and status != 'off':
                c.privmsg(self.channel,self.username() + ', for more info about how to set the protection settings, visit https://goo.gl/o1Otwc.')
                return 1            
            if status == self.protections[spam_type]['regular']:
                c.privmsg(self.channel, 'Regular protection from ' + spam_type.title() + ' protection is already ' + status + '.')
                return 1    
            self.protections[spam_type]['regular'] == status
            c.privmsg(self.channel, 'Regular protection from ' + spam_type.title() + ' protection is now turned ' + status + '.')
            return 1
        if option == 'subscriber':
            status = self.chatmessage[3].lower()
            print(status)
            if status != 'on' and status != 'off':
                c.privmsg(self.channel,self.username() + ', for more info about how to set the protection settings, visit https://goo.gl/o1Otwc.')
                return 1 
            elif status == self.protections[spam_type]['subscriber']:
                c.privmsg(self.channel, 'Subscriber protection from ' + spam_type.title() + ' protection is already ' + status + '.')
                return 1
            self.protections[spam_type]['subscriber'] == status
            c.privmsg(self.channel, 'Subscriber protection from ' + spam_type.title() + ' protection is now turned ' + status + '.')
            return 1
        if option == 'bits':
            status == self.chatmessage[3].lower()
            if status != 'on' and status != 'off':
                c.privmsg(self.channel,self.username() + ', for more info about how to set the protection settings, visit https://goo.gl/o1Otwc.')
                return 1            
            if status == self.protections[spam_type]['bits']:
                c.privmsg(self.channel, 'Bit donation protection from ' + spam_type.title() + ' protection is already ' + status + '.')
                return 1    
            self.protections[spam_type]['bit'] == status
            c.privmsg(self.channel, 'Bit donation protection from ' + spam_type.title() + ' protection is now turned ' + status + '.')
            return 1        
        if spam_type == 'emotes':
            edit = self.chatmessage[2].lower()
            emotes = set(self.chatmessage[3:])
            emotes_id = set()
            for emote in emotes:
                if emote.isdigit():
                    emotes_id.add(emote)
            if self.tags['emotes'] != None:
                emotes_message = self.tags['emotes'].split('/')
                for emote in emotes_message:
                    temp = emote.split(':')
                    emote_id = temp[0]
                    emotes_id.add(emote_id)
            print(emotes_id)
            if edit == 'add':
                self.protections['emotes']['ignore'] = self.protections['emotes']['ignore'].union(emotes_id)
                c.privmsg(self.channel, "Emotes have been added to the ignore list")
                return 1
            if edit == 'del':
                for emote in emotes:
                    self.protections['emotes']['ignore'].remove(emote)
                    c.privmsg(self.channel, "Emotes have been removed from the ignore list")
                    return 1                
        if spam_type == 'blacklist':
            edit = self.chatmessage[2].lower()
            blacklist = set(self.chatmessage[3:])
            if edit == 'add':
                self.protections['blacklist']['list'] = self.protections['blacklist']['list'].union(blacklist)
                c.privmsg(self.channel, "Words have been added to the blacklist")
                return 1            
            if edit == 'del':
                for word in blacklist:
                    self.protections['blacklist']['list'].remove(word)
                    c.privmsg(self.channel, "Words have been removed from the blacklist")
                    return 1
        if spam_type == 'whitelist':
            edit = self.chatmessage[2].lower()
            whitelist = set(self.chatmessage[3:])
            if edit == 'add':
                self.protections['whitelist']['list'] = self.protections['whitelist']['list'].union(whitelist)
                c.privmsg(self.channel, "Words have been added to the whitelist")
                return 1            
            if edit == 'del':
                for word in whitelist:
                    self.protections['whitelist']['list'].remove(word)
                    c.privmsg(self.channel, "Words have been removed from the whitelist")
                    return 1
        if option == 'silent':
            status == self.chatmessage[3].lower()
            if status != 'on' and status != 'off':
                c.privmsg(self.channel,self.username() + ', for more info about how to set the protection settings, visit https://goo.gl/o1Otwc.')
                return 1            
            if status == self.protections[spam_type]['silent']:
                c.privmsg(self.channel, spam_type.title() + ' protection silent status is already ' + status + '.')
                return 1    
            self.protections[spam_type]['regular'] == status
            c.privmsg(self.channel, spam_type.title() + ' protection silent status is now turned ' + status + '.')
            return 1
        c.privmsg(self.channel,self.username() + ', for more info about how to set the protection settings, visit https://goo.gl/o1Otwc.')
        return 1