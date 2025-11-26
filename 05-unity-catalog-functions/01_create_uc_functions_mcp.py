# Databricks notebook source
# MAGIC %md
# MAGIC # 🎅 Day 5: Unity Catalog Functions for MCP Integration
# MAGIC
# MAGIC ## Building Governed, Reusable Functions for AI Agents
# MAGIC
# MAGIC ### The Power of UC Functions + MCP
# MAGIC
# MAGIC Unity Catalog Functions can be exposed through **Model Context Protocol (MCP)** servers, making them:
# MAGIC - ✅ **Tools for AI agents** (Claude, ChatGPT, etc.)
# MAGIC - ✅ **Governed** with lineage and access control
# MAGIC - ✅ **Reusable** across SQL, Python, dashboards, and AI
# MAGIC - ✅ **Secure** with built-in data masking and PII protection
# MAGIC
# MAGIC ### Prerequisites
# MAGIC - Run `00_load_synthetic_data.py` first to load the santa_letters table
# MAGIC
# MAGIC ### What We'll Build
# MAGIC
# MAGIC **4 Production-Ready UC Functions:**
# MAGIC 1. **`mask_email()`** - PII protection for email addresses
# MAGIC 2. **`mask_name()`** - Anonymize child names for privacy
# MAGIC 3. **`get_province_summary()`** - Aggregate query function for MCP
# MAGIC 4. **`search_letters()`** - Table-valued function with auto-masking
# MAGIC
# MAGIC These functions will be callable by AI agents through MCP!
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

# Construct schema name
schema_name = f"{TARGET_CATALOG}.{TARGET_SCHEMA}"
table_name = f"{schema_name}.santa_letters_canada_email"

