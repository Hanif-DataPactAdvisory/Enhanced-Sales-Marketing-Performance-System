import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

# Define the file paths (assuming they are in the same directory as the script)
crm_file = 'crm_closed_deals.csv'
finance_file = 'finance_payments.csv'
marketing_file = 'marketing_touches.csv'
ad_spend_file = 'ad_spend.csv'

print("--- Loading Data ---")

# --- Load CRM Data ---
try:
    crm_df = pd.read_csv(crm_file)
    print(f"\nSuccessfully loaded {crm_file} ({len(crm_df)} rows)")
    print("CRM Data Head:")
    print(crm_df.head())
    print("\nCRM Data Info:")
    crm_df.info()
except FileNotFoundError:
    print(f"Error: {crm_file} not found. Make sure it's in the same directory.")
except Exception as e:
    print(f"Error loading {crm_file}: {e}")

# --- Load Finance Data ---
try:
    finance_df = pd.read_csv(finance_file)
    print(f"\nSuccessfully loaded {finance_file} ({len(finance_df)} rows)")
    print("Finance Data Head:")
    print(finance_df.head())
    print("\nFinance Data Info:")
    finance_df.info()
except FileNotFoundError:
    print(f"Error: {finance_file} not found. Make sure it's in the same directory.")
except Exception as e:
    print(f"Error loading {finance_file}: {e}")

# --- Load Marketing Data ---
try:
    marketing_df = pd.read_csv(marketing_file)
    print(f"\nSuccessfully loaded {marketing_file} ({len(marketing_df)} rows)")
    print("Marketing Data Head:")
    print(marketing_df.head())
    print("\nMarketing Data Info:")
    marketing_df.info()
except FileNotFoundError:
    print(f"Error: {marketing_file} not found. Make sure it's in the same directory.")
except Exception as e:
    print(f"Error loading {marketing_file}: {e}")

# --- Load Ad Spend Data ---
try:
    ad_spend_df = pd.read_csv(ad_spend_file)
    print(f"\nSuccessfully loaded {ad_spend_file} ({len(ad_spend_df)} rows)")
    print("Ad Spend Data Head:")
    print(ad_spend_df.head())
    print("\nAd Spend Data Info:")
    ad_spend_df.info()
except FileNotFoundError:
    print(f"Error: {ad_spend_file} not found. Make sure it's in the same directory.")
except Exception as e:
    print(f"Error loading {ad_spend_file}: {e}")

print("\n--- Data Loading Complete ---")

# Next steps will go here: Cleaning, Reconciling, etc.
# --- Data Cleaning & Preparation ---
print("\n--- Cleaning and Preparing Data ---")

# Convert Date Columns
print("Converting date columns...")
try:
    crm_df['CloseDate'] = pd.to_datetime(crm_df['CloseDate'])
    finance_df['PaymentDate'] = pd.to_datetime(finance_df['PaymentDate'])
    # errors='coerce' will turn invalid date formats into NaT (Not a Time)
    marketing_df['TouchpointDate'] = pd.to_datetime(marketing_df['TouchpointDate'], errors='coerce')
    ad_spend_df['Date'] = pd.to_datetime(ad_spend_df['Date'])
    print("Date columns converted.")
except Exception as e:
    print(f"Error converting date columns: {e}")

# Ensure Numeric Types (read_csv usually handles this well, but explicit check is good)
print("Ensuring numeric types...")
numeric_cols_crm = ['Amount']
numeric_cols_finance = ['Amount']
numeric_cols_ad = ['Spend', 'Impressions', 'Clicks']

for col in numeric_cols_crm:
    crm_df[col] = pd.to_numeric(crm_df[col], errors='coerce')
for col in numeric_cols_finance:
    finance_df[col] = pd.to_numeric(finance_df[col], errors='coerce')
for col in numeric_cols_ad:
    ad_spend_df[col] = pd.to_numeric(ad_spend_df[col], errors='coerce')
print("Numeric types ensured.")


