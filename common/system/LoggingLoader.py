#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import logging.config


def setup_logging():
    """Setup logging configuration from ../conf/logging.json
    """
    path = os.path.join(os.path.dirname(__file__), "..", "conf", "logging.json")
    if os.path.exists(path):
        # print("Loading user logger %s" % path)
        with open(path) as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        # print("Loading default logger")
        logging.basicConfig(level=logging.INFO)