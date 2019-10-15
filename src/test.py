import numpy as np
from climlab.solar.orbital import OrbitalTable
from climlab.solar.insolation import daily_insolation
import matplotlib.pyplot as plt


class SunlightCalculator:
    def __init__(self, lat=0, day=1, year=2019, num_years=1):
        self.lat = lat
        self.day = day
        self.year = year
        self.num_years = num_years

    def _daily_insolation(self, lat, day, num_years):
        years = np.linspace(-num_years, 0, num_years)
        orb = OrbitalTable.interp(kyear=years)
        return daily_insolation(lat=lat, day=day, orb=orb)

    def get_daily_average(self, lat=None, day=None, num_years=None):
        lat = lat if lat else self.lat
        day = day if day else self.day
        num_years = num_years if num_years else self.num_years

        running_total = 0

        insolation_data = self._daily_insolation(lat, day, num_years)
        for x in insolation_data:
            S_dict = x.to_dict()
            running_total += S_dict['data']

        average = running_total / len(insolation_data)
        return average

    def get_daily_averages_for_year(self, lat=None, num_years=None):
        lat = lat if lat else self.lat
        num_years = num_years if num_years else self.num_years
        daily_averages = []
        temps = []
        for day in range(1, 366):
            avg = self.get_daily_average(lat=lat, day=day, num_years=num_years)
            print("day: ", day, avg)
            temps.append(avg)
            day_avg_tuple = (day, avg)
            daily_averages.append(day_avg_tuple)
        self.plot_graph(temps, lat)
        return daily_averages

    def plot_graph(self, temps_array, lat):
        print("*** STARTING GRAPH ***")
        plt.plot(range(1, 366), temps_array)
        plt.xlabel('Day of year')
        plt.ylabel('Insolation')
        plt.ylim([0, 600])
        title = "Yearly insolation at " + str(lat) + " degrees latitude"
        plt.title(title)
        plt.show()

    def get_yearly_average(self):
        avgs = self.get_daily_averages_for_year()
        # print(avgs)
        acc = 0
        for x in range(0, len(avgs)):
            acc += avgs[x][1]
        return acc / len(avgs)

    def get_daily_averages_for_multiple_years(self, lat, num_years):
        pass


calc = SunlightCalculator(lat=6.3, day=172, year=2019, num_years=20)
# print("Average: ", calc.get_daily_average())
print("Daily: ", calc.get_yearly_average())

# Public API
# SunlightCalculator(lat, year, num_years)
# def get_yearly_average(lat, num_years)
# def get_daily_average(day, num_years)
# def get_daily_averages_for_year(lat, num_years)
