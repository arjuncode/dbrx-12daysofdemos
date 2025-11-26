# 🔄 Reproducibility Guide - Day 5: Unity Catalog Functions

## ✅ Making the Demo Fully Reproducible

This demo has been updated to use centralized configuration from `00-init/load-data.ipynb`.

---

## 📋 Prerequisites

### Step 1: Run the Init Notebook
Run **`00-init/load-data.ipynb`** first to:
- Set up the Unity Catalog structure
- Create the schema and volume
- Download all CSV files from GitHub
- Create base tables

### Configuration in Init Notebook:
```python
TARGET_CATALOG = "main"
TARGET_SCHEMA  = "dbrx_12daysofdemos"
TARGET_VOLUME  = "raw_data_volume"
```

This will create:
- **Catalog:** `main`
- **Schema:** `main.dbrx_12daysofdemos`
- **Volume:** `main.dbrx_12daysofdemos.raw_data_volume`
- **Tables:**
  - `main.dbrx_12daysofdemos.holiday_sales_and_trends`
  - `main.dbrx_12daysofdemos.santa_letters_canada`
  - `main.dbrx_12daysofdemos.santa_letters_canada_with_emails`

---

## 🚀 Running Day 5 Notebooks

All Day 5 notebooks now use the same configuration values:

```python
TARGET_CATALOG = "main"
TARGET_SCHEMA  = "dbrx_12daysofdemos"
```

### Notebook 1: `00_load_synthetic_data.py`
**Purpose:** Load the email-enhanced Santa letters dataset

**What it does:**
- Uses config to construct paths: `/Volumes/{TARGET_CATALOG}/{TARGET_SCHEMA}/{TARGET_VOLUME}/`
- Loads `santa_letters_canada_with_emails.csv`
- Creates table: `main.dbrx_12daysofdemos.santa_letters`
- Runs data quality checks

**Run order:** First (after init)

### Notebook 2: `01_create_uc_functions_mcp.py`
**Purpose:** Create 4 Unity Catalog Functions

**What it creates:**
- `main.dbrx_12daysofdemos.mask_email()` - Email masking function
- `main.dbrx_12daysofdemos.mask_name()` - Name masking function
- `main.dbrx_12daysofdemos.get_province_summary()` - JSON aggregation function
- `main.dbrx_12daysofdemos.search_letters()` - Table-valued search function

**Run order:** Second

### Notebook 3: `02_demo_mcp_functions.py`
**Purpose:** Demonstrate UC Functions in action

**What it does:**
- Shows raw data (PII visible)
- Applies masking functions
- Calls aggregation functions
- Uses table-valued search
- Creates governed view: `main.dbrx_12daysofdemos.santa_letters_masked`

**Run order:** Third

---

## 🔧 How Configuration Works

### In Each Notebook:
```python
# Config - update these to match your 00-init setup
TARGET_CATALOG = "main"
TARGET_SCHEMA  = "dbrx_12daysofdemos"

# Construct names
schema_name = f"{TARGET_CATALOG}.{TARGET_SCHEMA}"
table_name = f"{schema_name}.santa_letters"
```

### All Queries Use Variables:
```python
# Example: Query with variable
spark.sql(f"""
SELECT name, email
FROM {table_name}
LIMIT 10
""").display()

# Example: Function call with variable
spark.sql(f"SELECT {schema_name}.mask_email(email) FROM {table_name}").display()
```

**No hardcoded values** like `danny_park.day5_uc_functions` anywhere!

---

## 📊 Data Files

### In `00-init/data/`:
1. **`holiday-sales-and-trends.csv`** (1.6 MB)
   - Holiday sales data for other demos

2. **`santa_letters_canada.csv`** (1.9 MB)
   - Original Santa letters without emails
   - 5,000 records

3. **`santa_letters_canada_with_emails.csv`** (2.0 MB)
   - Enhanced with email addresses
   - 5,000 records, ~80% with emails
   - Used by Day 5 demo

---

## 🎯 Customization

### To Use Different Catalog/Schema:

**Option 1: Update in Each Notebook**
Change the config cell at the top of each Day 5 notebook:
```python
TARGET_CATALOG = "your_catalog"
TARGET_SCHEMA  = "your_schema"
```

**Option 2: Use Init Config (Recommended)**
Update `00-init/load-data.ipynb` config, then:
1. Run init notebook to set up your structure
2. Copy the same config values to Day 5 notebooks

---

## ✅ Validation Checklist

- [ ] Run `00-init/load-data.ipynb` successfully
- [ ] Verify tables created:
  - `main.dbrx_12daysofdemos.santa_letters_canada_with_emails`
- [ ] Run `00_load_synthetic_data.py` - loads santa_letters table
- [ ] Run `01_create_uc_functions_mcp.py` - creates 4 functions
- [ ] Run `02_demo_mcp_functions.py` - demonstrates functions
- [ ] Verify all queries work without errors

---

## 🔍 Troubleshooting

### Issue: "Table not found"
**Solution:** Make sure you ran `00-init/load-data.ipynb` first

### Issue: "Catalog does not exist"
**Solution:** Update `TARGET_CATALOG` to match your workspace catalog (usually "main")

### Issue: "Function not found"
**Solution:** Run `01_create_uc_functions_mcp.py` before `02_demo_mcp_functions.py`

### Issue: "File not found in volume"
**Solution:** Verify `00-init/load-data.ipynb` downloaded all CSVs successfully

---

## 📁 File Structure

```
dbrx-12daysofdemos/
├── 00-init/
│   ├── load-data.ipynb                         # ✅ Run this first!
│   └── data/
│       ├── holiday-sales-and-trends.csv
│       ├── santa_letters_canada.csv
│       └── santa_letters_canada_with_emails.csv # ✅ Email-enhanced
│
└── 05-unity-catalog-functions/
    ├── 00_load_synthetic_data.py               # ✅ Uses config
    ├── 01_create_uc_functions_mcp.py           # ✅ Uses config
    ├── 02_demo_mcp_functions.py                # ✅ Uses config
    ├── README.md
    ├── PROJECT_OUTLINE.md
    └── COMPLETION_SUMMARY.md
```

---

## 🎉 Benefits of This Approach

1. **Single Source of Truth**
   - Config defined once in `00-init`
   - Same values used everywhere

2. **Easy Customization**
   - Change 3 variables to adapt to any workspace
   - No find/replace across files needed

3. **No Hardcoded Values**
   - All queries use f-strings with variables
   - Catalog/schema names dynamically constructed

4. **Reproducible**
   - Anyone can run with their own catalog/schema
   - Works in any Databricks workspace

5. **Maintainable**
   - Easy to update paths and names
   - Clear dependencies between notebooks

---

## 🚀 Quick Start Commands

```python
# 1. Set your config (in 00-init/load-data.ipynb)
TARGET_CATALOG = "main"
TARGET_SCHEMA  = "dbrx_12daysofdemos"
TARGET_VOLUME  = "raw_data_volume"

# 2. Run init to set up structure
# (Run 00-init/load-data.ipynb)

# 3. Run Day 5 notebooks in order:
# - 00_load_synthetic_data.py
# - 01_create_uc_functions_mcp.py
# - 02_demo_mcp_functions.py

# 4. Verify functions created:
spark.sql("SHOW USER FUNCTIONS IN main.dbrx_12daysofdemos").display()

# 5. Test a function:
spark.sql("SELECT main.dbrx_12daysofdemos.mask_email('test@example.com')").display()
```

---

**✅ Your Day 5 demo is now fully reproducible!**
