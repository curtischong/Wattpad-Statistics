# Databricks notebook source exported at Wed, 14 Sep 2016 01:21:00 UTC
# read data
MOUNT_NAME = "hackondata-hayden-s3"
file_path1 = "/mnt/%s/Wattpad/part-00000" % MOUNT_NAME
file_path2 = "/mnt/%s/Wattpad/part-00001" % MOUNT_NAME
file_path3 = "/mnt/%s/Wattpad/part-00002" % MOUNT_NAME
file_path4 = "/mnt/%s/Wattpad/part-00003" % MOUNT_NAME

# COMMAND ----------

# create df
df1 = sqlContext.jsonFile(file_path1)
df2 = sqlContext.jsonFile(file_path2)
df3 = sqlContext.jsonFile(file_path3)
df4 = sqlContext.jsonFile(file_path4)
df = df1.unionAll(df2).unionAll(df3).unionAll(df4)

# COMMAND ----------

# data processing
from pyspark.ml.feature import *
from pyspark.sql.types import *
from pyspark.sql.functions import *

# parse age group
def get_age_group(age):
    try:
        age = int(age)
    except:
        return 'null'

    if age <= 17:
        return '12 - 17'
    if age <= 24:
        return '18 - 24'
    if age <= 34:
        return '25 - 34'
    if age <= 44:
        return '35 - 44'      
    if age <= 54:
        return '45 - 54'    
    return '55+'

get_age_udf = udf(get_age_group, StringType())  

# convert masked feature to string, in order to do one-hot-encoding later on
df_processed = df.select('*', 
                         get_age_udf('follower_age').alias('follower_age_group'), 
                         get_age_udf('followee_age').alias('followee_age_group'), 
                         df.follower_gender.cast("string").alias('follower_gender_s'),
                        df.followee_gender.cast("string").alias('followee_gender_s'),
                        df.follower_platform.cast("string").alias('follower_platform_s'),
                        df.followee_platform.cast("string").alias('followee_platform_s'),
                        df.followee_user_language.cast("string").alias('followee_user_language_s'),
                        df.follower_user_language.cast("string").alias('follower_user_language_s'),)

df_processed = df_processed.na.fill({'follower_gender_s': 'null', 
                                     'followee_gender_s': 'null', 
                                     'followee_user_language_s': 'null', 
                                     'follower_user_language_s': 'null',       
                                     'follower_latitude': 43.6532,
                                     'follower_longitude': -79.3832
                                    })

# COMMAND ----------

df_processed.printSchema()

# COMMAND ----------

from pyspark.ml.feature import OneHotEncoder, StringIndexer
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler

# create features on the df
def get_string_indexers(cols):
    return [StringIndexer(inputCol=col, outputCol=col + "_i") for col in cols]

def get_onehot_encoder(cols):
    return [OneHotEncoder(dropLast=False, inputCol=col + "_i", outputCol=col + "_v") for col in cols]
  
cols = ['followee_age_group', 'follower_age_group', 'follower_gender_s', 'followee_gender_s', 'follower_platform_s', 'followee_platform_s', 'followee_user_language_s', 'follower_user_language_s']   

string_indexers = get_string_indexers(cols)    
onehot_encoders = get_onehot_encoder(cols)                      

assembler = VectorAssembler(
    inputCols=[col + '_v' for col in cols] + ['followee_has_atleast_three_reading_lists', 'followee_has_profile_picture', 'followee_show_name', 'follower_has_profile_picture', 'follower_is_author', 'follower_show_age', 'follower_show_name', 'follower_has_atleast_three_reading_lists'], outputCol="features")

# pipeline for generating the features
pipeline = Pipeline(stages=string_indexers + onehot_encoders + [assembler])
feature_model = pipeline.fit(df_processed)

df_feature = feature_model.transform(df_processed)
df_feature.cache()

# COMMAND ----------

from pyspark.ml.clustering import KMeans

# kmeans clustering
k_cluster = 100
kmeans = KMeans(predictionCol="prediction", k=k_cluster, initMode="random", initSteps=5, tol=1e-4, maxIter=100, seed=42)
cluster_model = kmeans.fit(df_feature)
df_cluster = cluster_model.transform(df_feature).select("features", "prediction", "followee_id")

# COMMAND ----------

# clusters of followees
cluster_followee_ids = df_cluster.groupBy(['prediction', 'followee_id']).count().sort("prediction", desc("count"))
cluster_followee_ids.cache()

# COMMAND ----------

# prediction
test_sample = [{"followee_id":"5a9717ebb0cc0393d84bd2770dd24b860ac00dbb03402de54e1f0b990c03d90d","followee_age":"39","followee_latitude":43.655,"followee_longitude":-79.363,"followee_show_name":1,"followee_show_age":1,"followee_is_author":1,"followee_has_atleast_three_reading_lists":1,"followee_has_profile_picture":1,"follower_id":"61ef8d54c48181bd5dfc5cb74d484787e6378771084646d4c0536704d3da5605","follower_latitude":47.167,"follower_longitude":27.6,"follower_show_name":0,"follower_show_age":0,"follower_is_author":1,"follower_has_atleast_three_reading_lists":0,"follower_has_profile_picture":1,"follower_gender":70,"followee_gender":70,"follower_user_language":1831,"followee_user_language":1831,"follower_platform":3,"followee_platform":3,"follower_age": "23"}]
test_df = sqlContext.createDataFrame(test_sample)

df_processed_test = test_df.select('*', 
                         get_age_udf('follower_age').alias('follower_age_group'), 
                         get_age_udf('followee_age').alias('followee_age_group'), 
                         test_df.follower_gender.cast("string").alias('follower_gender_s'),
                        test_df.followee_gender.cast("string").alias('followee_gender_s'),
                        test_df.follower_platform.cast("string").alias('follower_platform_s'),
                        test_df.followee_platform.cast("string").alias('followee_platform_s'),
                        test_df.followee_user_language.cast("string").alias('followee_user_language_s'),
                        test_df.follower_user_language.cast("string").alias('follower_user_language_s'),)

df_processed_test = df_processed_test.na.fill({'follower_gender_s': 'null', 
                                     'followee_gender_s': 'null', 
                                     'followee_user_language_s': 'null', 
                                     'follower_user_language_s': 'null',       
                                     'follower_latitude': 43.6532,
                                     'follower_longitude': -79.3832
                                    })

df_feature_test = feature_model.transform(df_processed_test)
df_cluster_test = cluster_model.transform(df_feature_test).select("features", "prediction", "followee_id")

prediction_ids = cluster_followee_ids.join(df_cluster_test, df_cluster_test.prediction == cluster_followee_ids.prediction).drop(df_cluster_test.followee_id)


# COMMAND ----------

# recommend top 3 followees
n_top = 3
print 'You may like these followees, happy reading :) \n', prediction_ids.select('followee_id').take(n_top)