# Handle Missing Values (Example: Fill missing AssociatedOpportunityID with a placeholder)
print("Handling missing values...")
if 'AssociatedOpportunityID' in marketing_df.columns:
    marketing_df['AssociatedOpportunityID'].fillna('MISSING', inplace=True)
    print("Filled missing AssociatedOpportunityID in marketing data.")
# Drop rows where essential numeric data might be missing after coercion
crm_df.dropna(subset=numeric_cols_crm, inplace=True)
finance_df.dropna(subset=numeric_cols_finance, inplace=True)
ad_spend_df.dropna(subset=numeric_cols_ad, inplace=True)
print("Dropped rows with missing essential numeric values.")


# --- Prepare Finance Data for Reconciliation ---
# Attempt to extract OpportunityID from the Description field
print("Extracting potential Opportunity IDs from finance descriptions...")
# Regex to find Salesforce-like IDs (006 followed by alphanumerics)
opp_id_pattern = r'(006[a-zA-Z0-9]{12,15})' # Pattern for 15 or 18 char IDs starting with 006

# Create a new column 'ExtractedOppID'
# .str.extract finds the first match of the pattern in the 'Description' column
finance_df['ExtractedOppID'] = finance_df['Description'].str.extract(opp_id_pattern)

print("Potential Opportunity IDs extracted. Example:")
print(finance_df[['Description', 'ExtractedOppID']].head(10)) # Show first 10 results

print("\n--- Data Cleaning Complete ---")

# Display info again to see changes
print("\n--- Cleaned Data Info ---")
print("\nCRM Data Info (Post-Cleaning):")
crm_df.info()
print("\nFinance Data Info (Post-Cleaning):")
finance_df.info()
# Add info() calls for marketing_df and ad_spend_df if desired

# Next step: Reconcile CRM and Finance data
# --- Reconcile CRM and Finance Data ---
print("\n--- Reconciling CRM Deals and Finance Payments ---")

# Filter for only Closed Won deals and successful payments (exclude refunds for reconciliation)
closed_won_df = crm_df[crm_df['StageName'] == 'Closed Won'].copy()
successful_payments_df = finance_df[finance_df['Status'] == 'succeeded'].copy()

# --- Reconciliation Strategy ---
# We prioritize matching using the ExtractedOppID first.
# For payments without an ExtractedOppID, we might try other methods later (e.g., matching AccountName + Amount + Date proximity) - keeping it simple for now.

# Merge payments to deals based on the extracted Opportunity ID
# Use a 'left' merge to keep all successful payments and see which deal they match
# Suffixes help distinguish columns with the same name (e.g., Amount_deal vs Amount_payment)
reconciled_data = pd.merge(
    successful_payments_df,
    closed_won_df,
    left_on='ExtractedOppID',
    right_on='OpportunityID',
    how='left', # Keep all payments, match deals where possible
    suffixes=('_payment', '_deal')
)

print(f"Initial reconciliation complete. {len(reconciled_data)} payment records processed.")
print("Example reconciled data (showing matched/unmatched deals):")
# Show relevant columns to check the merge
print(reconciled_data[[
    'PaymentID', 'Amount_payment', 'PaymentDate', 'Description', 'ExtractedOppID', # From Finance
    'OpportunityID', 'AccountName', 'Amount_deal', 'CloseDate', 'OwnerName', 'ProductType' # From CRM (will be NaN if no match)
]].head(10))

# Identify payments that didn't match a Closed Won deal via ExtractedOppID
unmatched_payments = reconciled_data[reconciled_data['OpportunityID'].isna()]
print(f"\nIdentified {len(unmatched_payments)} successful payments that couldn't be matched to a Closed Won deal using extracted ID.")

# --- Apply Commission Logic ---
print("\n--- Calculating Commissions ---")

# Define commission rules function
def calculate_commission(row):
    # Only calculate for matched, successful payments
    if pd.isna(row['OpportunityID']) or row['Status'] != 'succeeded':
        return 0.0

    base_rate = 0.05
    product_modifier = 0.0

    # Apply product modifier
    if row['ProductType'] == 'SaaS License':
        product_modifier = 0.02
    elif row['ProductType'] == 'Hardware':
        product_modifier = -0.02 # Base rate is 5%, hardware is 3%, so modifier is -2%

    current_rate = base_rate + product_modifier
    commission = row['Amount_payment'] * current_rate

    # Note: Tiered accelerator requires grouping by rep and quarter later.
    # We calculate base commission per payment here first.
    # Clawbacks also handled later by referencing refund data.

    return round(commission, 2)

