# encoding: utf-8

"""
Copyright (c) 2017, Ernesto Ruge
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import os
import logging
from logging.handlers import WatchedFileHandler
from flask import current_app
from ..extensions import mail, celery
from flask_mail import Message
from ..config import DefaultConfig


class Logger:
    registered_logs = []

    def __init__(self):
        self.config = DefaultConfig

    def get_log(self, log_name):
        logger = logging.getLogger(log_name)
        if log_name in self.registered_logs:
            return logger
        logger.setLevel(logging.INFO)

        # Init File Handler
        file_name = os.path.join(self.config.LOG_DIR, '%s.log' % log_name)
        file_handler = WatchedFileHandler(file_name)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s ')
        )
        logger.addHandler(file_handler)

        file_name = os.path.join(self.config.LOG_DIR, '%s.err' % log_name)
        file_handler = WatchedFileHandler(file_name)
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s ')
        )
        logger.addHandler(file_handler)

        if self.config.DEBUG:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_format = logging.Formatter('%(message)s')
            console_handler.setFormatter(console_format)
            logger.addHandler(console_handler)

        self.registered_logs.append(log_name)
        return logger

    def debug(self, log_name, message):
        self.get_log(log_name).debug(message)

    def info(self, log_name, message):
        self.get_log(log_name).info(message)

    def warn(self, log_name, message):
        self.get_log(log_name).warning(message)

    def error(self, log_name, message, details=None):
        self.get_log(log_name).error(message)
        send_notification.delay('error', log_name, message, details)

    def exception(self, log_name, message, details=None):
        self.get_log(log_name).exception(message)
        send_notification.delay('exception', log_name, message, details)

    def critical(self, log_name, message, details=None):
        self.get_log(log_name).critical(message)
        send_notification.delay('critical', log_name, message, details)


@celery.task
def send_notification(level, log_name, message, details):
    try:
        if current_app.config['DEBUG']:
            return
        msg = Message(
            "%s %s Fehler" % (current_app.config['PROJECT_NAME'], current_app.config['MODE']),
            sender=current_app.config['MAILS_FROM'],
            recipients=current_app.config['ADMINS'],
            body="Auf %s %s ist im Bereich %s folgender Fehler der Klasse %s aufgetreten %s\n\nDetails:\n%s" % (
                current_app.config['PROJECT_NAME'],
                current_app.config['MODE'],
                log_name,
                level,
                message,
                details if details else 'keine'
            )
        )
        mail.send(msg)
    except:
        pass