### Wattpad Dataset Insights

###Project Scope:

To assist authors and advertisers to reach their target audiences by helping:

Authors - Discover similar authors and their userbase

Readers - Find recommended authors

Advertisers - Locate the most influential authors

We used the wattpad dataset from tranquint to generate the stats to visualize the data.

###Usage
####Spark

The spark script to create the recommendation system in the python notebook

You can view our recommendation algorithum which uses the features: age, language, gender, and platform 
to predict author recommendations for new readers that have the same follower characteristics.

####Maps
go to ```splacorn/github.io``` to view the map visualiztion of our hack.
Note: due to a lack of a powerful server try not to click on the map or else major lag will occur. clicking on the red points is okay
Simply click on a red point to view all of the followers for that author and some additional statistics.

From the recommendation algorithum in our databricks, you will receive the a list of 3 author ids.
simply paste that author id into the search box and it'll popup on screen (along with its followers)
