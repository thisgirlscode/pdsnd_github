import time
import pandas as pd
import numpy as np
"""
Welcome, thank you for checking out my code
"""
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities_list = ['all','chicago','new_york_city','washington']
months_list = ['all','january','february','march','april','may','june','july','august','september','october','november','december']
days_list = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #Initialize these variables as empty (for validation purposes
    city = ""
    month = ""
    day = ""
    #TO DO:
    #get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            if city == "":
                city = input("What city would you like to analyze? ").lower().replace(" ", "_")
                if city not in cities_list:
                    print("That is not a valid city. (Your options are all, chicago, new york city or washington")
                    city = ""
        except Exception as e:
            print("Exception occurred: {}".format(e))
            break
        #get user input for month (all, january, february, ... , june)
        if city in cities_list and month == "":
            try:
                if month == "":
                    month = input("What month would you like to explore (January through June only)? (Enter \'all\' to disregard this filter): ").lower()
                    if month not in months_list:
                        print("That is not a valid month. i.e.: January")
                        month = ""
            except Exception as e:
                print("Exception occurred: {}".format(e))
                break
        #get user input for day of week (all, monday, tuesday, ... sunday)
        elif city in cities_list and month in months_list:
            try:
                if day == "":
                    day = input("what day would you like to review? (Enter \'all\' to disregard this filter) ").lower()
                    if day not in days_list:
                        print("That is not a valid day. i.e.: Monday")
                        day = ""
                    else:
                        break
            except Exception as e: #if the try block throws an error then will run this code and will continue running the rest of the code
                print("Exception occurred: {}".format(e))
                break
    print('-'*40)
    return city, month, day

def load_data(c, m, d):
    #creating file name
    file_name = str(c + ".csv")

    #creating month dictionary to pass correct values as a filter.
    month_dictionary = {}
    for i in range(len(months_list)):
        dict_key = months_list[i]
        dict_value = i
        month_dictionary[dict_key] = i

    #filtering cities. If "all" then combine DF, if not create DF for the selected city. Also validating washington file format
    month_id = int(month_dictionary[m])
    day_id = d

    if c != "all":
        if c == "washington":
            city_df = pd.read_csv(file_name)[['Start Time','End Time','Trip Duration','Start Station','End Station','User Type']]
            city_df['Gender'] = np.nan
            city_df['Birth Year'] = np.nan
        else:
            city_df = pd.read_csv(file_name)[['Start Time','End Time','Trip Duration','Start Station','End Station','User Type','Gender','Birth Year']]
    else:
        ny_df = pd.read_csv("new_york_city.csv")[['Start Time','End Time','Trip Duration','Start Station','End Station','User Type','Gender','Birth Year']]
        chicago_df = pd.read_csv("chicago.csv")[['Start Time','End Time','Trip Duration','Start Station','End Station','User Type','Gender','Birth Year']]
        wash_df = pd.read_csv("washington.csv")[['Start Time','End Time','Trip Duration','Start Station','End Station','User Type']]
        wash_df['Gender'] = np.nan
        wash_df['Birth Year'] = np.nan
        city_df = pd.concat([ny_df,wash_df,chicago_df], axis=0)

    city_df['Start Time'] = pd.to_datetime(city_df['Start Time'])
    city_df['Month'] = city_df['Start Time'].dt.month
    city_df['Day_of_week'] = city_df['Start Time'].dt.weekday_name
    city_df['Hour'] = city_df['Start Time'].dt.hour


    if m != "all":
        city_df = city_df[city_df['Month'] == month_id]
    if d != "all":
        city_df = city_df[city_df['Day_of_week'] == d.capitalize()]

    return city_df


