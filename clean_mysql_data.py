import mysql.connector
from lxml import etree
from util import write2File,indent,addElement,addSimpleDataElement,addPlaceMrk,getLocation
from PlaceMark import PlaceMark
import re

import logging
import logging.handlers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/clean_mysql_data.log"),
        logging.StreamHandler()
    ]
)

log = logging.getLogger(__name__)


mydb = mysql.connector.connect(
    host="cicada.zayo.us",
    user="eng_user",
    password="||88&Shop&Hurry&River&44||",
    database="correlation_data"
)
curser =  mydb.cursor();

def truncate_pop_data():
    sql = "truncate test.tbl_cli_cordinates"
    curser.execute(sql)
    logging.info("truncated test.tbl_cli_cordinates")


    sql = "truncate test.tbl_pop_data"
    curser.execute(sql)
    logging.info("truncated test.tbl_pop_data")

    sql = "truncate test.tbl_back_bone"
    curser.execute(sql)
    logging.info("truncated test.tbl_back_bone")

    mydb.commit()

if __name__ == "__main__":
    truncate_pop_data()



