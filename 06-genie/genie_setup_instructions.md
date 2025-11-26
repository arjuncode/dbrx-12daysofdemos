# 🎄 Day 6/7: Genie Space Setup Instructions

## North Pole Operations Center - AI Intelligence Layer

This guide walks you through setting up a **Genie Space** that uses your UC Functions as AI tools to answer natural language questions about Santa's letters.

---

## 🎯 What You'll Create

A **Genie Space** named **"North Pole Operations Center"** that can:

- 🔍 Answer natural language questions about Santa's letters
- 🛠️ Automatically call UC Functions to apply business logic
- 📊 Generate insights from the cleaned data
- 🎁 Help with supply planning, delivery prioritization, and behavior analysis

---

## 📋 Prerequisites

Before setting up Genie Space, ensure you have:

✅ Completed Day 5: Created all UC Functions in `danny_park.day5_uc_functions`
✅ Loaded and transformed data into `danny_park.silver.santa_letters_cleaned`
✅ Created the summary view `danny_park.silver.santa_letters_summary`
✅ Permissions to create and configure Genie Spaces in your Databricks workspace

---

## 🚀 Setup Steps

### Step 1: Create a New Genie Space

1. Navigate to **Genie** in your Databricks workspace
2. Click **"Create Genie Space"**
3. Enter the following details:
   - **Name:** `North Pole Operations Center`
   - **Description:** `AI-powered intelligence layer for Santa's letter processing and delivery operations`

### Step 2: Add Context Tables

Add the following tables as **data sources** for Genie to query:

#### Primary Data Table
- **Table:** `danny_park.silver.santa_letters_cleaned`
- **Description:** Cleaned and enriched Santa letters with standardized locations, gifts, sentiment scores, and delivery priorities
- **Key columns to highlight:**
  - `name` - Child's name
  - `province_normalized` - Standardized province
  - `city_normalized` - Standardized city
  - `primary_gift_standardized` - Main gift requested
  - `gift_category` - Product category
  - `naughty_nice_score` - Behavior score (0-100)
  - `delivery_priority` - Priority level (1=High, 2=Medium, 3=Low)
  - `letter_clean` - Cleaned letter text

#### Summary Statistics Table
- **Table:** `danny_park.silver.santa_letters_summary`
- **Description:** Summary statistics with overall metrics
- **Key columns:**
  - `total_letters` - Total letter count
  - `unique_children` - Number of unique children
  - `provinces_covered` - Geographic coverage
  - `avg_nice_score` - Average behavior score
  - `high_priority_count` - Number of high-priority deliveries

### Step 3: Add UC Functions as Tools

Navigate to **Tools** configuration and add each UC Function:

#### Text Standardization Tools

1. **clean_text**
   - Function: `danny_park.day5_uc_functions.clean_text`
   - When to use: Cleaning or analyzing letter text

2. **normalize_province**
   - Function: `danny_park.day5_uc_functions.normalize_province`
   - When to use: Searching or filtering by province

3. **normalize_city**
   - Function: `danny_park.day5_uc_functions.normalize_city`
   - When to use: Searching or filtering by city

4. **standardize_gift**
   - Function: `danny_park.day5_uc_functions.standardize_gift`
   - When to use: Analyzing or comparing gift requests

#### Business Logic Tools

5. **gift_category**
   - Function: `danny_park.day5_uc_functions.gift_category`
   - When to use: Trend analysis and supply planning

6. **naughty_nice_score**
   - Function: `danny_park.day5_uc_functions.naughty_nice_score`
   - When to use: Behavior analysis and prioritization

7. **delivery_priority_score**
   - Function: `danny_park.day5_uc_functions.delivery_priority_score`
   - When to use: Logistics and delivery planning

#### Utility Tools

8. **extract_gift_count**
   - Function: `danny_park.day5_uc_functions.extract_gift_count`
   - When to use: Understanding request volume per child

