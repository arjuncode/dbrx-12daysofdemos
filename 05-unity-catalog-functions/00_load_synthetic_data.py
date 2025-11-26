# Databricks notebook source
# MAGIC %md
# MAGIC # 🎅 Day 5: Load Santa Letters Data
# MAGIC
# MAGIC ## Load Canadian Santa Letters into Unity Catalog
# MAGIC
# MAGIC This notebook loads the Canadian Santa letters dataset with added email addresses into Unity Catalog.
# MAGIC
# MAGIC ### Prerequisites
# MAGIC - Run `00-init/load-data.ipynb` first to set up the base data
# MAGIC
# MAGIC ### Dataset Schema
# MAGIC - **name**: First name of the child
# MAGIC - **email**: Email address (80% populated, 20% null)
# MAGIC - **province**: Canadian province of residence
# MAGIC - **city**: City where the child lives
# MAGIC - **date**: Date the letter was written
# MAGIC - **letter**: Content of the letter expressing holiday wishes
# MAGIC - **gifts**: A comma-separated list of requested gifts
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configuration
# MAGIC
# MAGIC These values should match your `00-init/load-data.ipynb` configuration.

# COMMAND ----------

# Config - update these to match your 00-init setup
TARGET_CATALOG = "main"
TARGET_SCHEMA  = "dbrx_12daysofdemos"
TARGET_VOLUME  = "raw_data_volume"

# Construct paths
csv_file_path = f"/Volumes/{TARGET_CATALOG}/{TARGET_SCHEMA}/{TARGET_VOLUME}/santa_letters_canada_with_emails.csv"
schema_name = f"{TARGET_CATALOG}.{TARGET_SCHEMA}"

print(f"Using catalog: {TARGET_CATALOG}")
print(f"Using schema: {schema_name}")
print(f"CSV path: {csv_file_path}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 2: Read the CSV File

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType

# Define schema
schema = StructType([
    StructField("name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("province", StringType(), True),
    StructField("city", StringType(), True),
    StructField("date", StringType(), True),
    StructField("letter", StringType(), True),
    StructField("gifts", StringType(), True)
])

# Read CSV
df = spark.read \
    .option("header", "true") \
    .option("multiLine", "true") \
    .option("escape", "\"") \
    .schema(schema) \
    .csv(csv_file_path)

# Display sample
display(df.limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 3: Verify Data Quality

# COMMAND ----------

from pyspark.sql.functions import count, countDistinct, when, col, avg, length

# Check record count and data quality
df.select(
    count("*").alias("total_records"),
    countDistinct("name").alias("unique_names"),
    count(when(col("email").isNotNull(), 1)).alias("records_with_email"),
    countDistinct("city").alias("unique_cities"),
    countDistinct("province").alias("unique_provinces"),
    count(when(col("gifts").isNotNull(), 1)).alias("records_with_gifts"),
    avg(length("letter")).alias("avg_letter_length")
).display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 4: Save to Unity Catalog

# COMMAND ----------

# Use the configured catalog and schema
spark.sql(f"USE CATALOG {TARGET_CATALOG}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")

print(f"✓ Using catalog: {TARGET_CATALOG}")
print(f"✓ Schema ready: {schema_name}")

# COMMAND ----------

# Write to Delta table
table_name = f"{schema_name}.santa_letters_canada_email"

df.write \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(table_name)

print(f"✅ Data loaded successfully to {table_name}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 5: Verify the Table

# COMMAND ----------

# Query the table
spark.sql(f"""
SELECT
  name,
  email,
  city,
  province,
  date,
  SUBSTRING(letter, 1, 100) AS letter_preview,
  gifts
FROM {table_name}
LIMIT 10
""").display()

# COMMAND ----------

# Check province distribution
spark.sql(f"""
SELECT
  province,
  COUNT(*) AS count
FROM {table_name}
GROUP BY province
ORDER BY count DESC
""").display()

# COMMAND ----------

# Sample gift requests
spark.sql(f"""
SELECT DISTINCT gifts
FROM {table_name}
LIMIT 30
""").display()

# COMMAND ----------

# Check email data quality
spark.sql(f"""
SELECT
  COUNT(*) AS total_records,
  COUNT(email) AS records_with_email,
  COUNT(*) - COUNT(email) AS records_without_email,
  ROUND(COUNT(email) * 100.0 / COUNT(*), 1) AS email_fill_rate_pct
FROM {table_name}
""").display()

# COMMAND ----------

# Sample email addresses
spark.sql(f"""
SELECT name, email
FROM {table_name}
WHERE email IS NOT NULL
LIMIT 15
""").display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Data Loaded Successfully!
# MAGIC
# MAGIC The table is ready with the configured catalog and schema.
# MAGIC
# MAGIC ### What's in the Data?
# MAGIC - ✅ **5,000 Canadian Santa letters** from children across all provinces
# MAGIC - ✅ **Email addresses**: 80% populated with realistic patterns (lindsey.red@hotmail.com, kevin.cal@outlook.com)
# MAGIC - ✅ **Real Canadian locations**: All 10 provinces and 3 territories
# MAGIC - ✅ **Date stamps**: Letters from Nov-Dec 2024
# MAGIC - ✅ **Diverse gift requests**: Modern toys, electronics, books, and more
# MAGIC - ✅ **Ready for UC Functions**: Perfect for demonstrating data masking and governance
# MAGIC
# MAGIC ### Next Steps
# MAGIC 1. Run `01_create_uc_functions.py` to create UC Functions
# MAGIC 2. Run `02_apply_transformations.py` to clean and enrich the data
# MAGIC 3. Explore the cleaned data with BI queries