# Apply the function row by row to calculate commission for each payment
# WARNING: .apply can be slow on very large datasets, but fine for portfolio size
reconciled_data['BaseCommission'] = reconciled_data.apply(calculate_commission, axis=1)

print("Base commission calculated per payment (before tiers/clawbacks). Example:")
print(reconciled_data[['PaymentID', 'Amount_payment', 'ProductType', 'BaseCommission']].head(10))


# --- Handle Refunds (for Clawbacks) ---
print("Identifying refunds for potential clawbacks...")
refund_df = finance_df[finance_df['Status'] == 'refunded'].copy()
# Try to link refunds back to original payments/deals if possible (using ExtractedOppID)
# This simple version just flags deals that had *any* refund associated via OppID
refunded_opp_ids = refund_df['ExtractedOppID'].dropna().unique()
reconciled_data['DealHasRefund'] = reconciled_data['OpportunityID'].isin(refunded_opp_ids)
print(f"Flagged {reconciled_data['DealHasRefund'].sum()} payments associated with deals that had a refund.")


# --- Aggregate Payments per Deal (for Tier calculation) ---
# Group by OpportunityID from the CRM side (where matches exist)
# Sum payments for deals that were successfully matched
payments_per_deal = reconciled_data.dropna(subset=['OpportunityID']).groupby('OpportunityID').agg(
    TotalPaid=('Amount_payment', 'sum'),
    OwnerName=('OwnerName', 'first'), # Get rep name
    PaymentQuarter=('PaymentDate', lambda date: date.dt.to_period('Q')) # Get Quarter of payment
).reset_index()

print("\nAggregated payments per matched deal. Example:")
print(payments_per_deal.head())

# --- Calculate Tiered Commission ---
# Note: This is simplified. Real tiering might look at TOTAL rep quarterly performance.
# This version applies tiers based on *this batch* of payments per deal.
def apply_tier_bonus(deal_total_paid):
    bonus_rate_tier1 = 0.01
    bonus_rate_tier2 = 0.02
    threshold1 = 50000
    threshold2 = 100000
    bonus = 0.0

    if deal_total_paid > threshold2:
        bonus += (deal_total_paid - threshold2) * bonus_rate_tier2
        bonus += (threshold2 - threshold1) * bonus_rate_tier1 # Add full tier 1 bonus
    elif deal_total_paid > threshold1:
        bonus += (deal_total_paid - threshold1) * bonus_rate_tier1

    return round(bonus, 2)

# Apply tier calculation (needs grouping by Rep and Quarter later for accuracy)
# For simplicity here, just showing the function - proper application needs more steps

print("Tiered commission logic defined (will be applied later after grouping by rep/quarter).")


print("\n--- Reconciliation and Initial Commission Logic Complete ---")

# Next step: Aggregate results by Rep, apply tiers/clawbacks, link marketing/ad data
# --- Aggregate Commission by Rep, Quarter ---
print("\n--- Aggregating Final Commissions by Rep & Quarter ---")

# We need to link the base commission back to the rep and quarter
# Merge aggregated payments (which has rep/quarter) with base commission sums
rep_commissions = reconciled_data.dropna(subset=['OpportunityID']).groupby(
    ['OwnerName', pd.Grouper(key='PaymentDate', freq='QE')] # Group by Rep and Quarter (FIX: Q -> QE)
).agg(
    TotalPaid=('Amount_payment', 'sum'),
    TotalBaseCommission=('BaseCommission', 'sum')
).reset_index()

# Apply Tiered Bonus
rep_commissions['TierBonus'] = rep_commissions['TotalPaid'].apply(apply_tier_bonus)

