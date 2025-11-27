# 12 Days of Demos
The Databricks for Startups team is excited to tell the story of how the North Pole Modernization Office (NPMO) migrates from spreadsheets, scattered mall-store data, and handwritten Santa letters into a fully automated, AI-driven Lakehouse running on Databricks.

# North Pole Modernization Office - Datasets

## Generated Datasets

1. **gift_requests.csv** - Children's letters with NLP-ready text and gift extraction
2. **reindeer_telemetry.csv** - IoT sensor data from training flights  
3. **workshop_production.csv** - Toy manufacturing quality metrics
4. **behavioral_analytics.csv** - Naughty/Nice scoring events
5. **delivery_optimization.csv** - Route planning and logistics data

## Setup & Execution

To get started with the North Pole Modernization Office Managed MCP demo, you will need to run the provided notebooks in your Databricks environment.

### Prerequisites
1. **Serverless Compute**: Ensure you are connected to a Serverless SQL Warehouse or a cluster with Unity Catalog enabled.
2. **Configuration**: Open each notebook and update the `catalog_name` and `schema_name` variables in the first code cell to match your Databricks environment (e.g., `main.default` or your custom catalog).

### Notebooks

*   **01-mcp-init.ipynb**: This notebook handles the initialization of the demo environment. It ingests the synthetic CSV datasets and creates the necessary Delta tables in your specified catalog and schema.
*   **02-mcp-functions.ipynb**: This notebook defines a suite of Unity Catalog SQL functions. These functions encapsulate business logic for the NPMO, enabling AI agents to easily query data about gift requests, reindeer telemetry, and workshop production.

You can simply click **"Run All"** in each notebook to execute the full workflow, or step through cell-by-cell to understand the logic.
