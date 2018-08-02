import time
from plugin import Plugin
from thread import start_new_thread

class Voice(Plugin):
  def __init__(self, config=None):
    super(Voice, self).__init__()

  def on_join(self, bot, user_nick, host, channel):
    #bot.send_message("#" + channel, "Hallo2 " + user_nick, user_nick)
    start_new_thread(mode, (bot, channel, user_nick,))
  
def mode(bot, channel, user_nick):
    #bot.send_message("#" + channel, "Warte fuer " + user_nick, user_nick)
    time.sleep(5)
    bot.irc.send_raw("MODE #" + channel + " +v " + user_nick)
