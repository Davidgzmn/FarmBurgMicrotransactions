#Import the needed libraries and tests
import pandas as pd
from scipy.stats import chi2_contingency
from scipy.stats import binom_test

# We load the csv with click information for the adds
#df = pd.read_csv('clicks.csv')
df= pd.read_csv('/Users/david/Documents/GitHub/IntroToDataAnalysis/FarmBurgMicrotransactions/clicks.csv')

# Create a new column that notes if the user_id completed a purchase when shown the ad
df['is_purchased'] = df.click_day.apply(lambda x: 'Purchase' if pd.notnull(x) else 'no purchase')
df.head(5) # Analize the df to verify that its made correctly

#Calculate total amount of purchases
purchase_counts = df.groupby(['is_purchased','group']).user_id.count()
#Calculate users who purchases by group A B and C
groupA_purchases = df[ (df.is_purchased == 'Purchase') & (df.group=='A')].user_id.count()
groupB_purchases = df[ (df.is_purchased == 'Purchase') & (df.group=='B')].user_id.count()
groupC_purchases = df[ (df.is_purchased == 'Purchase') & (df.group=='C')].user_id.count()
#Calculate users who didn't purchases by group A B and C
groupA_no_purchase = df[(df.is_purchased == 'no purchase') & (df.group=='A')].user_id.count()
groupB_no_purchase = df[(df.is_purchased == 'no purchase') & (df.group=='B')].user_id.count()
groupC_no_purchase = df[(df.is_purchased == 'no purchase') & (df.group=='C')].user_id.count()

#print the values to corroborate
print("Group A purchases: {0}").format(groupA_purchases)
print("Group B purchases: {0}").format(groupB_purchases)
print("Group C purchases: {0}").format(groupC_purchases)

print("Group A no purchase: {0}").format(groupA_no_purchase)
print("Group B no purchase: {0}").format(groupB_no_purchase)
print("Group C no purchase: {0}").format(groupC_no_purchase)

# Create a contingency table to use in a Chi2 test
contingency = [[groupA_purchases,groupA_no_purchase],[groupB_purchases,groupB_no_purchase],[groupC_purchases,groupC_no_purchase]]
# Do the Chi2 test to determine if there is a statistically significant difference between groups
chi2, pval, dof, expected = chi2_contingency(contingency)

#Print the p value, there is a difference, but where?
print(pval)

#Get the complete amount of users
weekly_customers = len(df)
print("Weekly customers: {0}").format(weekly_customers)

#Calculate how many people we need at each price point to get $1000 a week
#which is the value we set as the worth-it point for using a certain ad
#also determine the percent of total customers that amount would reprecent
clients_at_99 = 1000/.99
percent_at_99 = clients_at_99/weekly_customers
print("Percent at 99: {0}").format(percent_at_99)

clients_at_1_99 = 1000/1.99
percent_at_1_99 = clients_at_1_99/weekly_customers
print("Percent at 1.99: {0}").format(percent_at_1_99)

clients_at_4_99 = 1000/4.99
percent_at_4_99 = clients_at_4_99/weekly_customers
print("Percent at 4.99: {0}").format(percent_at_4_99)

#We use a binomial test determine if there is a difference between the results
#and the needed values

#we are determining if the amount of purchases we need per customer at price points
#exceeds the percent of people who purchased at that given price point
pvalA = binom_test(groupA_purchases, n=(groupA_purchases+groupA_no_purchase), p=percent_at_99)
print(pvalA)

pvalB = binom_test(groupB_purchases, n=(groupB_purchases+groupB_no_purchase), p=percent_at_1_99)
print(pvalB)

pvalC = binom_test(groupC_purchases, n=(groupC_purchases+groupC_no_purchase), p=percent_at_4_99)
print(pvalC)

#Surpirsingly, even thougth the .99 pricepoint sells the most apps, the percentage of our customers
#who buy the app at that price point is not enough to reach the needed revenue

#The 4.99 pricepoint is the only one where our purchase percentage matches our present results
