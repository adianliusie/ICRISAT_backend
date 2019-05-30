import pandas as pd
import numpy as np
import json
import datetime
from conversion import ConversionFactors

class BackendCalculator:

    def __init__(self):
        #Data files required
        self.fct = pd.read_csv('Fct.csv', encoding='utf-8')
        self.conv = pd.read_csv('RetentionFactors.csv', encoding='utf-8')

    #Function with JSON dictionary as the input
    def add_data_to_spreadsheet(self,data):
        individuals_data = pd.read_csv('individuals_data.csv', encoding='utf-8')
        total_data = pd.read_csv('total_data.csv', encoding='utf-8')
        # For now, we use a kinda hacky method to extract all the ingredients quickly, but it might be worth spending the
        # time to do this properly by separating it into different functions or something?
        foodIngredientsList = [foodItem.get("ingredients",[]) for foodItem in data.get("listOfFoods",[])]
        listOfIngredients = []
        for ingredientList in foodIngredientsList:
            for ingredient in ingredientList:
                listOfIngredients.append(ingredient)
        # Conv numbers are not returned at this moment!
        # For the demo, we just populate it with a random list of conv_numbers
        conv_numbers = self.conv.sample(len(listOfIngredients))["R_Code"].tolist()

        fct_numbers = [food_item["fctCode"] for food_item in listOfIngredients]
        # conv_numbers = [food_item["rCode"] for food_item in listOfIngredients]

        brirthDate = datetime.datetime.strptime( data["interviewData"]["respondent"]["birthDate"], "%Y-%m-%d %H:%M:%S.%f")
        data_header = [data["interviewData"]["respondent"]["name"], self.calculate_age(brirthDate), data["interviewData"]["householdIdentification"]]

        # Convert all the foods from their units to grams, and then normalise per 100g
        conversion_calculator = ConversionFactors()
        weights = [conversion_calculator.conversion(food_item["measurementUnit"], food_item["measurement"], food_item["fctCode"])/100 for food_item in listOfIngredients]

        #individual_matrix is used to calculate total micro and macro nutrients intake
        individual_matrix = []

        # To record all the collected data for the matrix
        full_data = []

        #Calculates the whole input data
        for i in range(len(weights)):
            fct_row = self.fct[self.fct["C_CODE"] == fct_numbers[i]]
            fct_row_np = np.array(fct_row)[0][3:]

            conv_row = self.conv[self.conv["R_Code"]==conv_numbers[i]]
            conv_row_np = np.array(conv_row)[0][2:]

            output_value = weights[i]*conv_row_np*fct_row_np
            individual_matrix.append(output_value)

            output_value = np.append(fct_row["C_DESCR"], output_value)
            full_data.append(output_value)

        #This gives us the total consumption of one person
        ind_data = sum(individual_matrix)
        ind_data = np.concatenate((data_header,ind_data))

        #Write the individuals daily consumption
        #Columns need to have the same column headers to append to each other
        columns = self.conv.head(1)
        del columns['R_Code']
        del columns['R_Descr']
        header_1 = ["Name", "Age", "HouseID"]
        ind_data_pd = (pd.DataFrame(ind_data)).T
        ind_data_pd.columns = header_1 + list(columns)

        individuals_data = individuals_data.append(ind_data_pd, ignore_index=True)
        individuals_data.to_csv('individuals_data.csv', index=False)

        print("Output written!")

        #Write the detailed data
        for i in range(len(full_data)):
            full_data[i] = np.concatenate((data_header,full_data[i]))

        header_2 = ["Name", "Age", "HouseID", "C_DESCR"]
        full_data_pd = pd.DataFrame(full_data)
        print(full_data_pd)
        full_data_pd.columns = header_2 + list(columns)
        total_data = total_data.append(full_data_pd, ignore_index=True)
        total_data.to_csv('total_data.csv', index=False)


    @staticmethod
    def calculate_age(born):
        today = datetime.date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
