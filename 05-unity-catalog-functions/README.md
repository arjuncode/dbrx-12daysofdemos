# 🎅 Day 5: Unity Catalog Functions - Governed Data Operations

## North Pole Modernization Project - Reusable Function Library

Welcome to **Day 5** of the **12 Days of Databricks Demos**!

---

## 📖 The Story: Why the North Pole Needs Governance

The **North Pole Modernization Office (NPMO)** processes millions of children's letters. The challenge:

### The Problem
- **PII everywhere:** Child names, emails, addresses in raw data
- **Repeated logic:** Same masking/aggregation code copied across notebooks and dashboards
- **No governance:** Can't track who accessed what data or how functions are used
- **Inconsistent security:** Different teams implement masking differently

### The Old Way
- Copy-paste masking logic across notebooks
- Manual data anonymization before sharing
- No lineage tracking
- Different logic in each application
- No reusability across SQL, Python, and BI tools

### The New Way (Unity Catalog Functions)
- ✅ **Reusable functions** callable from SQL, Python, and BI dashboards
- ✅ **Automatic PII masking** embedded in function definitions
- ✅ **Lineage tracking** via Unity Catalog
- ✅ **One source of truth** for business logic
- ✅ **Governed access** with Unity Catalog permissions

---

## 🎯 What You'll Build

### 4 Production-Ready UC Functions

| Function | Type | Purpose | Use Case |
|----------|------|---------|----------|
| `mask_email()` | Scalar | Mask email addresses | PII protection, GDPR compliance |
| `mask_name()` | Scalar | Anonymize personal names | Child privacy, safe demos |
| `get_province_summary()` | Scalar (JSON) | Aggregate letter stats | Dashboard analytics, API responses |
| `search_letters()` | Table-valued | Search with auto-masking | Safe search, governed data access |

---

## 📦 Deliverables

| File | Description |
|------|-------------|
| `01_create_uc_functions.py` | Create 4 Unity Catalog Functions |
| `02_uc_functions_demo.py` | Demo functions with real queries |
| `README.md` | This file - complete documentation |

---

## 🚀 Quick Start

### Prerequisites

1. **Configure your catalog and schema** in `00-init/load-data.ipynb`:
   ```python
   TARGET_CATALOG = "main"
   TARGET_SCHEMA  = "dbrx_12daysofdemos"
   TARGET_VOLUME  = "raw_data_volume"
   ```

2. **Run `00-init/load-data.ipynb`** to:
   - Create the Unity Catalog schema and volume
   - Download and load `santa_letters_canada_with_emails.csv`
   - Create table: `main.dbrx_12daysofdemos.santa_letters_canada_with_emails`

### Run the Notebooks (in order)

1. **`01_create_uc_functions.py`**
   - Creates 4 Unity Catalog Functions
   - Tests each function with sample queries

2. **`02_uc_functions_demo.py`**
   - Demonstrates functions with real queries
   - Shows PII masking in action
   - Creates governed views

---

## 🌟 Key Concepts Demonstrated

### 1. Data Masking Functions

**Without UC Functions:**
```sql
-- Repeated everywhere, inconsistent logic
SELECT
  CONCAT(SUBSTRING(name, 1, 1), '***', SUBSTRING(name, -1)) AS masked_name
FROM letters;
```

**With UC Functions:**
```sql
-- Consistent, reusable, governed
SELECT mask_name(name) AS masked_name FROM letters;
```

**Benefits:**
- ✅ One implementation, used everywhere
- ✅ Consistent masking logic
- ✅ Unity Catalog tracks usage
- ✅ Easy to update globally

### 2. Aggregation Functions

**Traditional Approach:**
```python
# Custom API endpoint for each query
@app.route('/province_stats')
def get_province_stats(province):
    query = f"SELECT COUNT(*) FROM letters WHERE province = '{province}'"
    # Security risk: SQL injection
    # No governance tracking
```

**UC Function Approach:**
```sql
-- Governed, reusable, safe
CREATE FUNCTION get_province_summary(province STRING) RETURNS STRING
-- Returns JSON, no SQL injection risk, tracked by UC
```

**Benefits:**
- ✅ Parameterized queries (no SQL injection)
- ✅ Unity Catalog governance
- ✅ Reusable from SQL, Python, BI tools
- ✅ Single function definition

### 3. Table-Valued Functions

**Without UC Functions:**
```sql
-- Search requires manual masking every time
SELECT
  CONCAT(SUBSTRING(name, 1, 1), '***') AS name,
  letter
FROM letters
WHERE letter LIKE '%bicycle%';
```

**With UC Functions:**
```sql
-- Masking built-in, always safe
SELECT * FROM TABLE(search_letters('bicycle'));
-- Names automatically masked!
```

**Benefits:**
- ✅ PII protection by design
- ✅ Can't forget to mask
- ✅ Safe to expose to AI agents
- ✅ Consistent results everywhere

