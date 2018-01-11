import pickle
import logging
from os.path import exists

class File_Dealer:
    def save_file(self):
        everything = dict()
        everything['commands'] = self.commands
        everything['protections'] = self.protections
        everything['settings'] = self.settings
        everything['timers'] = self.timers_info
        everything['regulars'] = self.regulars
        with open('channeldata/' + self.channel_id + '.pkl', 'wb') as f:
            pickle.dump(everything,f,pickle.HIGHEST_PROTOCOL)
        logging.info("Successfully saved settings.")
        return
    
    def save_file_game(self):
        with open('channeldata/games.pkl', 'wb') as f:
            pickle.dump(self.games,f,pickle.HIGHEST_PROTOCOL)
        logging.info("Successfully saved game info.")
        return
    def load_file_game(self):
        self.games = dict()
        if exists('channeldata/games.pkl') == False:
            self.save_file_game()
        with open('channeldata/games.pkl','rb') as f:
            self.games = pickle.load(f)
        logging.info("Successfully loaded game info.")
        return 
    def load_file(self):
        everything = dict()
        if exists("channeldata/"+ self.channel_id + '.pkl') == False:
            with open('config/default.pkl','rb') as f:
                everything = pickle.load(f)
        else:
            with open('channeldata/' + self.channel_id + '.pkl','rb') as f:
                everything = pickle.load(f)
        self.commands = everything['commands']
        self.protections = everything['protections']
        self.settings = everything['settings']
        self.timers_info = everything['timers']
        self.regulars = everything['regulars']
        logging.info("Successfully loaded settings.")
        return    