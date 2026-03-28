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

# Handling duplicate, different values for the same specie
def contradiction_indicator(subframe, column):
    column_list = subframe[column].to_list()
    if (len(set(column_list)) != 1):
        return True
    return False

# Cleaning observation dataframe
# scientific_name, park_name, observations

def prepare_observations(dataframe):
    sci_names = observations.scientific_name.drop_duplicates().to_list()
    
    for name in sci_names:
        species_observations = observations[observations.scientific_name == name]
        if len(species_observations) > 4:
            print(species_observations)
            

# Cleaning species dataframe
def prepare_species(dataframe):
    
    # Conservation status - replaced nan with neutral status, change data type to ordered category (based on severity)
    species_statuses = ["Neutral", "In Recovery", "Species of Concern", "Threatened", "Endangered"]
    dataframe.conservation_status = dataframe.conservation_status.fillna(species_statuses[0])
    dataframe.conservation_status = dataframe.conservation_status.astype('category')
    dataframe.conservation_status = dataframe.conservation_status.cat.set_categories(species_statuses, ordered=True)
    species_sci_names = dataframe.scientific_name.drop_duplicates().to_list()
    
    for one_species in species_sci_names:
        species_frame = dataframe[dataframe.scientific_name == one_species]
        
        # Only for more than one record of the same species
        if len(species_frame) > 1:
            counter+= 1
            # Handling category contradiction
            if contradiction_indicator(species_frame, 'category') == True:
                dataframe.loc[dataframe.scientific_name == one_species, 'category'] = 'Unknown'
        
        # Aligning common names
        common_names_list = species_frame.common_names.to_list()
        temp_names_list = []
        
        for name in common_names_list:
            if name not in temp_names_list:      
                if ', ' in name:
                    temp_var = name.split(', ')
                    for s_name in temp_var:
                        temp_names_list.append(s_name)
                else:
                    temp_names_list.append(name)
        
        temp_names_list = set(temp_names_list)
        common_names_string = ', '.join(name for name in temp_names_list)
        dataframe.loc[dataframe.scientific_name == one_species, 'common_names'] = common_names_string

    return dataframe

