from .botconfig import BotConfig, BOTDV
from .otherconfig import OtherConfig, OTHERDV
from .herokuconfig import HerokuConfig, HEROKUDV




class Configs(
    BotConfig,
    OtherConfig,
    HerokuConfig
    ):
    DVLIST = BOTDV + OTHERDV + HEROKUDV