---

## 📊 Function Details

### Function 1: `mask_email(email STRING)`

**Purpose:** Mask email addresses for privacy compliance

**Logic:**
- Preserves first/last char of username
- Masks middle chars: `***`
- Shows domain structure: `g***l.com`

**Example:**
```sql
SELECT mask_email('santa@northpole.com');
-- Returns: 's***a@n*********e.com'
```

**Use Cases:**
- GDPR compliance
- Safe demos and screenshots
- Sharing data with third parties
- Protecting PII in analytics dashboards

---

### Function 2: `mask_name(name STRING)`

**Purpose:** Anonymize personal names while preserving structure

**Logic:**
- Shows first and last character
- Masks everything in between
- Handles edge cases (short names, NULL)

**Example:**
```sql
SELECT mask_name('Emma');
-- Returns: 'E**a'

SELECT mask_name('Alexander');
-- Returns: 'A*******r'
```

**Use Cases:**
- Child privacy protection
- Analytics without PII
- Compliance with child data protection laws

---

### Function 3: `get_province_summary(province STRING)`

**Purpose:** Get aggregated statistics for a province (returns JSON)

**Returns:**
```json
{
  "province": "Ontario",
  "total_letters": 247,
  "unique_cities": 15,
  "sample_gifts": ["Bicycle", "LEGO Set", ...]
}
```

**Example:**
```sql
SELECT get_province_summary('Ontario');
```

**Use Cases:**
- Dashboard summaries and widgets
- API responses for applications
- Analytics aggregation
- Standardized reporting across teams

---

### Function 4: `search_letters(keyword STRING)`

**Purpose:** Search letters by keyword with automatic PII masking

**Returns:** Table with columns:
- `masked_name` - Automatically anonymized
- `city`
- `province`
- `letter_preview` - First 200 chars

**Example:**
```sql
SELECT * FROM TABLE(search_letters('bicycle'));
-- All names automatically masked!
```

**Use Cases:**
- Compliance-safe data exploration
- Keyword analysis without PII exposure
- Building governed search interfaces
- Safe ad-hoc querying across teams

---

## 🏆 Key Takeaways

### Why Unity Catalog Functions Matter

| Traditional Approach | UC Functions |
|---------------------|--------------|
| Copy-paste logic everywhere | Write once, use everywhere |
| Inconsistent implementations | Single source of truth |
| No lineage tracking | Full UC governance |
| Manual security | Security by design |
| Hard to maintain | Update once, applies globally |
| Siloed per tool | Works across SQL, Python, BI |

### The Power of Governed Functions

1. **Reusability**
   - Use in SQL queries
   - Call from Python notebooks
   - Embed in BI dashboards
   - Share across teams and workspaces

2. **Governance**
   - Unity Catalog tracks all usage
   - Lineage from source to consumer
   - Access control at function level
   - Audit trail for compliance

3. **Security by Design**
   - PII masking built into functions
   - Can't forget to apply
   - Consistent across all consumers
   - Safe for demos and external sharing

4. **Maintainability**
   - Update logic in one place
   - Changes propagate everywhere
   - Version control via UC
   - Easy testing and validation

---

## 📚 Data Dictionary

### Input: `santa_letters`

| Column | Type | Description | Sample Values |
|--------|------|-------------|---------------|
| `name` | STRING | Child's first name | Lucas, Donna, Tammy |
| `email` | STRING | Email address (80% populated) | lindsey.red@hotmail.com, kevin.cal@outlook.com |
| `province` | STRING | Canadian province | Ontario, Alberta, Nova Scotia |
| `city` | STRING | City name | Calgary, Brampton, Red Deer |
| `date` | STRING | Letter date | 2024-11-17, 2024-12-03 |
| `letter` | STRING | Letter content | "Dear Santa, I would like..." |
| `gifts` | STRING | Comma-separated gifts | "electric scooter, virtual reality headset" |

### Output: Masked Views

| Column | Type | Description | Sample Values |
|--------|------|-------------|---------------|
| `masked_name` | STRING | Anonymized name | L***s, D***a, T***y |
| `masked_email` | STRING | Anonymized email | l*****y@h*****l.com, k***n@o*****k.com |
| `city` | STRING | City (unchanged) | Calgary, Brampton |
| `province` | STRING | Province (unchanged) | Ontario, Alberta |
| `letter_preview` | STRING | Truncated letter | First 200 characters |

---

## 📖 Resources

- [Unity Catalog Functions Documentation](https://docs.databricks.com/en/sql/language-manual/sql-ref-functions.html)
- [Databricks Lakehouse Platform](https://www.databricks.com/product/unity-catalog)
- [Data Governance Best Practices](https://www.databricks.com/product/unity-catalog/governance)

---

**🎅 Build governed, reusable functions with Unity Catalog!**
