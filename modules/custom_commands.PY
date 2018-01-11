from calendar import timegm 
import requests
import time
import logging

class Commands():
    
    def edit_command_list(self):
        command = self.chatmessage[0]
        if command == '!addcom':
            if (self.add_command()):
                self.message_channel( self.chatmessage[1] + ' has been sucessfully added to the database!')
            return 1
        elif command == '!delcom':
            if (self.delete_command()):
                self.message_channel(self.chatmessage[1] + ' has been successfully deleted from the database!')
            return 1
        elif command == '!editcom':
            if (self.edit_command()):
                self.message_channel(self.chatmessage[1] + ' has been successfully edited!')
            return 1
        return 0
    def add_command(self):
        Permissions = {'own','owner','mod','moderator','reg','regular','sub','subscriber','everyone'}
        message = self.chatmessage[:]
        message[0] = ''
        command = message[1].lower()
        message[1] = ''
        cooldown = 30
        count = 0
        permission = 'everyone'
        if (command in self.commands):
            logging.info(command + " failed to be added because it was already in the commands list.")
            self.message_channel( command + " is already in the database!")
            return 0
        for check in range(len(message)):
            if message[check][:4].lower() == "-ul=":
                permission = message[check][4:].lower()
                if permission not in Permissions:
                    self.message_channel( permission + ' is not a valid permission level.')
                    logging.info(command + ' failed to be added because it did not have a valid permission level. Permision level entered: ' + message[check][4:])
                    return 0
                permission = self.format_permission(permission)
                message[check] = ""
            if message[check][:4].lower() == '-cd=':
                if message[check][4:].isdigit() == False:
                    self.message_channel(message[check][4:] + ' is not a valid cooldown. Please type cooldown in seconds.')
                    logging.info(command + ' failed to be added because it did not have a valid cooldown. Reason: Not a Digit. Cooldown Entered: ' + message[check][4:])
                    return 0
                cooldown = int(message[check][4:])
                if cooldown < 5:
                    self.message_channel(message[check][4:] + ' seconds is not a valid cooldown. Please use a cooldown of 5 seconds or greater.')
                    logging.info(command + ' failed to be added because it did not have a valid cooldown. Reason: Less than 5 seconds. Cooldown Entered: ' + message[check][4:])
                    return 0
                logging.info(command + " cooldown has successfully been added")
                message[check] = ""
            if message[check][:7] == "-count=":
                if message[check][7:].isdigit() == False:
                    self.message_channel(message[check][4:] + ' is not a valid number. Please type an integer.')
                    logging.info(command + ' failed to be added because it did not have a valid count. Reason: Not an integer. Cooldown Entered: ' + message[check][4:])
                    return 0
                count = int(message[check][7:])
                message[check] = ''
        command_message = ' '.join(message)
        if command_message.isspace():
            self.message_channel(command + ' does not have a message. Please attach one.')
            return 0 
        self.commands[command] = dict() 
        self.commands[command]['message'] = command_message
        self.commands[command]['permission'] = permission
        self.commands[command]['cooldown'] = cooldown
        self.commands[command]['count'] = count
        self.commands[command]['last_used'] = 0
        logging.info('Command Successfully Added: ' + command)
        self.save_file()
        return 1
    
    def delete_command(self):
        message = self.chatmessage[:]
        command = message[1].lower()
        if command not in self.commands:
            logging.info(command + ' failed to be deleted because command does not exist.')
            self.message_channel(command + ' is not in the database!')
            return 0
        del self.commands[command]
        logging.info('Command Successfully Deleted: ' + command)
        self.save_file()
        return 1
    def edit_command(self):
        message = self.chatmessage[:]
        command = message[1].lower()
        message[0:2] = ""
        Permissions = {'own','owner','mod','moderator','reg','regular','sub','subscriber','everyone'}
        #Will exist elsewhere
        if command not in self.commands:
            logging.info(command + ' failed to be deleted because command does not exist.')
            c.privmsg(command + ' is not in the database!')
            return 0
        command_message = self.commands[command]['message']
        permission = self.commands[command]['permission']
        cooldown = self.commands[command]['cooldown']
        count = self.commands[command]['count']
        if len(message) == 0:
            self.message_channel(command + ' has failed to be edited because nothing is being changed')
            return 0
        for check in range(len(message)):
            if message[check][:4].lower() == "-ul=":
                permission = message[check][4:].lower()
                if permission not in Permissions:
                    self.message_channel( permission + ' is not a valid permission level.')
                    logging.info(command + ' failed to be edited because it did not have a valid permission level. Permision level entered: ' + message[check][4:])
                    return 0
                permission = self.format_permission(permission)
                message[check] = ""
                logging.info(command + " permission has successfully been edited.")
            if message[check][:4] == '-cd=':
                if message[check][4:].isdigit() == False:
                    self.message_channel(message[check][4:] + ' is not a valid cooldown. Please type cooldown in seconds.')
                    logging.info(command + ' failed to be edited because it did not have a valid cooldown. Reason: Not a Digit. Cooldown Entered: ' + message[check][4:])
                    return 0
                cooldown = int(message[check][4:])
                if cooldown < 5:
                    self.message_channel(message[check][4:] + ' seconds is not a valid cooldown. Please use a cooldown of 5 seconds or greater.')
                    logging.info(command + ' failed to be edited because it did not have a valid cooldown. Reason: Less than 5 seconds. Cooldown Entered: ' + check[4:])
                    return 0
                message[check] = ""
            if message[check][:7] == "-count=":
                if message[check][7:].isdigit() == False:
                    self.message_channel(message[check][4:] + ' is not a valid number. Please type an integer.')
                    logging.info(command + ' failed to be added because it did not have a valid count. Reason: Not an integer. Cooldown Entered: ' + message[check][4:])
                    return 0
                count = int(message[check][7:])                
                logging.info(command + " cooldown has successfully been edited.")
        if message[0:] != ['']:
            logging.info(message[0:])
            command_message = ' '.join(message)
        self.commands[command]['message'] = command_message
        self.commands[command]['permission'] = permission
        self.commands[command]['cooldown'] = cooldown
        self.commands[command]['count'] = count
        logging.info('Command Successfully Edited: ' + command)
        self.save_file()
        return 1
        
        
    def do_command(self,command):
        message = self.commands[command]['message'].split()
        temp_message = set(message)
        permission = self.commands[command]['permission']
        cooldown = self.commands[command]['cooldown']
        count = self.commands[command]['count']
        time_last_used = self.commands[command]['last_used']
        if self.check_mod() and time.time() - time_last_used < 5:
            return
        elif time.time() - time_last_used < cooldown and self.check_mod() == 0:
            return
        if self.check_permission(permission) == 0:
            return
        for check in range(len(message)):
            if message[check][:7].lower() == "-alias=":
                self.chatmessage = (message[check][7:].lower() + "".join(message[(check + 1):])).split()
                self.run_everything()
                return 1
        count = count + 1
        message = " ".join(message)
        twitch_api_variables = { '@uptime@','@game@','@title@','@viewer_count@' }
        if len(temp_message.intersection(twitch_api_variables)) != 0:
            self.check_stream_api()
            if self.api['Error'] == True:
                for value in twitch_api_variables:
                    message = message.replace(value,'There has been an error grabbing the API. If problem persists, please contact Zapdos26.')
                    logging.debug("Could not reach reach API.")
            elif self.api['Offline'] == True:
                for value in twitch_api_variables:
                    message = message.replace(value,'Grabbing the API does not work when offline. ')
                    logging.info("Streamer is offline, could not get data from API")
            else:
                message = message.replace('@game@',self.get_game())
                message = message.replace('@title@',self.api['title'])
                message = message.replace('@viewer_count@',str(self.api['viewer_count']))
                message = message.replace('@uptime@',self.get_uptime())
        message = message.replace('@count@',str(count))
        message = message.replace('@channel@',self.channel[1:])
        if '@raid@' in message:
            if len(message) < 2:
                c.privmsg(self.channel,self.username() + ', you need to state the person you want to raid.')
                return
            if time.time() - self.raid_last_used > 5:
                self.raid(self.chatmessage[1])
                return
        if '@multi@' in message:
            list_message = self.chatmessage
            if len(list_message) < 2:
                self.multi_run()
                return
            if list_message[1] == 'set':
                self.multi_set()
                return 
            elif list_message[1] == 'off':
                self.multi_off()
                return 
            else:
                self.multi_run()
                return 
        if '@touser@' in message:
            touser= self.username()
            if len(self.chatmessage) > 1:
                touser = self.chatmessage[1]
            message = message.replace('@touser@',touser)
        if '@query@' in message:
            query = ''
            if len(message) > 1:
                query = ' '.join(self.chatmessage[1:])
            message = message.replace('@query@',query)
        self.message_channel(message)
        logging.info("Command message sent: " + message)
        self.commands[command]['count'] = count
        self.commands[command]['last_used'] = time.time()
        self.save_file()
        return
    def format_permission(self,permission):
        if permission == 'own':
            permission = 'owner'
        elif permission == 'mod':
            permission = 'moderator'
        elif permission == 'sub':
            permission = 'subscriber'
        elif permission == 'reg':
            permission = 'regular'
        return permission
    
    def check_permission(self,permission):
        if permission == 'everyone':
            return 1
        elif permission == 'owner' and self.check_owner():
            return 1
        elif permission == 'moderator' and self.check_mod():
            return 1
        elif permission == 'subscriber' and self.check_subscriber():
            return 1
        elif permission == 'regular' and self.check_regular():
            return 1
        return 0
    def check_stream_api(self):
        if timegm(time.gmtime()) - self.api_last_checked < 120:
            logging.info("Using cached API info.")
            return
        else:
            logging.info("Using new API info.")
            url = 'https://api.twitch.tv/helix/streams?user_id=' + self.channel_id
            headers = {'Client-ID': self.client_id}    
            r = requests.get(url, headers=headers).json()  
            self.api_last_checked = time.time()
            if 'data' not in r:
                self.api['Error'] = True
                self.api['Offline'] = False
                return
            elif r['data'] == []:
                self.api['Offline'] = True
                self.api['Error'] = False
                return
            else:
                for key in r['data'][0].keys():
                    self.api[key] = r['data'][0][key]
                self.api['Error'] = False
                self.api['Offline'] = False
                return
    def get_uptime(self):
        uptime = timegm(time.gmtime()) - timegm(time.strptime(self.api['started_at'],'%Y-%m-%dT%H:%M:%SZ :'))
        uptime = self.format_uptime(uptime).lstrip()
        return uptime
    
    def check_game_api(self,game_id):
        url = 'https://api.twitch.tv/helix/games?id=' + game_id
        headers = {'Client-ID': self.client_id}    
        r = requests.get(url, headers=headers).json() 
        self.games[game_id] = r['data'][0]['name']
        self.save_file_game()       
        #this is not good. Needs error info
        return
    
    def get_game(self):
        game_id = self.api['game_id']
        if game_id not in self.games:
            self.check_game_api(game_id)
        return self.games[game_id]
    
    
    def format_uptime(self,time):
        day = time //(24*3600)
        time = time%(24*3600)
        hour = time//3600
        time = time%3600
        minute = time//60
        second = time%60
        time = ''
        if day != 0:
            time = str(day) + ' days'
        if hour != 0:
            time = time + ' ' + str(hour) + ' hours'
        if minute != 0:
            time = time + ' ' + str(minute) + ' minutes'
        if second != 0:
            time = time + ' ' + str(second) + ' seconds'
        return time    