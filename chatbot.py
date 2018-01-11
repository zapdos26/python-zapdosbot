import sys
import irc.bot
import requests
from multiprocessing import Process
import logging
from modules import *    

class TwitchBot(irc.bot.SingleServerIRCBot,protection.Protection,custom_commands.Commands,timers.Timers,tag_checks.Checks,file_dealer.File_Dealer,multistream.Multistream,regular.Regular,usernotice_in.Usernotice_Messages,raids.Raid,bits.Bits,admin_commands.Admin_Commands):
    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel    
        self.commands = dict()
        self.protections = dict()
        self.settings = dict()
        self.timers_info = dict()    
        self.regulars = set()
        self.api_last_checked = 0
        self.api = dict()
        self.games = dict()
        self.number_of_messages = 0
        self.raid_last_used = 0
        self.repeats = dict()
        
        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/helix/users?login=' + channel
        headers = {'Client-ID': client_id}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['data'][0]['id']
        self.load_file()
        self.load_file_game()
        self.start_logging()

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print ('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)
        

    def on_welcome(self, c, e):
        print ('Joining ' + self.channel)

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)
        self.startup()

    def on_pubmsg(self, c, e):
        self.number_of_messages += 1
        self.chatmessage = e.arguments[0].split()
        self.tags = dict()
        self.check_tags(e)
        #self.run_everything()
        try:
            self.run_everything()
        except:
            return
    def on_action(self,c,e):
        self.number_of_messages += 1
        self.tags = dict()
        self.check_tags(e)        
        self.chatmessage = e.arguments[0].split()        
        self.run_protection(1)
        return
    def on_usernotice(self,c,e):    
        self.tags = dict()
        self.check_tags(e)
        self.usernotice_in()
        return
    def message_channel(self,message):
        c = self.connection
        c.privmsg(self.channel,message)
        return
    def run_everything(self):
        # If a chat message starts with an exclamation point, try to run it as a command
        if self.check_mod():    
            if self.edit_command_list():
                self.save_file()
                return
            if self.regular():
                self.save_file()
                return
            if self.run_admin_commands():
                self.save_file()
                return
            
            if self.protection_setup():
                self.save_file()
                return
            if self.edit_timer_list():
                self.save_file()
                return
        if self.run_protection(0):
            return
        self.bits_message()
        command = self.chatmessage[0]
        command = command.lower()  
        print(command)
        if command in self.commands:
            print ('Received command: ' + command)
            self.do_command(command)
        return 
    def start_logging(self):
        filename1 = str(self.channel_id) + '.log'
        logging.basicConfig(filename='myapp.log', level=logging.DEBUG, format='%(levelname)s:%(name)s %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.info('Started Logging')
        return
            
        
        
def main():
    if len(sys.argv) != 5:
        print("Usage: twitchbot <username> <client id> <token> <channel>")
        sys.exit(1)
        
    username  = sys.argv[1]
    client_id = sys.argv[2]
    token     = sys.argv[3]
    channel   = sys.argv[4]
    
    bot = TwitchBot(username, client_id, token, channel)
    bot.start()


if __name__ == "__main__":
    main()