import os
import pickle
import logging
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

import warnings

try:
    from constant import MB_PATH, TR_PATH, ROUTE_TRANS_PATH
except:
    from .constant import MB_PATH, TR_PATH, ROUTE_TRANS_PATH

warnings.filterwarnings("ignore")

pd.option_context('display.max_columns', 35)

logger = logging.getLogger(__name__)

MB_model = pickle.load(open(MB_PATH, 'rb'))
TR_model = pickle.load(open(TR_PATH, 'rb'))

# print('\n\n\nFLEET DATAFRAME:', fleet)  # jinghan
# print('\n\n\nPRICE DATAFRAME:', price)  # jinghan
# print('\n\n\nCONTRACT DATAFRAME:', share)  # jinghan
# print('\n\n\nFLEET DATAFRAME:', flight)  # jinghan

#
###############################################################
#################      Load Model     #########################
###############################################################


# Load Model from pickle file
###############################################################
##############          Load Data     #########################
###############################################################

def loadcsv(f_path,fname):
    df = pd.read_csv(f_path.format(fname))
    return df

f_data = r'./data/{}.csv'

######### Load region translation table #######################
df_region_trans = pd.read_csv(ROUTE_TRANS_PATH)


###########  Sample Generator for Flight Info  ###############

def SampleInput(df, TestSize=0.2, RandomState=23):
    x = df.drop(['Airline'], axis=1)

    # stratified sampling by Category
    y_ss = x.pop('Category')
    x_train, x_test, y_train, y_test = train_test_split(x, y_ss,\
                                                        test_size=TestSize,\
                                                        stratify=y_ss,\
                                                        random_state=RandomState)

    # Generate flight group id
    x_test.reset_index(inplace=True, drop=True)
    x_test.reset_index(inplace=True)
    x_test.rename(columns={'index':'Flight_Group'}, inplace=True)

    # Generate flight percentage
    size = x_test.shape[0]
    flight_pct = np.random.dirichlet(np.ones(size), size=1)
    flight_pct = flight_pct[0] * 100
    x_test['Flight_Pct'] = np.asarray(flight_pct)

    print('STRATIFIED DATA:')
    print('training size:{}'.format(x_train.shape))
    print('test size:{}'.format(x_test.shape))
    print(x_test.head())

    return x_test
#print(MB_model)
#print(TR_model)


###############################################################
###############    UI Input Translation    ####################
###############################################################




