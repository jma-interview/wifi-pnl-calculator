
from flask import Flask, request, redirect, render_template, session, jsonify
from flask_cors import CORS

from werkzeug.exceptions import HTTPException
import logging
from datetime import timedelta
import os
# from flask_bcrypt import Bcrypt\

# s3 bucket for model
# pac-bi-roicalcwifi-model-699071200452-us-west-2
# dict in prod instance for model
# /home/ec2-user/python-flask-service/pyroi/model

try:
    from .flaskrun import flaskrun
    from .exception import RoiException
    from .config import config
    from .roiinput import RoiInput, RoiFlight, flight_list_gen_df, RoiFleet, fleet_list_gen_df
    from .roioutput import output_merge, final_output, final_output_
    from .constant import UI_CONFIG
    from .InputTranslation import ui_translation,df_category,RunModel
    from .roiauth import cognito, get_token
except:
    from flaskrun import flaskrun
    from exception import RoiException
    from config import config
    from roiinput import RoiInput, RoiFlight, flight_list_gen_df, RoiFleet, fleet_list_gen_df
    from roioutput import output_merge, final_output, final_output_
    from constant import UI_CONFIG
    from InputTranslation import ui_translation,df_category,RunModel
    from roiauth import cognito, get_token

# try:
#     from .roiinput import RoiInput, RoiFlight, flight_list_gen_df
#     from .roioutput import output_merge, final_output
#     from .constant import UI_CONFIG, SAMPLE_OUTPUT, SAMPLE_COL, SAMPLE_VAL
#     from .InputTranslation import ui_translation,RunModel
#     from .config import config
# except:
#     from roiinput import RoiInput, RoiFlight, flight_list_gen_df
#     from roioutput import output_merge, final_output
#     from constant import UI_CONFIG, SAMPLE_OUTPUT, SAMPLE_COL, SAMPLE_VAL
#     from InputTranslation import ui_translation, RunModel
#     from config import config

# export FLASK_APP=pyroi.py
# nohup gunicorn -w 2 -b 127.0.0.1:5000 pyroi:app &

# https://127.0.0.1:5000/?code=39f1f071-0af7-437b-b460-4cabc35a476b

import ssl
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('keys/server.crt', 'keys/server.key')

# conn = cognito.get('default')

def create_app(config_filename=None):
    app = Flask(__name__)

    print(f'config file: {config_filename}')

    if not config_filename:
        print('-- Invalid config name, will use default config')
        cfg = config.get('default')
    else:
        print(f'-- Valid config name, will use {config_filename} config')
        cfg = config.get(config_filename)

    app.config.from_object(cfg)

    app.logger.setLevel(logging.INFO)
    return app

app = create_app('prod')
CORS(app)

def get_conn(app):
    env = app.config.get('CONN', None)
    if not env:
        app.logger.info(f"No Env Argument, will use default config")
        conn = cognito.get('default')
    else:
        conn = cognito.get(env, None)
    if conn:
        app.logger.info(f"Valid Env Argument, will use {env} config")
    else:
        app.logger.info(f"Invalid Env Argument, will use default config")
        conn = cognito.get('default')
    return conn

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=120)

@app.errorhandler(Exception)
def handle_server_side_exception(e):
    app.logger.info('Enter Error Handler')

    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    app.logger.info(str(e))

    return render_template('errors.html', errors=str(e)), code

# @app.template_global()
# def js_include(filename):
#     js_folder = os.path.join(app.static_folder, 'js')
#     full_path = os.path.join(js_folder, filename)
#     with open(full_path, 'r') as f:
#         return f.read()

@app.route("/")
def index():
    """
    Route for site index page
    :return:
    """

    # if session -- logged in:
    # if 'username' in session:
    # http: // flask.pocoo.org / docs / 1.0 / quickstart /

    conn = get_conn(app)
    code = request.args.get('code')
    login = session.get('login', None)

    app.logger.info(app.config.get('env', None))
    app.logger.info(code)
    app.logger.info(login)

    # if user have logged in, have user info in session
    if login:
        app.logger.info('Find login information in session')
    elif code:
        # call
        try:
            app.logger.info(f'Get code from Client: {code}')
            app.logger.info('-- Will exchange token with AWS TOKEN API')
            # request to token url to get token
            login = get_token(code, conn)

            app.logger.info('-- Get session back from AWS')
            # write result to session
            session['login'] = login

        except Exception as e:
            msg = f'Error in Code to Token: \n{str(e)}'
            app.logger.error(msg)
            raise RoiException(msg)

    else:
        # no session, no code. redirect to login url
        app.logger.info('No code from Client; No session in Server')
        app.logger.info('Redirect to login page')
        return redirect(conn.oauth2_login())

    # log session info
    app.logger.info('current session: ')
    app.logger.info(session.get('login'))

    return render_template('index.html', ui_config=UI_CONFIG)

