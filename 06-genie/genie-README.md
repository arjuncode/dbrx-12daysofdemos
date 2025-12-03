# 🧞 Welcome to the North Pole Operations Center
## AI/BI Genie: Natural Language Analytics for Santa's Workshop

*Part of the [12 Days of Demos](https://medium.com/@arjun.gheewala-databricks/3bf81e73524a) series*

---

### 📬 The Challenge
The elves on the operations floor had questions during the holiday rush:
- "How many letters came from Ontario?"
- "What are the most requested gifts in Quebec?"
- "Show me letters mentioning bicycles"

These elves were experts at toy logistics, not SQL. They needed answers quickly without filing a ticket or waiting for an analyst.

### ✨ The Solution: AI/BI Genie + Governed Views
AI/BI Genie is Databricks' natural language interface for querying data. Business users ask questions in plain English, and Genie translates them into SQL, executes the query, and returns results.

**The key insight:** Genie is only as safe as the data you give it access to.
- Point Genie at a raw table with PII → it returns PII
- Point Genie at governed views → it respects those guardrails automatically

That's why Day 05 matters. The UC Functions and governed views we built become the safety layer for natural language analytics.

### 🎓 What You'll Learn
This demo shows you how to configure **AI/BI Genie** to provide self-service analytics while maintaining data governance. No code required!

**Key concepts covered:**
- Creating a Genie Space in the Databricks UI
- Connecting Genie to governed views (not raw tables)
- Writing context instructions for better responses
- Testing governance with edge case questions

### 🚀 Getting Started

#### Prerequisites
1. Complete **Day 05** - Create UC Functions and the `santa_letters_masked` view
2. Access to create Genie Spaces in your workspace

#### Step 1: Create a New Genie Space
1. In your Databricks workspace, click **Genie** in the left sidebar
2. Click **New** in the top right corner
3. Enter name: `North Pole Letter Analytics`
4. Add description: `Natural language interface for querying Santa's letter data with automatic PII protection`

#### Step 2: Add the Governed View
1. Under **Tables**, click **Add tables**
2. Navigate to `main.dbrx_12daysofdemos`
3. Select `santa_letters_masked` (the governed view, NOT the raw table)

#### Step 3: Add Context Instructions
Under **General instructions**, add:

```
This dataset contains letters from children to Santa across Canada.

Available columns:
- child_name: Masked child name (e.g., "E**a")
- city: City where the child lives
- province: Canadian province
- letter: Full text of the letter to Santa
- gifts: Comma-separated list of requested gifts

Important context:
- Child privacy is already protected - names are pre-masked
- Letters are from the 2024 holiday season
- Gifts may contain multiple items separated by commas
```

#### Step 4: Save and Test
Click **Save**. Your Genie Space is ready!

### 🧪 Test Questions to Try

| Question | What It Tests |
|----------|---------------|
| "How many letters came from each province?" | Basic aggregation |
| "Show me letters that mention LEGO" | Keyword search with masked results |
| "What are the top 10 most requested gifts?" | Gift analysis |
| "Show me the real names of children in Toronto" | Governance test (should fail gracefully) |

### 💡 Why This Architecture Works

| Layer | Responsibility |
|-------|----------------|
| **Day 05 (UC Functions)** | Define how data should be masked and accessed |
| **Day 06 (Genie)** | Provide natural language interface on governed data |

**Benefits:**
- Business users get self-service analytics
- Data teams maintain governance in one place
- Security cannot be bypassed by clever prompts
- Same governed views work for Genie, dashboards, and notebooks

### ✅ Best Practices

**Do:**
- Use governed views as Genie data sources
- Test edge cases before sharing with users
- Provide clear context instructions
- Start with a narrow scope, expand later

**Don't:**
- Point Genie at raw tables containing PII
- Rely on instructions alone for governance
- Share Genie Spaces without testing
- Assume Genie will refuse to show sensitive data

### 📚 Resources
- [AI/BI Genie Documentation](https://docs.databricks.com/en/genie/index.html)
- [Genie Best Practices](https://docs.databricks.com/en/genie/best-practices.html)
- [12 Days of Demos Series](https://medium.com/@arjun.gheewala-databricks/3bf81e73524a)

---

*Powered by the Databricks Data Intelligence Platform* 🚀

**Happy Holidays and Happy Learning!** 🎄
