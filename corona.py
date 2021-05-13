import sys
import traceback
from flask import request
from common.pandas_man import DataFrameMan
from common.controller import Controller
from distutils.util import strtobool


def get_patients():
    controller = Controller()
    area = request.args.get('area')
    address = request.args.get('address')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    forced = request.args.get('forced')
    forced = forced if forced else "false"
    forced = strtobool(forced)

    offset = request.args.get('offset', type=int)
    limit = request.args.get('limit', type=int)

    option_keys = request.args.getlist('option_keys', lambda x: x.split(','))
    option_keys = list(controller.flatten(option_keys))
    print(f"options={option_keys}")

    option_values = request.args.getlist('option_values', lambda x: x.split(','))
    option_values = list(controller.flatten(option_values))
    print(f'values={option_values}')

    df = controller.get_dataframe(area, forced)
    conf_json = controller.get_config_json(area)
    df_man = DataFrameMan()

    df = df_man.change_date_type_to_datetime(df, conf_json["date_key"])
    df = df_man.find_records_within_period(df, conf_json["date_key"], start_date, end_date)
    df = df_man.find_records_by_address(df, conf_json["address_columns"], address)
    for k, v in zip(option_keys, option_values):
        df = df_man.search_dataframe_value(df, k, v)
    df = df_man.limit_records(df, offset, limit)
    results = df_man.change_date_type_to_str(df, conf_json["date_key"]).to_dict(orient='records')
    return results


def get_patients_list():
    controller = Controller()
    sm = controller.get_syslog_man()
    try:
        df = get_patients()
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_list = traceback.extract_tb(exc_traceback)
        print(e, exc_type, exc_value, tb_list)
        msg = f'traceback={tb_list}, error_type{exc_type}, error_msg={exc_value}'
        sm.log(msg, 'error')
        return msg, 500
    return df


def get_numbers():
    controller = Controller()
    sm = controller.get_syslog_man()
    try:
        df = get_patients()
        p_num = len(df)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_list = traceback.extract_tb(exc_traceback)
        print(e, exc_type, exc_value, tb_list)
        msg = f'traceback={tb_list}, error_type{exc_type}, error_msg={exc_value}'
        sm.log(msg, 'error')
        return msg, 500
    return p_num


def get_options():
    controller = Controller()
    sm = controller.get_syslog_man()
    try:
        area = request.args.get('area')
        address = request.args.get('address')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        forced = request.args.get('forced')
        forced = forced if forced else "false"
        forced = strtobool(forced)

        df = controller.get_dataframe(area, forced)
        conf_json = controller.get_config_json(area)
        df_man = DataFrameMan()

        df = df_man.change_date_type_to_datetime(df, conf_json["date_key"])
        df = df_man.find_records_within_period(df, conf_json["date_key"], start_date, end_date)
        if address:
            df = df_man.find_records_by_address(df, conf_json["address_columns"], address)
        return df_man.get_column_values(df)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_list = traceback.extract_tb(exc_traceback)
        print(e, exc_type, exc_value, tb_list)
        msg = f'traceback={tb_list}, error_type{exc_type}, error_msg={exc_value}'
        sm.log(msg, 'error')
        return msg, 500
