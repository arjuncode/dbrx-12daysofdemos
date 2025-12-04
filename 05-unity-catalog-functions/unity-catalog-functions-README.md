# 🎅 Welcome to the North Pole Data Governance Office
## Unity Catalog Functions: Secure, Reusable Tools for Santa's Workshop

*Part of the [12 Days of Demos](https://medium.com/@arjun.gheewala-databricks/3bf81e73524a) series*

---

### 📬 The Challenge
Santa receives **millions of letters** containing sensitive information - children's names, locations, and personal details. The old system had no way to protect this data when sharing with dashboards, AI agents, or external systems!

### ✨ The Solution: Unity Catalog Functions
The North Pole Modernization Office (NPMO) has deployed **Unity Catalog Functions** to automatically:
* 🎭 **`mask_name()`** - Anonymize personal names (Emma → E**a)
* 🗺️ **`get_province_summary()`** - Return governed aggregate stats as JSON
* 🔍 **`search_letters()`** - Safe keyword search with automatic PII masking
* 👁️ **`santa_letters_masked`** - Governed view with all PII automatically protected

### 🎓 What You'll Learn
This notebook shows you how to create **Unity Catalog Functions**, powerful reusable tools that enforce data governance at the query layer. No application code changes needed!

**Key concepts covered:**
- Creating scalar functions for PII masking
- Building aggregate functions that return structured JSON
- Creating table-valued functions for safe search
- Combining functions into governed views

### 🚀 Getting Started

1. **Run the init notebook** - Execute `00-init/load-data.ipynb` to load the source data
2. **Update the configuration** - Set your catalog and schema in the first code cell
3. **Run all cells** - Create functions and test them in action

**No prior Databricks experience needed!** Just follow along as we help Santa protect children's privacy.

### 💡 Real-World Applications
The same patterns work for:
- **GDPR Compliance** - Mask PII before sharing with analytics tools
- **AI Agent Safety** - Provide governed tools instead of raw table access
- **Self-Service Analytics** - Let users query without exposing sensitive data
- **Data Sharing** - Share insights without sharing identities

### 📚 Resources
- [Unity Catalog Functions Documentation](https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-ddl-create-sql-function.html)
- [12 Days of Demos Series](https://medium.com/@arjun.gheewala-databricks/3bf81e73524a)

---

*Powered by the Databricks Data Intelligence Platform* 🚀

**Happy Holidays and Happy Learning!** 🎄
