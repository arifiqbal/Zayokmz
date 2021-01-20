import mysql.connector
from lxml import etree
from util import write2File,indent,addElement,addSimpleDataElement,addPlaceMrk,getLocation,getLocation_list
from PlaceMark import PlaceMark
import re
import logging
import logging.handlers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/extraction_data.log"),
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

def insert_pop_data(placemark):
    sql = "INSERT INTO test.tbl_pop_data (cli_code,site,street,city,state,country,equipment,comment)VALUES ('"+placemark.cli_code+"','"+placemark.site+"','"+placemark.street+"'," \
           "'"+placemark.city+"','"+placemark.state+"','"+placemark.country+"','"+placemark.equipment+"','"+placemark.comment+"');"
    try:
        curser.execute(sql)
        mydb.commit()
    except Exception as err:
        log.error(err)

def extract_pop_data():
    curser.execute("SELECT equipment_id,equipment_name,addr_ln1,addr_ln2,addr_ln3,legacy_node_name FROM node_data WHERE architectural_group = 'AS6461' ORDER BY equipment_name")
    myresult = curser.fetchall()

    # initialising
    cli_code = ''
    prev_cli = None
    site = ''
    street = ''
    country = ''
    city = ''
    state = ''
    equipment = ''
    comment = ''
    long= 0
    lat =0
    counter=1
    actual_count = 1

    for x in myresult:

        counter=counter+1
        if x[1] is None:
            log.debug(x)
            continue

        log.info(str(counter).zfill(3) +'  '+ str(actual_count).zfill(3) + '   ' +  x[1])
        # if counter==20 :break;

        if prev_cli is None :
            equipment = equipment + x[5] + ','
            comment = comment + x[1] + ','
            cli_code = x[1][0:8]
            prev_cli = cli_code
        elif prev_cli == x[1][0:8]:
            equipment = equipment + x[5] + ','
            comment = comment + x[1] + ','
            cli_code = x[1][0:8]
            prev_cli = cli_code
            continue
        else :
            pm = PlaceMark(cli_code, site,street,city,state,country,equipment,long,lat)
            pm.setComment(comment)
            insert_pop_data(pm)
            actual_count = actual_count + 1
            cli_code = x[1][0:8]
            prev_cli = cli_code
            equipment = x[5] + ','
            comment =  x[1] + ','

        site = cli_code
        street = x[2]
        country = x[4]
        city = ''
        state = ''

        if x[3] is not None :
            st_list = x[3].split()
            try:
                city = ' '.join(st_list[0:-2])
            except Exception as err:
                log.info(st_list)
                log.info('Handling run-time error:', err)
            state = st_list[-2]

    pm = PlaceMark(cli_code, site,street,city,state,country,equipment,long,lat)
    pm.setComment(comment)
    insert_pop_data(pm)

def extract_backbone_data():
    curser.execute("SELECT c.exchange_carrier_circuit_id FROM correlation_data.m6_circuit c WHERE exchange_carrier_circuit_id LIKE '70%'")  # LIMIT 20
    myresult = curser.fetchall()
    final_dict ={}
    final_cli_list = set()
    for_counter = 0
    duplicate_count = 0
    duplicate_bb_count = 0
    for x in myresult:
        try:
            cli_list = re.findall( r'[a-zA-Z0-9]{11}', x[0])
            try:
                if cli_list[0][0:8] in final_cli_list :
                    duplicate_count = duplicate_count + 1
                final_cli_list.add(cli_list[0][0:8])
            except Exception as err:
                log.info('error@reading data for %s --> %s  : '% (x[0],str(err)))
            try:
                if cli_list[1][0:8] in final_cli_list :
                    duplicate_count = duplicate_count + 1
                final_cli_list.add(cli_list[1][0:8])
            except Exception as err:
                log.info('error@reading data for %s --> %s  : '% (x[0],str(err)))

            key = x[0][0:2]+cli_list[0][0:8]
            if key in final_dict :
                duplicate_bb_count = duplicate_bb_count +1
                final_dict[key].add(cli_list[1][0:8])
            else:
                final_dict[key] = {cli_list[1][0:8],}
        except Exception as err:
            log.info('error@reading data for %s --> %s  : '% (x[0],str(err)))
        for_counter = for_counter + 1
        if for_counter % 100 == 0 :
            log.info(str(for_counter) + ' back bones extracted')

    log.info('%d backbones found' % len(final_dict))
    log.info('%d duplicate backbones found' % duplicate_bb_count)
    for_counter = 0
    for key, value  in final_dict.items():
        try:
            sql = "INSERT INTO test.tbl_back_bone VALUES ('"+key[2:]+"','"+','.join(str(s) for s in value)+"','"+key[0:2]+"');"
            curser.execute(sql)
        except Exception as err:
            log.info('error@INSERT INTO test.tbl_back_bone : ', err)
        for_counter = for_counter + 1
        if for_counter % 100 == 0 :
            log.info(str(for_counter) + ' back bones inserted')
            mydb.commit()
    log.info('Records inserted into tbl_back_bone')

    log.info('%d clis found' % len(final_cli_list))
    log.info('%d duplicate clis found' % duplicate_count)
    cli_list = []
    for_counter = 0
    completed = 0
    for cli  in final_cli_list:
        for_counter = for_counter + 1
        if len(cli_list) <  19 :
            cli_list.append(cli)
        else:
            try:
                cli_list.append(cli)
                long_lat_list = getLocation_list(cli_list)
                completed = completed + len(long_lat_list)
                for item in long_lat_list:
                    try:
                        sql = "INSERT INTO test.tbl_cli_cordinates VALUES ('"+item[0]+"',"+str(item[1])+","+str(item[2])+");"
                        curser.execute(sql)
                    except Exception as err:
                        log.info('error@INSERT INTO test.tbl_cli_cordinates : %s ' % (err,))
            except Exception as err:
                log.info('error@INSERT INTO test.tbl_cli_cordinates1 : %s ' % (err,))
            cli_list.clear()
            log.info(str(for_counter) + ' back bones inserted')
            log.info(str(completed) + ' completed')
            mydb.commit()
    try:
        long_lat_list = getLocation_list(cli_list)
        for item in long_lat_list:
            sql = "INSERT INTO test.tbl_cli_cordinates VALUES ('"+item[0]+"',"+str(item[1])+","+str(item[2])+");"
            curser.execute(sql)
    except Exception as err:
        log.info('error@INSERT INTO test.tbl_cli_cordinates :', err)
    mydb.commit()
    log.info('Records inserted into tbl_cli_cordinates')

if __name__ == "__main__":
    extract_pop_data()
    extract_backbone_data()