def ui_translation(df_flight, df_price, df_fleet, df_contract):

    # convert data type for four input dataframes
    df_fleet.drop(['AC_Type'], axis=1, inplace=True)
    df_fleet = df_fleet.astype('float64')

    num_col_flight = df_flight.columns.difference(['Orig_Region', 'Dest_Region'])
    df_flight[num_col_flight] = df_flight[num_col_flight].astype('float64')

    num_col_price = df_price.columns.difference(['unit_text', 'unit_browse', 'unit_stream'])
    df_price[num_col_price] = df_price[num_col_price].astype('float64')

    num_col_contract = df_contract.columns.difference(['airline_region'])
    df_contract[num_col_contract] = df_contract[num_col_contract].astype('float64')



    # Calculated weighted average fleet info for both short-haul and long-haul fleets

    def fleet_weighted(df_fleet):
        df_fleet['flight_count_weighted'] = df_fleet['AC_Count'] * df_fleet['Flight_Per_AC']
        df_fleet['weight'] = df_fleet['flight_count_weighted']/(df_fleet['flight_count_weighted'].sum())
        df_fleet['Seat_Count_weighted'] = df_fleet['Seat_Count'] * df_fleet['weight']
        df_fleet['Eco_Count_weighted'] = df_fleet['Eco_Count'] * df_fleet['weight']
        df_fleet['Flight_Duration_weighted'] = df_fleet['Flight_Duration'] * df_fleet['weight']
        df_fleet['IFE_weighted'] = df_fleet['IFE'] * df_fleet['weight']
        df_fleet['TV_weighted'] = df_fleet['TV'] * df_fleet['weight']
        df_fleet['Phone_weighted'] = df_fleet['Phone'] * df_fleet['weight']
        df_fleet['OneMedia_weighted'] = df_fleet['OneMedia'] * df_fleet['weight']
        col = df_fleet.columns.str.contains('weighted')
        weighted_fleet = df_fleet[df_fleet.columns[col]]
        weighted_fleet = weighted_fleet.sum().to_frame().transpose()
        weighted_fleet['Flight_Type'] = df_fleet.Fleet_Type.max()
        weighted_fleet.rename(columns={'flight_count_weighted': 'flight_count_pre',
                                       'Seat_Count_weighted': 'Seat_Count',
                                       'Eco_Count_weighted': 'Economy_Seat_Count',
                                       'Flight_Duration_weighted': 'Flight_Duration',
                                       'IFE_weighted': 'IFE',
                                       'TV_weighted': 'TV',
                                       'Phone_weighted': 'Phone',
                                       'OneMedia_weighted': 'OneMedia'}, inplace=True)
        return weighted_fleet


    sh_fleet = fleet_weighted(df_fleet[df_fleet.Fleet_Type == 0])
    lh_fleet = fleet_weighted(df_fleet[df_fleet.Fleet_Type == 1])
    # print('^'*50)
    # print('THIS IS HOW weighted_fleet SH looks like')
    # print(sh_fleet)
    # print('^'*50)
    # print('THIS IS HOW weighted_fleet LH looks like')
    # print(lh_fleet)
    fleet_new = pd.concat([sh_fleet, lh_fleet], axis=0, ignore_index=True)
    # print('^'*50)
    # print('THIS IS HOW fleet_new looks like')
    # print(fleet_new)


    # Append new fleet info to flight info
    df_input = df_flight.merge(fleet_new, on='Flight_Type', how='left')


    # Convert Seat Count to Total Passenger Count
    df_input['TotalPassengers'] = df_input['Seat_Count'] * df_input['Load_Factor']/100

    # Convert Economy_Seat_Count to LnBusPassPercent
    df_input['BusPassPercent'] = 100 - 0.85 * (df_input['Economy_Seat_Count']/df_input['Seat_Count'])
    df_input.drop(['Economy_Seat_Count', 'Seat_Count'], axis=1, inplace=True)


    # Calculate true flight count and true flight percentage for each flight group

    df_input['total_flight_count'] = df_input['flight_count_pre'] * df_input['per_Total_Flight'] / 100

    # print('-' * 30, 'original df_input', '-' * 30)
    # print(df_input)

    # prepare night flights
    df_night = df_input.copy()
    df_night['Red_Eye'] = 1
    df_night['flight_count'] = df_night['total_flight_count'] * df_night['per_Night_Flight'] / 100
    # print('-' * 30, 'table df_night', '-' * 30)
    # print(df_night)

    # prepare day flights
    df_day = df_input.copy()
    df_day['Red_Eye'] = 0
    df_day['flight_count'] = df_day['total_flight_count'] * (100 - df_day['per_Night_Flight']) / 100
    # print('-' * 30, 'table df_day', '-' * 30)
    # print(df_night)

    # concat day flights and night flights together and then calculate true flight percentage
    df_input = pd.concat([df_night, df_day], axis=0, ignore_index=True)
    df_input['Flight_Pct'] = df_input['flight_count']/(df_input['flight_count'].sum()) * 100

    # clean columns
    df_input = df_input.reset_index()
    df_input.rename(columns={'index': 'Flight_Group'}, inplace=True)
    df_input.drop([#'Flight_ID',
                   'per_Total_Flight',
                   'Load_Factor',
                   'per_Night_Flight',
                   'total_flight_count',
                   'flight_count_pre'],
                  axis=1,
                  inplace=True)
    # print('^-^' * 30, 'df_input before df_factor', '^-^' * 30)
    # print(df_input)




    # extract base table for revenue calculation
    df_factor = df_input[['Flight_Group', 'Flight_Type', 'Flight_ID', 'TotalPassengers', 'Flight_Pct', 'flight_count', 'Flight_Duration']]
    df_factor['price_text'] = df_price.loc[0, 'text']
    df_factor['price_browse'] = df_price.loc[0, 'browse']
    df_factor['price_stream'] = df_price.loc[0, 'stream']
    df_factor['text_factor'] = df_factor['TotalPassengers'] * df_factor['flight_count'] * df_factor['price_text']
    df_factor['browse_factor'] = df_factor['TotalPassengers'] * df_factor['flight_count'] * df_factor['price_browse']
    df_factor['stream_factor'] = df_factor['TotalPassengers'] * df_factor['flight_count'] * df_factor['price_stream']
    df_factor = df_factor[['Flight_Group','Flight_Type', 'Flight_ID','Flight_Pct', 'flight_count', \
                           'text_factor', 'browse_factor', 'stream_factor', \
                           'Flight_Duration']]



    # Translate Region level to IATA level
    df_input['RouteRegion'] = df_input['Orig_Region'] + '-' + df_input['Dest_Region']
    df_input = df_input.merge(df_region_trans, on='RouteRegion', how='left')
    df_input = df_input.drop(['RouteRegion', 'Orig_Region', 'Dest_Region'], axis=1)



    # set variable order in line with model
    ordered_col = ['Flight_Group', 'Category',\
                   'MB', 'Hrs', 'Flight',\
                   'Orig_Country_frq', 'Dest_Country_frq', 'RouteCountry_frq',\
                   'OriginIATA_frq', 'DestinationIATA_frq', 'RouteIATA_frq',\
                   'RouteRegion_frq',\
                   #'Orig_Region_Americas', 'Orig_Region_Asia', 'Orig_Region_Europe','Orig_Region_Middle East', \
                   #'Dest_Region_Americas', 'Dest_Region_Asia', 'Dest_Region_Europe', 'Dest_Region_Middle East',\
                   'Flight_Duration',\
                   'IFE', 'OneMedia', 'Phone', 'TV', \
                   'Red_Eye',\
                   'TotalPassengers', 'BusPassPercent',\
                   'lnPrice_text', 'lnPrice_browse', 'lnPrice_stream']


    return df_input, df_factor, df_contract, ordered_col


