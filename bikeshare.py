# Final Project Code
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ["Chicago", "New York City", "Washington"]
months = ["January", "February", "March", "April", "May", "June", "All"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "All"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = input('Which city, Chicago, New York City, or Washington, would you like to look at?\n').title()
    while city not in cities:
        city = input('Error: You did not enter a valid city. Please select one of the following: Chicago, New York City, Washington, or all for no filter.\n').title()

    month = input('What month would you like to filter by? January, February, March, April, May, June or if you do not want to filter by the month type all.\n').title()
    while month not in  months:
        month = input('Error: You did not enter a valid month. Please correctly type in the name of the month or all for no filter.\n').title()

    day = input('What day of the week would you like to filter by? If you do not want to filter by the day type all.\n').title()
    while day not in  days:
        day = input('Error: You did not enter a valid day. Please correctly type in the day of the week or all for no filter.\n').title()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.DataFrame()
    df = df.append(pd.read_csv(CITY_DATA[city.lower()]))

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of the Week'] = df['Start Time'].dt.weekday_name

    if month != 'All':
        month = months.index(month) + 1
        df = df[df['Month'] == month]

    if day != 'All':
        df= df[df['Day of the Week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df["Month"].mode()[0]
    print('The most common month is {} with a count of {}.'.format(months[common_month - 1], df[df['Month'] == common_month]['Month'].count()))

    # display the most common day of week
    common_day = df["Day of the Week"].mode()[0]
    print('The most common day is {} with a count of {}.'.format(common_day, df[df['Day of the Week'] == common_day]['Day of the Week'].count()))

    # display the most common start hour
    common_hour = df["Start Time"].dt.hour.mode()[0]
    print('The most common start hour is {} with a count of {}.'.format(common_hour, df[df["Start Time"].dt.hour == common_hour]['Start Time'].count()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('The most common start station is {} with a count of {}.'.format(common_start, df[df['Start Station'] == common_start]['Start Station'].count()))

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('The most common end station is {} with a count of {}.'.format(common_end, df[df['End Station'] == common_end]['End Station'].count()))

    # display most frequent combination of start station and end station trip
    common_start_end = (df['Start Station'] + ' - ' + df['End Station']).mode()[0]
    starting_st = common_start_end.split(' - ')[0]
    ending_st = common_start_end.split(' - ')[1]
    common_start_end_count = df[(df['Start Station'] == starting_st) & (df['End Station'] ==  ending_st)]['Start Station'].count()
    print('The most frequent combination of start station and end station is {} with a count of {}'.format(common_start_end, common_start_end_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total amount of travel time is {}.'.format(df['Trip Duration'].sum(axis = 0)))

    # display mean travel time
    print('The average amount of travel time is {}.'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    for i in range(len(user_type_count)):
        print("The amount of {}(s) is {}.".format(user_type_count.index.values[i], user_type_count[i]))
    print()

    # Display counts of gender
    gender_count = df['Gender'].value_counts()
    for i in range(len(gender_count)):
        print("The amount of {}s is {}.".format(gender_count.index.values[i], gender_count[i]))

    # Display earliest, most recent, and most common year of birth
    print('\nThe earliest birth year is {}.'.format(int(df['Birth Year'].min())))
    print('The most recent birth year is {}.'.format(int(df['Birth Year'].max())))
    print('The most common birth year is {}.'.format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Will display 5 lines at a time of raw data until user stops"""
    multiple_of_5 = range(5, len(df.index) + 1, 5)
    counter = 0
    while True:
        for i in df.index:
            counter += 1
            print('\nRow {}'.format(i))
            print("\nStart Time: {}".format(df["Start Time"][i]))
            print("End Time: {}".format(df["End Time"][i]))
            print("Trip Duration: {}".format(df["Trip Duration"][i]))
            print("Start Station: {}".format(df["Start Station"][i]))
            print("End Station: {}".format(df["End Station"][i]))
            print("User Type: {}".format(df["User Type"][i]))
            print("Gender: {}".format(df["Gender"][i]))
            print("Birth Year: {}".format(df["Birth Year"][i]))
            if counter in multiple_of_5:
                next_page = input("\n\nWould you like to look at the next 5 rows of data? Enter yes or no.\n")
                if next_page.lower() != "yes":
                    break
        break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        if_raw_data = input('\nWould you like to look at the raw data? Enter yes or no.\n')
        if if_raw_data.lower() == 'yes':
            raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