# --- Calculate Clawbacks (by Rep and Quarter) ---
print("Identifying refunds for potential clawbacks...")
# Find total refunded amount per rep per quarter
refund_data_merged = pd.merge(
    refund_df,
    closed_won_df, # Use closed_won_df to find the OwnerName
    left_on='ExtractedOppID',
    right_on='OpportunityID',
    how='inner', # Only keep refunds we can match to a deal/owner
    suffixes=('_payment', '_deal') # FIX: Added suffixes
)

refund_summary = refund_data_merged.groupby(
    ['OwnerName', pd.Grouper(key='PaymentDate', freq='QE')] # FIX: Q -> QE
).agg(
    TotalRefundAmount=('Amount_payment', 'sum') # This will work now
).reset_index()

# Merge refund summary back to the main commission report
final_commission_report = pd.merge(
    rep_commissions,
    refund_summary,
    on=['OwnerName', 'PaymentDate'],
    how='left'
).fillna(0) # Fill NaN refunds with 0

# A simpler clawback: Just subtract the base commission we *already* calculated for refunded payments
refunded_commissions = reconciled_data[reconciled_data['DealHasRefund'] == True].groupby(
    ['OwnerName', pd.Grouper(key='PaymentDate', freq='QE')] # FIX: Q -> QE
).agg(
    TotalClawback=('BaseCommission', 'sum')
).reset_index()

# Merge this clawback calculation
final_commission_report = pd.merge(
    final_commission_report,
    refunded_commissions,
    on=['OwnerName', 'PaymentDate'],
    how='left'
).fillna(0)

# Calculate Final Commission
final_commission_report['FinalCommission'] = (
    final_commission_report['TotalBaseCommission'] +
    final_commission_report['TierBonus'] -
    final_commission_report['TotalClawback']
)

print("Final Commission Report by Rep & Quarter:")
print(final_commission_report.to_string()) # .to_string() prints all rows

# --- Link Marketing & Ad Spend Data ---
print("\n--- Calculating Marketing & Ad Spend ROI ---")

# 1. Total Ad Spend per Campaign
ad_spend_summary = ad_spend_df.groupby('CampaignName').agg(
    TotalSpend=('Spend', 'sum'),
    TotalImpressions=('Impressions', 'sum'),
    TotalClicks=('Clicks', 'sum')
).reset_index()
ad_spend_summary['AvgCPC'] = (ad_spend_summary['TotalSpend'] / ad_spend_summary['TotalClicks']).round(2)

# 2. Link Ad Spend to Deals (Revenue)
# We use the 'LeadSource' from the crm_df
deals_from_ads = closed_won_df[
    closed_won_df['LeadSource'].isin(ad_spend_summary['CampaignName']) |
    closed_won_df['LeadSource'].isin(['Google Ads', 'Facebook Ads', 'LinkedIn Ads']) # Catch generics
].copy() # Add .copy() to avoid SettingWithCopyWarning

# Simple mapping for generic sources
def map_generic_source(source):
    if source == 'Google Ads': return 'Google Search - Core Keywords' # Simple assumption
    if source == 'Facebook Ads': return 'Facebook - Retargeting Q4'
    if source == 'LinkedIn Ads': return 'LinkedIn Ads - Prospecting'
    return source

# Use .loc to safely modify the DataFrame
deals_from_ads.loc[:, 'CampaignName'] = deals_from_ads['LeadSource'].apply(map_generic_source)

# 3. Calculate Revenue per Campaign
revenue_per_campaign = deals_from_ads.groupby('CampaignName').agg(
    TotalRevenue=('Amount', 'sum'),
    TotalDeals=('OpportunityID', 'count')
).reset_index()

# 4. Merge Spend and Revenue to get ROAS/CPA
roi_report = pd.merge(
    ad_spend_summary,
    revenue_per_campaign,
    on='CampaignName',
    how='left'
).fillna(0)

# Handle potential divide by zero if TotalSpend or TotalDeals is 0
roi_report['ROAS'] = 0.0
roi_report['AvgCPA'] = 0.0

# Calculate only where denominator is not zero
roi_report.loc[roi_report['TotalSpend'] > 0, 'ROAS'] = (roi_report['TotalRevenue'] / roi_report['TotalSpend']).round(2)
roi_report.loc[roi_report['TotalDeals'] > 0, 'AvgCPA'] = (roi_report['TotalSpend'] / roi_report['TotalDeals']).round(2)


