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

def new_first_value(subframe, column, new_value):
    subframe.loc[subframe.index[0], column] = new_value

# Cleaning species dataframe
def consolidate_species(dataframe):
    # Conservation status - replaced nan with neutral status, change data type to ordered category (based on severity)
    species_statuses = ["Neutral", "In Recovery", "Species of Concern", "Threatened", "Endangered"]
    dataframe.conservation_status = dataframe.conservation_status.fillna(species_statuses[0])
    dataframe.conservation_status = dataframe.conservation_status.astype('category')
    dataframe.conservation_status = dataframe.conservation_status.cat.set_categories(species_statuses, ordered=True)
    
    # Creating a new dataframe with the same columns and datatypes to return it after handling duplicates
    new_species = species.iloc[:0].copy()
    
    species_sci_names = dataframe.scientific_name.drop_duplicates().to_list()
    for specie in species_sci_names:
        specie_frame = dataframe[dataframe.scientific_name == specie]
        
        # Only for more than one record of the same specie
        if len(specie_frame) > 1:
            # Handling category contradiction
            if contradiction_indicator(specie_frame, 'category') == True:
                new_first_value(specie_frame,  'category', 'Unknown')
                
            # Handling conservation statuses contradiction:
            if contradiction_indicator(specie_frame, 'conservation_status') == True:
                highest_conservation_status = specie_frame.conservation_status.max()
                new_first_value(specie_frame,  'conservation_status', highest_conservation_status)
            
        # Aligning common names
        common_names_list = specie_frame.common_names.to_list()
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
        new_first_value(specie_frame,  'common_names', common_names_string)
        
        # Adding a cleaned specie to our new dataframe
        specie_frame.drop_duplicates(subset='scientific_name', keep='first', inplace=True) 
        new_species = pd.concat([new_species, specie_frame])
    
    new_species.reset_index(inplace=True)
    new_species.drop(['index'], axis=1, inplace=True)
    return new_species

# cleaned_species = consolidate_species(species)

# Cleaning observation dataframe
# scientific_name, park_name, observations
print(observations[observations.scientific_name=='Puma concolor'].value_counts())
print(observations.park_name.value_counts())
print(len(species))