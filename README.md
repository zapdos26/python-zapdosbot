# Welcome To Zapdosbot
This is a Twitch Bot written in Python to assist streamers and moderators do basic functions in streams. 

## Features include:
  #### 1. Customizable Commands
  * Be able to change messages, cooldowns, counts, and permission levels. 
          
  * Variety of Variables
  #### 2. Announces Cheers and Subscriptions
  * Customizable 
#### 3. Optional and Customizable Chat protection


   * Times out links, spamming (letters, symbols, emotes and capital letters), repeated messages, 
      fake deletions, fake donations, forbidden words.
      
   * Optional Regulars and Subscribers Protection from Chat Protection
      
   * Optional Silent Option for Timeouts
      
   * Emote Ignore List. Add emotes which the emote protection ignores.
   
   * Customizable Whitelist. Whitelist words/links to not contribute to chat protection
      
   * Customizable Blackist. Blacklist words to be timed out. Supports wildcards (* and ?)
      
   #### 4. Customizable Timers
        
   * Add, delete, and edit timers via chat with customizable time lengths and 
      number of messages before activation
        
   * Command Support. Put commands on timers. If the command changes, the timer changes as well
  #### 5. Multi & Raid Assistance
  
  * Be able to set custom multi and raid messages
  
  * Easily set multi which can be reused without changing the command.
  Just do: ![multi command] set usernames 
  
  #### 6. Regulars
  * Easily add and remove regulars
  * Adapts to username changes
## Installation Instructions
* Uses irc and emoji packages
* To install a package. Open bash and do the following:
`$ pip install <package name> --upgrade`
### Operation
* To operate, open bash in the directory containing chatbot.py and type the following:

    `$ python chatbot.py <bot username> <client id> <oauth token> <channel>`
