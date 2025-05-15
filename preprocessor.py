import re
import pandas as pd
def preprocess(data):

     pattern = '\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}\s?(?:AM|PM)'
     messages = re.split(pattern, data)[1:]
     dates=re.findall(pattern,data)

     #convert the messages into date-time format
     # Assuming 'messages' and 'dates' are your lists of messages and dates
     df = pd.DataFrame({'user_message': messages, 'message_date': dates})
     # Convert message_date type to datetime with 12-hour format and handle errors by coercing to NaT
     df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M\u202f%p')
     # Rename the 'message_date' column to 'date'
     df.rename(columns={'message_date': 'date'}, inplace=True)

     
     # Assuming you have already created the DataFrame 'df'
     #Sepparate the user and messages
     users = []
     messages = []
     
    #  for message in df['user_message']:
    #      entry = re.split('([\w\W]+?):\s', message)
    #      if len(entry) > 1:  # Check if there is at least one element in entry
    #          users.append(entry[1])
    #          messages.append(" ".join(entry[2:]))
    #      else:
    #          users.append('group_notification')
    #          messages.append(entry[0])
     for message in df['user_message']:
         entry = re.split('([\w\W]+?):\s', message)
         if entry[1:]:  # user name
             users.append(entry[1])
             messages.append(" ".join(entry[2:]))
         else:
             users.append('group_notification')
             messages.append(entry[0])
     
     # Create new columns directly without assuming the existence of 'user_message'
     df['user'] = users
     df['message'] = messages

     # Drop the original 'user_message' column if it exists
     df.drop(columns=['user_message'], errors='ignore', inplace=True)
     

     #to write the coloum into the dataframe of lpandas library
     df['only_date'] = df['date'].dt.date
     df['year'] = df['date'].dt.year
     df['month'] = df['date'].dt.month_name()
     df['month_num'] = df['date'].dt.month
     df['day'] = df['date'].dt.day
     df['day_name'] = df['date'].dt.day_name()
     df['hour'] = df['date'].dt.hour
     df['minute'] = df['date'].dt.minute

     period = []
     for hour in df[['day_name', 'hour']]['hour']:
        if hour == 0:
            period.append("12 AM - 1 AM")
        elif hour < 11:
            period.append(str(hour) + " AM - " + str(hour + 1) + " AM")
        elif hour == 11:
            period.append("11 AM - 12 PM")
        elif hour == 12:
            period.append("12 PM - 1 PM")
        else:
            period.append(str(hour - 12) + " PM - " + str((hour - 12) + 1) + " PM")
 
     df['period'] = period


     return df
