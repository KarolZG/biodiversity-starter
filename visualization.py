import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from cleanup import status_handler

species = pd.read_csv('output-data/prepared_species.csv')
observations = pd.read_csv('output-data/prepared_observations.csv')

# Categories handling for further analysis
status_handler(species)
in_danger_statuses = ["In Recovery", "Species of Concern", "Threatened", "Endangered"]
species_with_in_danger_statuses = species[species.conservation_status.isin(in_danger_statuses)]
endangered_species = species[species.conservation_status == "Endangered"]

# Neutral and engangered count
neutral_length = len(species[species.conservation_status == "Neutral"])
in_danger_length = len(species[species.conservation_status != "Neutral"])
endangered_species_length = len(endangered_species)
total_observations = observations.observations.sum()

print(f"Found {in_danger_length} species with in danger status, including {endangered_species_length} endangered species. Majority of species - {neutral_length} - didn't have any conservation status.")
print(f'Total observations: {total_observations/1e6:.1f}M')

# Endangeres species analysis
endangered_species_obs = observations[observations.scientific_name.isin(endangered_species.scientific_name)]
endangered_species_amounts = endangered_species_obs.groupby('scientific_name')['observations'].sum().sort_values().reset_index()
endangered_species_amounts = pd.merge(endangered_species_amounts, species[['scientific_name', 'common_names', 'category']], on='scientific_name', how='left')
print(endangered_species_amounts)

endangered_species_by_category = endangered_species_amounts.groupby('category')['observations'].count().sort_values(ascending=False).reset_index()
print(endangered_species_by_category)


# Total observations by park
observations_by_park = observations.groupby('park_name').observations.sum().sort_values(ascending=False).reset_index()
national_parks_names_ordered = ['Yellowstone National Park', 'Yosemite National Park', 'Bryce National Park', 'Great Smoky Mountains National Park']
national_parks_labes_ordered = ['Yellowstone', 'Yosemite', 'Bryce', 'Great Smoky Mountains']
park_palette = {
    'Yellowstone National Park': '#F4D03F',
    'Yosemite National Park': '#85929E',
    'Bryce National Park': '#D35400',
    'Great Smoky Mountains National Park': '#2E86C1'
}

plt.figure(figsize=(10, 6))
ax = plt.subplot(1, 1, 1)
sns.barplot(data=observations_by_park, x='park_name', y='observations', hue='park_name', legend=False, palette=park_palette)
plt.title('Total Observations', fontsize=18, fontweight='bold', pad=20)

plt.xlabel('National Park', fontsize=14, labelpad=20)
ax.set_xticks(range(4))
ax.set_xticklabels(national_parks_labes_ordered, fontsize=12)
plt.ylabel('Amount of Observations', fontsize=14, labelpad=20)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: f'{y/1e6:.1f}M'))

ax.tick_params(axis='both', which='major', labelsize=12)
ax.yaxis.grid(True, linestyle='-', alpha=0.7)
ax.set_axisbelow(True)

sns.despine()
plt.tight_layout()
plt.savefig('plots/1-total-observations.png', dpi=300)
plt.close()

# Observations statistically - by park
plt.figure(figsize=(10, 6))
ax = plt.subplot(1, 1, 1)
sns.boxplot(data=observations, x='park_name', y='observations', hue='park_name', order=national_parks_names_ordered, palette=park_palette, legend=False)

