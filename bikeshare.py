# load required packages
import time
import pandas as pd
import numpy as np
# Provide dictionary for mapping to source files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def get_filters():
    '''
    Asks user to specify a city, month, and day to analyze.
    ''' 
    '''
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or 'all' to apply no month filter
        (str) day - name of the day of week to filter by, or 'all' to apply no day filter
    '''
    #dictionaries for City names, day or month selection, month, and day to allow user to use abbreviations, when deciding on what to filter for
    city_abbr = {   'ch': 'Chicago',
                    'chicago': 'Chicago',
                    'ny': 'New York City',
                    'new york': 'New York City',
                    'wa': 'Washington',
                    'washington': 'Washington'}
    
    filter_abbr = {'m': 'month',
                   'month': 'month',
                    'd': 'day',
                    'day': 'day',
                    'na': 'all',
                    'not at all': 'all'}

    month_abbr = {  'jan': 'January',
                    'january': 'January',
                    'feb': 'February',
                    'february': 'February',
                    'mar': 'March',
                    'march': 'March',
                    'apr': 'April',
                    'april': 'April',
                    'may': 'May', #used 'may' twice, to keep to the overall system
                    'may': 'May',
                    'jun': 'June',
                    'june': 'June',
                    'all': 'all'}

    day_abbr = {    'mon': 'Monday',
                    'monday': 'Monday',
                    'tue': 'Tuesday',
                    'tuesday': 'Tuesday',
                    'wed': 'Wednesday',
                    'wednesday': 'Wednesday',
                    'thu': 'Thursday',
                    'thursday': 'Thursday',
                    'fri': 'Friday',
                    'friday': 'Friday',
                    'sat': 'Saturday',
                    'saturday': 'Saturday',
                    'sun': 'Sunday',
                    'sunday': 'Sunday',
                    'all': 'all'}

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("For which city would you like to see data? Chicago (CH), New York City (NY), or Washington (WA).\
                    \nEnter 'none' to stop the program: ").lower()

        if city.lower() == 'none':
            return None, None, None     #return three times "none" as function is expected to return three values

        city = city_abbr.get(city)
        if city:
            break
        else:
            print("\nInvalid input. Please enter a valid city or 'none' to stop the program.\n")

    # get user input on how to filter the data for the selected city
    while True:
        filter_select = input("Would you like to see the information prefiltered by month (m), day (d) or not at all (na)?\
                                 \nEnter 'none' to stop the program: ").lower()

        if filter_select == 'none':
            return None, None, None     #return three times "none" as function is expected to return three values
        
        filter_select = filter_abbr.get(filter_select)

        if filter_select:
            # if user wants to filter for month, check which month or if all should be used
            if filter_select == 'month':
                # get user input for month (all, january, february, ... , june)
                while True:
                    month = input("For which month would you like to see the data? \
                                \nJanuary (jan), February (feb), March (mar), April (apr), May (may), June (jun), or all (all) six months?\
                                \nEnter 'none' to stop the program:  ").lower()

                    if month == 'none':
                        return None, None, None     #return three times "none" as function is expected to return three values

                    month = month_abbr.get(month)
                    if month:
                        day = 'all'     #set day to "all" as user selected to filter by month
                        break
                    else:
                        print("\nInvalid input. Please enter a valid month, 'all' for all month, or 'none' to stop the program.\n")
            
            # if user wants to filter by day, check which day of the week or if all days should be used
            if filter_select == 'day':
                # get user input for day of week (all, monday, tuesday, ... sunday)
                while True:
                    day = input("For which day of the week would you like to see the data? \
                                \nMonday (mon), Tuesday (tue), Wednesday (wed), Thursday (thu), Friday (fri), Saturday (sat), Sunday (sun), or all (all) days?\
                                \nEnter 'none' to stop the program: ").lower()
                    
                    if day == 'none':
                        return None, None, None     #return three times "none" as function is expected to return three values

                    day = day_abbr.get(day)
                    if day:
                        month = 'all'       #set month to "all" as user selected to filter by day
                        break
                    else:
                        print("\nInvalid input. Please enter a valid day, 'all' for all days, or 'none' to stop the program.\n")
            
            if filter_select == 'all':
                # if user selected to filter neither by month nor day, set month and day to 'all'
                month = 'all'
                day = 'all'
                break
            
            break
        
        else:
            print("\nInvalid input. Please enter a month, day, not at all (na) for no prefiltering, or 'none' to stop the program.\n")
   
    #provide the user with their selected values
    print(f"\nYou selected {city} as your place of interest.\
          \nThe information shown will be based on your selection, if not stated otherwise:\
          \nMonth(s): {month}\
          \nDay(s): {day}")
    print('-'*40)
    return city, month, day

