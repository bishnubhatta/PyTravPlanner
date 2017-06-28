#Place ID to details
#https://maps.googleapis.com/maps/api/place/details/xml?placeid=ChIJN1t_tDeuEmsRUsoyG83frY4&key=AIzaSyChZtdT2W7zA8w31Ft0unaeSPSypEkKFcI
#Nearby Search by location
#https://maps.googleapis.com/maps/api/place/nearbysearch/xml?location=-33.8670522,151.1957362&radius=500&type=restaurant&keyword=cruise&key=YOUR_API_KEY
#Nearby Search by text
#https://maps.googleapis.com/maps/api/place/textsearch/xml?query=restaurants+in+Sydney&key=YOUR_API_KEY
#Nearby Search by text, location and radius
#https://maps.googleapis.com/maps/api/place/textsearch/json?query=123+main+street&location=42.3675294,-71.186966&radius=10000&key=YOUR_API_KEY
#Nearby search by Radar
#https://maps.googleapis.com/maps/api/place/radarsearch/xml?location=51.503186,-0.126446&radius=5000&type=museum&key=YOUR_API_KEY
class pygeomaps:
    def __init__(self):
        import ConfigParser
        config = ConfigParser.ConfigParser()
        config.read("/home/bishnu/GeoPy.conf")
        self.api_key=config.get('geopy_config', 'api_key')
        self.place_id_search_link=config.get('geopy_config', 'place_id_search_link')
        self.nearby_search_link_location=config.get('geopy_config', 'nearby_search_link_location')
        self.nearby_text_search_link=config.get('geopy_config', 'nearby_text_search_link')
        self.nearby_radar_search_link=config.get('geopy_config', 'nearby_radar_search_link')
        self.geocode_link=config.get('geopy_config', 'geocode_link')
        self.lat=0.0
        self.lon=0.0
        self.radius=0
        self.final_loc=[]
        self.addr=''
        self.place_type=''
        self.rpt_name=''
        self.circle_colour='#ffcc99'

    def find_all_addresses_with_in_x_km_radius_of_y(self,y,x,option):
        try:
            import math
            center_addr=y
            self.radius=x
            gcode_input_addr=self.geocode_address(center_addr)
            self.lat = gcode_input_addr[6] #Setting center's latitude
            self.lon= gcode_input_addr[7] #Setting center's longitude
            self.addr= gcode_input_addr[4] #Setting center's address
            final_data_list = []
            if option == '2': # For risk circle, data will be fetched from table
                final_data_list = pgm.get_qualifying_locations_risk_circle(self.lat,self.lon,self.radius)
            else:
                final_data_list = pgm.find_places_around_center(self.radius,self.place_type)
            return final_data_list
        except Exception, e:
            print(str(e))

    def plot_addresses_on_google_map(self,lat,lon,titles):
        import gmplot
        # unit of radius in gmplot is meter. so it assumes KM passed as meter.So multiply by 1000
        gmap = gmplot.GoogleMapPlotter(self.lat,self.lon,16)
        gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
        gmap.scatter(lat, lon,titles,'#00FF00', edge_width=10)
        print "Center Location for this circle : " + self.addr
        gmap.marker(self.lat,self.lon,color='#FF0000',title=self.addr)
        gmap.circle(self.lat,self.lon,self.radius*1000,color=self.circle_colour)
        output = "/home/bishnu/"+self.rpt_name+"_gmap.html"
        gmap.draw(output)

    def generate_map_for_location(self,address):
        import gmplot
        self.addr=address
        self.rpt_name='map_for_location_gmap'
        det = self.geocode_address(self.addr)
        self.lat=det[6]
        self.lon=det[7]
        gmap = gmplot.GoogleMapPlotter(self.lat, self.lon, 18)
        gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
        gmap.marker(self.lat, self.lon, color='#FF0000', title=self.addr)
        output = "/home/bishnu/"+self.rpt_name+".html"
        gmap.draw(output)

    def removeNonAscii(self,s):
        return "".join(filter(lambda x: ord(x) < 128, s))

    def geocode_address(self,addr):
        import urllib2,urllib
        import untangle
        #Prepare the URL link
        address=urllib.quote_plus(addr)
        wiki = self.geocode_link + "?address=" + address
        geocode_result=[]
        #Query the website and return the data and parse the xml using untangle
        page = urllib2.urlopen(wiki)
        xmldata = page.read()
        obj = untangle.parse(xmldata)
        # If scrubbing status is OK then result should be received. Not sure how many result.
        scrb_sts = str(obj.GeocodeResponse.status.cdata).strip()
        if scrb_sts == "OK" :
            if(len(obj.GeocodeResponse.get_elements(name='result'))) == 1:
                scrb_addr = self.removeNonAscii(obj.GeocodeResponse.result.formatted_address.cdata)
                type_len = len(obj.GeocodeResponse.result.get_elements(name='type'))
                if (type_len) == 1:
                    addr_typ = str(obj.GeocodeResponse.result.type.cdata)
                else:
                    addr_typ = str(obj.GeocodeResponse.result.type[0].cdata)
                    for data in range(1,type_len):
                        addr_typ = addr_typ + ":" + str(obj.GeocodeResponse.result.type[data].cdata)
                place_id = str(obj.GeocodeResponse.result.place_id.cdata)
                for item in obj.GeocodeResponse.result.geometry:
                    lat = float(str(item.location.lat.cdata).strip())
                    lon = float(str(item.location.lng.cdata).strip())
                    loc_type = str(item.location_type.cdata).strip()
            else:
                # If multiple results returned, consider the 1st result
                scrb_addr = str(obj.GeocodeResponse.result[0].formatted_address.cdata)
                type_len = len(obj.GeocodeResponse.result[0].get_elements(name='type'))
                if (type_len) == 1:
                    addr_typ = str(obj.GeocodeResponse.result[0].type.cdata)
                else:
                    addr_typ = str(obj.GeocodeResponse.result[0].type[0].cdata)
                    for data in range(1, type_len):
                        addr_typ = addr_typ + ":" + str(obj.GeocodeResponse.result[0].type[data].cdata)
                place_id = str(obj.GeocodeResponse.result[0].place_id.cdata)
                for item in obj.GeocodeResponse.result[0].geometry:
                    lat = float(str(item.location.lat.cdata).strip())
                    lon = float(str(item.location.lng.cdata).strip())
                    loc_type = str(item.location_type.cdata).strip()
            geocode_result.append(addr)
            geocode_result.append(scrb_sts)
            geocode_result.append(addr_typ)
            geocode_result.append(loc_type)
            geocode_result.append(scrb_addr)
            geocode_result.append(wiki)
            geocode_result.append(lat)
            geocode_result.append(lon)
            geocode_result.append(place_id)
            return geocode_result
        else:
            geocode_result.append(addr)
            geocode_result.append(scrb_sts)
            geocode_result.append('NOK')
            geocode_result.append('NOK')
            geocode_result.append('NOK')
            geocode_result.append(wiki)
            geocode_result.append(0.0)
            geocode_result.append(0.0)
            geocode_result.append('NOK')
            return geocode_result

    def get_qualifying_locations_risk_circle_against_table(self,center_lat,center_lon,distancekm):
        from mysql.connector import MySQLConnection, Error
        import math
        ret_list = []
        try:
            conn = MySQLConnection(host='localhost', database='mysql', user='root', password='password')
            cursor = conn.cursor()
            query = "SELECT c.COMPANY_NAME, c.TIV,t.* FROM (SELECT RAW_ADDR,LATITUDE,LONGITUDE," \
                    "(acos(sin(radians(%s)) * sin(radians(Latitude)) + cos(radians(%s)) * cos(radians((Latitude))) " \
                    "* cos(radians(%s) - radians(Longitude))) * 6378.8) AS distance " \
                    "FROM  train_set.geo_scrub_addr where SCRUB_TYPE IN (%s,%s,%s) AND SCRUB_STS=%s) t," \
                    "(select COMPANY_NAME,COMPANY_ADDR,SUM(COMPANY_TIV) as TIV from " \
                    "train_set.company_info group by COMPANY_NAME,COMPANY_ADDR) c WHERE t.RAW_ADDR=c.COMPANY_ADDR  " \
                    "and t.distance <= %s"
            cursor.execute(query,[center_lat,center_lat,center_lon,'ROOFTOP','RANGE_INTERPOLATED','GEOMETRIC_CENTER','OK',distancekm])
            for (company_name,tiv,raw_addr,latitude,longitude,distance) in cursor:
                ret_list.append([company_name,tiv,raw_addr,latitude,longitude,distance])
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
            return ret_list

    def calculate_distance_between_2_lat_lon(self,Latitude,Longitude):
        import math
        distance = math.acos(math.sin(math.radians(self.lat)) * math.sin(math.radians(Latitude)) +
                   math.cos(math.radians(self.lat)) * math.cos(math.radians((Latitude))) *
                             math.cos(math.radians(self.lon) - math.radians(Longitude))) * 6378.8
        return distance

    def find_places_around_center(self,distance_in_km,place_type):
        import urllib2, urllib
        import untangle
        # Prepare the URL link
        wiki = self.nearby_search_link_location + "?location=" + str(self.lat)+","+str(self.lon)+\
               "&radius=" + str(distance_in_km*1000) + "&type=" + self.place_type + "&key=" + self.api_key
        final_list = []
        # Query the website and return the data and parse the xml using untangle
        page = urllib2.urlopen(wiki)
        xmldata = page.read()
        obj = untangle.parse(xmldata)
        # If scrubbing status is OK then result should be received. Not sure how many result.
        srch_sts = str(obj.PlaceSearchResponse.status.cdata).strip()
        if srch_sts == "OK":
            result_length = len(obj.PlaceSearchResponse.get_elements(name='result'))
            if result_length == 1:
                company_name =  str(self.removeNonAscii(obj.PlaceSearchResponse.result.name.cdata))
                latitude =  float(str(obj.PlaceSearchResponse.result.geometry.location.lat.cdata))
                longitude =  float(str(obj.PlaceSearchResponse.result.geometry.location.lng.cdata))
                #print str(obj.PlaceSearchResponse.result.place_id.cdata)
                distance = self.calculate_distance_between_2_lat_lon(latitude,longitude)
                final_list.append([company_name, latitude, longitude, distance])
            else:
                for i in range(0,result_length):
                    company_name =  str(self.removeNonAscii(obj.PlaceSearchResponse.result[i].name.cdata))
                    latitude =  float(str(obj.PlaceSearchResponse.result[i].geometry.location.lat.cdata))
                    longitude =  float(str(obj.PlaceSearchResponse.result[i].geometry.location.lng.cdata))
                    #print str(obj.PlaceSearchResponse.result[i].place_id.cdata)
                    distance = self.calculate_distance_between_2_lat_lon(latitude,longitude)
                    final_list.append([company_name, latitude, longitude, distance])
        return final_list

    #hdr_data = ['Name','Age','Gender','Salary']
    #rpt_recs = [['Bishnu','25','M','100'],['Raja','29','M','200'],['Rani','18','F','300']]
    def prepare_html_report(self,hdr_data,rpt_recs,rpt_name):
        try:
            HTMLFILE = '/home/bishnu/'+ self.rpt_name + '_rpt.html'
            dtl_data=[]
            f = open(HTMLFILE, 'w')
            f.write('<html><body><h1>')
            f.write('Report for '+ rpt_name)
            f.write('</h1>')
            f.write('<table border = "1">')
            f.write('<tr>')
            for head in hdr_data:
                f.write('<th>')
                f.write(head)
                f.write('</th>')
            f.write('</tr>')
            for data in rpt_recs:
                dtl_str="<tr><td>"
                #print data
                print len(data)
                for i in range(0,len(data)):
                    print data[i]
                    dtl_str=dtl_str+str(data[i]) + "</td><td>"
                print dtl_str
                dtl_data.append( dtl_str + "</tr>")
                print dtl_data
            for dtl_rec in dtl_data:
                f.write(dtl_rec)
        except Exception, e1:
            print str(e1)
           
pgm=pygeomaps()
hdr_data = ['Name','Age','Gender','Salary']
rpt_recs = [['Bishnu','25','M','100'],['Raja','29','M','200'],['Rani','18','F','300']]
pgm.rpt_name='TRY1'
pgm.prepare_html_report(hdr_data,rpt_recs,pgm.rpt_name)
