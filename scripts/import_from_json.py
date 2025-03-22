from zoneinfo import ZoneInfo
import datetime
import sys
import json


def convert_tg_export(json_data, local_timezone=ZoneInfo('Europe/Zurich')):
    """
    this converts jsondata that was exported by telegram
    """
    lst = []
    for message in json_data['messages']:
        msg_text = message['text']
        reply = 'reply_to_message_id' in message
        if msg_text and not reply:
            from_id = int(message['from_id'][4:])
            # this is CET time when I export it from telegram
            dt_str = message['date']
            dt_format = '%Y-%m-%dT%H:%M:%S'
            naive_dt = datetime.datetime.strptime(dt_str, dt_format)
            local_dt = naive_dt.replace(tzinfo=local_timezone)
            # storage in seconds, precise enough for this use case
            timestamp = int(local_dt.timestamp())
            # nano seconds way:
            # utc_dt = local_dt.replace(tzinfo=ZoneInfo('UTC'))
            # import pandas as pd
            # timestamp = pd.Timestamp(utc_dt)
            dix = {'agent_id': from_id,
                   'text': msg_text,
                   'local_datetime': dt_str,
                   'timestamp': timestamp}
            lst.append(dix)
    return lst


""" 
data cleaning for past data

for item in data:
    dix = {'text': item['text']}
    if 'unixtime' in item:
        dix['timestamp'] = item['unixtime']
    elif 'unix_timestamp' in item:
        dix['timestamp'] = item['unix_timestamp']
    elif 'timestamp' in item:
        dix['timestamp'] = item['timestamp']
    else:
        print('error')
    if 'datetime' in item:
        dt0 = datetime.datetime.strptime(item['datetime'], form)
        dtu = datetime.datetime.fromtimestamp(float(dix['timestamp']))
        if dt0 != dtu:
            if float(dix['timestamp']) == 0:
                dix['timestamp'] = dt0.timestamp()
        else:
            print('unit0', item)
            print('loc', dt0, 'st', dtu)
    elif 'local_datetime' in item:
        dt0 = datetime.datetime.strptime(item['local_datetime'], form)
        dtu = datetime.datetime.fromtimestamp(float(dix['timestamp']))
        if dt0 != dtu:
            print('unit', item)
            print('loc', dt0, 'st', dtu)
    cleaned.append(dix)

"""

def convert_tg_export_to_file(json_data):
    res = convert_tg_export(json_data)
    with open('converted.json', 'w') as f:
        json.dump(res, f, indent=2, ensure_ascii=False)


def main():
    if len(sys.argv) != 2:
        print(f'usage: python {sys.argv[0]} <json_file>')
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)



if __name__ == '__main__':
    main()

