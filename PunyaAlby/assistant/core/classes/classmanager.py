import time
import logging 
import platform

import pyrogram
from config import Config
from telegraph import Telegraph
from pyrogram import __version__ as pyrogram_version
from main.core.helpers import Helpers
from main.core.newpyrogram import Methods






class ClassManager(Config, Helpers, Methods):
    # versions /
    python_version = str(platform.python_version())
    pyrogram_version = str(pyrogram_version)

    # assistant /
    assistant_name = "ALBY"
    assistant_version = "v.0.0.4"

    # userbot /
    userbot_name = "ALBY-Pyrobot"
    userbot_version = "v.0.1.5"

    # containers /
    CMD_HELP = {}

    # owner details /
    owner_name = "࿇•[『ⒶⓁⒷⓎ』](https://t.me/punya_alby)•࿇"
    owner_id = 1441342342
    owner_username = "@Punya_Alby"

    # other /
    message_ids = {}
    PIC = "https://telegra.ph/file/38eec8a079706b8c19eae.mp4"
    Repo = "https://github.com/bitchlah/pyroku.git"
    StartTime = time.time()
    utube_object = object
    callback_user = None
    whisper_ids = {}

    # debugging /
    
   
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
    logging.getLogger("pyrogram.session.session").setLevel(logging.WARNING) 
    logging.getLogger("pyrogram.session.internals.msg_id").setLevel(logging.WARNING)
    logging.getLogger("pyrogram.dispatcher").setLevel(logging.WARNING)
    logging.getLogger("pyrogram.connection.connection").setLevel(logging.WARNING)
    log = logging.getLogger()

    # telegraph /
    telegraph = Telegraph()
    telegraph.create_account(short_name=Config.TL_NAME or "ALBY-Pyrobot")
