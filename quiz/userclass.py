import datetime
from dataclasses import dataclass

__version__ = 0.0002


@dataclass(frozen=False)
class User:
    id: int
    name: str
    phone: str
    time = datetime.datetime.now()
    score: int
    last_user_activity = datetime.datetime.now()
    user_activity_treshhold = datetime.timedelta(minutes=1)
