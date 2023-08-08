import pandas as pd
from datetime import datetime, timedelta
import calendar

   
def last_day_of_month(year_month):
    year = year_month[0]
    month = year_month[1]
    _, last_day = calendar.monthrange(year, month)
    last_day = datetime(year, month, last_day)
    return last_day


def is_workday(date):
    return date.weekday() < 5


def count_workday(start_date, stop_date):
    workday_count = 0
    while start_date <= stop_date:
        if is_workday(start_date):
            workday_count += 1
        start_date += timedelta(days=1)
    return workday_count


def work_days_distribute(start_date, end_date):
    start_datetime = datetime.strptime(start_date, '%m/%d/%Y %H:%M')
    end_datetime = datetime.strptime(end_date, '%m/%d/%Y %H:%M')
    result = {}
    times = {}
    while start_datetime <= end_datetime:
        start_year_month = (start_datetime.year, start_datetime.month)
        last_day_month = last_day_of_month(start_year_month)
        if last_day_month <= end_datetime:
            if start_year_month in result:
                result[start_year_month] += count_workday(start_datetime, last_day_month)
            else:
                result[start_year_month] = count_workday(start_datetime, last_day_month)

            if start_year_month in times:
                times[start_year_month] += 1
            else:
                times[start_year_month] = 1

            start_datetime = last_day_month+timedelta(days=1)
        else:
            if start_year_month in result:
                result[start_year_month] += count_workday(start_datetime, end_datetime)
            else:
                result[start_year_month] = count_workday(start_datetime, end_datetime)

            if start_year_month in times:
                times[start_year_month] += 1
            else:
                times[start_year_month] = 1

            start_datetime = end_datetime+timedelta(days=1)
    return result, times


df = pd.read_csv("/Users/ziweishi/Desktop/spectralmd-application-software-dv-imaging-app_issues_2023-08-07.csv")
title = df["Title"].to_list()
total_result = {}
total_times = {}
index = 0
for i in title:
    start = df["Created At (UTC)"].iloc[index]
    end = df["Closed At (UTC)"].iloc[index]
    index += 1
    try:
        result_time = work_days_distribute(start, end)
        result = result_time[0]
        time = result_time[1]
        for j in result:
            month_year = str(j[0]) + "_" + str(j[1])
            print(result[j])
            if month_year in total_result:
                total_result[month_year] += result[j]
            else:
                total_result[month_year] = result[j]
        for p in time:
            month_year = str(p[0]) + "_" + str(p[1])
            if month_year in total_times:
                total_times[month_year] += time[p]
            else:
                total_times[month_year] = time[p]
        print(index)
    except:
        print(index)


# print(total_result)
# print(total_times)

df_num = pd.DataFrame.from_dict(total_result, orient='index', columns=['Days'])
df_times = pd.DataFrame.from_dict(total_times, orient='index', columns=['Times'])

df_num.to_excel("/Users/ziweishi/Desktop/days.xlsx")
df_times.to_excel("/Users/ziweishi/Desktop/times.xlsx")
