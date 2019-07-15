import pandas as pd

class Loader ():
    
    def __init__ (self, city, months):
        
        self.city = city
        self.months = months

    def read_bookings_parkings (self):

        self.bookings = pd.DataFrame()
        self.parkings = pd.DataFrame()
        for month in self.months:
            month_bookings = pd.read_excel\
                ("./Data/" + self.city + "/"\
                 + str(month) + "-2017.xlsx",
                 "bookings")
            month_parkings = pd.read_excel\
                ("./Data/" + self.city + "/"\
                 + str(month) + "-2017.xlsx",
                 "parkings")
            self.bookings = pd.concat\
                ([self.bookings, month_bookings], 
                 ignore_index=True,
                 sort=False)
            self.parkings = pd.concat\
                ([self.parkings, month_parkings], 
                 ignore_index=True,
                 sort=False)

        return self.bookings, self.parkings
