# 🎄 Day 6/7: Genie Space - North Pole Operations Center

## AI Intelligence Layer Powered by Unity Catalog Functions

Welcome to **Day 6/7** of the **12 Days of Databricks Demos**! This folder contains everything you need to set up an AI-powered **Genie Space** that uses your UC Functions from Day 5 to answer natural language questions about Santa's letters.

---

## 📖 The Vision

### From Manual Analysis → AI-Powered Intelligence

**The Old Way:**
- Elves manually query databases with complex SQL
- Business analysts create static reports
- No self-service for stakeholders
- Insights take days to generate

**The New Way (Genie Space):**
- **Natural language queries:** "Which kids in Toronto asked for gaming consoles?"
- **Automatic function calling:** Genie uses your UC Functions as tools
- **Instant insights:** Answers in seconds, not days
- **Governed AI:** Uses the same business logic as humans

---

## 🎯 What You'll Build

### North Pole Operations Center

An AI assistant that can:

- 🎁 **Gift Trend Analysis:** "What are the top gift categories in Quebec?"
- 📊 **Behavior Insights:** "Show me very nice children with high-priority requests"
- 🚚 **Delivery Planning:** "Which cities need urgent deliveries?"
- 📈 **Supply Forecasting:** "How many gaming consoles do we need?"
- 🗺️ **Geographic Analysis:** "What's the average nice score by province?"

### Powered By

- ✅ **11 UC Functions** from Day 5
- ✅ **Clean Silver Data** with standardized fields
- ✅ **Governed Business Logic** used consistently
- ✅ **AI Agents** that explain their reasoning

---

## 📦 What's in This Folder

| File | Description |
|------|-------------|
| `genie_setup_instructions.md` | Step-by-step guide to configure Genie Space |
| `config/genie_uc_functions_tools.json` | UC Functions configuration for Genie tools |
| `README.md` | This file - overview and use cases |

---

## 🚀 Quick Start

### Step 1: Prerequisites

Ensure you've completed Day 5:

```sql
-- Verify UC Functions exist
SHOW USER FUNCTIONS IN danny_park.day5_uc_functions;

-- Verify Silver table exists
SELECT COUNT(*) FROM danny_park.silver.santa_letters_cleaned;

-- Verify Summary view exists
SELECT * FROM danny_park.silver.santa_letters_summary;
```

### Step 2: Create Genie Space

Follow the detailed instructions in `genie_setup_instructions.md`:

1. Create a new Genie Space named "North Pole Operations Center"
2. Add context tables (cleaned data + summary view)
3. Register all 11 UC Functions as tools
4. Configure instructions and behavior
5. Test with sample queries

### Step 3: Verify It Works

Try these test queries:

```
"How many letters did we receive?"
"What are the top 5 gift categories?"
"Show me high-priority deliveries from very nice children"
```

---

## 🎁 Key Use Cases

### 1. Operations Team: Daily Delivery Planning

**User:** *"Show me all high-priority letters from children in Ontario with nice scores above 70"*

**Genie:**
- Calls `normalize_province('Ontario')`
- Filters `delivery_priority = 1` AND `naughty_nice_score > 70`
- Returns 847 results with child names, cities, and gift requests

**Value:** Immediate actionable delivery list

---

### 2. Supply Chain: Demand Forecasting

**User:** *"What are the top 10 gift categories by demand? Break it down by province."*

**Genie:**
- Calls `gift_category()` for all gifts
- Groups by category and province
- Returns ranked list with counts

**Value:** Data-driven inventory planning

---

### 3. Executive Team: Behavioral Insights

**User:** *"What percentage of children are naughty vs nice? Show trends by region."*

**Genie:**
- Uses `naughty_nice_score()` to categorize
- Aggregates by province
- Calculates percentages

**Value:** Strategic insights for resource allocation

---

### 4. Customer Service: Specific Child Lookup

**User:** *"Find all children named Emma in Vancouver who asked for electronics"*

**Genie:**
- Calls `normalize_city('Vancouver')`
- Calls `gift_category()` to filter Electronics
- Filters by name

**Value:** Quick customer inquiry resolution

---

### 5. Quality Assurance: Data Validation

**User:** *"How many letters have invalid postal codes?"*

**Genie:**
- Calls `is_valid_postal_code()` on all records
- Counts FALSE results

**Value:** Data quality monitoring

---

## 🧠 How Genie Uses UC Functions

### Automatic Function Selection

Genie automatically chooses the right functions based on your question:

| Question Contains... | Genie Calls... |
|---------------------|----------------|
| Location name (Toronto, Quebec) | `normalize_province()` or `normalize_city()` |
| Gift analysis, trends | `gift_category()`, `standardize_gift()` |
| Behavior, naughty, nice | `naughty_nice_score()` |
| Priority, urgent | `delivery_priority_score()` |
| Multiple gifts | `extract_gift_count()` |
| Postal code validation | `is_valid_postal_code()` |

### Transparency

Genie shows you which functions it called:

```
🔧 Functions Used:
- normalize_city('toronto') → 'Toronto'
- gift_category('PlayStation 5') → 'Gaming Consoles'

📊 Query Executed:
SELECT * FROM ... WHERE city_normalized = 'Toronto'
AND gift_category = 'Gaming Consoles'
```

---

## 📊 Sample Queries by Persona

### 🎅 For Santa

```
"Which children sent the most heartfelt letters?"
"Show me special requests that mention medical needs or hardship"
"Who are the nicest kids in each province?"
```

### 🧝 For Elves (Operations)

