#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#import re
import io
#import sys

import ConfigParser
from hermes_python.hermes import Hermes, MqttOptions
from hermes_python.ontology import *

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"


class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
        except (IOError, ConfigParser.Error) as e:
            return dict()


def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    """
    :param hermes:
    :param intentMessage:
    :param conf:
    :return:
    """
    if len(intentMessage.slots.number) > 0:
        number = intentMessage.slots.number.first().value
        hermes.publish_end_session(intentMessage.session_id, "number")
    else:
        hermes.publish_end_session(intentMessage.session_id, "An error occured")



if __name__ == "__main__":
   with Hermes("localhost:1883") as h:
        h.subscribe_intent("miles-nash:square", subscribe_intent_callback) \
        .start()
