import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

species = pd.read_csv('species_info.csv')
observations = pd.read_csv('observations.csv')

# Data preview
# print(species.head())
# print(observations.head())

"""
# Primary analysis of species
print(species.columns)
print(species.dtypes)
print(species.describe(include='all'))
print(species.info(verbose=True, show_counts=True))
print(species.conservation_status.value_counts())

# Primary analysis of observations
print(observations.columns)
print(observations.dtypes)
print(observations.describe(include='all'))
print(observations.info(verbose=True, show_counts=True))
print(observations.park_name.value_counts())

# Searching for inconsistencies, duplicates
print(species.scientific_name.value_counts())
print(observations.scientific_name.value_counts())

# Duplicate example
print(species[species.scientific_name == 'Puma concolor'])
print(observations[observations.scientific_name == 'Puma concolor'])
"""

# Data consistency approach:
# species - species will be consolidated by keeping one record with universal scientific name, concatenated common names, and the highest conservation_status
# observations - if there are two observations for the same specie in the same park count will be replaced them with an average value

# Conservation status - replaced nan with neutral status, change data type to ordered category (based on severity)
species_statuses = ["Neutral", "In Recovery", "Species of Concern", "Threatened", "Endangered"]

species.conservation_status = species.conservation_status.fillna(species_statuses[0])
species.conservation_status = species.conservation_status.astype('category')
species.conservation_status = species.conservation_status.cat.set_categories(species_statuses, ordered=True)
# print(species.conservation_status.sort_values())

# category, scientific_name, common_names, conservation_status

def consolidate_species(dataframe):
    species = dataframe.scientific_name.drop_duplicates().to_list()
    
    for specie in species:
        if len(dataframe[dataframe.scientific_name == specie]) > 1:
            specie_frame = dataframe[dataframe.scientific_name == specie]
            
            # Handling category error
            category = specie_frame.category.to_list()
            if (len(set(category)) != 1):
                specie_frame[0].category = 'Unknown'
            
            # Aligning common names
            common_names_list = specie_frame.common_names.to_list()
            common_names_string = ''
            counter = 0
            for name in common_names_list:
                if ', ' in name:
                    temp_name_list = name.split(', ')
                    temp_name = ', '.join(word for word in temp_name_list)
                else:
                    temp_name = name
                if (counter > 0):
                    common_names_string += ','
                common_names_string += temp_name
                counter += 1
                
            print(common_names_string)
            
            

consolidate_species(species)        

# species = species.apply(consolidate_species).reset_index()


