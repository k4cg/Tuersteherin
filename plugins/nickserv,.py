import ConfigParser
from plugin import Plugin

class Nickserv(Plugin):
  def __init__(self, config=None):
    super(Nickserv, self).__init__()

    try:
      self.nickservpassword=config.get('IRC', 'nickservpassword')
      self.identified = False
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
      self.identified = True # No password -> no auth

  def on_notice(self, bot, user_nick, host, channel, message):
    if user_nick.lower() == "nickserv" and ("msg NickServ identify") and not self.identified:
      self.identified = True
      bot.send_command("NickServ", "identify " + self.nickservpassword)