def time_stats(city_df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    #print()
    if city_df['Month'].count() != 0:
        popular_month = city_df['Month'].mode()[0]
        trips_by_month = city_df['Month'].value_counts().max()
        month_name = months_list[popular_month]
        print("The most common month is {} with a total count of {} trips".format(month_name.capitalize(),trips_by_month))
    else:
        print("Oops... No common month at this time")

    # TO DO: display the most common day of week
    if city_df['Day_of_week'].count() != 0:
        popular_day = city_df['Day_of_week'].mode()[0]
        trips_by_day = city_df['Day_of_week'].value_counts().max()
        print("The most common day is {} with a total count of {} trips".format(popular_day,trips_by_day))
    else:
        print("Oops...No common day of week at this time")

    # TO DO: display the most common start hour
    if city_df['Hour'].count() != 0:
        popular_hour = city_df['Hour'].mode()[0]
        trips_by_hr = city_df['Hour'].value_counts().max()
        print("The most common hour is {} with a total count of {} trips".format(popular_hour,trips_by_hr))
    else:
        print("Oops...No common hour at this time")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(city_df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    if city_df['Start Station'].count() != 0:
        popular_ststation = city_df['Start Station'].mode()[0]
        trips_ststation = city_df['Start Station'].value_counts().max()
        print("The most commonly used Start Station is {} with a total count of {} trips".format(popular_ststation,trips_ststation))
    else:
        print("Oops...No frequent Start Station at this time")

    # TO DO: display most commonly used end station
    if city_df['End Station'].count() != 0:
        popular_endstation = city_df['End Station'].mode()[0]
        trips_endstation = city_df['End Station'].value_counts().max()
        print("The most commonly used End Station is {} with a total count of {} trips".format(popular_endstation,trips_endstation))
    else:
        print("Oops...No frequent End Station at this time")

    # TO DO: display most frequent combination of start station and end station trip
    city_df['Station set']= city_df['Start Station'] + " - " + city_df['End Station']

    if city_df['Station set'].count() != 0:
        popular_stationset = city_df['Station set'].mode()[0]
        trips_stationset = city_df['Station set'].value_counts().max()
        print("The most frequent combination of Start station and End station is {} with a total count of {} trips".format(popular_stationset,trips_stationset))
    else:
        print("Oops...No common combination of Start station and End station at this time")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(city_df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Total Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total and mean travel time
    if city_df['Trip Duration'].count() != 0:
        tot_travel_time = city_df['Trip Duration'].sum()
        tot_minutes = int(tot_travel_time / 60)
        tot_hours = int(tot_travel_time / 3600)

        print("Total travel time is: {} seconds which is about {} minutes or {} hours".format(tot_travel_time,tot_minutes,tot_hours))
        mean_travel_time = city_df['Trip Duration'].mean()
        print("Mean travel time is: {} seconds".format(mean_travel_time))
    else:
        print("Oops...There were zero trips made and a mean travel time could not be calculated")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(city_df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if city_df['User Type'].count() == 0:
        print("There is not available user type data")
    else:
        tot_user_types = city_df['User Type'].value_counts()
        print("The count per user types is:\n{}".format(tot_user_types.to_string()))
    print()
    # TO DO: Display counts of gender
    if city_df['Gender'].count() == 0:
        print("There is not available gender data")
    else:
        tot_gender = city_df['Gender'].value_counts()
        print("The counts of Gender are:\n{}".format(tot_gender.to_string()))
    print()
    # TO DO: Display earliest, most recent, and most common year of birth
    if city_df['Birth Year'].count() == 0:
            print("There is not available year of birth data")
    else:
        city_df['Birth Yearx']= pd.to_numeric(city_df['Birth Year'], downcast='signed')
        common_byear = city_df['Birth Year'].value_counts().idxmax()

        print("The earliest year of birth is: {}".format(min(city_df['Birth Yearx'])))
        print("The most recent year of birth is: {}".format(max(city_df['Birth Yearx'])))
        print("The most common year of birth is: {}".format(common_byear))
        print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def see_raw_data(city_df):
    """Displays raw data if user chooses to see it"""

    raw_data = city_df[['Start Time','End Time','Trip Duration','Start Station','End Station','User Type','Gender','Birth Year']].head(5)

    return raw_data

def main():
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.width', 1850)

    while True:
        city, month, day = get_filters()
        city_df = load_data(city, month, day)

        time_stats(city_df)
        station_stats(city_df)
        trip_duration_stats(city_df)
        user_stats(city_df)

        question = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n').lower()

        if question == 'yes':
            data = see_raw_data(city_df)
            print(data)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break

        elif question == 'no':
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        else:
            print("You entered an incorrect value. Try again next time")

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break



if __name__ == "__main__":
    main()
