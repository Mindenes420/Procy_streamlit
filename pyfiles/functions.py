import uuid
from datetime import datetime,timedelta
def date(format):
        now = datetime.now()
        date = now.strftime(format)
        return date
def sid():
        sid = uuid.uuid1()
        sid=str(sid).replace('-','').upper()
        return str(sid)
