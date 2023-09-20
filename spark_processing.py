from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, lit, struct, when
from pyspark.sql.types import (
    DateType,
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)


def save_to_mysql(df, epoch_id):
    db_credentials = {
        "user": "test",
        "password": "test",
        "driver": "com.mysql.jdbc.Driver",
    }
    print("Epoch ID: ", epoch_id)
    now = datetime.now()
    mysql_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    cdf = (
        df.select(
            [
                "CityName",
                "Temperature",
                "Humidity",
                "CreationDate",
                "CreationTime",
            ]
        )
        .withColumn("ProcessedAt", lit(mysql_datetime))
        .withColumn("BatchId", lit(epoch_id))
    )
    cdf.write.jdbc(
        url="jdbc:mysql://host.docker.internal:3306/weather",
        table="data",
        mode="append",
        properties=db_credentials,
    )
    print("Data processed and saved to mysql" + str(epoch_id))


def spark_processing():
    spark = (
        SparkSession.builder.appName("SparkKafkaApp")
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1",
        ).config('spark.jars.packages', 'mysql:mysql-connector-j:8.0.33')
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "kafka1:19092")
        .option("subscribe", "test-topic")
        .option("startingOffsets", "latest")
        .load()
    )
    print(df.printSchema())
    df1 = df.selectExpr(
        "CAST(timestamp AS TIMESTAMP)", "CAST(value AS STRING)"
    )
    transcation_detail_schema = StructType(
        [
            StructField("CityName", StringType(), True),
            StructField("Temperature", DoubleType(), True),
            StructField("Humidity", IntegerType(), True),
            StructField("CreationTime", StringType(), True),
        ]
    )

    df2 = df1.select(
        from_json(col("value"), transcation_detail_schema).alias(
            "weather_detail"
        ),
        col("timestamp"),
    )
    df3 = df2.select("weather_detail.*", "timestamp")
    df4 = df3.withColumn("CreationDate", df3["CreationTime"].cast(DateType()))
    print(df4.printSchema())
    print("Here should be output from kafka topic: ")
    weather_write_stream = (
        df4.writeStream.trigger(processingTime="15 seconds")
        .outputMode("append")
        .option("truncate", "false")
        .format("console")
        .start()
    )  # for writing to console, debug only

    df4.writeStream.trigger(processingTime="15 seconds").outputMode(
        "update"
    ).foreachBatch(save_to_mysql).start()

    weather_write_stream.awaitTermination()


spark_processing()
