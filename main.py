import mysql.connector
from lxml import etree
from util import write2File,indent,addElement,addSimpleDataElement,addPlaceMrk,getLocation
from PlaceMark import PlaceMark

import logging
import logging.config

logging.config.fileConfig('logging.conf')

logger = logging.getLogger('simpleExample')


mydb = mysql.connector.connect(
    host="cicada.zayo.us",
    user="eng_user",
    password="||88&Shop&Hurry&River&44||",
    database="correlation_data"
)
curser =  mydb.cursor();

if __name__ == "__main__":

    kml = etree.Element('kml')
    doc = etree.Element('Document')
    kml.append(doc)
    name = etree.Element('name')
    name.text = 'Zayo Packet Network Testing 2020.kmz'
    doc.append(name)
    folder = etree.Element('Folder')
    doc.append(folder)
    open = etree.Element('open')
    open.text = '1'
    doc.append(folder)
    name1 = etree.Element('name')
    name1.text = 'Zayo Packet Network'
    folder.append(name1)
    doc1 = etree.Element('Document')
    folder.append(doc1)

    folder_layer0 = etree.Element('Folder')
    folder_layer0.set("id", "layer 0")
    folder.append(folder_layer0)
    name2 = etree.Element('name')
    name2.text = 'Zayo POP Locations'
    folder_layer0.append(name2)

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
    i=1


    for x in myresult:
        print(i)
        i=i+1
        if x[1] is None:
            print(x)
            continue
        # if i==20 :break;

        if prev_cli is None or prev_cli == x[1][0:8]:
            equipment = equipment + x[5] + ','
            comment = comment + x[1] + ','
            cli_code = x[1][0:8]
            prev_cli = cli_code
            continue
        else :
            pm = PlaceMark(cli_code, site,street,city,state,country,equipment,long,lat)
            pm.setComment(comment)
            pop_pm = addPlaceMrk(pm)
            folder_layer0.append(pop_pm)
            cli_code = x[1][0:8]
            prev_cli = cli_code
            equipment = x[5] + ','
            comment =  x[1] + ','


        site = cli_code
        street = x[2]
        country = x[4]
        city = ''
        state = ''
        long_lat = getLocation(cli_code)
        long= long_lat[1]
        lat = long_lat[0]

        if x[3] is not None :
            st_list = x[3].split()
            try:
                city = ' '.join(st_list[0:-2])
            except Exception as err:
                print(st_list)
                print('Handling run-time error:', err)
            state = st_list[-2]
        # ef __init__(self, cli_code,site,street,city,state,country,equipment,long,lat)


    indent(kml)
    tree = etree.ElementTree(kml)
    tree.write("out_put.kml", xml_declaration=True, encoding='utf-8', method="xml")
