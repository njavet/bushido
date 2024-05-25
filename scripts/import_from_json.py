import datetime
import sys
import json
import pytz

from unit_manager import UnitManager
from telegram_client import TelegramMessage
import config
import db


def convert_telegram_messages(json_data):
    lst = []
    to_id = json_data['id']
    for message in json_data['messages']:
        text = message['text']
        if text:
            from_id = int(message['from_id'][4:])
            # this is CET time when I export it from telegram
            dt_str = message['date']
            dt_format = '%Y-%m-%dT%H:%M:%S'
            dt_cet = datetime.datetime.strptime(dt_str, dt_format)
            dt_utc = dt_cet.astimezone(pytz.utc)
            unix_timestamp = dt_utc.timestamp()
            tg = TelegramMessage(msg_id=message['id'],
                                 from_id=from_id,
                                 to_id=to_id,
                                 log_time=dt_cet,
                                 unix_timestamp=unix_timestamp)
            lst.append((tg, text))
    return lst


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'usage: python {sys.argv[0]} <json_file>')
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
    try:
        db.Agent.create(agent_id=347663493,
                        name='N300')
    except:
        pass
    um = UnitManager(config.emojis)
    for tg, text in convert_telegram_messages(data):
        pr = um.process_string(text)
        if pr.success:
            um.save_unit_data(tg)
        else:
            print(pr.msg)

