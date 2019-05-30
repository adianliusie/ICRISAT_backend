import pandas as pd

class ConversionFactors:
    def __init__(self):
        self.food_data = pd.read_csv('conversion_factors.csv', encoding='utf-8')

        #Contant measurement units and givide by 100 since all weights are per 100g
        self.cups = 236.59
        self.tablespoon = 17.76
        self.teaspoon = 5.92

    def conversion(self, measurement_unit, measurement, fct_code):
        ingredient = self.food_data[self.food_data["C_CODE"] == fct_code]
        density = float(ingredient["DENSITY"])
        measurement = float(measurement)
        #1 = volume , 2= weight, 3=teaspoon, 4=tablespoon, 5=cups, 6=small, 7=medium, 8=large

        #If direct volume multiply by density
        if measurement_unit == 1:
            return measurement*density

        if measurement_unit == 2:
            return measurement

        if measurement_unit == 3:
            return measurement*self.teaspoon*density

        if measurement_unit == 4:
            return measurement*self.tablepoon*density

        if measurement_unit == 5:
            return measurement*self.cups*density

        if measurement_unit == 6:
            return measurement*float(ingredient["SIZE_S"])

        if measurement_unit == 7:
            return measurement*float(ingredient["SIZE_M"])

        if measurement_unit == 8:
            return measurement*float(ingredient["SIZE_L"])

a = ConversionFactors()
print(a.conversion(6,12,118))
