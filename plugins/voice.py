import time
import ConfigParser
from plugin import Plugin
from thread import start_new_thread

class Voice(Plugin):
  def __init__(self, config=None):
    super(Voice, self).__init__()

    try:
      self.delay=int(config.get('Voice', 'delay'))
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
      self.delay = 30

  def on_join(self, bot, user_nick, host, channel):
    #bot.send_message("#" + channel, "Hallo2 " + user_nick, user_nick)
    start_new_thread(mode, (bot, channel, user_nick, self.delay,))

def mode(bot, channel, user_nick, delay):
    #bot.send_message("#" + channel, "Warte fuer " + user_nick, user_nick)
    time.sleep(delay)
    bot.irc.send_raw("MODE #" + channel + " +v " + user_nick)
