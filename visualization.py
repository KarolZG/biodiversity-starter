import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from cleanup import status_handler

species = pd.read_csv('output-data/prepared_species.csv')
observations = pd.read_csv('output-data/prepared_observations.csv')
status_handler(species)
observations_and_species = pd.merge(observations, species, on='scientific_name', how='left')


# Conservation statuses boxplot
status_by_park = observations_and_species.groupby('park_name')['conservation_status'].value_counts().reset_index()
print(status_by_park)

# plt.figure(figsize=(10, 6))
# ax = plt.subplot(1, 1, 1)
# sns.boxplot(data=status_by_park, x='park_name', palette='magma')
# plt.title('Endangered Species by Park', fontsize=18, fontweight='bold', pad=20)

# plt.xlabel('National Park', fontsize=14, labelpad=20)
# ax.set_xticks(range(4))
# ax.set_xticklabels(['Yellowstone', 'Yosemite', 'Brice', 'Great Smoky Mountain'], fontsize=12)

# plt.ylabel('Status', fontsize=14, labelpad=20)

# ax.tick_params(axis='both', which='major', labelsize=12)
# ax.yaxis.grid(True, linestyle='-', alpha=0.7)
# ax.set_axisbelow(True)

# sns.despine()
# plt.tight_layout()
# # plt.savefig('plots/conservation-statuses-boxplot.png', dpi=300)
# plt.close()

# Conservation statuses countplot
endangered_statuses = ["In Recovery", "Species of Concern", "Threatened", "Endangered"]
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

# New plot