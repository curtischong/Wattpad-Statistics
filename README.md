# Insights From Wattpad's Userdata
Created by [Hayden Liu](https://www.linkedin.com/in/hayden-liu-80445056/) and [Curtis Chong](https://www.linkedin.com/in/chongcurtis/) at [HackOn(Data) 2016](http://hackondata.com/2016/index.html)

![image of our demo app](http://res.cloudinary.com/dj2eq8czc/image/upload/v1473918557/wattpadMap_aqhjfh.png)

## Project Scope:

We made this repo to help:

1) __Authors__ expand their readership through the userbase of other authors

2) __Readers__ search for new authors

3) __Advertisers__ locate the most influential Toronto-based authors

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
If you want to view a [visualization of our hack](https://visualizing-wattpads-userbase.github.io/), pull the repo for the [demo site](https://github.com/visualizing-wattpads-userbase/visualizing-wattpads-userbase.github.io)

Our recommendation algorithm will return a list of three author ids. If you want to know where those authors are, simply paste that author id into the search box (from the demo) and the author (along with their followers) will popup on the map!
