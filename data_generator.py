import pandas as pd
import numpy as np
import random

# --- Configuration ---
days = 90
start_date = '2025-01-01'
countries = ['US', 'UK', 'DE', 'FR', 'AU']
channels = ['Paid Search', 'Paid Social', 'Organic']

campaigns = {
    'Paid Search': ['Brand_Exact_Match', 'Generic_Search_Q1', 'Competitor_Targeting', 'Search_Retargeting', 'Shopping_Top_Products'],
    'Paid Social': ['FB_Prospecting_Q1', 'IG_Showcase_Video', 'TikTok_UGC_Collab', 'Social_Retargeting_DPA', 'LinkedIn_B2B_LeadGen'],
    'Organic': ['SEO_NonBranded_Blog', 'SEO_Branded_Home', 'Direct_Traffic', 'Email_Newsletter_Weekly', 'Referral_Program']
}
country_weights = {'US': 1.5, 'UK': 1.2, 'DE': 1.0, 'FR': 0.9, 'AU': 0.7}

# Format: [CTR Mean, CPC Mean, ConvRate Mean, AOV Mean]
channel_performance = {
    'Paid Search': [0.04, 2.50, 0.05, 120],  # High Intent: High CTR, High Cost, High CR
    'Paid Social': [0.015, 1.20, 0.02, 85],   # Interruption: Low CTR, Low Cost, Lower CR
    'Organic':     [0.15, 0.00, 0.03, 95]     # High Intent: Best CTR, Zero Cost
}

data = []

dates = pd.date_range(start=start_date, periods=days)

for date in dates:
    for country in countries:
        for channel in channels:
            # Randomly select 1-3 active campaigns per channel per day 
            active_campaigns = random.sample(campaigns[channel], k=random.randint(1, 3))
            
            for campaign in active_campaigns:
                # 1. Impressions 
                base_volume = random.randint(1000, 50000)
                impressions = int(base_volume * country_weights[country])
                
                # 2. Clicks (Impressions * CTR)
                ctr_limit = channel_performance[channel][0]
                
                actual_ctr = np.random.normal(ctr_limit, ctr_limit * 0.1)
                actual_ctr = max(0.001, min(actual_ctr, 1.0)) # Clamp between 0.1% and 100%
                clicks = int(impressions * actual_ctr)
                
                # 3. Sessions (Clicks * Drop-off Rate)
                sessions = int(clicks * np.random.uniform(0.85, 0.98))
                
                # 4. Conversions (Sessions * Conversion Rate)
                cr_base = channel_performance[channel][2]
                actual_cr = np.random.normal(cr_base, cr_base * 0.2)
                conversions = int(sessions * actual_cr)
                
                # 5. Cost (Clicks * CPC)
                if channel == 'Organic':
                    cost = 0.00
                else:
                    cpc_base = channel_performance[channel][1]
                    # US/UK clicks are usually more expensive than other regions
                    cpc_country_adj = 1.1 if country in ['US', 'UK'] else 0.9
                    
                    # Calculate final cost with random variance
                    final_cpc = cpc_base * cpc_country_adj
                    cost = round(clicks * np.random.normal(final_cpc, final_cpc * 0.1), 2)
                
                # 6. Revenue (Conversions * AOV)
                aov_base = channel_performance[channel][3]
                # Revenue fluctuates based on order size variance
                revenue = round(conversions * np.random.normal(aov_base, 20), 2)
                
                # Append Row
                data.append([
                    date.strftime('%Y-%m-%d'), 
                    country, 
                    channel, 
                    campaign, 
                    impressions, 
                    clicks, 
                    sessions, 
                    conversions, 
                    cost, 
                    revenue
                ])

# Create DataFrame
columns = ['date', 'country', 'channel', 'campaign', 'impressions', 'clicks', 'sessions', 'conversions', 'cost', 'revenue']
df = pd.DataFrame(data, columns=columns)

# Save to CSV
filename = 'marketing_performance_dataset.csv'
df.to_csv(filename, index=False)

print(f"Success! Generated {len(df)} rows.")
print(f"File saved as: {filename}")
print(df.head(5))