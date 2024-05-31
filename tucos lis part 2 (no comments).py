import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()
random.seed(42)
np.random.seed(42)

items = [
    'bread', 'butter', 'milk', 'cheese', 'eggs', 'apples', 'bananas', 'grapes', 'chicken', 'beef',
    'pork', 'fish', 'rice', 'pasta', 'cereal', 'tomatoes', 'potatoes', 'onions', 'lettuce', 'carrots',
    'orange juice', 'soda', 'coffee', 'tea', 'cookies', 'chips', 'chocolate', 'yogurt', 'ice cream', 'pizza'
]

items_categories = {
    'bread': 'bakery', 'butter': 'dairy', 'milk': 'dairy', 'cheese': 'dairy', 'eggs': 'dairy',
    'apples': 'produce', 'bananas': 'produce', 'grapes': 'produce', 'chicken': 'meat', 'beef': 'meat',
    'pork': 'meat', 'fish': 'seafood', 'rice': 'grains', 'pasta': 'grains', 'cereal': 'grains',
    'tomatoes': 'produce', 'potatoes': 'produce', 'onions': 'produce', 'lettuce': 'produce', 'carrots': 'produce',
    'orange juice': 'beverage', 'soda': 'beverage', 'coffee': 'beverage', 'tea': 'beverage',
    'cookies': 'snacks', 'chips': 'snacks', 'chocolate': 'snacks', 'yogurt': 'dairy', 'ice cream': 'dairy',
    'pizza': 'frozen'
}

prices = {item: round(random.uniform(1, 15), 2) for item in items}

discount_dates_categories = {
    '2024-05-24': ['dairy'],
}

discount_rates = [0.05, 0.10, 0.20]


def generate_date_last_12_months():
    today = datetime.today()
    start_date = today - timedelta(days=365)
    random_date = fake.date_between(start_date=start_date, end_date=today)
    return random_date


def generate_weather_condition():
    weather_conditions = ['sunny', 'cloudy', 'rainy', 'stormy']
    return random.choice(weather_conditions)


def generate_hour():
    return random.randint(9, 21)  # Random hour from 9am to 9pm (inclusive)


def generate_promotion():
    promotions = ['Buy One Get One Free', '20% Off Entire Purchase', 'Free Gift with Purchase',
                  'Loyalty Rewards Points']
    return random.choice(promotions)


def generate_payment_method():
    payment_methods = ['card', 'cash']
    return random.choice(payment_methods)


def generate_cost(price):
    # Assume cost is 70% of the price with some variation
    return round(price * 0.7 * random.uniform(0.9, 1.1), 2)


transactions_last_12_months = []
num_transactions = 1000

for _ in range(num_transactions):
    transaction_id = fake.uuid4()
    date = generate_date_last_12_months().strftime('%Y-%m-%d')
    hour = generate_hour()
    weather = generate_weather_condition()
    customer_id = fake.uuid4()
    num_items_bought = 2 if random.random() < 0.15 else 1  # Set quantity to 2 with 15% probability
    items_bought = random.sample(list(items_categories.keys()), num_items_bought)

    for item in items_bought:
        discount_rate = 0
        if date in discount_dates_categories and items_categories[item] in discount_dates_categories[date]:
            discount_rate = random.choice(discount_rates)

        price = prices[item]
        discounted_price = price * (1 - discount_rate)
        cost = generate_cost(price)
        promotion = generate_promotion()
        payment_method = generate_payment_method()

        transactions_last_12_months.append({
            'TransactionID': transaction_id,
            'Date': date,
            'Hour': hour,
            'CustomerID': customer_id,
            'Item': item,
            'Category': items_categories[item],
            'Price': price,
            'Quantity': num_items_bought,
            'Discount': discount_rate,
            'Promotion': promotion,
            'PaymentMethod': payment_method,
            'Weather': weather,
            'Cost': cost
        })

df_last_12_months = pd.DataFrame(transactions_last_12_months)

file_path_last_12_months = "/Users/snatch./Desktop/tuco_grocery_transactions_last_12_months_version_2.csv"
df_last_12_months.to_csv(file_path_last_12_months, index=False, mode='a',
                         header=not os.path.exists(file_path_last_12_months))

print(f"Dataset saved to {file_path_last_12_months}")
