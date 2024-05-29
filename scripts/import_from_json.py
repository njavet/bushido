import collections
import os

from dotenv import load_dotenv
import datetime
import sys
import json
import pytz

from unit_manager import UnitManager
import config
import db


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
            dt_utc = dt_cet.astimezone(pytz.utc)
            unix_timestamp = dt_utc.timestamp()
            dix = {'agent_id': from_id,
                   'text': msg_text,
                   'utc_datetime': datetime.datetime.strftime(dt_utc, dt_format),
                   'local_datetime': dt_str,
                   'unix_timestamp': unix_timestamp}
            lst.append(dix)
    return lst


def convert_tg_export_to_file(json_data):
    res = convert_tg_export(json_data)
    with open('converted.json', 'w') as f:
        json.dump(res, f, indent=2, ensure_ascii=False)


def insert_json_in_db(unit_manager, json_data):
    for msg in json_data:
        pr = unit_manager.process_string(msg['text'])
        if pr.success:
            agent_id = msg['agent_id']
            unix_timestamp = msg['unix_timestamp']
            unit_manager.save_unit_data(agent_id, unix_timestamp)
        else:
            print(pr.msg)


def init_database(unit_manager):
    load_dotenv()
    agent_id = int(os.getenv('AGENT_ID'))
    models = [u.subunit_model for u in unit_manager.unit_modules.values()]
    db.init_storage(models)
    db.add_agent(agent_id, 'N300', True)


def insert_from_tg_export(unit_manager, json_data):
    res = convert_tg_export(json_data)
    insert_json_in_db(unit_manager, res)


def main():
    if len(sys.argv) != 2:
        print(f'usage: python {sys.argv[0]} <json_file>')
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)

    #convert_tg_export_to_file(data)
    um = UnitManager(config.emojis)
    init_database(um)
    insert_json_in_db(um, data)
    #insert_from_tg_export(um, data)


if __name__ == '__main__':
    main()
