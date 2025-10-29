import pandas as pd
import random
import string
from faker import Faker
from datetime import datetime, timedelta

# --- Configuration ---
NUM_DEALS = 150
NUM_PAYMENTS_PER_DEAL_RANGE = (1, 3) # Min/Max payments per successful deal
NUM_MARKETING_TOUCHES_PER_LEAD_RANGE = (2, 7)
NUM_AD_SPEND_DAYS = 90 # Generate ~3 months of ad spend data
START_DATE = datetime(2025, 8, 1)

# --- Initialize Faker ---
fake = Faker()

# --- Helper Functions ---
def generate_mock_salesforce_opp_id(length=12):
    """Generates a mock Salesforce Opportunity ID (15 char total)."""
    prefix = "006"
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return prefix + random_chars

def generate_mock_stripe_payment_id(length=24):
    """Generates a mock Stripe Payment Intent ID."""
    prefix = "py_"
    random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return prefix + random_chars

# --- Generate CRM Deals ---
print(f"Generating {NUM_DEALS} CRM deals...")
crm_data = []
owner_names = [fake.name() for _ in range(5)] # 5 distinct sales reps
product_types = ['SaaS License', 'Consulting Hours', 'Hardware']
lead_sources = ['Google Ads', 'Referral', 'Cold Outreach', 'Webinar', 'LinkedIn Ads', 'Organic Search']
account_names = [fake.company() for _ in range(NUM_DEALS // 2)] # Re-use some account names

for i in range(NUM_DEALS):
    opp_id = generate_mock_salesforce_opp_id()
    account_name = random.choice(account_names)
    amount = round(random.uniform(1500, 25000), 2)
    close_date = START_DATE + timedelta(days=random.randint(0, NUM_AD_SPEND_DAYS + 30))
    owner_name = random.choice(owner_names)
    # 75% chance of Closed Won
    stage_name = 'Closed Won' if random.random() < 0.75 else 'Closed Lost'
    product_type = random.choice(product_types)
    lead_source = random.choice(lead_sources)

    # Make Lead Source consistent with Ad Spend sometimes
    if lead_source == 'Google Ads' and random.random() < 0.3:
        lead_source = 'Google Search CPC' # More specific variant

    crm_data.append([
        opp_id, account_name, amount, close_date.strftime('%Y-%m-%d'), owner_name,
        stage_name, product_type, lead_source
    ])

crm_df = pd.DataFrame(crm_data, columns=[
    'OpportunityID', 'AccountName', 'Amount', 'CloseDate', 'OwnerName',
    'StageName', 'ProductType', 'LeadSource'
])
print("CRM deals generated.")

# --- Generate Finance Payments (linked to Closed Won deals + some noise) ---
print("Generating finance payments...")
finance_data = []
closed_won_deals = crm_df[crm_df['StageName'] == 'Closed Won'].copy()

for index, deal in closed_won_deals.iterrows():
    num_payments = random.randint(NUM_PAYMENTS_PER_DEAL_RANGE[0], NUM_PAYMENTS_PER_DEAL_RANGE[1])
    total_paid = 0
    opp_id = deal['OpportunityID']
    deal_amount = deal['Amount']
    close_date = datetime.strptime(deal['CloseDate'], '%Y-%m-%d')

    for p in range(num_payments):
        payment_id = generate_mock_stripe_payment_id()
        # Simulate partial payments - ensure total doesn't massively exceed deal amount
        if p == num_payments - 1: # Last payment tries to match remaining
             payment_amount = max(0, round(deal_amount - total_paid + random.uniform(-deal_amount*0.05, deal_amount*0.05), 2)) # Slight variance
        else:
             payment_amount = round(random.uniform(deal_amount * 0.1, deal_amount * (1 / num_payments)), 2)

        if payment_amount <= 0: continue # Skip zero/negative payments

        total_paid += payment_amount
        payment_date = close_date + timedelta(days=random.randint(1, 45))
        status = 'succeeded'
        # Add occasional refund based on previous payment
        if random.random() < 0.05 and len(finance_data)>0: # 5% refund chance
            refund_target_idx = random.randint(0, len(finance_data)-1)
            refund_id = generate_mock_stripe_payment_id()
            refund_amount = finance_data[refund_target_idx][1] # Refund full amount
            refund_date = datetime.strptime(finance_data[refund_target_idx][2], '%Y-%m-%d') + timedelta(days=random.randint(5, 29)) # within 30 days
            refund_desc = f"REFUND {finance_data[refund_target_idx][3]}"
            finance_data.append([refund_id, refund_amount, refund_date.strftime('%Y-%m-%d'), refund_desc, 'refunded'])


        # Messy Description Logic
        desc_style = random.choice(['opp_id_clean', 'opp_id_partial', 'account_name', 'invoice_num', 'mixed'])
        description = f"Payment {p+1}/{num_payments}" # Default
        if desc_style == 'opp_id_clean':
            description = f"Payment for OppID {opp_id}"
        elif desc_style == 'opp_id_partial':
            description = f"{deal['AccountName']} Pymt Ref:{opp_id[5:]}" # Partial ID
        elif desc_style == 'account_name':
            description = f"{deal['AccountName']} Service Fee Q{payment_date.month // 3 + 1}"
        elif desc_style == 'invoice_num':
            description = f"INV#{random.randint(1000, 9999)} Payment"
        elif desc_style == 'mixed':
             description = f"{deal['AccountName']} Pymt {p+1} (Opp {opp_id})"

        finance_data.append([payment_id, payment_amount, payment_date.strftime('%Y-%m-%d'), description, status])

# Add some unmatched payments
print("Adding unmatched payments...")
for _ in range(NUM_DEALS // 10): # ~10% unmatched
    payment_id = generate_mock_stripe_payment_id()
    payment_amount = round(random.uniform(100, 5000), 2)
    payment_date = START_DATE + timedelta(days=random.randint(0, NUM_AD_SPEND_DAYS + 60))
    description = f"Misc Payment - {fake.company_suffix()} Services"
    status = 'succeeded' if random.random() < 0.95 else 'failed'
    finance_data.append([payment_id, payment_amount, payment_date.strftime('%Y-%m-%d'), description, status])

finance_df = pd.DataFrame(finance_data, columns=[
    'PaymentID', 'Amount', 'PaymentDate', 'Description', 'Status'
])
print("Finance payments generated.")

# --- Generate Marketing Touches ---
print("Generating marketing touches...")
marketing_data = []
lead_emails = [fake.email() for _ in range(NUM_DEALS * 2)] # Generate more potential leads than deals
action_types = ['Website Visit', 'Email Opened', 'Form Submitted', 'Webinar Attended',
                'Case Study Downloaded', 'Pricing Page Viewed', 'Demo Requested', 'Trial Started']
campaign_sources = ['Google Search CPC', 'Google Ads Display', 'Facebook - Retargeting Q3',
                    'Facebook - Retargeting Q4', 'LinkedIn Ads - Prospecting', 'Q4 Webinar',
                    'Cold Email Sequence', 'Referral Program', 'Organic Search', 'Direct Sales']

# Link touches primarily to Closed Won deals for realism in ROI calcs
deals_to_touch = closed_won_deals.sample(frac=0.8) # 80% of won deals get touches

for index, deal in deals_to_touch.iterrows():
    lead_email = random.choice(lead_emails) # Assign a random email
    opp_id = deal['OpportunityID']
    close_date = datetime.strptime(deal['CloseDate'], '%Y-%m-%d')
    num_touches = random.randint(NUM_MARKETING_TOUCHES_PER_LEAD_RANGE[0], NUM_MARKETING_TOUCHES_PER_LEAD_RANGE[1])

    for _ in range(num_touches):
        action_type = random.choice(action_types)
        # Make high-intent actions less frequent
        if action_type in ['Demo Requested', 'Trial Started', 'Contact Us Form Submitted']:
            if random.random() > 0.2: # Only 20% chance for these high-intent ones per touch
                action_type = random.choice(['Website Visit', 'Email Opened']) # Default to lower intent

        touch_date = close_date - timedelta(days=random.randint(5, 90)) # Touches happen before close
        campaign_source = deal['LeadSource'] if random.random() < 0.6 else random.choice(campaign_sources) # 60% chance touch matches lead source
        # Occasionally make OppID association messy
        assoc_opp_id = opp_id if random.random() < 0.85 else (generate_mock_salesforce_opp_id() if random.random() < 0.5 else None)


        marketing_data.append([
            lead_email, touch_date.strftime('%Y-%m-%d %H:%M:%S'), campaign_source,
            action_type, assoc_opp_id
        ])

# Add some touches for leads that didn't convert or are unknown
num_extra_touches = (NUM_DEALS * (sum(NUM_MARKETING_TOUCHES_PER_LEAD_RANGE)//2)) - len(marketing_data)
for _ in range(max(0, num_extra_touches // 2)):
     lead_email = random.choice(lead_emails)
     touch_date = START_DATE + timedelta(days=random.randint(0, NUM_AD_SPEND_DAYS + 30))
     campaign_source = random.choice(campaign_sources)
     action_type = random.choice(['Website Visit', 'Email Opened', 'Form Submitted']) # Lower intent generally
     assoc_opp_id = None # No associated deal yet
     marketing_data.append([
            lead_email, touch_date.strftime('%Y-%m-%d %H:%M:%S'), campaign_source,
            action_type, assoc_opp_id
        ])


marketing_df = pd.DataFrame(marketing_data, columns=[
    'ContactEmail', 'TouchpointDate', 'CampaignSource', 'ActionType', 'AssociatedOpportunityID'
])
print("Marketing touches generated.")

# --- Generate Ad Spend ---
print("Generating ad spend data...")
ad_spend_data = []
campaigns = {
    'GA_123': {'Name': 'Google Search - Core Keywords', 'Platform': 'Google Ads'},
    'GA_456': {'Name': 'Google Ads Display', 'Platform': 'Google Ads'},
    'GA_789': {'Name': 'Google Search - New Feature', 'Platform': 'Google Ads'},
    'FB_ABC': {'Name': 'Facebook - Retargeting Q4', 'Platform': 'Facebook Ads'},
    'FB_DEF': {'Name': 'Facebook - Lookalike Audience', 'Platform': 'Facebook Ads'},
    'LI_XYZ': {'Name': 'LinkedIn Ads - Prospecting', 'Platform': 'LinkedIn Ads'}
}

for i in range(NUM_AD_SPEND_DAYS):
    current_date = START_DATE + timedelta(days=i)
    # Simulate spend for a subset of campaigns each day
    active_campaign_ids = random.sample(list(campaigns.keys()), k=random.randint(2, len(campaigns)-1))
    for camp_id in active_campaign_ids:
        campaign_info = campaigns[camp_id]
        spend = round(random.uniform(20, 150) * (1 + (current_date.weekday() / 10)), 2) # Slightly higher spend later in week
        clicks = random.randint(int(spend * 0.5), int(spend * 3))
        impressions = clicks * random.randint(30, 100)

        ad_spend_data.append([
            camp_id, campaign_info['Name'], current_date.strftime('%Y-%m-%d'), spend,
            campaign_info['Platform'], impressions, clicks
        ])

ad_spend_df = pd.DataFrame(ad_spend_data, columns=[
    'CampaignID', 'CampaignName', 'Date', 'Spend', 'SourcePlatform', 'Impressions', 'Clicks'
])
print("Ad spend data generated.")

# --- Save to CSV ---
print("Saving files...")
crm_df.to_csv('crm_closed_deals.csv', index=False)
finance_df.to_csv('finance_payments.csv', index=False)
marketing_df.to_csv('marketing_touches.csv', index=False)
ad_spend_df.to_csv('ad_spend.csv', index=False)

print("\n--- Mock Data Generation Complete ---")
print(f"Generated {len(crm_df)} CRM deals.")
print(f"Generated {len(finance_df)} finance payments.")
print(f"Generated {len(marketing_df)} marketing touches.")
print(f"Generated {len(ad_spend_df)} ad spend records.")
print("Files saved: crm_closed_deals.csv, finance_payments.csv, marketing_touches.csv, ad_spend.csv")