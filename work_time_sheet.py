import csv
import datetime
import math
import os
import re
import sys

MY_MANE = '出口雅也'
STANDARD_WORK_TIME = '08:00'


def work_time_sheet(input_file):
    with open(input_file, newline='', encoding='utf-8-sig') as input_csv_file:
        ws_reader = csv.reader(input_csv_file, delimiter=',')
        result = []

        first_loop = True
        for row in ws_reader:
            del row[-1]
            if first_loop:
                first_loop = False
                row[-1] = '業務内容'
            else:
                if (not row[1]) and row[5] and row[6]:
                    row[-1] = 'Web ページ作成'
                    row[5] = time_ceil(row[5])
                    row[6] = time_floor(row[6])
                    row[7] = working_time(row[5], row[6])
                    row[8] = overtime_work(row[7])

            result.append(row)

        month = re.search(r'\d+/(\d+)/\d+', result[1][0]).group(1)
        date = datetime.date.today().day
        if round(date / 15) % 2 == 1:
            division = '前半'
        else:
            division = ''
        output_file_name = '_'.join([MY_MANE, str(month) + '月度' + division, '勤務表'])
        output_file = os.path.dirname(input_file) + os.path.sep + output_file_name + '.csv'

        with open(output_file, 'w', newline='') as output_csv_file:
            ws_writer = csv.writer(output_csv_file, quoting=csv.QUOTE_ALL)

            for row in result:
                ws_writer.writerow(row)

        return output_file


def time_ceil(s: str) -> str:
    t = s.split(':')
    t = [int(t1) for t1 in t]
    t[1] = math.ceil(t[1] / 15.0) * 15
    if t[1] == 60:
        t[0] += 1
        t[1] = 0

    return ':'.join(['{0:02d}'.format(t1) for t1 in t])


def time_floor(s: str) -> str:
    t = s.split(':')
    t = [int(t1) for t1 in t]
    t[1] = math.floor(t[1] / 15.0) * 15

    return ':'.join(['{0:02d}'.format(t1) for t1 in t])


def working_time(s1: str, s2: str) -> str:
    t1 = datetime.datetime.strptime(s1, '%H:%M')
    t2 = datetime.datetime.strptime(s2, '%H:%M') - datetime.timedelta(hours=1)

    return td_to_str(t2 - t1)


def overtime_work(s: str) -> str:
    t = datetime.datetime.strptime(s, '%H:%M')
    td = t - datetime.datetime.strptime(STANDARD_WORK_TIME, '%H:%M')

    if td.total_seconds() < 0:
        return '00:00'

    return td_to_str(td)


def td_to_str(td: datetime.timedelta) -> str:
    return ':'.join(['{0:02d}'.format(t1) for t1 in [td.seconds // 3600, td.seconds % 3600 // 60]])


if __name__ == '__main__':
    args = sys.argv
    print(args)
    if len(args) != 2:
        print('Argument is invalid')
    elif not os.path.exists(args[1]):
        print('File not found')
    elif not os.path.isfile(args[1]):
        print(args[1] + ' is not a file')
    elif os.path.splitext(args[1])[1] != '.csv':
        print(args[1] + ' is not a CSV file')
    else:
        sys.stdout.write(work_time_sheet(args[1]))
