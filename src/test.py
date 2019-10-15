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
        self.temps = []

    def _daily_insolation(self, day):
        years = np.linspace(-self.num_years, 0, self.num_years)
        orb = OrbitalTable.interp(kyear=years)
        return daily_insolation(lat=self.lat, day=day, orb=orb)

    def get_daily_average(self, day):
        running_total = 0

        insolation_data = self._daily_insolation(day)
        for x in insolation_data:
            S_dict = x.to_dict()
            running_total += S_dict['data']

        average = running_total / len(insolation_data)
        return average

    def get_daily_averages_for_year(self):
        daily_averages = []
        self.temps = []
        for day in range(1, 366):
            avg = self.get_daily_average(day)
            print("day: ", day, avg)
            self.temps.append(avg)
            day_avg_tuple = (day, avg)
            daily_averages.append(day_avg_tuple)
        self.plot_graph()
        return daily_averages

    def plot_graph(self):
        print("*** STARTING GRAPH ***")
        plt.plot(range(1, 366), self.temps)
        plt.xlabel('Day of year')
        plt.ylabel('Insolation')
        plt.ylim([0, 600])
        title = "Yearly insolation at " + str(self.lat) + " degrees latitude"
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

# TODO
# Remove all args from methods
# Easier to test and reason about
