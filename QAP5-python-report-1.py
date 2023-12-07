# Filename: QAP5-python-report1.py
# Author: Brenda Armstrong SD10
# Date: 2023-12-07
# Version: 1.0.0
# Description: This program reads the default values and policies from the OSICDef.dat and Policies.dat files

from datetime import datetime

# Read Defaults file
with open('OSICDef.dat', 'r') as f:
    defaults_lines = f.read().splitlines()

# Store default values in a dictionary
defaults = {
    'NEXT_POLICY_NUMBER': int(defaults_lines[0]),
    'BASIC_PREMIUM': float(defaults_lines[1]),
    'DISCOUNT_FOR_ADDITIONAL_CARS': float(defaults_lines[2]),
    'COST_EXTRA_LIABILITY_COVERAGE': float(defaults_lines[3]),
    'COST_GLASS_COVERAGE': float(defaults_lines[4]),
    'COST_LOANER_CAR_COVERAGE': float(defaults_lines[5]),
    'HST_RATE': float(defaults_lines[6]),
    'PROCESSING_FEE': float(defaults_lines[7])
}

# Read Policies file
with open('Policies.dat', 'r') as f:
    policies_lines = f.readlines()

# Function to calculate insurance premium and extra costs
def calculate_insurance_and_costs(num_cars, extra_liability, glass_coverage, loaner_car, defaults):
    basic_premium_first_car = defaults['BASIC_PREMIUM']
    discount_for_additional_cars = (num_cars - 1) * defaults['DISCOUNT_FOR_ADDITIONAL_CARS']
    basic_premium_additional_cars = basic_premium_first_car - discount_for_additional_cars
    total_premium = basic_premium_first_car + (num_cars - 1) * basic_premium_additional_cars

    total_cost_extra_coverage = num_cars * (
        defaults['COST_EXTRA_LIABILITY_COVERAGE'] * extra_liability +
        defaults['COST_GLASS_COVERAGE'] * glass_coverage +
        defaults['COST_LOANER_CAR_COVERAGE'] * loaner_car
    )

    total_premium += total_cost_extra_coverage

    return total_premium, total_cost_extra_coverage

# Function to format currency
def format_currency(amount):
    return '${:,.2f}'.format(amount)

# Define the date variable
date = datetime.now().strftime("%d-%m-%y")

print(f'POLICY LISTING AS OF {date}')  # Fix the syntax error by adding 'date' variable
print('')
print('ONE STOP INSURANCE COMPANY')
print(f'POLICY LISTING AS OF {date}')
print()
print('POLICY CUSTOMER                POLICY     INSURANCE     EXTRA      TOTAL')
print('NUMBER NAME                     DATE       PREMIUM      COSTS     PREMIUM')
print('=========================================================================')

# Lists for storing totals
premium_totals = []
extra_costs_totals = []
total_premium_totals = []

# Iterate through policies
for policy_line in policies_lines:
    policy_values = policy_line.strip().split(', ')
    claim_values = {
        'year': policy_values[0],
        'date': policy_values[1],
        'first_name': policy_values[2],
        'last_name': policy_values[3],
        'address': policy_values[4],
        'city': policy_values[5],
        'province': policy_values[6],
        'postal_code': policy_values[7],
        'phone': policy_values[8],
        'num_cars': int(policy_values[9]),
        'extra_liability': policy_values[10] == 'Y',
        'glass_coverage': policy_values[11] == 'Y',
        'loaner_car': policy_values[12] == 'Y',
        'payment_option': policy_values[13],
        'down_payment': float(policy_values[14])
    }

    # Calculate insurance premium and extra costs
    total_premium, total_cost_extra_coverage = calculate_insurance_and_costs(
        claim_values['num_cars'],
        claim_values['extra_liability'],
        claim_values['glass_coverage'],
        claim_values['loaner_car'],
        defaults
    )

    # Display policy details
    print(f'{claim_values["year"]:>4}  {claim_values["first_name"] + " " + claim_values["last_name"]:<20}   {claim_values["date"]:>10}  {format_currency(total_premium):>9}  {format_currency(total_cost_extra_coverage):>9}  {format_currency(total_premium + total_cost_extra_coverage):>9}')

    # Append values to totals lists
    premium_totals.append(total_premium)
    extra_costs_totals.append(total_cost_extra_coverage)
    total_premium_totals.append(total_premium + total_cost_extra_coverage)

# Display totals
print(f'=========================================================================')
print(f'Total policies: {len(policies_lines):>3}                      {format_currency(sum(premium_totals)):>10} {format_currency(sum(extra_costs_totals)):>10} {format_currency(sum(total_premium_totals)):>10}')

# Update next policy number in Defaults file
with open('OSICDef.dat', 'r') as f:
    data = f.readlines()

data[0] = f'{defaults["NEXT_POLICY_NUMBER"]}\n'

with open('OSICDef.dat', 'w') as f:
    f.writelines(data)
