# -*- coding: utf-8 -*-
import consts
import os
import datetime
import time
import random

import pymongo
from pymongo.objectid import ObjectId
db = pymongo.Connection(consts.MONGODB[0], consts.MONGODB[1])['weiin']

from helpers import *