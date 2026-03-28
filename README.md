# Biodiversity Starter

## Analysis of biodiversity of species in four different parks. The main focus of analysis in showing the spread of species across the locations and the dependencies between it, their category and the conservation status.

## The observations were made in the following National Parks:
* Great Smoky Mountains National Park    
* Yosemite National Park                 
* Bryce National Park
* Yellowstone National Park

## Key findings

## Data Analysis

### Dataframes:
1. Species:
* size (rows): 5824
* columns: category, scientific_name, common_names, conservation_status
2. Observations: 
* size (rows): 5824 * 4
* scientific_name, park_name, observations

### Data preparation challenges (& conclusion)
1. Species:
* common names: do not match for the same spiecies
* conservation_status: nan values, not a category
* detected 274 species with multiple entries (same scientific name)

2. Observations:
* detected 274 species with multiple entries in the same parks (contradictory amount of species in the same place)

> The amount of species duplicate entries is _identical_ in both dataframes.

### Approach:

1. Duplicates in observations dataframe were handled by taking the mean of observations (same spiecies, same park), replacing the first value and dropping the other entries.
2. Common names in species dataframe for the same species were concatinated into one string after removing the identical descriptions. I have left the mutliple spellings though

    e.g. Road Hawk and Road-Hawk

3. Replaced the nan values for conservation status with _Neutral_ value. 
4. Changed category column to categorical value with following statuses:

| 0 | 1 | 2 | 3 | 4 |
| ------- | ----------- | ------------------ | ---------- | ---------- |
| Neutral | In Recovery | Species of Concern | Threatened | Endangered |

5. For the same spiecies and contradicting categories, the more severe one were always chosen

   e.g. Threatened when categories: Species of Concern and Threatened


### Risks

## Sources

*Data source:* [Biodiversity in National Parks](https://www.codecademy.com/paths/bi-data-analyst/tracks/dsf-portfolio-project/modules/dscp-biodiversity-in-national-parks/kanban_projects/biodiversity-in-national-parks-portfolio-project "CodeAcademy Exericse Page")

> Part of the BI Data Analyst CodeAcademy Certification Path.
