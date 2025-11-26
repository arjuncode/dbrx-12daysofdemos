# 🎅 Day 5: Unity Catalog Functions - Project Outline

## Executive Summary

**Project:** North Pole Modernization - Governed Data Operations with Unity Catalog Functions

**Goal:** Demonstrate how Unity Catalog Functions provide reusable, governed business logic for data masking, aggregation, and safe AI agent access.

**Duration:** 15-minute demo

**Audience:** Data engineers, architects, governance teams, AI practitioners

---

## 🎯 Problem Statement

Santa's operations team faces critical data governance challenges:

1. **PII Everywhere** - Child names, emails, and contact info in raw data
2. **Scattered Logic** - Masking code copy-pasted across 50+ notebooks
3. **No Governance** - Can't track who accessed what data
4. **Unsafe for AI** - Can't share data with AI agents without PII leaks
5. **Maintenance Nightmare** - Change masking logic = update 50 files

---

## ✨ Solution: Unity Catalog Functions

**4 Production-Ready Functions:**

| # | Function | Type | Purpose |
|---|----------|------|---------|
| 1 | `mask_email()` | Scalar | PII protection for email addresses |
| 2 | `mask_name()` | Scalar | Anonymize personal names |
| 3 | `get_province_summary()` | Scalar (JSON) | Aggregate statistics for AI queries |
| 4 | `search_letters()` | Table-valued | Search with automatic masking |

---

## 📦 Project Structure

```
05-unity-catalog-functions/
│
├── data/
│   ├── generate_santa_letters.py       # Python script to generate synthetic data
│   └── santa_letters_synthetic.csv     # 1,000 synthetic letters with PII
│
├── 00_load_synthetic_data.py           # Databricks notebook to load CSV
├── 01_create_uc_functions_mcp.py       # Create 4 UC Functions
├── 02_demo_mcp_functions.py            # Demo functions in action
│
├── README.md                            # Complete documentation
├── PROJECT_OUTLINE.md                   # This file
└── DEMO_GUIDE.md                        # 15-min demo script
```

---

## 🔄 Data Flow

```
┌─────────────────────┐
│  Kaggle Inspired    │
│  Synthetic Data     │
│  (1,000 letters)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   CSV File          │
│  santa_letters.csv  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Unity Catalog      │
│  Raw Table          │
│  (Bronze Layer)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  UC Functions       │
│  • mask_email()     │
│  • mask_name()      │
│  • get_summary()    │
│  • search_letters() │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Governed Views     │
│  (Silver Layer)     │
│  Auto-masked data   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────┐
│  Consumers                      │
│  • SQL Queries                  │
│  • Python Notebooks             │
│  • BI Dashboards                │
│  • AI Agents (future: MCP)      │
└─────────────────────────────────┘
```

---

## 🚀 Demo Flow (15 minutes)

### Act 1: The Problem (3 minutes)

**Objective:** Show why scattered PII logic is dangerous

**Actions:**
1. Show raw `santa_letters` table
2. Highlight PII: names and emails visible
3. Point out: "Can't safely share this with AI or external systems"
4. Show example of inconsistent masking code copy-pasted

**Key Message:** "We need governed, reusable functions for data operations"

---

### Act 2: Create UC Functions (5 minutes)

**Objective:** Build 4 governed functions

**Notebook:** `01_create_uc_functions_mcp.py`

**Flow:**
1. **Function 1:** `mask_email()`
   - Show the code
   - Test it: `mask_email('santa@northpole.com')` → `'s***a@n*********e.com'`
   - Highlight: "One line of code, reusable everywhere"

2. **Function 2:** `mask_name()`
   - Test: `mask_name('Emma')` → `'E**a'`
   - Highlight: "Child privacy protection built-in"

3. **Function 3:** `get_province_summary()`
   - Test: `get_province_summary('Ontario')` → JSON
   - Highlight: "Perfect for AI agent consumption"

4. **Function 4:** `search_letters()`
   - Test: `SELECT * FROM TABLE(search_letters('bicycle'))`
   - Highlight: "Results automatically have masked names"

**Key Message:** "These are now governed assets in Unity Catalog"

---

### Act 3: Functions in Action (5 minutes)

**Objective:** Show reusability and automatic governance

**Notebook:** `02_demo_mcp_functions.py`

**Flow:**
1. **Before/After Comparison**
   ```sql
   -- Before: PII visible
   SELECT name, email, city FROM santa_letters;

   -- After: Automatic masking
   SELECT mask_name(name), mask_email(email), city FROM santa_letters;
   ```

2. **Create Governed View**
   ```sql
   CREATE VIEW santa_letters_masked AS
   SELECT
     mask_name(name) AS child,
     mask_email(email) AS email_masked,
     city,
     letter
   FROM santa_letters;
   ```
   - Query the view → always safe
   - Highlight: "Can't forget to mask - it's built in"

3. **Search with Auto-Masking**
   ```sql
   SELECT * FROM TABLE(search_letters('LEGO'));
   ```
   - Results: All names masked
   - Highlight: "Safe for AI agents to consume"

