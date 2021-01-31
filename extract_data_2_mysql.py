import mysql.connector
from lxml import etree

from Config import Config
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
    str()
    sql = "INSERT INTO test.tbl_pop_data (cli_code,site,street,city,state,country,equipment,comment)VALUES ('"+xstr(placemark.cli_code)+"','"+xstr(placemark.site)+"','"+xstr(placemark.street)+"'," \
           "'"+xstr(placemark.city)+"','"+xstr(placemark.state)+"','"+xstr(placemark.country)+"','"+xstr(placemark.equipment)+"','"+xstr(placemark.comment)+"');"
    try:
        curser.execute(sql)
        mydb.commit()
    except Exception as err:
        log.error(err)

def xstr(s):
    if s is None:
        return ''
    return s

def extract_pop_data():
    query = "SELECT equipment_id,equipment_name,addr_ln1,addr_ln2,addr_ln3,legacy_node_name FROM node_data WHERE architectural_group is not null and equipment_name is not NULL AND LEFT(equipment_name,8) IN (SELECT cli FROM test.tbl_cli_cordinates) ORDER BY equipment_name"
    curser.execute(query)
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
            if x[5] is not None:
                equipment = equipment + x[5] + ','
            comment = comment + x[1] + ','
            cli_code = x[1][0:8]
            prev_cli = cli_code
        elif prev_cli == x[1][0:8]:
            if x[5] is not None:
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
            if x[5] is not None:
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

def extract_backbone_data(config):
    log.info('processing config  \n'+ config.__str__())
    curser.execute(config.query)  # LIMIT 20
    back_bone_data = curser.fetchall()
    final_dict ={}
    final_cli_list = set()
    for_counter = 0
    duplicate_cli_count = 0
    duplicate_bb_count = 0
    bb_failed = 0;

    """
    Reading all back bones from database
    """
    for x in back_bone_data:
        bb_status = 'success'
        from_cli = 'Failed'
        to_cli = 'Failed'
        try:
            cli_list = re.findall( r'[a-zA-Z0-9]{8}', x[0])
            try:
                from_cli = cli_list[0][0:8]
                if  from_cli in final_cli_list :
                    duplicate_cli_count = duplicate_cli_count + 1
                final_cli_list.add(from_cli)
            except Exception as err:
                bb_status = 'failed'
                log.info('error@reading from cli for %s %s --> %s  : '% (x[1],x[0],str(err)))
            try:
                to_cli = cli_list[1][0:8]
                if to_cli in final_cli_list :
                    duplicate_cli_count = duplicate_cli_count + 1
                final_cli_list.add(to_cli)
            except Exception as err:
                bb_status = 'failed'
                log.info('error@reading to cli for %s %s --> %s  : '% (x[0],str(err)))

            key = from_cli
            if key in final_dict :
                duplicate_bb_count = duplicate_bb_count +1
                final_dict[key].add(to_cli)
            else:
                final_dict[key] = {to_cli,}
        except Exception as err:
            bb_status = 'failed'
            log.info('error@reading data for %s %s --> %s  : '% (x[1],x[0],str(err)))
        if bb_status == 'failed' : bb_failed = bb_failed + 1
        for_counter = for_counter + 1
        if for_counter % 100 == 0 :
            log.info(str(for_counter) + ' back bones extracted out of '+ str(len(back_bone_data)))
            mydb.commit()
        # Insert into bb log
        try:
            sql = "INSERT INTO test.tbl_back_bone_log VALUES ("+str(x[1])+",'"+str(x[0])+"','"+str(config.network)+"','"+from_cli+"','"+to_cli+"','"+bb_status+"');"
            curser.execute(sql)
        except Exception as err:
            log.info('error while inserting in to bb_log  : %s ', str(err))

    log.info('%d backbones found' % len(back_bone_data))
    log.info('%d failes backbones found' % bb_failed)

    log.info('%d clis found' % len(final_cli_list))
    log.info('%d duplicate clis found' % duplicate_cli_count)


    log.info('%d backbones found' % len(final_dict))
    log.info('%d duplicate backbones found' % duplicate_bb_count)
    for_counter = 0
    from_cli_list = []
    for key, value  in final_dict.items():
        from_cli = key[2:].strip()
        if(from_cli_list.__contains__(from_cli)):continue
        try:
            sql = "INSERT INTO test.tbl_back_bone VALUES ("+str(config.network)+",'"+config.name+"','"+from_cli+"','"+','.join(str(s) for s in value)+"','"+str(len(value))+"');"
            from_cli_list.append(from_cli)
            curser.execute(sql)
        except Exception as err:
            log.info('error@INSERT INTO test.tbl_back_bone : %s ', str(err))
        for_counter = for_counter + 1
        if for_counter % 100 == 0 :
            log.info(str(for_counter) + ' back bones inserted for '+ config.name + ' -- ' +str(final_dict.__len__()))
            mydb.commit()
    log.info('Records inserted into tbl_back_bone')

    """
    Inserting Cordinates
    """
    cli_list = []
    inserted_cli_list = []
    for_counter = 0
    completed = 0
    for cli  in final_cli_list:
        for_counter = for_counter + 1
        if inserted_cli_list.__contains__(cli) : continue
        inserted_cli_list.append(cli)
        if len(cli_list) <  99 :
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
            log.info(str(for_counter) + ' back cordinates inserted for '+ config.name)
            log.info(str(completed) + ' completed out of ' + str(len(final_cli_list)))
            mydb.commit()

    long_lat_list = getLocation_list(cli_list)
    for item in long_lat_list:
        try:
            print(item)
            sql = "INSERT INTO test.tbl_cli_cordinates VALUES ('"+item[0]+"',"+str(item[1])+","+str(item[2])+");"
            curser.execute(sql)
        except Exception as err:
            log.info('error@INSERT INTO test.tbl_cli_cordinates : %s ' % (err,))

    mydb.commit()
    log.info('Records inserted into tbl_cli_cordinates')

def extract_config_data():
    curser.execute("SELECT * FROM test.tbl_config WHERE UPPER(genarate)='Y'")
    myresult = curser.fetchall()
    for rec in myresult:
        config = Config(rec[0],rec[1],rec[2],rec[3])
        extract_backbone_data(config)


if __name__ == "__main__":

    extract_config_data();
    extract_pop_data()



