#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import time
import ConfigParser
import logging
from plugin import Plugin
from vendor import importdir

from asyncirc.ircbot import IRCBot

class Tuersteherin(object):

  # Constructor
  #

  def __init__(self):

    # load config
    self.config = ConfigParser.ConfigParser()

    if not self.config.read("config.ini"):
      print "Error: your config.ini could not be read"
      exit(1)

    # load plugins
    importdir.do("plugins", globals())
    self.plugins = [module(config=self.config) for module in Plugin.__subclasses__()]

    # load required config
    self.server=self.config.get('IRC','server')
    self.port=int(self.config.get('IRC', 'port'))
    self.nick=self.config.get('IRC', 'nick')
    self.ircchan=self.config.get('IRC', 'ircchan').split(",")
    self.debugchan=self.config.get('IRC', 'debugchan')

    # optional config
    try:
      self.ignore=self.config.get('IRC','ignore').split(',')
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
      self.ignore = []

    try:
      self.joindelay=int(self.config.get('IRC','joindelay'))
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
      self.joindelay = 0

    self.irc = IRCBot(self.server, self.port, self.nick)


  # Helper Methods
  #

  def debug(self, msg):
    logging.debug(msg)

  def send_message(self, recipient, msg, srcuser=''):
      if srcuser not in self.ignore:
        self.irc.msg(recipient, "\x0F" + msg)

  def send_command(self, recipient, cmd):
    self.irc.msg(recipient, cmd)

  # IRC Handlers

  def on_msg(self, irc, user_nick, host, channel, message):
    for plugin in self.plugins:
      plugin.on_msg(self, user_nick, host, channel, message)

  def on_privmsg(self, irc, user_nick, host, message):
    for plugin in self.plugins:
      plugin.on_privmsg(self, user_nick, host, message)

  def on_join(self, irc, user_nick, host, channel):
    for plugin in self.plugins:
      plugin.on_join(self, user_nick, host, channel)

  def on_notice(self, irc, user_nick, host, channel, message):
    for plugin in self.plugins:
      plugin.on_notice(self, user_nick, host, channel, message)


  # Operations

  def run(self):
    # Assign event handlers
    self.irc.on_msg(self.on_msg)
    self.irc.on_privmsg(self.on_privmsg)
    self.irc.on_join(self.on_join)
    self.irc.on_notice(self.on_notice)

    # Start Bot
    self.irc.start()
    
    time.sleep(self.joindelay)
    for channel in self.ircchan:
      self.irc.join(channel)
    self.irc.join(self.debugchan)

    # Run Eventloop
    try:
      while self.irc.running:
	      time.sleep(1)
    except KeyboardInterrupt:
      print("Received exit command")
    finally:
      self.irc.stop()