4. **JSON Aggregation**
   ```sql
   SELECT get_province_summary('British Columbia');
   ```
   - Show JSON output
   - Highlight: "Perfect for API responses and AI queries"

**Key Message:** "Same functions work in SQL, Python, dashboards, and AI agents"

---

### Act 4: Unity Catalog Governance (2 minutes)

**Objective:** Show governance benefits

**Actions:**
1. Open Unity Catalog UI
2. Navigate to functions
3. Show:
   - Function definitions
   - Lineage tracking (if available)
   - Access control options
   - Comments and metadata

**Key Message:** "Every function call is tracked - full auditability and governance"

---

## 🏆 Key Value Props

### For Data Engineers
- ✅ Write once, use everywhere
- ✅ No more copy-paste
- ✅ Easy to test and maintain
- ✅ Version control via Unity Catalog

### For Security/Compliance Teams
- ✅ PII protection by design
- ✅ Can't forget to mask data
- ✅ Full audit trail
- ✅ Consistent across all systems

### For Business Stakeholders
- ✅ Faster time to insights
- ✅ Safe to share with AI
- ✅ Reduces risk of data breaches
- ✅ Enables self-service analytics

### For AI/ML Teams
- ✅ Functions become AI agent tools
- ✅ Governed access patterns
- ✅ Structured outputs (JSON)
- ✅ Safe for production AI

---

## 📊 Technical Details

### Function Types

**1. Scalar Functions**
- Input: Single value
- Output: Single value
- Example: `mask_name(STRING) → STRING`
- Use: Data transformation, masking

**2. Scalar Functions (JSON)**
- Input: Parameters
- Output: JSON string
- Example: `get_summary(STRING) → STRING (JSON)`
- Use: API responses, AI agent consumption

**3. Table-Valued Functions**
- Input: Parameters
- Output: Table/rows
- Example: `search_letters(STRING) → TABLE(...)`
- Use: Complex queries, filtered result sets

---

## 🎨 Design Patterns

### Pattern 1: PII Masking
```sql
CREATE FUNCTION mask_field(input STRING) RETURNS STRING
-- Always masks, never exposes raw PII
-- Reusable across all PII fields
```

### Pattern 2: Aggregation for AI
```sql
CREATE FUNCTION get_summary(dimension STRING) RETURNS STRING
-- Returns JSON for easy parsing
-- Parameterized for flexibility
-- No SQL injection risk
```

### Pattern 3: Safe Search
```sql
CREATE FUNCTION search_table(keyword STRING)
RETURNS TABLE(masked_col STRING, ...)
-- Built-in masking
-- Can't forget to apply
-- Safe for any consumer
```

---

## 🔮 Future Extensions

### Day 6/7: Genie Space Integration

**Vision:** UC Functions become tools for AI agents

**Example Interaction:**
```
User: "How many letters from Ontario?"
Genie: [Calls get_province_summary('Ontario')]
Genie: "Ontario sent 247 letters from 15 cities."
```

**Example with Masking:**
```
User: "Show kids who asked for bicycles"
Genie: [Calls search_letters('bicycle')]
Genie: "Found 12 children: E**a, L**m, O*****r..."
       (Names automatically masked)
```

### Day 8: MCP Server (Model Context Protocol)

Expose UC Functions as MCP tools for:
- Claude Desktop
- ChatGPT
- Custom AI agents

---

## 📈 Success Metrics

**Quantitative:**
- 4 UC Functions created
- 1,000 rows of synthetic data
- 100% PII masking coverage
- 0 hardcoded masking logic in notebooks

**Qualitative:**
- Audience understands UC Functions value
- Clear before/after story
- Governance benefits demonstrated
- AI-readiness shown

---

## 🎯 Call to Action

**For Attendees:**
1. Try the notebooks in your workspace
2. Identify PII in your data
3. Build your first UC masking function
4. Explore Unity Catalog governance features

**For Teams:**
1. Audit existing masking logic
2. Consolidate into UC Functions
3. Create governed views with auto-masking
4. Prepare for AI agent integration

---

## 📚 Supporting Materials

- **Notebooks:** Complete, runnable Databricks notebooks
- **Data:** Synthetic dataset (no real PII)
- **Documentation:** Comprehensive README with examples
- **Demo Script:** Step-by-step guide for presenters

---

## 🎓 Learning Objectives

By the end of this demo, attendees will understand:

1. ✅ **What** Unity Catalog Functions are
2. ✅ **Why** they matter for governance and AI
3. ✅ **How** to create scalar and table-valued functions
4. ✅ **When** to use functions vs views vs tables
5. ✅ **Where** UC Functions fit in the Lakehouse architecture

---

## 🔑 Key Takeaways

| Traditional | UC Functions |
|------------|--------------|
| Copy-paste everywhere | Write once, use everywhere |
| No governance | Full lineage tracking |
| Manual security | Security by design |
| Not AI-ready | Perfect for AI agents |
| Hard to maintain | Update in one place |

---

**🎅 Transform scattered logic into governed, enterprise-grade functions!**

This project demonstrates the future of data operations: reusable, governed, AI-ready functions that power everything from analytics to autonomous agents.

