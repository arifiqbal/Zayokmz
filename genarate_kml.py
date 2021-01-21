import mysql.connector
from lxml import etree
from util import write2File, indent, addElement, addSimpleDataElement, addPlaceMrk, getLocation, addBBPlaceMrk
from PlaceMark import PlaceMark

mydb = mysql.connector.connect(
    host="cicada.zayo.us",
    user="eng_user",
    password="||88&Shop&Hurry&River&44||",
    database="correlation_data"
)
curser =  mydb.cursor();

main_doc_tag = etree.fromstring('''
<Document>
	<name>Zayo Packet Network Testing 2020.kmz</name>
	<Schema name="clean_locations_temp" id="S_clean_locations_temp_SSDDSSSSS">
		<SimpleField type="string" name="CLLI"><displayName>&lt;b&gt;CLLI&lt;/b&gt;</displayName>
</SimpleField>
		<SimpleField type="string" name="Site"><displayName>&lt;b&gt;Site&lt;/b&gt;</displayName>
</SimpleField>
		<SimpleField type="double" name="Long"><displayName>&lt;b&gt;Long&lt;/b&gt;</displayName>
</SimpleField>
		<SimpleField type="double" name="Lat"><displayName>&lt;b&gt;Lat&lt;/b&gt;</displayName>
</SimpleField>
		<SimpleField type="string" name="Street"><displayName>&lt;b&gt;Street&lt;/b&gt;</displayName>
</SimpleField>
		<SimpleField type="string" name="City"><displayName>&lt;b&gt;City&lt;/b&gt;</displayName>
</SimpleField>
		<SimpleField type="string" name="State"><displayName>&lt;b&gt;State&lt;/b&gt;</displayName>
</SimpleField>
		<SimpleField type="string" name="Country"><displayName>&lt;b&gt;Country&lt;/b&gt;</displayName>
</SimpleField>
		<SimpleField type="string" name="Equipment"><displayName>&lt;b&gt;Equipment&lt;/b&gt;</displayName>
</SimpleField>
	</Schema>
	<Style id="normPointStyle">´
		<IconStyle>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
			</Icon>
		</IconStyle>
		<BalloonStyle>
			<text>
			<!-- cdata_start -->
			<![CDATA[
                <table border="0">
                  <tr><td><b>CLLI</b></td><td>$[clean_locations_temp/CLLI]</td></tr>
                  <tr><td><b>Site</b></td><td>$[clean_locations_temp/Site]</td></tr>
                  <tr><td><b>Long</b></td><td>$[clean_locations_temp/Long]</td></tr>
                  <tr><td><b>Lat</b></td><td>$[clean_locations_temp/Lat]</td></tr>
                  <tr><td><b>Street</b></td><td>$[clean_locations_temp/Street]</td></tr>
                  <tr><td><b>City</b></td><td>$[clean_locations_temp/City]</td></tr>
                  <tr><td><b>State</b></td><td>$[clean_locations_temp/State]</td></tr>
                  <tr><td><b>Country</b></td><td>$[clean_locations_temp/Country]</td></tr>
                  <tr><td><b>Equipment</b></td><td>$[clean_locations_temp/Equipment]</td></tr>
                </table>
            ]]>
            <!-- cdata_end -->
            </text>
		</BalloonStyle>
	</Style>
	<Style id="hlightPointStyle">
		<IconStyle>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle_highlight.png</href>
			</Icon>
		</IconStyle>
		<BalloonStyle>
			<text>
			<!-- cdata_start -->
			<![CDATA[
			<table border="0">
              <tr><td><b>CLLI</b></td><td>$[clean_locations_temp/CLLI]</td></tr>
              <tr><td><b>Site</b></td><td>$[clean_locations_temp/Site]</td></tr>
              <tr><td><b>Long</b></td><td>$[clean_locations_temp/Long]</td></tr>
              <tr><td><b>Lat</b></td><td>$[clean_locations_temp/Lat]</td></tr>
              <tr><td><b>Street</b></td><td>$[clean_locations_temp/Street]</td></tr>
              <tr><td><b>City</b></td><td>$[clean_locations_temp/City]</td></tr>
              <tr><td><b>State</b></td><td>$[clean_locations_temp/State]</td></tr>
              <tr><td><b>Country</b></td><td>$[clean_locations_temp/Country]</td></tr>
              <tr><td><b>Equipment</b></td><td>$[clean_locations_temp/Equipment]</td></tr>
            </table>
            ]]>
            <!-- cdata_start -->
            </text>
		</BalloonStyle>
	</Style>
	<StyleMap id="pointStyleMap">
		<Pair>
			<key>normal</key>
			<styleUrl>#normPointStyle</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#hlightPointStyle</styleUrl>
		</Pair>
	</StyleMap>
</Document>
 ''')

