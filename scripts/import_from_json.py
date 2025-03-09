import collections
import os
import datetime
import sys
import json


def convert_tg_export(json_data):
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
            dt_cet = datetime.datetime.strptime(dt_str, dt_format)
            timestamp = dt_cet.timestamp()
            dix = {'agent_id': from_id,
                   'text': msg_text,
                   'local_datetime': dt_str,
                   'timestamp': timestamp}
            lst.append(dix)
    return lst


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

