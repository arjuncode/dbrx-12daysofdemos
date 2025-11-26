# Databricks notebook source
# MAGIC %md
# MAGIC # 🎄 Day 5: Demo - UC Functions for MCP
# MAGIC
# MAGIC ## See Governed Functions in Action
# MAGIC
# MAGIC This notebook demonstrates how UC Functions provide:
# MAGIC - **Data masking** for privacy
# MAGIC - **Governed queries** for AI agents
# MAGIC - **Reusable logic** across all platforms
# MAGIC
# MAGIC ### Prerequisites
# MAGIC - Run `00_load_synthetic_data.py` to load data
# MAGIC - Run `01_create_uc_functions_mcp.py` to create functions
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configuration

# COMMAND ----------

# Config - update these to match your 00-init setup
TARGET_CATALOG = "main"
TARGET_SCHEMA  = "dbrx_12daysofdemos"

# Construct names
schema_name = f"{TARGET_CATALOG}.{TARGET_SCHEMA}"
table_name = f"{schema_name}.santa_letters"

print(f"Using schema: {schema_name}")
print(f"Table: {table_name}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📊 Step 1: View Raw Data (Unmasked)

# COMMAND ----------

spark.sql(f"""
SELECT
  name,
  email,
  city,
  province,
  SUBSTRING(letter, 1, 100) AS letter_preview,
  gifts
FROM {table_name}
LIMIT 10
""").display()

# COMMAND ----------

# MAGIC %md
# MAGIC ⚠️ **Problem:** Raw names AND emails visible - not safe to share with AI or external systems

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🔒 Step 2: Apply Masking Functions

# COMMAND ----------

spark.sql(f"""
SELECT
  {schema_name}.mask_name(name) AS masked_name,
  {schema_name}.mask_email(email) AS masked_email,
  city,
  province,
  SUBSTRING(letter, 1, 100) AS letter_preview,
  gifts
FROM {table_name}
LIMIT 10
""").display()

# COMMAND ----------

# MAGIC %md
# MAGIC ✅ **Solution:** Names automatically masked - safe for AI agents and demos!

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📈 Step 3: Use Aggregate Functions (MCP-Ready)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Get Summary for Ontario

# COMMAND ----------

spark.sql(f"SELECT {schema_name}.get_province_summary('Ontario') AS ontario_stats").display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Get Summary for All Major Provinces

# COMMAND ----------

spark.sql(f"""
SELECT
  'Ontario' AS province,
  {schema_name}.get_province_summary('Ontario') AS stats
UNION ALL
SELECT
  'Quebec' AS province,
  {schema_name}.get_province_summary('Quebec') AS stats
UNION ALL
SELECT
  'British Columbia' AS province,
  {schema_name}.get_province_summary('British Columbia') AS stats
""").display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🔍 Step 4: Safe Search Function

# COMMAND ----------

# MAGIC %md
# MAGIC ### Search for letters mentioning "bicycle"

# COMMAND ----------

spark.sql(f"SELECT * FROM TABLE({schema_name}.search_letters('bicycle'))").display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Search for letters mentioning "LEGO"

# COMMAND ----------

spark.sql(f"SELECT * FROM TABLE({schema_name}.search_letters('LEGO'))").display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Search for letters mentioning "PlayStation"

# COMMAND ----------

spark.sql(f"SELECT * FROM TABLE({schema_name}.search_letters('PlayStation'))").display()

# COMMAND ----------

# MAGIC %md
# MAGIC ✅ **Notice:** All results have **automatically masked names** - safe for AI!

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🎯 Step 5: Create a Governed View for MCP

# COMMAND ----------

# Use catalog and create schema for safe views
spark.sql(f"USE CATALOG {TARGET_CATALOG}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")

print(f"✓ Using catalog: {TARGET_CATALOG}")
print(f"✓ Schema: {schema_name}")

# COMMAND ----------

# Create masked view
view_name = f"{schema_name}.santa_letters_masked"

spark.sql(f"""
CREATE OR REPLACE VIEW {view_name} AS
SELECT
  {schema_name}.mask_name(name) AS child_name,
  {schema_name}.mask_email(email) AS masked_email,
  city,
  province,
  letter,
  gifts
FROM {table_name}
""")

print(f"✓ Created view: {view_name}")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Query the Masked View

# COMMAND ----------

spark.sql(f"SELECT * FROM {view_name} LIMIT 10").display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📊 Step 6: Analytics with Governed Functions

# COMMAND ----------

# MAGIC %md
# MAGIC ### Letters by Province (Safe to Share)

# COMMAND ----------

spark.sql(f"""
SELECT
  province,
  COUNT(*) AS letter_count,
  COUNT(DISTINCT city) AS unique_cities
FROM {view_name}
GROUP BY province
ORDER BY letter_count DESC
""").display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Top Gift Requests (Anonymized)

# COMMAND ----------

spark.sql(f"""
SELECT
  gifts,
  COUNT(*) AS request_count,
  SLICE(COLLECT_LIST(child_name), 1, 5) AS sample_requesters
FROM {view_name}
WHERE gifts IS NOT NULL
GROUP BY gifts
ORDER BY request_count DESC
LIMIT 15
""").display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🎉 Success! MCP-Ready Data Platform
# MAGIC
# MAGIC ### ✅ What You Accomplished
# MAGIC
# MAGIC 1. **Built secure UC Functions** - PII masking, aggregation, search
# MAGIC 2. **Created governed views** - Safe for AI agent access
# MAGIC 3. **Demonstrated reusability** - Same functions everywhere
# MAGIC
# MAGIC ### 🌟 How This Powers MCP
# MAGIC
# MAGIC **MCP Server Configuration:**
# MAGIC ```python
# MAGIC # MCP server exposes UC functions as tools
# MAGIC @mcp.tool()
# MAGIC def search_santa_letters(keyword: str) -> dict:
# MAGIC     # Calls UC Function via SQL endpoint
# MAGIC     result = spark.sql(f"""
# MAGIC         SELECT * FROM TABLE(
# MAGIC             {schema_name}.search_letters('{keyword}')
# MAGIC         )
# MAGIC     """)
# MAGIC     return result.toPandas().to_dict()
# MAGIC ```
# MAGIC
# MAGIC **AI Agent Usage:**
# MAGIC - Claude/ChatGPT can call these functions as tools
# MAGIC - Results are **automatically governed and masked**
# MAGIC - No direct table access needed
# MAGIC - Unity Catalog tracks all usage
# MAGIC
# MAGIC ### 🔑 Key Benefits
# MAGIC
# MAGIC | Traditional | UC Functions + MCP |
# MAGIC |-------------|-------------------|
# MAGIC | AI queries raw tables | AI calls governed functions |
# MAGIC | Manual PII masking in code | Automatic masking built-in |
# MAGIC | No lineage tracking | Full UC lineage |
# MAGIC | Custom API per query | Reusable UC Functions |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **🎅 Your Lakehouse is now MCP-ready with governed UC Functions!**
