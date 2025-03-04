import pandas as pd

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')
    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?

    average_age_men = df.loc[df['sex']=='Male']['age'].mean().round(1)

    # What is the percentage of people who have a Bachelor's degree?
    p = df.loc[df['education']=='Bachelors']['education'].count()
    f = df['education'].count()
    percentage_bachelors = ((p * 100)/f).round(1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?

    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`

    selected = df.loc[:, ['education', 'salary']]
    high_ed = selected[(selected['education'] == 'Bachelors') | (selected['education'] == 'Masters') | (
                selected['education'] == 'Doctorate')]
    low_ed = selected[~((selected['education'] == 'Bachelors') | (selected['education'] == 'Masters') | (
                selected['education'] == 'Doctorate'))]

    higher_education = high_ed[high_ed['salary']=='>50K'].value_counts().sum()
    lower_education = low_ed[low_ed['salary']=='>50K'].value_counts().sum()
    # percentage with salary >50K
    higher_education_rich = round((higher_education * 100)/(high_ed.value_counts().sum()),1)
    lower_education_rich = round((lower_education * 100)/(low_ed.value_counts().sum()),1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    a = df.loc[:, ['hours-per-week', 'salary']]
    b = a[a['salary'] == '>50K']
    num_min_workers = b[b['hours-per-week'] == b['hours-per-week'].min()].value_counts().sum()
    total_people_with_min_working_hours = a[a['hours-per-week'] == df['hours-per-week'].min()].value_counts().sum()

    rich_percentage = round((num_min_workers*100)/(total_people_with_min_working_hours),1)

    # What country has the highest percentage of people that earn >50K?
    country_frame = df.loc[:, ('native-country', 'salary')]
    c = pd.DataFrame(country_frame[country_frame['salary'] == '>50K'].value_counts()).reset_index()
    c.columns = ['native-country', 'salary', 'counts']
    total_ppl = country_frame['native-country'].value_counts().reset_index()
    total_ppl.columns = ['native-country', 'total-people']
    c = c[['native-country', 'counts']]
    country_stats = c.merge(total_ppl, on='native-country')
    country_stats['percentage'] = round((country_stats['counts'] * 100) / (country_stats['total-people']), 1)

    highest_earning_country = country_stats.loc[country_stats['percentage'].idxmax(), 'native-country']

    highest_earning_country_percentage = country_stats['percentage'].max()

    # Identify the most popular occupation for those who earn >50K in India.
    filtered = df.loc[:, ('native-country', 'occupation', 'salary')]
    filtering_india = filtered[
        (filtered['native-country'] == 'India') & (filtered['salary'] == '>50K')].value_counts().reset_index()
    filtering_india.columns = ['native-country', 'occupation', 'salary', 'frequency']
    filtering_india[['occupation', 'frequency']]
    top_IN_occupation = filtering_india.loc[filtering_india['frequency'].idxmax(), 'occupation']

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)
    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation,
    }