```
"How many letters need urgent delivery?"
"Which cities have the highest concentration of requests?"
"Show me all gaming console requests sorted by priority"
```

### 📦 For Supply Chain

```
"Generate demand forecast for top 15 gift categories"
"Which gifts are most requested by province?"
"What's the total count of each standardized gift?"
```

### 📈 For Executives

```
"What's the overall average nice score?"
"How many provinces did we receive letters from?"
"Show me year-over-year trends in gift categories"
```

### 🛠️ For Data Quality Team

```
"How many records have missing or invalid cities?"
"Show me letters with unusually high or low nice scores"
"Which postal codes failed validation?"
```

---

## 🎯 Advanced Genie Capabilities

### Multi-Step Reasoning

**User:** *"Find the top gift in each province, but only for children with scores above 80"*

**Genie's Process:**
1. Filters `naughty_nice_score > 80`
2. Calls `normalize_province()` to group
3. Calls `gift_category()` for gifts
4. Ranks by province
5. Returns top result per province

### Follow-Up Questions

**User:** *"What are gaming console trends?"*
**Genie:** *Shows PlayStation 5, Xbox, Nintendo Switch counts*

**User:** *"Now show only high-priority ones"*
**Genie:** *Filters previous results by `delivery_priority = 1`*

### Aggregations & Analytics

**User:** *"Compare average nice scores across the 5 biggest cities"*

**Genie:**
- Identifies top 5 cities by letter count
- Calculates `AVG(naughty_nice_score)` per city
- Returns comparison table

---

## 🔧 Configuration Details

### Context Tables

1. **Primary Data:** `danny_park.silver.santa_letters_cleaned`
   - All cleaned letters with enriched fields
   - Used for detailed queries

2. **Summary Stats:** `danny_park.silver.santa_letters_summary`
   - Aggregated metrics
   - Used for high-level questions

### UC Functions as Tools

All 11 functions from Day 5 are available:

**Text Standardization:**
- `clean_text()`
- `normalize_province()`
- `normalize_city()`
- `standardize_gift()`

**Business Logic:**
- `gift_category()`
- `naughty_nice_score()`
- `delivery_priority_score()`

**Utilities:**
- `extract_gift_count()`
- `extract_first_gift()`
- `is_valid_postal_code()`
- `age_category()`

### Instructions & Behavior

Genie is configured with:
- Business context about the North Pole operations
- Scoring guides (naughty/nice, priority levels)
- When to use each function
- Output formatting preferences

See `genie_setup_instructions.md` for full configuration details.

---

## 🏆 Benefits of UC Functions + Genie

### 1. Consistent Business Logic

**Same functions used by:**
- SQL queries
- Python notebooks
- Dashboards
- **AI agents (Genie)**

**Result:** Everyone gets the same answer

### 2. Governed & Auditable

**Unity Catalog tracking:**
- Who called which function
- When and from where
- Function versioning
- Access controls

### 3. Self-Service Analytics

**Stakeholders can:**
- Ask questions in plain English
- Get instant answers
- No SQL knowledge required
- Trust the results (governed logic)

### 4. Explainable AI

**Genie shows:**
- Which functions it called
- What SQL it executed
- Why it chose that approach

**Result:** Trust and transparency

---

## 🔜 Next Steps

### After Setting Up Genie Space

1. **Share with stakeholders**
   - Invite Santa's operations team
   - Train elves on how to ask questions
   - Create a query library

2. **Monitor usage**
   - Track most common questions
   - Identify gaps in functionality
   - Refine instructions

3. **Extend capabilities**
   - Add more UC Functions (e.g., sentiment analysis)
   - Connect external data (weather, traffic)
   - Build AI agents for automated actions

4. **Integrate with workflows**
   - Embed Genie in dashboards
   - Create scheduled reports
   - Set up alerts for anomalies

---

## 📚 Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                  GENIE SPACE                        │
│         North Pole Operations Center                │
└─────────────────────────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
┌───────────────┐              ┌───────────────┐
│ CONTEXT TABLES│              │  UC FUNCTIONS │
│               │              │   (TOOLS)     │
│ • Letters     │              │               │
│   (Cleaned)   │              │ • normalize_* │
│ • Summary     │              │ • clean_text  │
│   Stats       │              │ • gift_*      │
└───────────────┘              │ • scoring     │
                               └───────────────┘
                                       │
                               ┌───────┴──────────┐
                               ▼                  ▼
                        ┌─────────────┐   ┌─────────────┐
                        │   BRONZE    │   │   SILVER    │
                        │ Raw Letters │→→→│  Cleaned    │
                        └─────────────┘   └─────────────┘
```

---

## 🤝 Troubleshooting

See `genie_setup_instructions.md` for detailed troubleshooting steps.

**Common issues:**
- Functions not being called → Check permissions
- Incorrect results → Verify function logic
- Can't find table → Check Unity Catalog access

---

## 📖 Resources

- [Genie Space Documentation](https://docs.databricks.com/en/genie/index.html)
- [UC Functions as AI Tools](https://docs.databricks.com/en/genie/use-tools.html)
- [Best Practices for Natural Language Queries](https://docs.databricks.com/en/genie/best-practices.html)
- [Day 5: UC Functions Documentation](../05-unity-catalog-functions/README.md)

---

## 📝 License

MIT License - see repository root for details

---

**🎅 Welcome to the Future of Santa's Operations!**

Your AI-powered North Pole Operations Center is ready to revolutionize how Santa's team analyzes letters, plans deliveries, and spreads holiday joy! 🎄✨

Built with ❤️ on the Databricks Lakehouse Platform