@app.route("/output", methods=['GET', 'POST'])
def roi():
    """
    Route for roi calculator
    :return:
    """
    conn = get_conn(app)
    login = session.get('login', None)
    # if session -- logged in:
    if login:
        app.logger.info('Find login information in session')

        app.logger.info('current session: ')
        app.logger.info(session.get('login'))
    else:
        return redirect(conn.oauth2_login())
    try:
        app.logger.info("load input: ")
        jsonData = request.form

        print(jsonData)

        input_form = RoiInput.load_request(jsonData)

        app.logger.info(f"--> input_form: \n{input_form}")

        fleet_zip = RoiFleet.load_request(jsonData)

        flight_zip = RoiFlight.load_request(jsonData)

        fleet_ls = RoiFleet.load_input(fleet_zip)

        flight_ls = RoiFlight.load_input(flight_zip)

        fleet = fleet_list_gen_df(fleet_ls)

        flight = flight_list_gen_df(flight_ls)

        additional, price = input_form.gen_df()
        share = additional

        # # for test
        # import pandas as pd
        # fleet = pd.read_csv(os.path.join('.', 'data', 'sample_fleet.csv'))
        # price = pd.read_csv(os.path.join('.', 'data', 'sample_price.csv'))
        # flight = pd.read_csv(os.path.join('.', 'data', 'sample_flight.csv'))
        # share = pd.read_csv(os.path.join('.', 'data', 'sample_contract.csv'))

        app.logger.info(f"--> df")

        app.logger.info(f"--> flight: \n{flight}")
        app.logger.info(f"--> fleet: \n{fleet}")
        app.logger.info(f"--> price: \n{price}")
        app.logger.info(f"--> additional: \n{additional}")

        app.logger.info(f"--> dict")

        app.logger.info(f"--> fleet: \n{fleet.to_dict('records')}")
        app.logger.info(f"--> flight: \n{flight.to_dict('records')}")

        app.logger.info(f"--> price: \n{price.to_dict('records')}")
        app.logger.info(f"--> additional: \n{additional.to_dict('records')}")


    except Exception as e:
        msg = f'Error in Input Loading: \n{str(e)}'
        app.logger.error(msg)

        raise RoiException(msg)
    try:
        app.logger.info("Transform input data")
        # input transformation and model prediction
        df_input, df_factor, df_contract, col_order = ui_translation(flight, price, fleet, share)
        df_input_text = df_category(df_input, price, \
                                    unit='unit_text', num='num_text', \
                                    category=1, ordered_col=col_order)
        df_input_browse = df_category(df_input, price, \
                                      unit='unit_browse', num='num_browse', \
                                      category=2, ordered_col=col_order)
        df_input_stream = df_category(df_input, price, \
                                      unit='unit_stream', num='num_stream', \
                                      category=3, ordered_col=col_order)
        #
        # app.logger.info(f"--> df_input_text: \n{df_input_text.describe()}")
        # app.logger.info(f"--> df_input_browse: \n{df_input_browse.describe()}")
        # app.logger.info(f"--> df_input_stream: \n{df_input_stream.describe()}")
    except Exception as e:
        msg = f'Error in Input Transforming: \n{str(e)}'
        raise RoiException(msg)

    try:
        app.logger.info("Running Core Model, generate result")
        result_text = RunModel(df_input_text)
        result_browse = RunModel(df_input_browse)
        result_stream = RunModel(df_input_stream)

    except Exception as e:
        msg = f'Error in Model Running: \n{str(e)}'
        raise RoiException(msg)
    try:
        app.logger.info("Reformat result")
        # res = output_merge(result_text, result_browse, result_stream)
        # detail_res, sum_res = final_output(res, df_factor, fleet.to_dict('records'), share.to_dict('records'), price.to_dict('records'))
        #
        # app.logger.info(f"--> sum: \n{sum_res}")
        # app.logger.info(f"--> detail: \n{detail_res}")

        res_ls = dict()
        res_ls['result_text'] = result_text
        res_ls['result_browse'] = result_browse
        res_ls['result_stream'] = result_stream
        input_ls = dict()
        input_ls['fleet'] = fleet.to_dict('records')
        input_ls['share'] = share.to_dict('records')
        input_ls['price'] = price.to_dict('records')

        detail_res, sum_res = final_output_(res_ls, df_factor, input_ls)

        app.logger.info(f"--> sum: \n{sum_res}")
        app.logger.info(f"--> detail: \n{detail_res}")

        print(detail_res)
        print(sum_res)
    except Exception as e:
        msg = f'Error in Result Reformatting: \n{str(e)}'
        raise RoiException(msg)

    return render_template('output.html', detail_result=detail_res, sum_result=sum_res,
                           input_form=input_form, flight_ls=flight_ls, fleet_ls=fleet_ls)


