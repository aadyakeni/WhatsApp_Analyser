import pandas as pd
import re

# Read the data from the file
with open('WhatsApp Chat with Boys Drinking Sus Mixtures.txt', 'r', encoding='utf-8') as f:
    data = f.read()

# Define the pattern for date matching
pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

# Split messages and extract dates
messages = re.split(pattern, data)[1:]
dates = re.findall(pattern, data)

# Create DataFrame
df = pd.DataFrame({'user_message': messages, 'message_date': dates})

# Print extracted dates for debugging
# print("Extracted Dates:", df['message_date'].tolist())

# Adjust the date format in to_datetime
df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')

# Rename the column
df.rename(columns={'message_date': 'date'}, inplace=True)

# Split users and messages
users = []
messages = []

for message in df['user_message']:
    entry = re.split('([\w\W]+?):\s', message)
    
    if entry[1:]:
        users.append(entry[1])
        messages.append(entry[2])
    else:
        users.append('group_notification')
        messages.append(entry[0])

# Add users and messages to DataFrame
df['user'] = users
df['message'] = messages
df.drop(columns=['user_message'], inplace=True)

df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month_name()
df['day'] = df['date'].dt.day
df['hour'] = df['date'].dt.hour
df['minute'] = df['date'].dt.minute

# print(df.head())
