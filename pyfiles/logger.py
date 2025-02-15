import os
import time,configparser
from datetime import datetime
config = configparser.ConfigParser()



import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
# .ini fájl beolvasása

log_directory = '\\log'
max_file_size = 5
def setup_logger():
    year=datetime.now().strftime("%Y")
    month=datetime.now().strftime("%m")
    day=datetime.now().strftime("%d")
    # Ellenőrizze, hogy a log könyvtár létezik-e, ha nem, hozza létre
    if not os.path.exists(os.path.join(log_directory, year,month,day)):
        os.makedirs(os.path.join(log_directory, year,month,day))

    # Állítsa be a log fájl nevét a jelenlegi dátum és idő alapján
    log_filename = f'Procy_{datetime.now().strftime("%Y%m%d.log")}'
    log_filepath = os.path.join(log_directory, year,month,day,log_filename)

    # Állítsa be a logolót
    logger = logging.getLogger("sqlalchemy.engine.Engine")

    logger.setLevel(logging.INFO)

    # Állítsa be a forgató log fájlkezelőt
    handler = RotatingFileHandler(
        log_filepath,
        maxBytes=int(max_file_size) * 1024 * 1024,  # MB to bytes
        backupCount=0  # Nincs korlátozás a biztonsági másolatok számában
    )
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger.addHandler(handler)

    return logger

# Példa használat


log=setup_logger()