@app.route("/session", methods=['GET', 'POST'])
def session_check():
    login = session.get('login', None)

    return jsonify(login)


@app.route("/dev_session", methods=['GET', 'POST'])
def def_session():
    info = {
        'user' : 'test'
    }
    session['login'] = info
    login = session.get('login', None)

    return jsonify(login)


@app.route("/logout_cognito", methods=['GET', 'POST'])
def logout_cognito():
    conn = get_conn(app)

    app.logger.info("Click Logout Button!!!")
    app.logger.info("Redirect to Cognito Logout URL")
    return redirect(conn.oauth2_logout())


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    app.logger.info("Complete Cognito Logout!!! Start to clean Flask Session.")

    login = session.get('login', None)
    app.logger.info(login)

    session.pop('login', None)

    return render_template('logout.html', login=login)


if __name__ == "__main__":
    app.config['env'] = 'test'

    flaskrun(app, context)
    # python pyroi.py -P 5000
    # app.run(ssl_context=context)

#
# [('airline_region', 'Americas'),
#  ('fleet_type', '0'), ('fleet_type', '0'), ('fleet_type', '1'), ('fleet_type', '1'),
#  ('ac_type', 't1'), ('ac_type', 't2'), ('ac_type', 't3'), ('ac_type', 't4'),
#  ('ac_cnt', '10'), ('ac_cnt', '20'), ('ac_cnt', '30'), ('ac_cnt', '40'),
#  ('st_cnt', '100'), ('st_cnt', '200'), ('st_cnt', '300'), ('st_cnt', '400'),
#  ('eco_cnt', '80'), ('eco_cnt', '160'), ('eco_cnt', '200'), ('eco_cnt', '300'),
#  ('f_dur', '2'), ('f_dur', '10'), ('f_dur', '5'), ('f_dur', '10'),
#  ('f_per', '10'), ('f_per', '20'), ('f_per', '30'), ('f_per', '40'),
#  ('service_ife', '0'), ('service_ife', '0'), ('service_ife', '0'), ('service_ife', '0'),
#  ('service_tv', '0'), ('service_tv', '0'), ('service_tv', '0'), ('service_tv', '0'),
#  ('service_phone', '0'), ('service_phone', '0'), ('service_phone', '0'), ('service_phone', '0'),
#  ('service_media', '0'), ('service_media', '0'), ('service_media', '0'), ('service_media', '0'),
#  ('flight_type', '0'), ('flight_type', '0'), ('flight_type', '0'), ('flight_type', '1'), ('flight_type', '1'),
#  ('orig_reg', 'Americas'), ('orig_reg', 'Europe'), ('orig_reg', 'Japan'), ('orig_reg', 'Americas'), ('orig_reg', 'Japan'),
#  ('dest_reg', 'Americas'), ('dest_reg', 'Europe'), ('dest_reg', 'Japan'), ('dest_reg', 'Americas'), ('dest_reg', 'Japan'),
#  ('tt_flt', '50'), ('tt_flt', '30'), ('tt_flt', '20'), ('tt_flt', '40'), ('tt_flt', '60'),
#  ('ld_fct', '50'), ('ld_fct', '80'), ('ld_fct', '80'), ('ld_fct', '80'), ('ld_fct', '80'),
#  ('nt_flt', '10'), ('nt_flt', '10'), ('nt_flt', '20'), ('nt_flt', '10'), ('nt_flt', '10'),
#
#  ('price_per_mb', '10'), ('pac_pct', '40'), ('air_pct', '30'), ('wisp_pct', '30'),
#
#  ('price_text', '10'), ('num_text', '10'), ('unit_text', 'mb'),
#  ('text_free', '0'), ('price_browse', '20'), ('num_browse', '20'),
#  ('unit_browse', 'mb'), ('browse_free', '0'), ('price_stream', '75'),
#  ('num_stream', '100'), ('unit_stream', 'mb'), ('stream_free', '0')
#  ]
