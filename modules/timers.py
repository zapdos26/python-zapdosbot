from threading import Timer
import random


class Timers:
    def startup(self):
        self.timers = dict()
        self.startup_timers = dict()
        for timer in self.timers_info.keys():
            if self.timers_info[timer]['status']:
                t = Timer(random.random() * 5, self.start_timer,[timer])
                self.startup_timers[timer] = t
                t.start()
        Timer(601,self.clear_startup_timers)
        Timer(300,self.save_file).start()
        return
    def clear_startup_timers(self):
        self.startup_timers = None
        
    def start_timer(self,timer):
        self.timers_info[timer][3] = self.number_of_messages
        time = self.timers_info[timer]['timelength']
        self.timers[timer] = Timer(time,self.run_timer,[timer])
        self.timers[timer].start()
        return 
    def run_timer(self,timer):
        message = self.timers_info[timer]['message']
        list_message = self.timers_info[timer]['message'].split()
        if self.number_of_messages > self.timers_info[timer]['chatlength'] + self.timers_info[timer]['n-o-m']:
            self.timers_info[timer]['n-o-m'] = self.number_of_messages
            for check in range(len(list_message)):
                if list_message[check][:9]  == '-command=':
                    command =  list_message[check][9:]
                    if command not in self.commands:
                        self.message_channel(command + " is not a command. This is a timer. The timer is called: " +timer )
                        return
                    else:
                        command_message = self.commands[command]['message']                
                        self.message_channel(command_message)
                        self.start_timer(timer)
                        return
            self.message_channel(message)
        self.start_timer(timer)
        return
    def stop_timer(self,timer):
        if timer in self.timers.keys():
            t = self.timers[timer]
            t.cancel
        elif self.startup_timers != None and timer in self.startup_timers:
            t = self.startup_timers[timer]
            t.cancel()
        return
    def edit_timer_list(self):
        message = self.chatmessage
        command = self.chatmessage[0].lower()
        if command == '!timer':
            edit = {'add','edit','del','on','off'}
            option = self.chatmessage[1].lower()
            if option in edit:
                if option == 'add':
                    self.add_timer(message)
                    return 1
                elif option == 'edit':
                    self.edit_timer(message)
                    return 1
                elif option == 'del':
                    self.delete_timer(message)
                    return 1
                elif option == 'on':
                    self.timer_on(message)
                    return 1
                elif option == 'off':
                    self.timer_off(message)
                    return 1
        return 0

    def add_timer(self,message):
        timer_name = message[2]
        del message[0:3]
        timelength = 600
        chatlength = 20
        command = None
        command_message = ''
        if timer_name in self.timers_info.keys():
            self.message_channel(timer_name + ' timer already exists.')
            return
        for check in range(len(message)):
            if message[check][:12].lower() == "-timelength=":
                timelength = message[check][12:]
                if timelength.isdigit() == False:
                    self.message_channel("Time length needs to be a number.")
                    return
                timelength = int(timelength)
                if timelength < 60:
                    self.message_channel("Time length needs to be 60 seconds or greater.")
                    return
                message[check] = ''
            if message[check][:12].lower() == '-chatlength=':
                chatlength = message[check][12:]
                if chatlength.isdigit() == False:
                    self.message_channel("Chat length needs to be a number.")
                    return
                chatlength = int(chatlength)
                if chatlength < 1:
                    self.message_channel("Chat length needs to be 1 or greater.")
                    return
                message[check]=''
            if message[check][:9]  == '-command=':
                command =  message[check][9:]
                if command not in self.commands.keys():
                    self.message_channel(command + " is not a command.")
                    return
        if command_message == None and message == '':
            self.message_channel("There is not a valid message. Please type one up.")
            return
        message = command_message + "".join(message)
        self.timers_info[timer_name] = {'message':message,'timelength':timelength,'chatlength':chatlength,'n-o-m':0,'status':True}
        self.start_timer(timer_name)
        self.message_channel(timer_name + ' has been successfully added as a timer!')
        self.save_file()
        return
    def edit_timer(self,message):
        timer_name = message[2]
        del message[0:3]
        if timer_name not in self.timers_info.keys():
            self.message_channel(timer_name + " does not exist.")
            return
        timelength = self.timers_info[timer_name]['timelength']
        chatlength = self.timers_info[timer_name]['chatlength']
        prev_msg = self.timers_info[timer_name]['message']
        for check in range(len(message)):
            if message[check][:12].lower() == "-timelength=":
                timelength = message[check][12:]
                if timelength.isdigit() == False:
                    self.message_channel("Time length needs to be a number.")
                    return
                timelength = int(timelength)
                if timelength < 60:
                    self.message_channel("Time length needs to be 60 seconds or greater.")
                    return
                message[check] = ''
            if message[check][:12].lower() == '-chatlength=':
                chatlength = message[check][12:]
                if chatlength.isdigit() == False:
                    self.message_channel("Chat length needs to be a number.")
                    return
                chatlength = int(chatlength)
                if chatlength < 1:
                    self.message_channel("Chat length needs to be 1 or greater.")
                    return
                message[check]=''
            if message[check][:9]  == '-command=':
                command =  message[check][9:]
                if command not in self.commands.keys():
                    self.message_channel(command + " is not a command.")
                    return

        if message == '':
            message = prv_message
        message = "".join(message)
        self.timers_info[timer_name] = {'message':message,'timelength':timelength,'chatlength':chatlength,'n-o-m':0,'status':True}
        self.message_channel(timer_name + ' has been successfully edited!')
        self.stop_timer(timer_name)
        self.start_timer(timer_name)
        self.save_file()        
        return
    def delete_timer(self,message):
        timer_name = message[2]
        del message[0:3]
        print(self.timers_info.keys())
        if timer_name not in self.timers_info.keys():
            self.message_channel(timer_name + " timer does not exist.")
            return
        self.stop_timer(timer_name)
        del self.timers_info[timer_name]
        self.message_channel(timer_name + " timer has been deleted.")
        return
    def timer_on(self,message):
        timer_name = message[2]
        if timer_name not in self.timers_info.keys():
            self.message_channel(timer_name + " timer does not exist.")
            return
        if selfs.timers_info[timer]['status'] == True:
            self.message_channel(timer_name + " timer is already on.")
            return            
        self.start_timer(timer)
        self.message_channel(timer_name + " timer is now on.")
        return
    def timer_off(self,message):
        timer_name = message[2]
        if timer_name not in self.timers_info.keys():
            self.message_channel(timer_name + " timer does not exist.")
            return
        if selfs.timers_info[timer]['status'] == True:
            self.message_channel(timer_name + " timer is already on.")
            return            
        self.start_timer(timer)
        self.message_channel(timer_name + " timer is now on.")
        return    
    def ran_command(self,command):
        for timer in self.timers_info.keys():
            if self.timers_info[timer][4] == command:
                self.stop_timer(timer)
                self.start_timer(timer)
        return
    def stop_all_timers(self):
        for timer in self.timers:
            timer.cancel()
        return
    
        
    