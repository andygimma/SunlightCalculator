import numpy as np
from climlab.solar.orbital import OrbitalTable
from climlab.solar.insolation import daily_insolation
import matplotlib.pyplot as plt
from functools import reduce


class SunlightCalculator:
    def __init__(self, lat=0, day=1, year=2019, num_years=10, city_name=None):
        self.lat = lat
        self.day = day
        self.year = year
        self.num_years = num_years
        self.city_name = city_name
        self.temps = []

    def _daily_insolation(self, day):
        years = np.linspace(-self.num_years, 0, self.num_years)
        orb = OrbitalTable.interp(kyear=years)
        return daily_insolation(lat=self.lat, day=day, orb=orb)

    def calculate_daily_average(self, day):
        insolation_data = self._daily_insolation(day)
        acc = reduce((lambda x, y: x + y.to_dict()['data']), insolation_data)
        average = acc.to_dict()['data'] / len(insolation_data)
        return average

    def calculate_temps_for_year(self):
        self.temps = []
        for day in range(1, 366):
            avg = self.calculate_daily_average(day)
            print("day: ", day, avg)
            self.temps.append(avg)

    def plot_graph_for_year(self):
        if (len(self.temps) == 0):
            self.calculate_temps_for_year()
        average = self.calculate_yearly_average()
        plt.plot(range(1, 366), self.temps, label="Daily temps")
        # plt.plot(range(1, 366), self.calculate_yearly_average())
        label = "Average: " + str(round(average, 2))
        plt.axhline(average, color='blue', linewidth=2, label=label)
        plt.xlabel('Day of year')
        plt.ylabel('Insolation')
        plt.ylim([0, 600])
        title = "Yearly insolation at " + \
            str(self.lat) + " degrees latitude " + self.city_name
        plt.title(title)
        plt.legend()
        plt.show()

    def calculate_yearly_average(self):
        if (len(self.temps) == 0):
            self.calculate_temps_for_year()
        acc = reduce((lambda x, y: x + y), self.temps)
        return acc / len(self.temps)

    def calculate_daily_averages_for_multiple_years(self, lat, num_years):
        pass


calc = SunlightCalculator(lat=52.5, day=172, year=2019,
                          num_years=20, city_name="Berlin, Germany")
# print("Average: ", calc.calculate_temps_for_year())
print("Daily: ", calc.plot_graph_for_year())
# print("calculate_daily_average", calc.calculate_daily_average(1))
# print("calculate_yearly_average", calc.calculate_yearly_average())