bb_doc_tag = etree.fromstring('''
	<Document>
			<name>Backbone Facilities</name>
			<StyleMap id="m_ylw-pushpin">
				<Pair>
					<key>normal</key>
					<styleUrl>#s_ylw-pushpin1</styleUrl>
				</Pair>
				<Pair>
					<key>highlight</key>
					<styleUrl>#s_ylw-pushpin_hl1</styleUrl>
				</Pair>
			</StyleMap>
			<Style id="s_ylw-pushpin_hl3">
				<IconStyle>
					<scale>1.3</scale>
					<Icon>
						<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
					</Icon>
					<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
				</IconStyle>
				<LineStyle>
					<color>ff0000aa</color>
					<width>3</width>
				</LineStyle>
			</Style>
			<Style id="s_ylw-pushpin">
				<IconStyle>
					<scale>1.1</scale>
					<Icon>
						<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
					</Icon>
					<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
				</IconStyle>
				<LineStyle>
					<color>ffff00ff</color>
					<width>3</width>
				</LineStyle>
			</Style>
			<Style id="s_ylw-pushpin_hl1">
				<IconStyle>
					<scale>1.3</scale>
					<Icon>
						<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
					</Icon>
					<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
				</IconStyle>
				<LineStyle>
					<color>ffffff55</color>
					<width>3</width>
				</LineStyle>
			</Style>
			<StyleMap id="m_ylw-pushpin0">
				<Pair>
					<key>normal</key>
					<styleUrl>#s_ylw-pushpin2</styleUrl>
				</Pair>
				<Pair>
					<key>highlight</key>
					<styleUrl>#s_ylw-pushpin_hl2</styleUrl>
				</Pair>
			</StyleMap>
			<StyleMap id="m_ylw-pushpin3">
				<Pair>
					<key>normal</key>
					<styleUrl>#s_ylw-pushpin4</styleUrl>
				</Pair>
				<Pair>
					<key>highlight</key>
					<styleUrl>#s_ylw-pushpin_hl3</styleUrl>
				</Pair>
			</StyleMap>
			<Style id="s_ylw-pushpin1">
				<IconStyle>
					<scale>1.1</scale>
					<Icon>
						<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
					</Icon>
					<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
				</IconStyle>
				<LineStyle>
					<color>ffffff55</color>
					<width>3</width>
				</LineStyle>
			</Style>
			<Style id="s_ylw-pushpin0">
				<IconStyle>
					<scale>1.1</scale>
					<Icon>
						<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
					</Icon>
					<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
				</IconStyle>
				<LineStyle>
					<color>ff00aaff</color>
					<width>3</width>
				</LineStyle>
			</Style>
			<Style id="s_ylw-pushpin_hl2">
				<IconStyle>
					<scale>1.3</scale>
					<Icon>
						<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
					</Icon>
					<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
				</IconStyle>
				<LineStyle>
					<color>ff00ff00</color>
					<width>3</width>
				</LineStyle>
			</Style>
			<Style id="s_ylw-pushpin_hl0">
				<IconStyle>
					<scale>1.3</scale>
					<Icon>
						<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
					</Icon>
					<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
				</IconStyle>
				<LineStyle>
					<color>ff00aaff</color>
					<width>3</width>
				</LineStyle>
			</Style>
			<Style id="s_ylw-pushpin4">
				<IconStyle>
					<scale>1.1</scale>
					<Icon>
						<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
					</Icon>
					<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
				</IconStyle>
				<LineStyle>
					<color>ff0000aa</color>
					<width>3</width>
				</LineStyle>
			</Style>
			<Style id="s_ylw-pushpin3">
				<IconStyle>
					<scale>1.1</scale>
					<Icon>
						<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
					</Icon>
					<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
				</IconStyle>
				<LineStyle>
					<color>ffff5500</color>
					<width>3</width>
				</LineStyle>
			</Style>
			<Style id="s_ylw-pushpin_hl4">
				<IconStyle>
					<scale>1.3</scale>
					<Icon>
						<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
					</Icon>
					<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
				</IconStyle>
				<LineStyle>
					<color>ffff00ff</color>
					<width>3</width>
				</LineStyle>
			</Style>
			<StyleMap id="m_ylw-pushpin2">
				<Pair>
					<key>normal</key>
					<styleUrl>#s_ylw-pushpin</styleUrl>
				</Pair>
				<Pair>
					<key>highlight</key>
					<styleUrl>#s_ylw-pushpin_hl4</styleUrl>
				</Pair>
			</StyleMap>
			<StyleMap id="m_ylw-pushpin1">
				<Pair>
					<key>normal</key>
					<styleUrl>#s_ylw-pushpin0</styleUrl>
				</Pair>
				<Pair>
					<key>highlight</key>
					<styleUrl>#s_ylw-pushpin_hl0</styleUrl>
				</Pair>
			</StyleMap>
			<Style id="s_ylw-pushpin_hl">
				<IconStyle>
					<scale>1.3</scale>
					<Icon>
						<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
					</Icon>
					<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
				</IconStyle>
				<LineStyle>
					<color>ffff5500</color>
					<width>3</width>
				</LineStyle>
			</Style>
			<StyleMap id="m_ylw-pushpin4">
				<Pair>
					<key>normal</key>
					<styleUrl>#s_ylw-pushpin3</styleUrl>
				</Pair>
				<Pair>
					<key>highlight</key>
					<styleUrl>#s_ylw-pushpin_hl</styleUrl>
				</Pair>
			</StyleMap>
			<Style id="s_ylw-pushpin2">
				<IconStyle>
					<scale>1.1</scale>
					<Icon>
						<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
					</Icon>
					<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
				</IconStyle>
				<LineStyle>
					<color>ff00ff00</color>
					<width>3</width>
				</LineStyle>
			</Style>
			
</Document>
 ''')