print("\nMarketing ROI Report (Simple Attribution):")
print(roi_report.to_string())

# --- Implement Lead Scoring Logic ---
print("\n--- Scoring Leads based on Marketing Touches ---")

# Define high-intent actions (from our Phase 1 rules)
high_intent_actions = [
    'Demo Requested',
    'Pricing Page Viewed',
    'Contact Us Form Submitted',
    'Trial Started'
]

# Simple rule-based scoring
def calculate_lead_score(touches):
    score = 0
    actions = touches['ActionType'].values
    
    if 'Demo Requested' in actions:
        score += 50
    if 'Trial Started' in actions:
        score += 40
    if 'Contact Us Form Submitted' in actions:
        score += 30
    if 'Pricing Page Viewed' in actions:
        score += 20
    if 'Case Study Downloaded' in actions:
        score += 10
    if 'Webinar Attended' in actions:
        score += 10
    
    # Add points for number of touches
    score += len(actions) * 1 # 1 point per touch
    
    # Cap score
    return min(score, 100)

# Group touches by lead
grouped_touches = marketing_df.groupby('ContactEmail')

# Apply scoring
lead_scores = grouped_touches.apply(calculate_lead_score).reset_index(name='LeadScore')
lead_scores = lead_scores.sort_values(by='LeadScore', ascending=False)

print("\nTop 20 Lead Scores:")
print(lead_scores.head(20).to_string())

print("\n--- Phase 2: Core Development Complete ---")
print("--- Phase 3: Output & Documentation (Begins) ---")
print("\n--- FINAL REPORTS ---")
print("\nFinal Commission Report:")
print(final_commission_report.to_string())
print("\nMarketing ROI Report:")
print(roi_report.to_string())
print("\nTop Lead Scores:")
print(lead_scores.head(20).to_string())

print("\n--- Analysis Complete ---")

# --- Phase 3: Save Reports & Visualizations ---
print("\n--- Phase 3: Saving Reports & Visualizations ---")

# Create a directory to store reports if it doesn't exist
report_dir = 'reports'
if not os.path.exists(report_dir):
    os.makedirs(report_dir)
    print(f"Created directory: {report_dir}")

# --- 1. Save Final Reports as CSV Files ---
try:
    final_commission_report.to_csv(f"{report_dir}/final_commission_report.csv", index=False)
    roi_report.to_csv(f"{report_dir}/marketing_roi_report.csv", index=False)
    lead_scores.to_csv(f"{report_dir}/top_lead_scores.csv", index=False)
    print("Successfully saved final reports to CSV files in 'reports/' folder.")
except Exception as e:
    print(f"Error saving reports to CSV: {e}")

# --- 2. Add Visualizations ---
print("Generating and saving visualizations...")

try:
    # Visualization 1: Final Commission by Rep
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=final_commission_report,
        x='OwnerName',
        y='FinalCommission',
        estimator=sum, # Sum up quarterly commissions for total
        ci=None # Disable confidence intervals
    )
    plt.title('Total Final Commission by Sales Rep')
    plt.ylabel('Total Commission ($)')
    plt.xlabel('Sales Rep')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f"{report_dir}/commission_by_rep.png")
    print("Saved 'commission_by_rep.png'")

    # Visualization 2: ROAS by Campaign
    # Filter for campaigns with spend to avoid clutter
    roi_report_visual = roi_report[roi_report['TotalSpend'] > 0].copy()
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=roi_report_visual,
        x='CampaignName',
        y='ROAS'
    )
    plt.title('Return on Ad Spend (ROAS) by Campaign')
    plt.ylabel('ROAS (Revenue / Spend)')
    plt.xlabel('Campaign Name')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f"{report_dir}/roas_by_campaign.png")
    print("Saved 'roas_by_campaign.png'")

    print("\n--- Phase 3 Complete: All deliverables saved. ---")

except Exception as e:
    print(f"Error generating visualizations: {e}")

# End of script