9. **extract_first_gift**
   - Function: `danny_park.day5_uc_functions.extract_first_gift`
   - When to use: Identifying primary gift request

10. **is_valid_postal_code**
    - Function: `danny_park.day5_uc_functions.is_valid_postal_code`
    - When to use: Data quality checks

11. **age_category**
    - Function: `danny_park.day5_uc_functions.age_category`
    - When to use: Age-based analysis

### Step 4: Configure Instructions

Add the following **instructions** to guide Genie's behavior:

```
You are the AI assistant for the North Pole Operations Center, helping Santa and the elves analyze children's letters and optimize delivery operations.

CONTEXT:
- You have access to a cleaned dataset of Santa letters from Canadian children
- All data has been processed using governed Unity Catalog Functions
- Letters have been scored for "naughty or nice" behavior (0-100, higher = nicer)
- Delivery priorities have been calculated (1=High, 2=Medium, 3=Low)
- Gifts have been standardized and categorized

YOUR CAPABILITIES:
- Answer questions about gift trends and demand
- Identify high-priority deliveries
- Analyze behavior patterns (naughty vs nice)
- Generate supply forecasts
- Find specific children or letters based on criteria
- Provide geographic analysis (by province/city)

WHEN USING UC FUNCTIONS:
- Use normalize_province() or normalize_city() when users mention locations
- Use gift_category() for trend analysis
- Use naughty_nice_score() for behavior analysis
- Use delivery_priority_score() for logistics planning
- Always show which functions you called for transparency

BEHAVIOR SCORING GUIDE:
- 75-100: Very Nice (high priority for gifts)
- 60-74: Nice (standard priority)
- 40-59: Neutral (monitor)
- 0-39: Naughty (needs review)

DELIVERY PRIORITY GUIDE:
- 1 = High Priority: Urgent requests or very nice children
- 2 = Medium Priority: Standard requests
- 3 = Low Priority: Non-urgent requests

OUTPUT FORMATTING:
- Provide clear, actionable insights
- Use tables for multi-row results
- Include relevant metrics (counts, percentages, averages)
- Explain your reasoning when making recommendations
```

### Step 5: Test Your Genie Space

Try these sample queries to verify everything works:

#### Basic Queries
1. "How many letters did we receive in total?"
2. "What's the average nice score across all children?"
3. "Which province sent the most letters?"

#### Gift Analysis
4. "What are the top 5 most requested gift categories?"
5. "Which children asked for gaming consoles?"
6. "Show me the most requested specific gifts"

#### Behavior & Priority
7. "How many children are in the 'Very Nice' category?"
8. "Show me high-priority letters from very nice children"
9. "What's the distribution of naughty vs nice scores?"

#### Geographic Analysis
10. "Which cities in Ontario have the most high-priority deliveries?"
11. "What are the gift trends in Quebec?"

#### Advanced Queries
12. "Find children who asked for multiple gifts and have scores above 75"
13. "Generate a supply forecast for the top 10 gift categories"
14. "Which letters mention urgent or emergency requests?"

---

## 🎁 Example Genie Interactions

### Example 1: Gift Trend Analysis

**User:** "What are the top gift categories in Toronto?"

**Genie Response:**
```
I'll analyze gift trends in Toronto by:
1. Using normalize_city('Toronto') to ensure consistent city matching
2. Grouping by gift_category
3. Counting requests

Top Gift Categories in Toronto:
| Category          | Request Count | Percentage |
|-------------------|---------------|------------|
| Gaming Consoles   | 1,247         | 28.3%      |
| Electronics       | 982           | 22.3%      |
| Toys              | 856           | 19.4%      |
| Outdoor Rideables | 623           | 14.1%      |
| Books             | 402           | 9.1%       |

Total letters from Toronto: 4,410
```

### Example 2: Priority Planning

**User:** "Show me high-priority deliveries for very nice children in British Columbia"