def load_data(city):
    '''
    Loads data for the specified city and add columns for month, days and hours.

    Args:
        (str) city - name of the city to analyze
    Returns:
        df_total - Pandas DataFrame containing city data
    '''
    filename = CITY_DATA[city.lower()]
    df_total = pd.read_csv(filename)

    df_total['Start Time'] = pd.to_datetime(df_total['Start Time'])
    df_total['Month'] = df_total['Start Time'].dt.month_name()  # add month column based on 'Start Time'
    df_total['Day'] = df_total['Start Time'].dt.day_name()      # add day column based on 'Start Time'
    df_total['Hour'] = df_total['Start Time'].dt.hour         # add time (hour) column based on 'Start Time'

    return df_total
def filter_data(df_total, month, day):
    '''
    Loads prepared data (df_total) for the specified city and filters by month and day if applicable.

    Args:
        (str) month - name of the month to filter by, or 'all' to apply no month filter
        (str) day - name of the day of week to filter by, or 'all' to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    '''
    # load prepared DataFrame
    df = pd.DataFrame(df_total)

    # filter table by month, if a single month was selected
    if month.lower() != 'all':
        df = df[df['Month'] == month]

    # filter by day, if a single day was selected
    if day.lower() != 'all':
        df = df[df['Day'] == day]

    return df
