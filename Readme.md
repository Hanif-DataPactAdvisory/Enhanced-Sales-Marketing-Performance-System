# Enhanced Sales & Marketing Performance System

This portfolio project demonstrates a complete, automated data pipeline built in Python. It simulates a real-world business process by ingesting, cleaning, and reconciling data from four separate business systems (CRM, Finance, Marketing, Ad Platforms) to generate high-value, actionable reports on sales commissions, marketing ROI, and lead quality.

This script is the "engine" for a high-value service, replacing thousands of hours of manual, error-prone spreadsheet work.

---

## 🚀 The Business Problem ("Papercut Pains")

This project directly solves several acute, high-frustration "papercut pains" for businesses:

* **The Manual Report Factory :** Marketing and sales teams struggle to connect disparate data. This script automates the generation of complex performance reports, saving hours of manual data pulling.
* **The Spreadsheet Maze :** Calculating commissions is often a "VLOOKUP hell" of complex, brittle spreadsheets. This script replaces that with robust, maintainable Python logic.
* **The Data Janitor :** Data is never clean. This project performs essential data cleaning and reconciliation, like extracting Opportunity IDs from messy finance descriptions.
* **The CRM Sinkhole  / Ad Spend Waste :** It's hard to prove value. This script links ad spend to actual CRM deals and calculates true ROAS, demonstrating mastery of sales/marketing data.
* **Bookkeeping Black Hole :** It applies complex financial rules (commissions, tiers, clawbacks) automatically, reducing errors and saving time.

## 🛠️ The Solution: An Automated Analysis Engine

This Python script ingests four mock CSV files:
1.  **`crm_closed_deals.csv`** (Simulating a Salesforce export)
2.  **`finance_payments.csv`** (Simulating a Stripe/QuickBooks export)
3.  **`marketing_touches.csv`** (Simulating a HubSpot/Marketo export)
4.  **`ad_spend.csv`** (Simulating a Google/Facebook Ads export)

It then automatically performs:
* **Data Cleaning:** Converts data types, handles missing values, and standardizes data.
* **Financial Reconciliation:** Intelligently merges finance payments with CRM deals using extracted IDs.
* **Commission Calculation:** Applies complex, multi-tiered commission rules, including product modifiers and refund clawbacks.
* **Marketing ROI Analysis:** Attributes ad spend to closed deals to calculate real-time ROAS and CPA.
* **Lead Scoring:** Implements a rule-based engine to score leads based on high-intent marketing actions.

---

## 🖥️ The "Before & After" (The Final Reports)

The script transforms raw, disconnected data into three powerful, clean reports:

### 1. Final Commission Report

(This report calculates final pay for each rep, per quarter, after applying all business logic.)

**[PASTE YOUR `Final Commission Report` CONSOLE OUTPUT HERE, FORMATTED AS A MARKDOWN TABLE]**
*Example (paste your real output):*
| OwnerName | PaymentDate | TotalPaid | TotalBaseCommission | ... | FinalCommission |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Cody Montgomery | 2025-09-30 | 34010.77 | 1952.63 | ... | 1952.63 |
| Cody Montgomery | 2025-12-31 | 58746.87 | 2822.54 | ... | 2910.01 |
| ... | ... | ... | ... | ... | ... |

### 2. Marketing ROI Report

(This report identifies which ad campaigns are profitable and which are wasting money.)

**[PASTE YOUR `Marketing ROI Report` CONSOLE OUTPUT HERE, FORMATTED AS A MARKDOWN TABLE]**
*Example (paste your real output):*
| CampaignName | TotalSpend | ... | TotalRevenue | ROAS | AvgCPA |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Google Search - Core Keywords | 6777.97 | ... | 108809.83 | 16.05 | 847.25 |
| LinkedIn Ads - Prospecting | 5213.51 | ... | 195630.25 | 37.52 | 347.57 |
| Facebook - Lookalike Audience | 5426.52 | ... | 0.00 | 0.00 | 0.00 |
| ... | ... | ... | ... | ... | ... |

### 3. Top Lead Scores

(This report ranks leads by engagement, identifying the hottest prospects for the sales team.)

**[PASTE YOUR `Top Lead Scores` CONSOLE OUTPUT HERE, FORMATTED AS A MARKDOWN TABLE]**
*Example (paste your real output):*
| ContactEmail | LeadScore |
| :--- | :--- |
| lisa43@example.com | 100 |
| michael58@example.net | 100 |
| ... | ... |

---

## 🛠️ Tech Stack & Setup

* **Python 3**
* **Pandas:** For core data manipulation and analysis.
* **Faker:** Used by `generate_data.py` to create mock data.
* **Matplotlib / Seaborn:** For generating report visualizations.

## 🚀 How to Run

1.  Ensure you have Python 3 installed.
2.  Install required libraries:
    ```sh
    pip install pandas faker matplotlib seaborn
    ```
3.  Run the mock data generator (only needs to be run once):
    ```sh
    python generate_data.py
    ```
4.  Run the main analysis script:
    ```sh
    python commission_analyzer.py
    ```
5.  Check the `reports/` folder for the saved CSV and PNG (chart) files.