if __name__ == "__main__":

    kml = etree.Element('kml')

    #doc = etree.Element('Document')
    kml.append(main_doc_tag)
    main_folder = etree.Element('Folder')
    name_tag = etree.Element('name')
    name_tag.text = 'Zayo Packet Network'
    open_tag = etree.Element('open')
    open_tag.text = '1'
    main_folder.append(name_tag)
    main_folder.append(open_tag)

    comment = etree.Comment("Backbone document start")
    main_folder.append(comment)
    main_folder.append(bb_doc_tag)
    bb_folder = etree.Element('Folder')
    comment = etree.Comment("Backbone document end")
    main_folder.append(comment)

    bb_folder = etree.Element('Folder')
    bb_doc_tag.append(bb_folder)

    # processing BB data
    curser.execute(
        "SELECT bb.from_cli,bb.to_cli,"
        "from_cordinates.longitude from_longitude,from_cordinates.lattitude from_lattitude,"
        "to_cordinates.longitude to_longitude,to_cordinates.lattitude to_lattitude FROM"
        " test.tbl_back_bone bb,test.tbl_cli_cordinates from_cordinates,test.tbl_cli_cordinates to_cordinates "
        "WHERE bb.from_cli=from_cordinates.cli AND bb.to_cli=to_cordinates.cli AND ("
        "bb.from_cli in (select cli_code from  test.tbl_pop_data) OR bb.to_cli in (select cli_code from  test.tbl_pop_data) "
        ")"
    )
    pop_data = curser.fetchall()
    for y in pop_data:
        bb_cordinates = '%f,%f,0 %f,%f,0' % (y[2], y[3],y[4],y[5])
        bb_pop_pm = addBBPlaceMrk(y[0], y[1],bb_cordinates)
        bb_folder.append(bb_pop_pm)

    main_doc_tag.append(main_folder)
    folder_layer0 = etree.Element('Folder')
    folder_layer0.set("id", "layer 0")
    main_folder.append(folder_layer0)
    name2 = etree.Element('name')
    name2.text = 'Zayo POP Locations'
    folder_layer0.append(name2)



    # processing pop data
    curser.execute("SELECT cli_code equipment_id,site equipment_name,street,city,state,country,comment,cordinates.longitude,cordinates.lattitude "
                   "FROM test.tbl_pop_data pop,test.tbl_cli_cordinates cordinates WHERE pop.cli_code=cordinates.cli")
    pop_data = curser.fetchall()
    for x in pop_data:
        print(x)
        pm = PlaceMark(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7],x[8])
        #pm.setComment(comment)
        pop_pm = addPlaceMrk(pm)
        folder_layer0.append(pop_pm)


    indent(kml)
    tree = etree.ElementTree(kml)
    tree.write("out_put.kml", xml_declaration=True, encoding='utf-8', method="xml")