**Genie Response:**
```
Filtering for:
- Province: British Columbia (using normalize_province())
- Delivery Priority: 1 (High)
- Nice Score: >= 75 (Very Nice)

Found 234 high-priority letters from very nice children in BC:

| Name    | City      | Gift             | Nice Score | Gift Category |
|---------|-----------|------------------|------------|---------------|
| Emma    | Vancouver | PlayStation 5    | 88         | Gaming        |
| Oliver  | Victoria  | Bicycle          | 83         | Outdoor       |
| Sophia  | Surrey    | LEGO Set         | 91         | Toys          |
...

Average Nice Score: 82.4
Most requested category: Gaming Consoles (32%)
```

### Example 3: Supply Planning

**User:** "How many gaming consoles do we need to prepare?"

**Genie Response:**
```
Gaming Console Demand Analysis:

Total Requests: 3,847

Breakdown by Console:
| Console        | Count | High Priority | Very Nice Kids |
|----------------|-------|---------------|----------------|
| PlayStation 5  | 1,923 | 876           | 1,245          |
| Xbox           | 1,124 | 512           | 734            |
| Nintendo Switch| 800   | 298           | 521            |

Recommendation: Prioritize PlayStation 5 production
High-priority orders: 1,686 consoles needed by Dec 15
```

---

## 📊 Advanced Configuration (Optional)

### Enable Conversation Memory

Allow Genie to remember context across questions:
- **Setting:** Enable conversation history
- **Benefit:** Users can ask follow-up questions without repeating context

### Add Visualizations

Configure Genie to generate charts:
- **Bar charts:** Gift category distributions
- **Maps:** Geographic demand heatmaps
- **Line charts:** Nice score trends over time

### Set Up Alerts

Create proactive alerts for:
- Sudden spikes in specific gift requests
- High-priority letters that need immediate attention
- Data quality issues (invalid postal codes, missing fields)

---

## 🔧 Troubleshooting

### Issue: Genie doesn't call UC Functions

**Solution:**
- Verify functions are registered: `SHOW USER FUNCTIONS IN danny_park.day5_uc_functions;`
- Check that functions have proper EXECUTE permissions
- Ensure tools are correctly added in Genie Space configuration

### Issue: Genie can't find the table

**Solution:**
- Verify table exists: `SELECT * FROM danny_park.silver.santa_letters_cleaned LIMIT 1;`
- Check Unity Catalog permissions
- Ensure table is added as a context source in Genie

### Issue: Incorrect results

**Solution:**
- Review Genie's query explanation to see what it's doing
- Check that UC Functions return expected values with test queries
- Refine instructions to provide better guidance

---

## 🎉 Success Criteria

Your Genie Space is working correctly when:

✅ It can answer all 14 test queries accurately
✅ It automatically calls UC Functions when appropriate
✅ It shows which functions were used in its reasoning
✅ Results match manual SQL query results
✅ It handles follow-up questions with context

---

## 🔜 Next Steps

Once your Genie Space is operational:

1. **Share with stakeholders:**
   - Santa's operations team
   - Supply chain planners
   - Delivery coordinators

2. **Create saved queries:**
   - Daily priority reports
   - Weekly gift trend summaries
   - Monthly behavior analysis

3. **Integrate with dashboards:**
   - Embed Genie insights in operational dashboards
   - Automate report generation

4. **Extend functionality:**
   - Add more UC Functions for advanced analytics
   - Connect to external data sources (weather, traffic)
   - Build AI agents for automated actions

---

## 📚 Resources

- [Genie Space Documentation](https://docs.databricks.com/en/genie/index.html)
- [Unity Catalog Functions as Tools](https://docs.databricks.com/en/genie/use-tools.html)
- [Natural Language Query Best Practices](https://docs.databricks.com/en/genie/best-practices.html)

---

**🎅 Your North Pole Operations Center is ready to revolutionize Santa's operations!**