def time_stats_overall(df_total, city):
    '''Displays statistics on the most frequent times of travel for the selected city overall.'''

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # count the overall number of rows for a total of the recorded trips in the provided file
    total_count = df_total.shape[0]

    # display the most common month, independent from user selection
    most_common_month = df_total['Month'].mode()[0]
    most_common_month_count = df_total['Month'].value_counts()[most_common_month]

    df_month = df_total[df_total['Month'] == most_common_month]

    # most common day within this month, independent from user selection
    common_day = df_month['Day'].mode()[0]
    common_day_count = df_month['Day'].value_counts()[common_day]

    df_day = df_month[df_month['Day'] == common_day]

    # most common hour within this day, independent from user selection
    common_hour = df_day['Hour'].mode()[0]
    common_hour_count = df_day['Hour'].value_counts()[common_hour]

	#least common month, independent from user selection
    least_common_month_count = df_total['Month'].value_counts()
    least_common_month = least_common_month_count[least_common_month_count == least_common_month_count.min()].index

    least_common_month_count = least_common_month_count.values[0]
    least_common_month = least_common_month[0]

    print(f"The most common month for {city} is {most_common_month} with {most_common_month_count} counts out of {total_count}. \
          \nDuring this time, {common_day} is the most common starting day of the week with a total of {common_day_count} counts. \
          \nOthers mostly started at about this hour of the day {common_hour} (Count: {common_hour_count}). \
          \nIn contrast, {least_common_month} is the least common month (Counts: {least_common_month_count}).")

    # display the most common day of week, independent from user selection
    most_common_day = df_total['Day'].mode()[0]
    most_common_day_count = df_total['Day'].value_counts()[most_common_day]

    print(f"\nOverall, {most_common_day} is the most common day to start in {city} with a total count of {most_common_day_count}.")

    # display the most common start hour, independent from user selection
    most_common_hour = df_total['Hour'].mode()[0]
    most_common_hour_count = df_total['Hour'].value_counts()[most_common_hour]

    print(f"Overall, {most_common_hour} is the most common hour to start in {city} with a total count of {most_common_hour_count}.")

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)
def time_stats(df, city, month, day):
    '''Displays statistics on the most frequent times of travel for selected city and month and day.'''

    print("\nCalculating The Most Frequent Times of Travel based on your selection...\n")
    start_time = time.time()

    # count the rows after filtering by the user made selection to get a total of trips corresponding to the selection
    total_count = df.shape[0]

    # get the most common values, if all month and days were selected
    if month == 'all' and day == 'all':
        # display the most common month
        most_common_month = df['Month'].mode()[0]
        most_common_month_count = df['Month'].value_counts()[most_common_month]

        df_month = df[df['Month'] == most_common_month]

        # most common day within this month
        common_day = df_month['Day'].mode()[0]
        common_day_count = df_month['Day'].value_counts()[common_day]

        # display the most common start hour on the most common day of the most common month
        df_day = df[df['Day'] == common_day]

        most_common_hour = df_day['Hour'].mode()[0]
        most_common_hour_count = df_day['Hour'].value_counts()[most_common_hour]


        print(f"The most common month for {city} is {most_common_month} with {most_common_month_count} counts out of {total_count}. \
            \nDuring this time, {common_day} is the most common starting day of the week with a total of {common_day_count} counts.\
            \nOn this day of the week, the most common hour to start is {most_common_hour} (Counts: {most_common_hour_count}).")

    # get the most common values, if a single month was selected
    if day == 'all' and month != 'all':

        # display the most common day of week in the selected month
        most_common_day = df['Day'].mode()[0]
        most_common_day_count = df['Day'].value_counts()[most_common_day]

        df_day = df[df['Day'] == most_common_day]

         # display the most common start hour on the most common day
        most_common_hour = df_day['Hour'].mode()[0]
        most_common_hour_count = df_day['Hour'].value_counts()[most_common_hour]

        print(f"During {month}, {most_common_day} is the most common day to start in {city} with a total count of {most_common_day_count}.\
              \nOn this day of the week, the most common hour to start is {most_common_hour} with a count of {most_common_hour_count}.")

    # get the most common values, if a single day was selected
    if month == 'all' and day != 'all':
        # display the most common month
        most_common_month = df['Month'].mode()[0]
        most_common_month_count = df['Month'].value_counts()[most_common_month]

        df_month = df[df['Month'] == most_common_month]

        # display the most common start hour during the most common month
        most_common_hour = df_month['Hour'].mode()[0]
        most_common_hour_count = df_month['Hour'].value_counts()[most_common_hour]

        print(f"{day}s it is most common to start during {most_common_month} in {city} with a total count of {most_common_month_count}.\
              \nDuring {most_common_month} it is most common to start at about {most_common_hour} on a {day} with a count of {most_common_hour_count}.")

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)
def station_stats(df):
    '''Displays statistics on the most popular stations and trip.'''

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    most_common_start_station_count = df['Start Station'].value_counts()[most_common_start_station]
    print(f"The most commonly used Start Station is {most_common_start_station} with a count of {most_common_start_station_count}.")

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    most_common_end_station_count = df['End Station'].value_counts()[most_common_end_station]
    print(f"The most commonly used End Station is {most_common_end_station} with a count of {most_common_end_station_count}.")

    # display most frequent combination of start station and end station trip
    df['Start-End Stations'] = df['Start Station'] + ' to ' + df['End Station']
    most_common_start_end_station = df['Start-End Stations'].mode()[0]
    most_common_start_end_station_count = df['Start-End Stations'].value_counts()[most_common_start_end_station]
    print(f"The most frequented combination of Start and End Station is {most_common_start_end_station} (Count: {most_common_start_end_station_count}).")

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)
def trip_duration_stats(df):
    '''Displays statistics on the total and average trip duration, based on the user selection.'''

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # count the rows after filtering by the user made selection to get a total of trips corresponding to the selection
    total_count = '{:,}'.format(df.shape[0])

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() / 60 / 60
    total_travel_time_days = total_travel_time / 24

    # round and reformat the values to makes them easier to read
    total_travel_time = '{:,}'.format(round(total_travel_time,2))
    total_travel_time_days = '{:,}'.format(round(total_travel_time_days,2))
    print(f"Your selection matches a total of {total_count} trips, which add up to a total of {total_travel_time} hours ({total_travel_time_days} days) of travel.")

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean() / 60 / 60
    average_travel_time_minutes = average_travel_time * 60

    # round and reformat the values to makes them easier to read
    average_travel_time = '{:,}'.format(round(average_travel_time,2))
    average_travel_time_minutes = '{:,}'.format(round(average_travel_time_minutes))

    print(f"On average the trip duration was {average_travel_time} hours (about {average_travel_time_minutes} minutes).")


    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)
