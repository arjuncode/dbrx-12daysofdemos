# 12 Days of Demos
The Databricks for Startups team is excited to tell the story of how the North Pole Modernization Office (NPMO) migrates from spreadsheets, scattered mall-store data, and handwritten Santa letters into a fully automated, AI-driven Lakehouse running on Databricks.

# North Pole Modernization Office - Synthetic Datasets

## Generated Datasets

1. **gift_requests.csv** - Children's letters with NLP-ready text and gift extraction
2. **reindeer_telemetry.csv** - IoT sensor data from training flights  
3. **workshop_production.csv** - Toy manufacturing quality metrics
4. **behavioral_analytics.csv** - Naughty/Nice scoring events
5. **delivery_optimization.csv** - Route planning and logistics data

## Usage

Load these datasets into Databricks using:
```python
df = spark.read.csv("/path/to/dataset.csv", header=True, inferSchema=True)
df.write.mode("overwrite").saveAsTable("npmo.table_name")
```
