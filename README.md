# Insights From Wattpad's Userdata
Created by [Hayden Liu](https://www.linkedin.com/in/hayden-liu-80445056/) and [Curtis Chong](https://www.linkedin.com/in/chongcurtis/) at [HackOn(Data) 2016](http://hackondata.com/2016/index.html)

## Project Scope:

We made this repo to help:

1) __Authors__ expand their readership through the userbase of other authors

2) __Readers__ searching from fresh authors

3) __Advertisers__ locate the most influential authors

All of our data was taken from TranQuant's Wattpad Userbase.
## Usage
#### Spark

Have you ever tried running a pySpark file without Jupyter? Same here. Lets do a quick [google search](https://stackoverflow.com/questions/40028919/how-to-run-a-script-in-pyspark).

The following features were used to predict author recommendations for new readers:
 - age
 - language
 - gender
 - platform


#### Maps
If you want to see to view the map visualiztion of our hack.
Note: due to a lack of a powerful server try not to click on the map or else major lag will occur. clicking on the red points is okay
Simply click on a red point to view all of the followers for that author and some additional statistics.

From the recommendation algorithm in our databricks, you will receive the a list of 3 author ids.
simply paste that author id into the search box and it'll popup on screen (along with its followers)