plt.title('Observations Statistics by Park', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('National Park', fontsize=14, labelpad=20)
plt.ylabel('Amount of Observations', fontsize=14, labelpad=20)

ax.set_xticks(range(4))
ax.set_xticklabels(national_parks_labes_ordered, fontsize=12)
ax.tick_params(axis='both', which='major', labelsize=12)
ax.yaxis.grid(True, linestyle='-', alpha=0.7)
ax.set_axisbelow(True)

sns.despine()
plt.tight_layout()
plt.savefig('plots/2-stat-of-park-observations.png', dpi=300)
plt.close()

# Observations statistically
plt.figure(figsize=(10, 6))
ax = plt.subplot(1, 1, 1)
sns.boxplot(data=observations, x='observations', fill=False, color='green')
plt.title('Observations - Five Number Summary', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Number', fontsize=14, labelpad=20)
ax.tick_params(axis='both', which='major', labelsize=12)

sns.despine()
plt.tight_layout()
plt.savefig('plots/3-stat-of-total-observations.png', dpi=300)
plt.close()

# Danger Scale - conservation statuses countplot
plt.figure(figsize=(10,6))
ax = plt.subplot(1, 1, 1)

sns.countplot(data=species, x='conservation_status', order=in_danger_statuses, hue='conservation_status', dodge=False, palette='YlOrRd', legend=False)

plt.title('Danger Scale',  fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Conservation Status', fontsize=14, labelpad=20)
plt.ylabel('Number of Species', fontsize=14, labelpad=20)

ax.tick_params(axis='both', which='major', labelsize=12)
ax.yaxis.grid(True, linestyle='-', alpha=0.7)
ax.yaxis.grid(True, alpha=0.7)
ax.set_axisbelow(True)

sns.despine()
plt.tight_layout()
plt.savefig('plots/4-danger-scale.png', dpi=300)
plt.close()

# Species with danger status - countplot
in_danger_category_order = species_with_in_danger_statuses['category'].value_counts().index

plt.figure(figsize=(10, 6))
ax = plt.subplot(1, 1, 1)
sns.countplot(data=species_with_in_danger_statuses, x='category', hue='category', order=in_danger_category_order, dodge=False, palette='Set2', legend=False)
plt.title('Species in Danger by Category', fontsize=18, fontweight='bold', pad=20)

plt.xlabel('Category', fontsize=14, labelpad=20)
plt.ylabel('Number of Species', fontsize=14, labelpad=20)

ax.tick_params(axis='both', which='major', labelsize=12)
plt.xticks(rotation=10)
ax.yaxis.grid(True, linestyle='-', alpha=0.7)
ax.set_axisbelow(True)

sns.despine()
plt.tight_layout()
plt.savefig('plots/5-categories-in_danger.png', dpi=300)
plt.close()

# Percentage of observed species in danger by park
observations_in_danger = observations[observations.scientific_name.isin(species_with_in_danger_statuses.scientific_name)]
observations_in_danger = pd.merge(observations_in_danger, species_with_in_danger_statuses[['scientific_name', 'category']], on='scientific_name', how='left')

observations_in_danger_yellowstone = observations_in_danger[observations_in_danger.park_name == 'Yellowstone National Park'].groupby('category')['observations'].sum().sort_values().reset_index()
observations_in_danger_yosemite = observations_in_danger[observations_in_danger.park_name == 'Yosemite National Park'].groupby('category')['observations'].sum().sort_values().reset_index()
observations_in_danger_bryce = observations_in_danger[observations_in_danger.park_name == 'Bryce National Park'].groupby('category')['observations'].sum().sort_values().reset_index()
observations_in_danger_smoky = observations_in_danger[observations_in_danger.park_name == 'Great Smoky Mountains National Park'].groupby('category')['observations'].sum().sort_values().reset_index()

# Calculating the percentage values for each park
observations_in_danger_by_park_list = [observations_in_danger_yellowstone, observations_in_danger_yosemite, observations_in_danger_bryce, observations_in_danger_smoky]

for park in observations_in_danger_by_park_list:
    park['percentage'] = round((100 * (park['observations'] / park['observations'].sum())), 1)


# Creating the plot consisting of 4 subplots for each park
plt.figure(figsize=(16, 12))
plt.suptitle('Distribution of "In-Danger" Species Observations by Park', fontsize=22, fontweight='bold')

for i, (park, label) in enumerate(zip(observations_in_danger_by_park_list, national_parks_labes_ordered), 1):
    ax = plt.subplot(2, 2, i)
    
    palette = f'Set{i}'
    if i > 3:
        palette = 'magma'
        
    sns.barplot(data=park, x='category', y='percentage', hue='category', dodge=False, palette=f'{palette}', legend=False, ax=ax)
        
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', padding=3)

    ax.set_title(label, fontsize=16, pad=10, fontweight='semibold')
    ax.set_xlabel('Species Category', fontsize=12, labelpad=10)
    ax.set_ylabel('Percentage of Observations', fontsize=12)
    ax.tick_params(labelsize=10)
    
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    
    sns.despine(left=True, bottom=False)

plt.tight_layout(pad=3.0)
plt.savefig('plots/6-percentage-in_danger-by-park.png', dpi=300, bbox_inches='tight')
plt.close()

