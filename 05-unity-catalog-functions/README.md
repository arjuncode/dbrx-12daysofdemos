# 🎅 Day 5: Unity Catalog Functions - Governed Data Operations

## North Pole Modernization Project - Reusable Function Library

Welcome to **Day 5** of the **12 Days of Databricks Demos**!

---

## 📖 The Story: Why the North Pole Needs Governance

The **North Pole Modernization Office (NPMO)** processes millions of children's letters. The challenge:

### The Problem
- **PII everywhere:** Child names, emails, addresses in raw data
- **Repeated logic:** Same masking/aggregation code copied everywhere
- **No governance:** Can't track who accessed what data
- **Unsafe for AI:** Can't share data with AI agents without PII exposure

### The Old Way
- Copy-paste masking logic across notebooks
- Manual data anonymization before sharing
- No lineage tracking
- Different logic in each application

### The New Way (Unity Catalog Functions)
- ✅ **Reusable functions** with built-in governance
- ✅ **Automatic PII masking** embedded in functions
- ✅ **Lineage tracking** via Unity Catalog
- ✅ **One source of truth** for business logic
- ✅ **Safe for AI agents** - governed access patterns

---

## 🎯 What You'll Build

### 4 Production-Ready UC Functions

| Function | Type | Purpose | Use Case |
|----------|------|---------|----------|
| `mask_email()` | Scalar | Mask email addresses | PII protection, GDPR compliance |
| `mask_name()` | Scalar | Anonymize personal names | Child privacy, safe demos |
| `get_province_summary()` | Scalar (JSON) | Aggregate letter stats | AI agent queries, analytics |
| `search_letters()` | Table-valued | Search with auto-masking | Safe search, governed access |

---

## 📦 Deliverables

| File | Description |
|------|-------------|
| `data/santa_letters_canada_with_emails.csv` | 5,000 Canadian Santa letters with emails |
| `data/add_emails_to_dataset.py` | Script to add email addresses to dataset |
| `00_load_synthetic_data.py` | Load CSV into Unity Catalog |
| `01_create_uc_functions_mcp.py` | Create 4 UC Functions |
| `02_demo_mcp_functions.py` | Demo functions in action |
| `README.md` | This file - complete documentation |

---

## 🚀 Quick Start

### Step 1: Prepare & Load Data

The dataset is ready with 5,000 Canadian Santa letters including email addresses!

**Upload** `santa_letters_canada_with_emails.csv` to Databricks:
- Recommended path: `/Volumes/danny_park/day5_uc_functions/data/`

### Step 2: Run the Notebooks

**In order:**

1. **`00_load_synthetic_data.py`**
   - Loads CSV into `danny_park.day5_uc_functions.santa_letters`
   - Verifies data quality

2. **`01_create_uc_functions_mcp.py`**
   - Creates 4 UC Functions in `danny_park.day5_uc_functions`
   - Tests each function

3. **`02_demo_mcp_functions.py`**
   - Demonstrates functions in real scenarios
   - Shows before/after PII masking
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
- AI agent access

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
- AI agent queries ("How many letters from Ontario?")
- Dashboard summaries
- API responses
- Analytics aggregation

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
- Safe search for AI agents
- Compliance-safe exploration
- Keyword analysis without PII exposure

---

## 🎯 Demo Flow (15 minutes)

### Part 1: The Problem (3 min)

**Show raw data:**
```sql
SELECT name, email, city, letter FROM santa_letters LIMIT 5;
```

**Point out:** "Look at all this PII - names, emails, locations. Can't safely share this with AI or external systems."

### Part 2: Create UC Functions (5 min)

**Run:** `01_create_uc_functions_mcp.py`

**Highlight key moments:**
1. **Scalar functions** - Simple masking logic
2. **Table-valued function** - Returns entire result sets
3. **JSON function** - Structured output for APIs/AI

**Key message:** "These functions are now governed assets in Unity Catalog - reusable everywhere."

### Part 3: Functions in Action (5 min)

**Run:** `02_demo_mcp_functions.py`

**Show:**
1. **Before/after** - Raw data vs masked data
2. **Search function** - Automatic masking in results
3. **Aggregation** - JSON output for consumption

**Key message:** "Same functions work in SQL, Python, dashboards, and eventually AI agents."

### Part 4: Governance Benefits (2 min)

**Show in Unity Catalog:**
- Function definitions
- Lineage tracking
- Access control options

**Key message:** "Unity Catalog tracks every function call - full governance and auditability."

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
| Not AI-ready | Ready for AI agent consumption |

### The Power of Governed Functions

1. **Reusability**
   - Use in SQL queries
   - Call from Python notebooks
   - Embed in BI dashboards
   - Expose to AI agents (future: MCP)

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

## 🔜 What's Next

### Day 6/7: Genie Space (Future)

These UC Functions will eventually power AI agents:

**Scenario:** User asks Genie Space, *"How many letters from Ontario?"*

**Genie automatically:**
1. Calls `get_province_summary('Ontario')`
2. Parses JSON response
3. Answers: "247 letters from 15 cities in Ontario"

**Scenario:** User asks, *"Show me kids who asked for LEGO"*

**Genie automatically:**
1. Calls `search_letters('LEGO')`
2. Gets results with masked names
3. Shows safe, anonymized results

**The magic:** Same UC Functions used by humans and AI - all governed!

---

## 💡 Use Cases Beyond Santa Letters

These function patterns apply to any industry:

### Healthcare
```sql
CREATE FUNCTION mask_patient_id(id STRING) RETURNS STRING
CREATE FUNCTION search_diagnoses(condition STRING) RETURNS TABLE(...)
```

### Finance
```sql
CREATE FUNCTION mask_account_number(account STRING) RETURNS STRING
CREATE FUNCTION get_transaction_summary(customer_id STRING) RETURNS STRING
```

### E-commerce
```sql
CREATE FUNCTION mask_customer_email(email STRING) RETURNS STRING
CREATE FUNCTION search_orders(keyword STRING) RETURNS TABLE(...)
```

**The pattern is universal:** Governed, reusable functions for safe data operations.

---

## 🤝 Contributing

This is a demo project for educational purposes. Extend it by:
- Adding more masking functions (SSN, credit card, etc.)
- Creating aggregation functions for different dimensions
- Building more complex table-valued functions

---

## 📖 Resources

- [Unity Catalog Functions Documentation](https://docs.databricks.com/en/sql/language-manual/sql-ref-functions.html)
- [Databricks Lakehouse Platform](https://www.databricks.com/product/unity-catalog)
- [Data Governance Best Practices](https://www.databricks.com/product/unity-catalog/governance)

---

## 📝 License

MIT License - see repository root for details

---

**🎅 Build governed, reusable functions with Unity Catalog!**

Transform your data operations from scattered logic to governed, enterprise-grade functions that power everything from SQL queries to AI agents.

Built with ❤️ on the Databricks Lakehouse Platform
