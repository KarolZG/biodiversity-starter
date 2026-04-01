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
endangered_statuses = ["In Recovery", "Species of Concern", "Threatened", "Endangered"]

# Neutral and engangered count
neutral_length = len(species[species.conservation_status == "Neutral"])
endangered_length = len(species[species.conservation_status != "Neutral"])
print(f"Found {endangered_length} species with danger status and {neutral_length} without it.")

# Endangeres species analysis
endangered_species = species[species.conservation_status == "Endangered"]
endangered_species_names = endangered_species.scientific_name

endangered_species_obs = observations[observations.scientific_name.isin(endangered_species.scientific_name)]
endangered_species_amounts = endangered_species_obs.groupby('scientific_name')['observations'].sum().sort_values().reset_index()
endangered_species_amounts = pd.merge(endangered_species_amounts, species[['scientific_name', 'common_names', 'category']], on='scientific_name', how='left')
# print(endangered_species_amounts)

endangered_species_by_category = endangered_species_amounts.groupby('category')['observations'].count().sort_values(ascending=False).reset_index()
# print(endangered_species_by_category)

# Species with danger status - countplot

plt.figure(figsize=(10, 6))
ax = plt.subplot(1, 1, 1)
sns.countplot(data=species, x='category', order=endangered_statuses, hue='category', dodge=False, palette='YlOrBr')
plt.title('Species with Conservation Status by Category', fontsize=18, fontweight='bold', pad=20)

plt.xlabel('Cateogry', fontsize=14, labelpad=20)
plt.ylabel('Amount of Species', fontsize=14, labelpad=20)

ax.tick_params(axis='both', which='major', labelsize=12)
ax.yaxis.grid(True, linestyle='-', alpha=0.7)
ax.set_axisbelow(True)

sns.despine()
plt.tight_layout()
plt.savefig('plots/categories-endangered.png', dpi=300)
plt.close()

# Conservation statuses countplot
plt.figure()
ax = plt.subplot(1, 1, 1)
sns.countplot(data=species, x='conservation_status', order=endangered_statuses, hue='conservation_status', dodge=False, palette='YlOrBr')

plt.title('Danger Scale')
plt.xlabel('Conservation Status')
plt.ylabel('Count')

ax.yaxis.grid(True, alpha=0.8)
ax.set_axisbelow(True)

sns.despine()
plt.tight_layout()
plt.savefig('plots/endangered_statuses.png', dpi=300)
plt.close()

# Observations boxplot
plt.figure(figsize=(10, 6))
ax = plt.subplot(1, 1, 1)
sns.boxplot(data=observations, x='observations', fill=False, color='green')
plt.title('Observations', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Amount', fontsize=14, labelpad=20)

sns.despine()
plt.tight_layout()
plt.savefig('plots/observations-boxplot.png', dpi=300)
plt.close()

# Amount of observations in each park
observations_by_park = observations.groupby('park_name').observations.sum().sort_values(ascending=False).reset_index()

plt.figure(figsize=(10, 6))
ax = plt.subplot(1, 1, 1)
sns.barplot(data=observations_by_park, x='park_name', y='observations', hue='park_name', legend=False, palette='Spectral')
plt.title('Total Observations by Park', fontsize=18, fontweight='bold', pad=20)

plt.xlabel('National Park', fontsize=14, labelpad=20)
ax.set_xticks(range(4))
ax.set_xticklabels(['Yellowstone', 'Yosemite', 'Brice', 'Great Smoky Mountain'], fontsize=12)
plt.ylabel('Total Observations', fontsize=14, labelpad=20)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: f'{y/1e6:.1f}M'))

ax.tick_params(axis='both', which='major', labelsize=12)
ax.yaxis.grid(True, linestyle='-', alpha=0.7)
ax.set_axisbelow(True)

sns.despine()
plt.tight_layout()
plt.savefig('plots/observations-by-park.png', dpi=300)
plt.close()