def user_stats(df, city):
    '''Displays statistics on bikeshare users.'''

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # count the rows after filtering by the user made selection to get a total of trips corresponding to the selection
    user_total = df.shape[0]
    print(f"Statistics for the {user_total} users:")
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("\nCounts of User Types:")
    for user_type, count in user_types.items():
        print("{}: {} ({}%)".format(user_type, count, round(count/user_total*100)))


    # Display counts of gender
    if city != 'Washington':
        user_genders = df['Gender'].value_counts()
        print("\nCounts of Gender:")
        for user_gender, count in user_genders.items():
            print("{}: {} ({}%)".format(user_gender, count, round(count/user_total*100)))

    # Display earliest, most recent, and most common year of birth
    if city != 'Washington':
        earliest_birth_year = int(df['Birth Year'].min())
        latest_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])

        # calculate the age of the users
        age_oldest_user = 2017 - earliest_birth_year
        age_youngest_user = 2017 - latest_birth_year
        age_average_user = 2017 - most_common_birth_year

        print(f"\nThe youngest user was {age_youngest_user} while the oldest user was {age_oldest_user} years old according to the records.\
              \nOn average, the users were {age_average_user} years old.")


    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)
def df_raw_data(df):
    '''Display 5 rows of raw data and add more rows of data upon request'''
    
    response_abbr = {'yes': 'yes',
                     'y': 'yes',
                     'no': 'no',
                     'n': 'no'}
    
    # Count the total rows in the DataFrame
    total_rows = len(df)
    
    # Check if user wants to see the first 5 rows of data
    while True:
        raw_data = input(f"Would you like to see the first 5 of {total_rows} rows of data based on your previous selection? Enter yes (y) or no (n): ").lower()
        raw_data = response_abbr.get(raw_data)
    
        if raw_data == 'no':
            return
        if raw_data == 'yes':
            print(f"\nData will be shown in steps of 5 rows of at a time till the max of {total_rows} rows.\
                \nData from the filtered table:\n")
            print(df.head(5))
            print('-'*40)
            break
        else:
            print("\nInvalid input. Please enter yes (y) to show the first 5 rows or no (n) to not show any rows of data.\n")
            
    # Asking, if further rows should be shown in steps of 5 to 20 rows at a time
    row = 5 # row variable to allow a continues adding of data rows upon user request. Starting value is 5, as rows 0-4 were already displayed
    min_steps = 5 # Minimum number of rows displayed per iteration
    max_steps = 200 # Maximum number of rows displayed per iteration
    
    
    # Asked user how many rows at a time should be added. Values between min_steps and max_steps are allowed.
    while True:
        steps = input(f"How many rows at a time would you like to add going onwards? \
                \nSelect a number between {min_steps} and {max_steps}.\
                \nIf you do not want to add any further rows, enter no: ")
        
        if steps == 'no':
            print('-'*40)
            return
        
        # Try if the entered value is an integer and if it is a value between 5 and 20.
        try:
            steps = int(steps)
            if min_steps <= steps <= max_steps:
                break
            else:
                print("\nInvalid input. Please enter a valid number (5 to 20) or no to stop adding rows.\n")
                
        except ValueError:
            print("\nInvalid input. Please enter a valid number (5 to 20) or no to stop adding rows.\n")
    
    # Ask user if more rows should be added
    while row < total_rows:
        raw_data = input(f"Would you like to see the the next {steps} lines of data? (Displayed {row} of {total_rows} till now.) Enter yes (y) or no (n): ").lower()
        raw_data = response_abbr.get(raw_data)
        
        if raw_data == 'no':
            print('-'*40)
            return
        if raw_data == 'yes':
            print(df[row:row+steps])
            print('-'*40)
            row += steps
        else:
            print("\nInvalid input. Please enter yes (y) to add more rows or no (n) to stop adding rows: \n")
def main():
    #main function of script, organising the overall flow and allowing restart of the program
    while True:
        city, month, day = get_filters()
        # check if "none" was entered and leave program if true
        if city == None:
            print("\nProgram was stopped\n")
            print('-'*40)
            print('-'*40)
            break
        
        # run functions and display results in order
        df_total = load_data(city)
        df = filter_data(df_total, month, day)

        time_stats_overall(df_total, city)
        time_stats(df, city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        df_raw_data(df)

        # provide option to restart the program
        while True:
            restart = input("\nWould you like to restart? Enter yes or no: \n")
            if restart.lower() == 'no':
                print("\nProgram was stopped\n")
                print('-'*40)
                print('-'*40)
                return
            if restart.lower() == 'yes':
                print('-'*40)
                print("\nProgram is restarted\n")
                print('-'*40)
                break
            else:
                print("\nInvalid input. Please enter a valid city or 'none' to stop the program.\n")

#check if script is run as main program
if __name__ == '__main__':
	main()