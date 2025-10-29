# Enhanced Sales & Marketing Performance System

This portfolio project demonstrates a complete, automated data pipeline built in Python. It simulates a real-world business process by ingesting, cleaning, and reconciling data from four separate business systems (CRM, Finance, Marketing, Ad Platforms) to generate high-value, actionable reports on sales commissions, marketing ROI, and lead quality.

This script is the "engine" for a high-value service, replacing thousands of hours of manual, error-prone spreadsheet work.

---

## 🚀 The Business Problem ("Papercut Pains")

This project directly solves several acute, high-frustration "papercut pains" for businesses:

* **The Manual Report Factory:** Marketing and sales teams struggle to connect disparate data. This script automates the generation of complex performance reports, saving hours of manual data pulling.
* **The Spreadsheet Maze:** Calculating commissions is often a "VLOOKUP hell" of complex, brittle spreadsheets. This script replaces that with robust, maintainable Python logic.
* **The Data Janitor:** Data is never clean. This project performs essential data cleaning and reconciliation, like extracting Opportunity IDs from messy finance descriptions.
* **The CRM Sinkhole:** This script demonstrates mastery of CRM data structures, using deal and owner information as the central hub for all business logic.
* **Ad Spend Waste:** It's hard to prove value. This script links ad spend directly to actual revenue, calculating true ROAS, and identifying which campaigns are profitable.
* **Bookkeeping Black Hole:** It applies complex financial rules (commissions, tiers, clawbacks) automatically, reducing errors and saving time.

---

## 🛠️ The Solution: An Automated Analysis Engine

This Python script ingests four mock CSV files:
1.  `crm_closed_deals.csv` (Simulating a Salesforce export)
2.  `finance_payments.csv` (Simulating a Stripe/QuickBooks export)
3.  `marketing_touches.csv` (Simulating a HubSpot/Marketo export)
4.  `ad_spend.csv` (Simulating a Google/Facebook Ads export)

It then automatically performs:
* **Data Cleaning:** Converts data types, handles missing values, and standardizes data.
* **Financial Reconciliation:** Intelligently merges finance payments with CRM deals using extracted IDs.
* **Commission Calculation:** Applies complex, multi-tiered commission rules, including product modifiers and refund clawbacks.
* **Marketing ROI Analysis:** Attributes ad spend to closed deals to calculate real-time ROAS and CPA.
* **Lead Scoring:** Implements a rule-based engine to score leads based on high-intent marketing actions.

---

## 🖥️ The "Before & After" (The Final Deliverables)

The script transforms raw, disconnected data into three powerful, clean deliverables:

### 1. Sales Commission & Financial Report

The Final Commission Report (data) and a visual breakdown by sales representative.

| **Visual Summary** | **Full Data Output** |
| :--- | :--- |
| **![](/reports/commission_by_rep.png)** | [Download Commission Data (.csv)](/reports/final_commission_report.csv) |

### 2. Marketing ROI Report

The ROI Report (data) and a visual breakdown of campaign profitability.

| **Visual Summary** | **Full Data Output** |
| :--- | :--- |
| **![](/reports/roas_by_campaign.png)** | [Download ROI Data (.csv)](/reports/marketing_roi_report.csv) |

### 3. Lead Scoring Report

This ranks leads by engagement, identifying the hottest prospects for immediate follow-up.

* **Full Data Output:** [Download Lead Scores (.csv)](/reports/top_lead_scores.csv)

---

## 🛠️ Tech Stack & Setup

* **Python 3**
* **Pandas:** For core data manipulation and analysis.
* **Faker:** Used by `generate_data.py` to create mock data.
* **Matplotlib / Seaborn:** For generating report visualizations.
* **Setup:** The full list of required libraries is available in [requirements.txt](/requirements.txt).

## 🚀 How to Run

1.  Ensure you have Python 3 installed.
2.  Install required libraries:
    ```sh
    pip install -r requirements.txt
    ```
3.  Run the mock data generator (only needs to be run once):
    ```sh
    python generate_data.py
    ```
4.  Run the main analysis script:
    ```sh
    python commission_analyzer.py
    ```
5.  The final reports and charts are saved to the local `reports/` folder.