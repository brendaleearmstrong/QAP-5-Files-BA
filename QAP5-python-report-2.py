
"""
Filename: QAP5-python-report-2.py
Author: Brenda Armstrong SD10
Date: 2023-12-07
Version: 1.4.4
Description: Generates insurance policy reports, including a general policy exception report.
             The program reads information from 'OSICDef.dat' for default values and 'Policies.dat' for policy details.
"""

from datetime import datetime

# Function to format currency with a fixed width and right justification
def format_currency(value):
    return f'${value:>,.2f}'

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

# Define the date variable
date = datetime.now().strftime("%d-%b-%y")

print()
print('ONE STOP INSURANCE COMPANY')
print(f"MONTHLY PAYMENT LISTING AS OF {date}")
print()
print('POLICY CUSTOMER         TOTAL                  TOTAL     DOWN     MONTHLY')
print('NUMBER NAME             PREMIUM       HST      COST      PAYMENT  PAYMENT')
print('='*73)

# Lists for storing totals
premium_totals = []
extra_costs_totals = []
total_premium_totals = []
down_payment_totals = []
monthly_payment_totals = []

# Filtering out any customers that paid in full, leaving us only the monthly and downpayment options
filtered_policies = [policy for policy in policies_lines if policy.split(', ')[13] != 'Full']

# Iterate through policies
for policy_line in filtered_policies:
    policy_values = policy_line.strip().split(', ')
    policy_details = {
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

    # Check if the payment option is not Full
    if policy_details['payment_option'] != 'Full':
        # Calculate insurance premium and extra costs
        total_premium, total_cost_extra_coverage = calculate_insurance_and_costs(
            policy_details['num_cars'],
            policy_details['extra_liability'],
            policy_details['glass_coverage'],
            policy_details['loaner_car'],
            defaults
        )

        # Calculate HST
        hst = total_premium * defaults['HST_RATE']

        # Calculate Total Cost
        total_cost = total_premium + hst

        # Calculate Monthly Payment
        monthly_payment = (total_cost - policy_details['down_payment'] + defaults['PROCESSING_FEE']) / 12

        # Print values for general report with right justification and formatted currency
        print(f'{defaults["NEXT_POLICY_NUMBER"]:<4}  {policy_details["first_name"] + " " + policy_details["last_name"]:<15}    {format_currency(total_premium):<10}  {format_currency(hst):<10}{format_currency(total_cost):<8}  {format_currency(policy_details["down_payment"]):<8} {format_currency(monthly_payment):<8}')

        # Increment the NEXT_POLICY_NUMBER for the next policy
        defaults["NEXT_POLICY_NUMBER"] += 1

        # Append values to totals lists
        premium_totals.append(total_premium)
        extra_costs_totals.append(total_cost_extra_coverage)
        total_premium_totals.append(total_premium + total_cost_extra_coverage)
        down_payment_totals.append(policy_details['down_payment'])
        monthly_payment_totals.append(monthly_payment)

# Display totals for general report with right justification and formatted currency
# Calculate the total policies
total_policies = len(filtered_policies)

# Calculate the total premium
total_premium = sum(premium_totals)

# Calculate the total HST
total_hst = total_premium * defaults["HST_RATE"]

# Calculate the total extra costs
total_extra_costs = sum(extra_costs_totals)

# Calculate the total cost
total_cost = sum(total_premium_totals)

# Calculate the total down payment
total_down_payment = sum(down_payment_totals)

# Calculate the total monthly payment
total_monthly_payment = sum(monthly_payment_totals)

# Print the totals for the general report with right justification and formatted currency
print('='*73)
print(f'Total Policies:{total_policies:>3}      {format_currency(total_premium)}   {format_currency(total_hst)}  {format_currency(total_cost)} {format_currency(total_down_payment)} {format_currency(total_monthly_payment)}')
