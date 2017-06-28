from goibibo import goibiboAPI
import ConfigParser

class TripPlanner:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read('C:/PyTripPlanner/PTP.conf')
        self.ibibo_app_id=config.get('ptp_config', 'ibibo_app_id')
        self.ibibo_appkey=config.get('ptp_config', 'ibibo_appkey')
        self.source_airport='',
        self.dest_airport='',
        self.dateofdeparture=None,
        self.dateofarrival = None,
        self.seatingclass = "E",
        self.passenger_count=1
        self.adults_count = 1,
        self.non_adult_count = 0,
        self.infants_count = 0
        self.name=[]
        self.travel_mode=0
        self.trip_id = 0
        self.break_journey=''
        self.round_trip=''
        self.source_city=''
        self.dest_city=''
        self.go_inst = goibiboAPI(self.ibibo_app_id, self.ibibo_appkey)

    def generate_trip_id(self,trip_id):
        self.trip_id=trip_id

    def get_passenger_detail(self):
        self.passenger_count = int(raw_input("What is the headcount for this trip (Min:1)? "))
        self.adults_count = int(raw_input("How many passengers are more than 18 Years age? "))
        self.infants_count = int(raw_input("How many passengers are less than 2 Years age? "))
        if self.infants_count > self.adults_count:
            print "A maximum of one Infant is allowed per adult"
            exit()
        elif self.passenger_count <= 0:
            print "Total Passenger count should be more than Zero"
            exit()
        elif self.infants_count+self.adults_count > self.passenger_count:
            print "Total travelling passenger count is incorrect"
        else:
            self.non_adult_count=self.passenger_count-self.adults_count-self.infants_count
            if self.adults_count > 0:
                for i in range(1,self.adults_count+1):
                    self.name.append(raw_input("Please enter the Adult passenger"+str(i)+ " name : "))
            if self.infants_count > 0:
                for i in range(1,self.infants_count+1):
                    self.name.append(raw_input("Please enter the infant passenger" + str(i) + " name : "))
            if self.non_adult_count > 0:
                for i in range(1, self.non_adult_count+1):
                    self.name.append(raw_input("Please enter the other passenger" + str(i) + " name : "))

    def get_mode_of_travel(self):
        self.travel_mode=int(raw_input("Press\n\t 0 for Air travel,\n\t 1 for Domestic Bus travel\n"))

    def check_date(self,date_in_yyyymmdd):
        import datetime
        correctDate = None
        try:
            newDate = datetime.datetime.strptime(date_in_yyyymmdd, '%Y%m%d').date()
            print newDate
            correctDate = True
        except ValueError:
            correctDate = False
        return correctDate

    def print_trip_details(self):
        print 'source_airport:' + str(self.source_airport)
        print 'dest_airport:'+ str(self.dest_airport)
        print 'dateofdeparture:'+ self.dateofdeparture
        print 'dateofarrival:'+ self.dateofarrival
        print 'seatingclass:'+ str(self.seatingclass)
        print 'passenger_count:'+ str(self.passenger_count)
        print 'adults_count:'+ str(self.adults_count)
        print 'non_adult_count:'+ str(self.non_adult_count)
        print 'infants_count:'+ str(self.infants_count)
        print 'name:'+ str(self.name)
        print 'travel_mode:'+ str(self.travel_mode)
        print 'trip_id:'+ str(self.trip_id)
        print 'break_journey:'+self.break_journey
        print 'round_trip:'+ self.round_trip
        print 'source_city:'+ self.source_city
        print 'dest_city:'+self.dest_city

    def get_journey_details(self):
        import airport_codes
        import datetime
        import time
        import city_cityid as city
        if self.travel_mode == 0:
            airport_flag = 'N'
            date_flag = 'N'
            print "************ This mode of journey would be Air Travel ****************"
            self.seatingclass = raw_input("\nPlease enter the class of travel (E/B): ")
            while airport_flag =='N':
                self.source_airport = raw_input("Please enter the 3 character source airport code: ").upper()
                self.dest_airport = raw_input("Please enter the 3 character destination airport code: ").upper()
                default='NOT FOUND'
                print "\nSource airport is : " + airport_codes.airport.setdefault(self.source_airport, default)
                print "Destination airport is: " +  airport_codes.airport.setdefault(self.dest_airport, default)
                airport_flag=raw_input("\nIs the above info correct? (Y/N): ").upper()
                self.round_trip=raw_input("Is it a round_trip?(Y/N): ").upper()
            if(self.round_trip == 'Y'):
                while date_flag == 'N':
                    print "************* This is a round trip journey ***********"
                    self.dateofdeparture = raw_input("Please enter the depart date in YYYYMMDD format: ")
                    self.dateofarrival =  raw_input("Please enter the return date in YYYYMMDD format: ")
                    if self.check_date(self.dateofdeparture) == False or self.check_date(self.dateofarrival) == False:
                        print "Date entered are not correct please check"
                    elif self.dateofdeparture < time.strftime("%Y%m%d"):
                        print "Date of departure is in past. Please correct"
                    elif self.dateofarrival < time.strftime("%Y%m%d"):
                        print "Date of arrival is in past. Please correct"
                    elif self.dateofarrival < self.dateofdeparture:
                        print "Date of arrival is less than date of departure. Please correct"
                    else:
                        date_flag=raw_input("Is the above info correct? (Y/N): ").upper()
            else:
                while date_flag == 'N':
                    self.dateofarrival = 'NOT APPLICABLE'
                    self.dateofdeparture = raw_input("Please enter the depart date in YYYYMMDD format: ")
                    if self.check_date(self.dateofdeparture) == False:
                        print "Date entered is not correct. please check"
                    elif self.dateofdeparture < time.strftime("%Y%m%d"):
                        print "Date of departure is in past. Please correct"
                    else:
                        date_flag = raw_input("Is the above info correct? (Y/N): ").upper()
            #End of Air travel mode
        else:
            bus_flag = 'N'
            bus_date_flag = 'N'
            print "************ This mode of journey would be Bus travel with in India *************"
            while bus_flag == 'N':
                self.source_city = raw_input("Please enter the source city name: ").upper()
                self.dest_city = raw_input("Please enter the destination city name: ").upper()
                default = 'NOT FOUND'
                if city.city_name.setdefault(self.source_city, default) == 'NOT FOUND':
                    print "Source city not correct. please check"
                elif city.city_name.setdefault(self.dest_city, default) == 'NOT FOUND':
                    print "Destination city not correct. Please check"
                else:
                    bus_flag = raw_input("Is the above info correct?(Y/N): ").upper()
            if (raw_input("Is it a round_trip?(Y/N):").upper() == 'Y'):
                while date_flag == 'N':
                    print "*********This is a round trip journey********** "
                    self.dateofdeparture = raw_input("Please enter the depart date in YYYYMMDD format: \n")
                    self.dateofarrival = raw_input("Please enter the return date in YYYYMMDD format: \n")
                    if self.check_date(self.dateofdeparture) == False or self.check_date(self.dateofarrival) == False:
                        print "Date entered are not correct please check\n"
                    elif self.dateofdeparture < time.strftime("%Y%m%d"):
                        print "Date of departure is in past. Please correct\n"
                    elif self.dateofarrival < time.strftime("%Y%m%d"):
                        print "Date of arrival is in past. Please correct\n"
                    elif self.dateofarrival < self.dateofdeparture:
                        print "Date of arrival is less than date of departure. Please correct\n"
                    else:
                        date_flag = raw_input("Is the above info correct? (Y/N): ").upper()
            else:
                while date_flag == 'N':
                    self.dateofarrival='NOT APPLICABLE'
                    self.dateofdeparture = raw_input("Please enter the depart date in YYYYMMDD format: ")
                    if self.check_date(self.dateofdeparture) == False:
                        print "Date entered is not correct. please check"
                    elif self.dateofdeparture < time.strftime("%Y%m%d"):
                        print "Date of departure is in past. Please correct"
                    else:
                        date_flag = raw_input("Is the above info correct? (Y/N): ").upper()

    def show_options_for_travel(self):
        try:
            if self.travel_mode == '0' and self.round_trip == 'N':
                print(self.go_inst.FlightSearch(self.source_airport,self.dest_airport,
                                                self.dateofdeparture,self.dateofarrival,self.seatingclass,
                                                self.adults_count,self.non_adult_count,self.infants_count))
        except Exception, e1:
            print str(e1)



tp=TripPlanner()
tp.get_passenger_detail()
tp.get_mode_of_travel()
tp.generate_trip_id('12345678')
tp.get_journey_details()
tp.print_trip_details()
tp.show_options_for_travel()


#print GO.FlightSearch("BLR", "HYD", 20170628)
#print GO.MinimumFare("BLR", "HYD", 20170628)
#print GO.BusSearch("bangalore", "hyderabad", 20170628)
#print GO.BusSeatMap("vJ52KC0ymd0635qTD9bDDy9GHBkGl5FJMJje0aFX\
#                     _GQTyev_4N9Y62TTfrmS-Re3dCHl0-UxLq4AsoQ%3D")
#print GO.SearchHotelsByCity(6771549831164675055)
# print GO.GetHotelData([1017089108070373346, 6085103403340214927])
# print GO.GetHotelPriceByCity(6771549831164675055, 20170628, 20170629)