def df_category(df_input, df_price, unit, num, category, ordered_col):

    df_input_category = df_input.copy()
    df_input_category.loc[:, 'Category'] = category

    # Append Price info and convert to LnPriceUSD
    df_input_category.loc[:, 'lnPrice_text'] = np.log1p(df_price.loc[0, 'text'])
    df_input_category.loc[:, 'lnPrice_browse'] = np.log1p(df_price.loc[0, 'browse'])
    df_input_category.loc[:, 'lnPrice_stream'] = np.log1p(df_price.loc[0, 'stream'])


    unit_cat = df_price.loc[0, unit]
    num_cat = df_price.loc[0, num]

    # parse the ProductName info for model
    if unit_cat =='mb':
        df_input_category.loc[:, 'MB'] = num_cat
        df_input_category.loc[:, 'Hrs'] = -1
        df_input_category.loc[:, 'Flight'] = 0
    elif unit_cat =='time':
        df_input_category.loc[:, 'Hrs'] = num_cat
        df_input_category.loc[:, 'MB'] = -1
        df_input_category.loc[:, 'Flight'] = 0
    elif unit_cat == 'flight':
        df_input_category.loc[:, 'Flight'] = 1
        df_input_category.loc[:, 'Hrs'] = -1
        df_input_category.loc[:, 'MB'] = -1
    else:
        print('Errors in Paring Price Info')

    # keep the feature order in line with model inputs
    df_input_category = df_input_category[ordered_col]


    return df_input_category




###############################################################
#############    Run Model to Get Outputs     #################
###############################################################

def RunModel(df_data,mb_model=MB_model, tr_model=TR_model):

    df_result = df_data[['Flight_Group']]
    df_data.drop(['Flight_Group'], axis=1,
                 inplace=True)
    MB = mb_model.predict(df_data)
    TR = tr_model.predict(df_data)
    df_result.loc[:, 'TotalUsageMB'] = MB
    df_result.loc[:, 'TakeRate'] = TR

    # print(df_result.describe())

    return df_result





if __name__ == '__main__':
    ######## Load Sample Input for fleet and price  ###############
    df_fleet = pd.read_csv(os.path.join('.','data','sample_fleet.csv'))
    df_price = pd.read_csv(os.path.join('.','data','sample_price.csv'))
    df_flight = pd.read_csv(os.path.join('.','data','sample_flight.csv'))
    df_contract = pd.read_csv(os.path.join('.','data','sample_contract.csv'))
    print(df_fleet)
    print(df_price)
    print(df_flight)
    print(df_contract)

    df_input, df_factor, df_contract, col_order = ui_translation(df_flight, df_price, df_fleet, df_contract)

    print('-'*20, 'Input table', '-'*20)
    print(df_input.describe())
    print(df_input.head())
    print(df_input.isnull().sum())
    print('-' * 20, 'factor table', '-'*20)
    print(df_factor)
    print('-' * 20, 'contract', '-'*20)
    print(df_contract)
    print(col_order)
    print('-' * 20)

    df_input_text = df_category(df_input, df_price, \
                                unit='unit_text', num='num_text', \
                                category=1, ordered_col=col_order)
    df_input_browse = df_category(df_input, df_price, \
                                  unit='unit_browse', num='num_browse', \
                                  category=2, ordered_col=col_order)
    df_input_stream = df_category(df_input, df_price, \
                                  unit='unit_stream', num='num_stream', \
                                  category=3, ordered_col=col_order)

    # Print translation result
    # print(df_input_text)
    # print(df_input_browse)
    # print(df_input_stream)

    result_text = RunModel(df_input_text)
    result_browse = RunModel(df_input_browse)
    result_stream = RunModel(df_input_stream)


    print(result_text.groupby('Flight_Group').describe())
    print(result_browse.groupby('Flight_Group').describe())
    print(result_stream.groupby('Flight_Group').describe())
