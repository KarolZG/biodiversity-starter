import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Conservation status - replaced nan with neutral status, change data type to ordered category (based on severity)
def status_handler(dataframe):
    species_statuses = ["Neutral", "In Recovery", "Species of Concern", "Threatened", "Endangered"]
    dataframe.conservation_status = dataframe.conservation_status.fillna(species_statuses[0])
    dataframe.conservation_status = dataframe.conservation_status.astype('category')
    dataframe.conservation_status = dataframe.conservation_status.cat.set_categories(species_statuses, ordered=True)

if __name__ == "__main__":
    species = pd.read_csv('input-data/species_info.csv')
    observations = pd.read_csv('input-data/observations.csv')
    
    # Data preview
    print(species.head())
    print(observations.head())
    
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
    
    # Data consistency approach:
    # observations - if there are two observations for the same specie in the same park count will be replaced them with an average value
    # species - species will be consolidated by keeping one record with universal scientific name, concatenated common names, and the highest conservation_status
    
    # Cleaning observation dataframe
    def prepare_observations(dataframe):
        scientific_names = dataframe.scientific_name.drop_duplicates().to_list()
        parks = set(dataframe.park_name.to_list())
        
        for name in scientific_names:
            species_observations = dataframe[dataframe.scientific_name == name]
            for park in parks:
                species_in_park_observations = species_observations[species_observations.park_name == park]
                if len(species_in_park_observations) > 1:
                    avg_observations = round(species_in_park_observations.observations.mean(), 0)
                    matching_indices = dataframe[(dataframe['scientific_name'] == name) & (dataframe['park_name'] == park)].index
                    first_index = matching_indices[0]
                    dataframe.loc[first_index, 'observations'] = avg_observations
        dataframe.drop_duplicates(subset=['scientific_name', 'park_name'], keep='first', inplace=True)
        
        return dataframe
    
    # Helper functions for prepare_species
    def contradiction_indicator(subframe, column):
        column_list = subframe[column].to_list()
        if (len(set(column_list)) != 1):
            return True
        return False
    
    def contradiction_handler(dataframe, condition_column, condition, column, new_value):
        matching_indices = dataframe[dataframe[condition_column] == condition].index
        first_index = matching_indices[0]
        dataframe.loc[first_index, column] = new_value
    
    # Cleaning species dataframe
    def prepare_species(dataframe):
        
        status_handler(dataframe)
        scientific_names = dataframe.scientific_name.drop_duplicates().to_list()
        
        for one_species in scientific_names:
            species_frame = dataframe[dataframe.scientific_name == one_species]
            
            # Only for more than one record of the same species
            if len(species_frame) > 1:
                counter+= 1
                # Handling category contradiction
                if contradiction_indicator(species_frame, 'category') == True:
                    contradiction_handler(dataframe, 'scientific_name', one_species, 'category', 'Unknown')
                    
                # Handling contradicting consevations statuses
                if contradiction_indicator(species_frame, 'conservation_status') == True:
                    highest_con_status = species_frame.conservation_status.max()
                    contradiction_handler(dataframe, 'scientific_name', one_species, 'conservation_status', highest_con_status)
                    
            
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
            contradiction_handler(dataframe, 'scientific_name', one_species, 'common_names', common_names_string)
            
            # Dropping duplicates - keeping only first rows, as the correct values have been replaced there only
            dataframe.drop_duplicates(subset=['scientific_name'], keep='first', inplace=True)
    
        return dataframe
    
    observations = prepare_observations(observations)
    species = prepare_species(species)
    
    observations.to_csv('cleaned_csvs/prepared_observations', index=False)
    species.to_csv('cleaned_csvs/prepared_species.csv', index=False)