print(f"Using schema: {schema_name}")
print(f"Table: {table_name}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🛠️ Setup: Use Catalog and Schema

# COMMAND ----------

# Use the configured catalog and schema
spark.sql(f"USE CATALOG {TARGET_CATALOG}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
spark.sql(f"USE {schema_name}")

print(f"✓ Using catalog: {TARGET_CATALOG}")
print(f"✓ Using schema: {schema_name}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🔒 Function 1: `mask_email()` - PII Protection
# MAGIC
# MAGIC **Purpose:** Mask email addresses for data privacy compliance
# MAGIC
# MAGIC **Use Case:**
# MAGIC - Protect PII when sharing data with AI agents
# MAGIC - GDPR/privacy compliance
# MAGIC - Safe data exploration in demos
# MAGIC
# MAGIC **MCP Usage:** AI agent can call this to safely display sensitive data
# MAGIC
# MAGIC **Example:**
# MAGIC - Input: `"santa@northpole.com"`
# MAGIC - Output: `"s***a@n*********e.com"`

# COMMAND ----------

spark.sql("""
CREATE OR REPLACE FUNCTION mask_email(email STRING)
RETURNS STRING
COMMENT 'Masks email addresses for PII protection - exposes first/last char of username and domain'
RETURN
  CASE
    WHEN email IS NULL OR email = '' THEN NULL
    WHEN INSTR(email, '@') = 0 THEN '***INVALID_EMAIL***'
    ELSE CONCAT(
      -- First char of username
      SUBSTRING(SPLIT(email, '@')[0], 1, 1),
      '***',
      -- Last char of username
      SUBSTRING(SPLIT(email, '@')[0], LENGTH(SPLIT(email, '@')[0]), 1),
      '@',
      -- First char of domain
      SUBSTRING(SPLIT(email, '@')[1], 1, 1),
      REPEAT('*', GREATEST(LENGTH(SPLIT(email, '@')[1]) - 6, 1)),
      -- Last 5 chars of domain (e.g., ".com")
      SUBSTRING(SPLIT(email, '@')[1], -5)
    )
  END
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ✅ **Test it:**

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   mask_email('santa@northpole.com') AS masked_santa,
# MAGIC   mask_email('emma.wilson@gmail.com') AS masked_emma,
# MAGIC   mask_email('invalid-email') AS invalid_test;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🎭 Function 2: `mask_name()` - Anonymize Personal Names
# MAGIC
# MAGIC **Purpose:** Anonymize child names while preserving data utility
# MAGIC
# MAGIC **Use Case:**
# MAGIC - Protect child privacy in demos
# MAGIC - Share analytics without exposing identities
# MAGIC - Compliance with child data protection laws
# MAGIC
# MAGIC **MCP Usage:** AI can safely query data without seeing real names
# MAGIC
# MAGIC **Example:**
# MAGIC - Input: `"Emma"`
# MAGIC - Output: `"E***a"`

# COMMAND ----------

spark.sql("""
CREATE OR REPLACE FUNCTION mask_name(name STRING)
RETURNS STRING
COMMENT 'Masks personal names for privacy - shows first and last character only'
RETURN
  CASE
    WHEN name IS NULL OR TRIM(name) = '' THEN NULL
    WHEN LENGTH(TRIM(name)) <= 2 THEN REPEAT('*', LENGTH(TRIM(name)))
    ELSE CONCAT(
      SUBSTRING(TRIM(name), 1, 1),
      REPEAT('*', LENGTH(TRIM(name)) - 2),
      SUBSTRING(TRIM(name), -1)
    )
  END
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ✅ **Test it:**

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   mask_name('Emma') AS masked_emma,
# MAGIC   mask_name('Alexander') AS masked_alexander,
# MAGIC   mask_name('Jo') AS masked_short_name;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📊 Function 3: `get_province_summary()` - Aggregate Query Function
# MAGIC
# MAGIC **Purpose:** Get letter statistics for a province (callable by MCP)
# MAGIC
# MAGIC **Use Case:**
# MAGIC - AI agents can query aggregated data
# MAGIC - No direct table access needed
# MAGIC - Governed query patterns
# MAGIC
# MAGIC **MCP Usage:**
# MAGIC ```
# MAGIC User: "How many letters from Ontario?"
# MAGIC AI Agent: calls get_province_summary('Ontario')
# MAGIC Returns: JSON with stats
# MAGIC ```
# MAGIC
# MAGIC **Returns:** JSON string with letter count and top gifts

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE FUNCTION get_province_summary(province_name STRING)
RETURNS STRING
COMMENT 'Returns JSON summary of letters from a specific province - designed for MCP tool use'
RETURN (
  SELECT TO_JSON(
    STRUCT(
      province_name AS province,
      COUNT(*) AS total_letters,
      COUNT(DISTINCT city) AS unique_cities,
      COLLECT_SET(SUBSTRING(gifts, 1, 50)) AS sample_gifts
    )
  )
  FROM {table_name}
  WHERE UPPER(province) = UPPER(province_name)
     OR province = province_name
)
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ✅ **Test it:**

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT get_province_summary('Ontario') AS ontario_summary;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT get_province_summary('Quebec') AS quebec_summary;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📋 Function 4: `search_letters()` - Safe Search Interface
# MAGIC
# MAGIC **Purpose:** Search letters by keyword with automatic PII masking
# MAGIC
# MAGIC **Use Case:**
# MAGIC - AI can search letters safely
# MAGIC - Results are automatically anonymized
# MAGIC - Prevents PII leakage to AI agents
# MAGIC
# MAGIC **MCP Usage:**
# MAGIC ```
# MAGIC User: "Find letters mentioning bicycles"
# MAGIC AI: calls search_letters('bicycle')
# MAGIC Returns: Masked results
# MAGIC ```

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE FUNCTION search_letters(keyword STRING)
RETURNS TABLE(
  masked_name STRING,
  city STRING,
  province STRING,
  letter_preview STRING
)
COMMENT 'Searches letters by keyword and returns results with masked names - safe for MCP'
RETURN
  SELECT
    mask_name(name) AS masked_name,
    city,
    province,
    SUBSTRING(letter, 1, 200) AS letter_preview
  FROM {table_name}
  WHERE UPPER(letter) LIKE CONCAT('%', UPPER(keyword), '%')
     OR UPPER(gifts) LIKE CONCAT('%', UPPER(keyword), '%')
  LIMIT 10
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ✅ **Test it:**

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM search_letters('bicycle');

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM search_letters('lego');

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📊 Verify All Functions Created

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW USER FUNCTIONS;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🎉 Success! MCP-Ready UC Functions Library
# MAGIC
# MAGIC ### ✅ What You Built
# MAGIC
# MAGIC | Function | Type | MCP Use Case |
# MAGIC |----------|------|--------------|
# MAGIC | `mask_email()` | Scalar | Protect email PII in results |
# MAGIC | `mask_name()` | Scalar | Anonymize personal names |
# MAGIC | `get_province_summary()` | Scalar (JSON) | Query aggregated stats |
# MAGIC | `search_letters()` | Table-valued | Safe search with auto-masking |
# MAGIC
# MAGIC ### 🌟 Why This Powers MCP Integration
# MAGIC
# MAGIC **Traditional Approach:**
# MAGIC - AI agents query raw tables directly → PII exposure risk
# MAGIC - No governance on what AI can access
# MAGIC - Custom API endpoints for each query pattern
# MAGIC
# MAGIC **UC Functions + MCP:**
# MAGIC - ✅ **Governed access** - Functions enforce security policies
# MAGIC - ✅ **Automatic PII masking** - Built into the function
# MAGIC - ✅ **Reusable patterns** - Same functions for humans and AI
# MAGIC - ✅ **Lineage tracking** - Unity Catalog tracks all usage
# MAGIC
# MAGIC ### 🔜 MCP Server Configuration
# MAGIC
# MAGIC These functions can be exposed via MCP as tools:
# MAGIC
# MAGIC ```json
# MAGIC {
# MAGIC   "tools": [
# MAGIC     {
# MAGIC       "name": "mask_email",
# MAGIC       "description": "Mask email addresses for privacy",
# MAGIC       "parameters": {"email": "string"}
# MAGIC     },
# MAGIC     {
# MAGIC       "name": "get_province_summary",
# MAGIC       "description": "Get letter statistics for a province",
# MAGIC       "parameters": {"province_name": "string"}
# MAGIC     },
# MAGIC     {
# MAGIC       "name": "search_letters",
# MAGIC       "description": "Search letters by keyword with auto-masking",
# MAGIC       "parameters": {"keyword": "string"}
# MAGIC     }
# MAGIC   ]
# MAGIC }
# MAGIC ```
# MAGIC
# MAGIC ### 💡 Example AI Agent Interaction
# MAGIC
# MAGIC **User:** "How many letters did we get from British Columbia?"
# MAGIC
# MAGIC **AI Agent:**
# MAGIC 1. Calls `get_province_summary('British Columbia')`
# MAGIC 2. Receives: `{"province":"British Columbia","total_letters":47,"unique_cities":6,...}`
# MAGIC 3. Responds: "We received 47 letters from British Columbia across 6 different cities."
# MAGIC
# MAGIC **User:** "Show me some kids who asked for LEGO"
# MAGIC
# MAGIC **AI Agent:**
# MAGIC 1. Calls `search_letters('LEGO')`
# MAGIC 2. Receives masked results: `E***a from Toronto...`
# MAGIC 3. Shows results with **names automatically protected**
# MAGIC
# MAGIC ### 🎯 Key Takeaways
# MAGIC
# MAGIC 1. **Security by Design** - PII masking built into functions, not application layer
# MAGIC 2. **Governed AI Access** - Unity Catalog controls who/what can call functions
# MAGIC 3. **Reusable Logic** - Same functions for SQL, Python, BI, and AI agents
# MAGIC 4. **Production-Ready** - Built for real enterprise governance needs
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **🎅 Your UC Functions are ready to power secure AI agents via MCP!**
