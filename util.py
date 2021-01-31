import sys
from lxml import etree
from simple_salesforce import Salesforce


def write2File(file_name, file_content):
    with open(file_name, 'w') as f:
        print(file_content, file=f)


def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def addElement(name, value):
    tag = etree.Element(name)
    tag.text = value
    return tag


def addSimpleDataElement(name, value):
    tag = etree.Element("SimpleData")
    tag.attrib['name'] = name
    tag.text = str(value).strip()
    return tag


def addPlaceMrk(placemark):
    pm_style_url_tag = etree.fromstring('''
    <styleUrl>#pointStyleMap</styleUrl>
    ''')
    pm_style_tag = etree.fromstring('''
    <Style id="inline">
        <IconStyle>
            <color>ff00aaff</color>
            <colorMode>normal</colorMode>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/paddle/red-diamond.png</href>
            </Icon>
        </IconStyle>
        <LineStyle>
            <color>ff00aaff</color>
            <colorMode>normal</colorMode>
        </LineStyle>
        <PolyStyle>
            <color>ff00aaff</color>
            <colorMode>normal</colorMode>
        </PolyStyle>
    </Style>
    ''')
    pop_pm = etree.Element('Placemark')
    pop_name = etree.Element('name')
    if placemark.comment:
        comment = etree.Comment(placemark.comment)
        pop_pm.append(comment)
    pop_name.text = placemark.cli_code
    pop_pm.append(pop_name)
    pop_pm.append(pm_style_url_tag)
    pop_pm.append(pm_style_tag)

    ed = etree.Element('ExtendedData')
    pop_pm.append(ed)

    scd = etree.Element('SchemaData')
    ed.append(scd)
    scd.set("schemaUrl", "#S_clean_locations_temp_SSDDSSSSS")
    scd.append(addSimpleDataElement('CLLI', placemark.cli_code))
    scd.append(addSimpleDataElement('Site', placemark.site))
    scd.append(addSimpleDataElement('Street', placemark.street))
    scd.append(addSimpleDataElement('City', placemark.city))
    scd.append(addSimpleDataElement('State', placemark.state))
    scd.append(addSimpleDataElement('Country', placemark.country))
    scd.append(addSimpleDataElement('Equipment', placemark.equipment))

    scd.append(addSimpleDataElement('Long', '%.3f' % (placemark.long)))
    scd.append(addSimpleDataElement('Lat', '%.3f' % (placemark.lat)))

    pt = etree.Element('Point')
    pop_pm.append(pt)
    cord = etree.Element('coordinates')
    cord.text = str(placemark.long) + "," + str(placemark.lat)
    pt.append(cord)
    return pop_pm


def addBBPlaceMrk(from_cli, to_cli, cordinate_str,color):
    print('%s %s %s ' % (from_cli, to_cli, cordinate_str))
    pm_tag_str = '''
    <Placemark>
        <name>BB Facility %s to %s</name>
        <styleUrl>#%s</styleUrl>
        <LineString>
            <tessellate>1</tessellate>
            <coordinates>
                %s
            </coordinates>
        </LineString>
    </Placemark>
    ''' % (from_cli, to_cli,color, cordinate_str)
    pm_tag = etree.fromstring(pm_tag_str)
    return pm_tag


def getLocation(cli_code):
    lat = 0
    long = 0
    sfuname = "arif.iqbal@zayo.com"
    sfpass = "kV#LVFQ!T5EeGyE"
    sfsecurity = "6DFw0At9VLOO1taoNEByhleZ"
    sfinstance = "zayo.my.salesforce.com"
    sfsandbox = False
    # Salesforce Login
    sf = Salesforce(sfuname, sfpass, sfsecurity, sfinstance, sfsandbox)
    sfquery = sf.query("SELECT Latitude__c, Longitude__c FROM Building__c WHERE CLLI_Code__c ='" + cli_code + "'")
    try:
        lat = sfquery["records"][0]["Latitude__c"]
        long = sfquery["records"][0]["Longitude__c"]
    except Exception as err:
        print('error@getLocation ' + cli_code + ':', err)

    return (lat, long)


def getLocation_list(cli_code_list):
    opt = []
    lat = 0
    long = 0
    sfuname = "arif.iqbal@zayo.com"
    sfpass = "kV#LVFQ!T5EeGyE"
    sfsecurity = "6DFw0At9VLOO1taoNEByhleZ"
    sfinstance = "zayo.my.salesforce.com"
    sfsandbox = False
    # Salesforce Login
    sf = Salesforce(sfuname, sfpass, sfsecurity, sfinstance, sfsandbox)
    qry = "SELECT CLLI_Code__c,Latitude__c, Longitude__c FROM Building__c WHERE CLLI_Code__c in ('" + "','".join(
        cli_code_list) + "')"
    sfquery = sf.query(qry)
    list1 = []
    for rec in sfquery["records"]:
        try:
            if rec["CLLI_Code__c"] not in list1:
                list1.append(rec["CLLI_Code__c"])
                opt.append((rec["CLLI_Code__c"], rec["Longitude__c"], rec["Latitude__c"]))
        except Exception as err:
            print('error@getLocation ' + rec["CLLI_Code__c"] + ':', err)

    return opt
