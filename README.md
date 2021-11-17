# Mapping conflict 

Code and sample video for mapping the UCDP GED conflict data onto the NASA blue marble images. 

[![UCDP GED time series](https://img.youtube.com/vi/-k6o3E1RLHs/0.jpg)](https://www.youtube.com/watch?v=-k6o3E1RLHs)

## Instructions

1. Download the background maps from NASA (blue marble, one for each month). Or use this [Dropbox link](https://www.dropbox.com/sh/gf1ibffp185k0y9/AADT5PmrAM-xY4gUdDF5mvAka?dl=0).
1. Download the[ UCDP GED data](https://ucdp.uu.se/downloads/ged/ged211-csv.zip).
1. Install initial requirements with: `pip install requirements.txt`
1. Install cartopy with: `conda install -c conda-forge cartopy`
1. Run world_map.py with `python world_map.py`

world_map.py will generate thousands of individual frames. 
To create a video version, use: `create_video.py`

I plan to also create an interactive version quite easily with plotly if there is any interest.
