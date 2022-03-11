import findspark

findspark.init("/opt/manual/spark")

from pyspark.ml.pipeline import PipelineModel
from pyspark.sql import SparkSession, functions as F

spark = (SparkSession.builder
         .appName("Read From Kafka")
         .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1")
         .getOrCreate()
         )

spark.sparkContext.setLogLevel('ERROR')

lines = (spark.readStream
         .format("kafka")
         .option("kafka.bootstrap.servers", "localhost:9092")
         .option("subscribe", "office-input")
         .load())

lines2 = lines.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

lines3 = lines2.withColumn("Value_co2", F.split(F.col("value"), ",")[2]) \
    .withColumn("Value_humidity", F.split(F.col("value"), ",")[3]) \
    .withColumn("Value_temperature", F.split(F.col("value"), ",")[4]) \
    .withColumn("Value_light", F.split(F.col("value"), ",")[5]) \
    .withColumn("Room", F.split(F.col("value"), ",")[0]) \
    .withColumn("Time", F.split(F.col("value"), ",")[1]) \
    .selectExpr("CAST(Value_co2 AS FLOAT)", "CAST(Value_humidity AS FLOAT)"
                                     , "CAST(Value_temperature AS FLOAT)"
                                     , "CAST(Value_light AS FLOAT)", "value", "Room", "Time")

model = PipelineModel.load('~/saved_models/Clf_Tuned_Decision_Tree')

transformed_frame = model.transform(lines3).selectExpr('Value_co2', 'Value_humidity', 'Value_temperature', 'Value_light'
                                                       , "CAST(prediction AS FLOAT)", "value", "Room", "Time")
"""
pred = transformed_frame.selectExpr("prediction")"""

"""if pred == 1:
    topic = "office-activity"
else:
    topic = "office-no-activity"""""

checkpoint_dir = "file:///home/train/project_fin/streaming_logs"

streamingQuery = (transformed_frame
                  .writeStream
                  .format("console")
                  #.option("kafka.bootstrap.servers", "localhost:9092")
                  #.option("topic", topic)
                  .outputMode("append")
                  .option("checkpointLocation", checkpoint_dir)
                  .start())

streamingQuery.awaitTermination()