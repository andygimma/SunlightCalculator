import numpy as np
from climlab.solar.orbital import OrbitalTable
from climlab.solar.insolation import daily_insolation
import matplotlib.pyplot as plt
from functools import reduce


class SunlightCalculator:
    def __init__(self, lat=0, day=1, year=2019, num_years=10):
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
        insolation_data = self._daily_insolation(day)
        acc = reduce((lambda x, y: x + y.to_dict()['data']), insolation_data)
        average = acc.to_dict()['data'] / len(insolation_data)
        return average

    def get_temps_for_year(self):
        self.temps = []
        for day in range(1, 366):
            avg = self.get_daily_average(day)
            print("day: ", day, avg)
            self.temps.append(avg)

    def plot_graph_for_year(self):
        if (len(self.temps) == 0):
            self.get_temps_for_year()
        plt.plot(range(1, 366), self.temps)
        plt.xlabel('Day of year')
        plt.ylabel('Insolation')
        plt.ylim([0, 600])
        title = "Yearly insolation at " + str(self.lat) + " degrees latitude"
        plt.title(title)
        plt.show()

    def get_yearly_average(self):
        self.get_temps_for_year()
        acc = reduce((lambda x, y: x + y), self.temps)
        return acc / len(self.temps)

    def get_daily_averages_for_multiple_years(self, lat, num_years):
        pass


calc = SunlightCalculator(lat=6.3, day=172, year=2019, num_years=20)
# print("Average: ", calc.get_temps_for_year())
# print("Daily: ", calc.plot_graph_for_year())
print("get_daily_average", calc.get_daily_average(1))
