# Biodiversity Starter

**_Analysis of biodiversity of species in four different parks. The main focus of analysis lays in showing the spread of species across the locations and the dependencies between them, their category and the conservation status._**

## The observations were made in the following US National Parks: [^1]
* Great Smoky Mountains National Park    
* Yosemite National Park                 
* Bryce National Park
* Yellowstone National Park

## Key findings

1. Found 178 species with assigned conservation statuses, including 15 endangered (the most severe conservations status) species. Majority of species (5363) lacked any conservation status.
2. Total amount of observations for all species rounds 3.2 million. The median of observed units for each species is equal to 124, and the most frequent observed range lies lower between 75 and 90 species.
3. The fewest observations of species with assigned conservation statuses were noted for categories: Reptile, Amphibian and Non-Vascular Plant.
4. Detailed endangered species analysis [^4]

| id |            scientific_name    | observations  |                 common_names                    |    category    |
|----| ----------------------------- | ------------- | ------------------------------------------------| -------------- |
| 0  |                Grus americana |          131  |                                   Whooping Crane|            Bird|
| 1  |                   Canis rufus |          137  |                                         Red Wolf|          Mammal|
| 2  |           Vermivora bachmanii |          141  |        Bachman's Wood Warbler, Bachman's Warbler|            Bird|
| 3  |               Noturus baileyi |          143  |                                     Smoky Madtom|            Fish|
| 4  |                  Rana sierrae |          144  |                 Sierra Nevada Yellow-Legged Frog|       Amphibian|
| 5  |                Myotis sodalis |          145  |            Indiana Or Social Myotis, Indiana Bat|          Mammal|
| 6  |             Chasmistes liorus |          146  |                                      June Sucker|            Fish|
| 7  |             Picoides borealis |          146  |                          Red-Cockaded Woodpecker|            Bird|
| 8  |  Glaucomys sabrinus coloratus |          153  |Northern Flying Squirrel, Carolina Northern Fl...|          Mammal|
| 9  |       Ovis canadensis sierrae |          153  |                      Sierra Nevada Bighorn Sheep|          Mammal|
| 10 |       Gymnogyps californianus |          156  |                                California Condor|            Bird|
| 11 |             Myotis grisescens |          160  |                                      Gray Myotis|          Mammal|
| 12 |                 Geum radiatum |          162  |                  Mountain Avens, Spreading Avens|  Vascular Plant|
| 13 |          Etheostoma percnurum |          166  |                                 Duskytail Darter|            Fish|
| 14 |                   Canis lupus |          238  |                                        Gray Wolf|          Mammal|

| id |     category   |     count    |
|----|----------------|--------------|
|0   |         Mammal |            6 |
|1   |           Bird |            4 |
|2   |           Fish |            3 |
|3   |      Amphibian |            1 |
|4   | Vascular Plant |            1 |

## Data Analysis

![Yellowstone has 1.4M observations](https://github.com/KarolZG/blob/main/plots/1-total-observations.png "Total Observations by Park")
![Yellowstone with the highest 5S number values ](https://github.com/KarolZG/biodiversity-starter/blob/main/plots/2-stat-of-park-observations.png "Observation Statistics by Park")
![Median for observation around 120 observations ](https://github.com/KarolZG/biodiversity-starter/blob/main/plots/3-stat-of-total-observations.png "Five Number Summary for Observations")
![Mode for observation around 100 observations](https://github.com/KarolZG/biodiversity-starter/blob/main/plots/7-observations-histplot.png "Observations Histplot")
![Above 140 Species of Concern](https://github.com/KarolZG/biodiversity-starter/blob/main/plots/4-danger-scale.png "Danger Scale")
![Species of birds have the highest amount of species in-danger](https://github.com/KarolZG/biodiversity-starter/blob/main/plots/5-categories-in_danger.png "Total Observations by Park")
![Reptile, Amphibian and Non-Vascular Plant with the lowest amount of observations](https://github.com/KarolZG/biodiversity-starter/blob/main/plots/6-percentage-in_danger-by-park.png "Distribution of In-Danger Species Observations By Park")

### Project Flow

To optimize the running time I have splitted the project into two python files:

[Data cleaning and export to new csv files](cleanup.py)
[Data visualization](visualization.py)

and to bring more structure I have created 3 directories:

[Original data](https://github.com/KarolZG/biodiversity-starter/tree/main/input-data)
[Cleaned data](https://github.com/KarolZG/biodiversity-starter/tree/main/output-data)
[Created plots](https://github.com/KarolZG/biodiversity-starter/tree/main/plots)

### Dataframes
1. Species:
* size:
    | Raw  |        Cleaned       |
    | ---  | -------------------  |
    | 5824 |        5541          |
* 283 duplicates (5824 - 5541)
* columns: category, scientific_name, common_names, conservation_status
2. Observations: 
* size:
    |       Raw        |        Cleaned      |
    | ---------------- | ------------------- |
    | 5824 * 4 = 23296 |   5541 * 4 = 22164  |
* 283 * 4 duplicates (283 for each of 4 parks?) 
* scientific_name, park_name, observations

### Data preparation challenges (& conclusion)
1. Species:
* common names: do not match for the same spiecies
* conservation_status: nan values, not a category
* detected species with multiple entries (same scientific name)

2. Observations:
* detected species with multiple entries in the same parks (contradictory amount of species in the same place)

> The amount of species duplicate entries is _identical_ in both dataframes.

### Approach

1. Duplicates in observations dataframe were handled by taking the mean of observations (same spiecies, same park), replacing the first value and dropping the other entries.
2. Common names in species dataframe for the same species were concatinated into one string after removing the identical descriptions. I have left the mutliple spellings though

    e.g. Road Hawk and Road-Hawk

3. Changed category column to categorical value with following statuses:

| 0 | 1 | 2 | 3 | 4 |
| ------- | ----------- | ------------------ | ---------- | ---------- |
| Neutral | In Recovery | Species of Concern | Threatened | Endangered |

4. Replaced the nan values for conservation status with _Neutral_ value. [^2]
5. For the same spiecies and contradicting categories, the more severe one were always chosen [^3]

   e.g. Threatened when categories: Species of Concern and Threatened

### Project Origin

> Part of the BI Data Analyst CodeAcademy Certification Path.

### Footnotes

[^1]: *Data source:* [Biodiversity in National Parks](https://www.codecademy.com/paths/bi-data-analyst/tracks/dsf-portfolio-project/modules/dscp-biodiversity-in-national-parks/kanban_projects/biodiversity-in-national-parks-portfolio-project "CodeAcademy Exercise Page")
[^2]: Nan values in conservation status might have been the result of omission, not always the lack of danger indicator. The analysis of observations amount and thresholds could be performed to mitigate this threat.
[^3]: This approach might not be true, and e.g. status appearing later should be chosen.
[^4]: [Detailed endagnered species analysis by park](https://github.com/KarolZG/biodiversity-starter/blob/main/output-data/endangered_species_by_park.csv)