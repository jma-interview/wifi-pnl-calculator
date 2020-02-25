import os

# cost of MB
COST_FACTOR = 0.1

# setup for output
group_col = 'Flight_Group'
out_col = 'TakeRate'
out_map = {
    None: 'min',
    'low': '25%',
    None: '50%',
    'median': '50%',
    'high': '75%',
}

out_cat = ['text', 'browse', 'stream']

# setup for folder
BASE_FOLDER = dir_path = os.path.dirname(os.path.realpath(__file__))
MODEL_FOLDER = os.path.join(BASE_FOLDER, 'model')
OUTPUT_FOLDER = os.path.join(BASE_FOLDER, 'output')
KEY_FOLDER = os.path.join(BASE_FOLDER, 'keys')

MB_MD = 'MB_model.pkl'
TR_MD = 'TR_model.pkl'
MB_MD_fake = 'MB_model_fake.pkl'
TR_MD_fake = 'TR_model_fake.pkl'
Route_Trans = 'Route_Translation.csv'

Append_mb_euusjpn = 'FOC_MB_EUUSJPN.csv'
Append_tr_euusjpn = 'FOC_TR_EUUSJPN.csv'
Append_mb_measaf = 'FOC_MB_MEASAF.csv'
Append_tr_measaf = 'FOC_TR_MEASAF.csv'

MB_PATH = os.path.join(MODEL_FOLDER, MB_MD)
TR_PATH = os.path.join(MODEL_FOLDER, TR_MD)
MB_PATH_fake = os.path.join(MODEL_FOLDER, MB_MD_fake)
TR_PATH_fake = os.path.join(MODEL_FOLDER, TR_MD_fake)

ROUTE_TRANS_PATH = os.path.join(MODEL_FOLDER, Route_Trans)

APP_MB_EUJ = os.path.join(MODEL_FOLDER, Append_mb_euusjpn)
APP_TR_EUJ = os.path.join(MODEL_FOLDER, Append_tr_euusjpn)
APP_MB_MAA = os.path.join(MODEL_FOLDER, Append_mb_measaf)
APP_TR_MAA = os.path.join(MODEL_FOLDER, Append_tr_measaf)

TEST_OUTPUT_FILE = 'sample_output.csv'
TEST_OUTPUT_PATH = os.path.join(OUTPUT_FOLDER, TEST_OUTPUT_FILE)



UI_CONFIG = {
    "region_ls": [
        "Americas",
        "Europe",
        "Middle East",
        "Japan",
        #"Oceania",
        "Africa",
        "Asia",
    ],
    "region": {
        "Americas": "Americas",
        "Europe": "Europe",
        "Middle East": "Middle East",
        #"Japan": "Japan",
        #"Oceania": "Oceania",
        "Africa": "Africa",
        "Asia": "Asia"
    },
    "price": {
        "text": {
            "min": 0,
            "max": 20,
            "default": 7,
            "global": "$1.25 to $16"
        },
        "browse": {
            "min": 0,
            "max": 35,
            "default": 15,
            "global": "$4.9 to $22.74"
        },
        "stream": {
            "min": 0,
            "max": 75,
            "default": 25,
            "global": "$8.9 to $69"
        },
    },
    "seat_count": {
        "min": 10,
        "max": 500,
        "default": 10
    }
}

# authneticatoin - AWS Cognito

cognito_pool = 'us-west-2_NJ1dWCJiV'
cognito_domain = 'https://pac-idam-userpool-prd.auth.us-west-2.amazoncognito.com'
cognito_client_id = '4dbh4toj0gq3en2enh2vnl6md4'
cognito_client_secret = 'ar6t5mbvbm0c9imku5e6dg4mthrcnf6kojgrhcgvtre0ufmt9nn'

#
local_host = 'https://127.0.0.1:5000/'
dev_url = 'https://roi-calculator-wifi-dev.nextcloud.aero/'
prod_url = 'https://roi-calculator-wifi.nextcloud.aero/'

# SSL Key
CRT_PATH = os.path.join(KEY_FOLDER, 'server.crt')
KEY_PATH = os.path.join(KEY_FOLDER, 'server.key')

