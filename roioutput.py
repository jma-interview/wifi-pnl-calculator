import pandas as pd
import numpy as np
from functools import reduce

try:
    from constant import group_col, out_col, out_map, out_cat, COST_FACTOR, APP_MB_EUJ, \
    APP_TR_EUJ, APP_MB_MAA, APP_TR_MAA
except:
    from .constant import group_col, out_col, out_map, out_cat, COST_FACTOR, APP_MB_EUJ, \
    APP_TR_EUJ, APP_MB_MAA, APP_TR_MAA


# PROCESS
# 1. Merge 3 DFs
# 2. Detail Page
#   2.1 Detail Parse for TR -> get 25%, 50% and 75% for low, media and high -> description, get result based on mapping, output result
#   2.2 FOC logic
#       2.2.1 TR
#       2.2.2 MB
# 3. Summary Table
#   3.1 Bottom table in summary page - calculate weighted average with medium value of each flight group - for TR
#       -- medium value -> from output_transfer (50%), weight -> df_factor - Flight_Pct
#   3.2 TRPY (Total Rev Per Year) - Rev of all flight group
#       Rev of single flight group
#       - Text_TR * Text_Factor + Browse_TR * Browse_Factor + Stream_TR * Stream_Factor
#   3.3 different REV
#       3.3.1 PAC REV WHOLE

#       3.3.2 Rev Share
#       Weighted Rev share for PAC, Airline, 3rd Party WISP
#       - TRPY * share_pct
#       -- share_pct -> share table
#   3.4 APRA per month (Average Rev Per Aircraft)
#       TRPY / ac_count / 12
#       -- ac_count -> fleet
#   3.5 AUPF (Average Usage Per Flight) - for MB
#       Median_MB weighted by flight_pct
#       -- medium value -> from output_transfer (25%), weight -> df_factor - Flight_Pct
#
#   3.6.0 Total MB
#       AUPF * Total Flight OR
#       df['total_MB'] = df['text_MB'] * df['flight_count'] + df['browse_MB'] * df['flight_count'] + df['stream_MB'] * df['flight_count']
#   3.6 Whole Sale Rev
#       Total MB * Price
#   3.7 Total Cost Per Year($)
#       Whole Sale Rev of PAC / Price_Per_MB * 0.1
#   3.8 Suggest Contact Type / Profit
#       compare WholeSale_Rev vs. Rev_Share_Pac, suggest the one with more profit
#       profit = max(WholeSale_Rev, Rev_Share_Pac) - Total Cost er Year($)


append_mb_mapping = {
    "Americas" : APP_MB_EUJ ,
    "Europe" : APP_MB_EUJ,
    "Middle East": APP_MB_MAA,
    "Japan" : APP_MB_EUJ ,
    #"Oceania",
    "Africa": APP_MB_MAA,
    "Asia": APP_MB_MAA
}
append_tr_mapping = {
    "Americas" : APP_TR_EUJ ,
    "Europe" : APP_TR_EUJ,
    "Middle East": APP_TR_MAA,
    "Japan": APP_TR_EUJ,
    #"Oceania",
    "Africa": APP_TR_MAA,
    "Asia": APP_TR_MAA
}

# out_map = {
#     None: 'min',
#     'low': '25%',
#     None: '50%',
#     'median': '75%',
#     'high': 'max',
# }
#
# out_cat = ['text', 'browse', 'stream']
#
# result_col = ['_'.join((c, v)) for c in out_cat for v in out_map.keys() if v]
#

# generate col list for
result_col = []
for c in out_cat:
    for v in out_map.keys():
        if v:
            result_col.append('_'.join((c, v)))
    result_col.append('_'.join((c, 'MB')))
# ['text_low', 'text_median', 'text_high', 'text_MB', 'browse_low', 'browse_median', 'browse_high', 'browse_MB', 'stream_low', 'stream_median', 'stream_high', 'stream_MB']

def output_value(input_value):
    try:
        return "{:,}".format(int(input_value))
    except:
        return input_value

def output_transfer(df):
    """
    from result df, generate description of data and generate output based on

    :param df:
    :return:
    """
    # get describe for each group
    df_ = df.groupby(group_col).describe().reset_index()
    # update df from multiple level index to single level index - generate standard column name
    df_.columns = ['_'.join(filter(None, col)) for col in df_.columns]

    # based on output_map, get columns need to output
    out_maps = [group_col] + ['_'.join((out_col, v)) for k, v in out_map.items() if k]
    # based on output_map, get output column name of final result
    keys = [group_col] + [k for k, v in out_map.items() if k]

    # + ['TotalUsageMB_50%']
    # use 25% MB value as usage for calculation - backend only
    r = df_[out_maps + ['TotalUsageMB_25%']]
    # name
    r.columns = keys + ['MB_Median']

    return r


def output_merge(text, browse, stream):

    text_r = output_transfer(text)
    browse_r = output_transfer(browse)
    stream_r = output_transfer(stream)

    dfs = [text_r, browse_r, stream_r]

    df_final = reduce(lambda left, right: pd.merge(left, right, on=group_col), dfs)

    df_final.columns = [group_col] + result_col

    # ['text_low', 'text_median', 'text_high', 'text_MB', 'browse_low', 'browse_median', 'browse_high', 'browse_MB', 'stream_low', 'stream_median', 'stream_high', 'stream_MB']

    return df_final


def append_tr(foc_ind, airline_region, flight_dur):
    """
    Calculate TR that need to be appended for FOC plan
    If do provide FOC plan, check TR need to append, return
    If do NOT provide POC plan, return 0
    :param free_ind:
    :param airline_region:
    :param flight_dur:
    :return:
    """
    if int(foc_ind) == 1:
        append_config_file = append_tr_mapping.get(airline_region)
        append_config = pd.read_csv(append_config_file)
        filter = append_config.loc[append_config['Threshold'] >= flight_dur]
        return filter['AvgTR'].iloc[0]
    else:
        return 0

def append_mb(foc_ind, airline_region, flight_dur):
    """
    Calculate MB that need to be appended for FOC plan
    If do provide FOC plan, check MB need to append, return
    If do NOT provide POC plan, return 0
    :param free_ind:
    :param airline_region:
    :param flight_dur:
    :return:
    """
    if int(foc_ind) == 1:
        append_config_file = append_mb_mapping.get(airline_region)
        append_config = pd.read_csv(append_config_file)
        filter = append_config.loc[append_config['Threshold'] >= flight_dur]
        return filter['AvgMB'].iloc[0]
    else:
        return 0


def append_foc_value(df, share, price):
    # load input from fleet and price
    airline_region = share[0]['airline_region']

    free_text = price[0]['free_text']
    free_browse = price[0]['free_browse']
    free_stream = price[0]['free_stream']

    # create original copy of TR and MB, will be used for calculation of Rev
    df['text_low_org'] = df['text_low']
    df['text_median_org'] = df['text_median']
    df['text_high_org'] = df['text_high']
    df['text_MB_org'] = df['text_MB']

    df['browse_low_org'] = df['browse_low']
    df['browse_median_org'] = df['browse_median']
    df['browse_high_org'] = df['browse_high']
    df['browse_MB_org'] = df['browse_MB']

    df['stream_low_org'] = df['stream_low']
    df['stream_median_org'] = df['stream_median']
    df['stream_high_org'] = df['stream_high']
    df['stream_MB_org'] = df['stream_MB']

    # Calculate TR and MB need to be appended to org value, will be used for calculation of Cost
    df['append_text_tr'] = df.apply(lambda x: append_tr(free_text, airline_region, x.Flight_Duration), axis=1)
    df['append_text_mb'] = df.apply(lambda x: append_mb(free_text, airline_region, x.Flight_Duration), axis=1)

    df['append_browse_tr'] = df.apply(lambda x: append_tr(free_browse, airline_region, x.Flight_Duration), axis=1)
    df['append_browse_mb'] = df.apply(lambda x: append_mb(free_browse, airline_region, x.Flight_Duration), axis=1)

    df['append_stream_tr'] = df.apply(lambda x: append_tr(free_stream, airline_region, x.Flight_Duration), axis=1)
    df['append_stream_mb'] = df.apply(lambda x: append_mb(free_stream, airline_region, x.Flight_Duration), axis=1)

    # Append TR and MB
    df['text_low'] = df['text_low'] + df['append_text_tr']
    df['text_median'] = df['text_median'] + df['append_text_tr']
    df['text_high'] = df['text_high'] + df['append_text_tr']
    df['text_MB'] = df['text_MB'] + df['append_text_mb']

    df['browse_low'] = df['browse_low']+ df['append_browse_tr']
    df['browse_median'] = df['browse_median'] + df['append_browse_tr']
    df['browse_high'] = df['browse_high'] + df['append_browse_tr']
    df['browse_MB'] = df['browse_MB'] + df['append_browse_mb']

    df['stream_low'] = df['stream_low']+ df['append_stream_tr']
    df['stream_median'] = df['stream_median'] + df['append_stream_tr']
    df['stream_high'] = df['stream_high'] + df['append_stream_tr']
    df['stream_MB'] = df['stream_MB'] + df['append_stream_mb']

    return df

def gen_detail_result(df):
    """
    generate result set for detail page -- need information based on merged df with append information
    :param df:
    :return:
    """

    df_detail = df[['Flight_Group', 'text_low', 'text_median', 'text_high', 'text_MB',
                    'browse_low', 'browse_median', 'browse_high', 'browse_MB', 'stream_low',
                    'stream_median', 'stream_high', 'stream_MB', 'total_low', 'total_median', 'total_high']]
    return df_detail


def append_summary_information(df):
    """
    calculate weighted average with medium value of each flight group - for TR
    #-- medium value -> from output_transfer (50%), weight -> df_factor - Flight_Pct
    append to orig df
    :param df:
    :return:
    """

    # append total number for each type
    for k in out_map.keys():
        if k:
            df['_'.join(('total', k))] = df[['_'.join((c, k)) for c in out_cat]].sum(axis=1)

    # get weighted take rate for each cat
    for c in out_cat:
        df['_'.join((c, 'weight'))] = df['_'.join((c, 'median'))] * df['Flight_Pct'] / 100.0

    return df


def gen_summary_table(df):
    """
    generate result set for detail page -- need information based on merged df with append information
    :param df:
    :return:
    """

    df_summary = df[['text_weight', 'browse_weight', 'stream_weight']]

    # calculate sum of all flight groups
    res_sum = df_summary.sum()
    res_sum['total_TR'] = res_sum['text_weight'] + res_sum['browse_weight'] + res_sum['stream_weight']
    res_sum = res_sum.round(2)

    return res_sum



def calculate_total_rev(df):
    """
    #   3.2 TRPY (Total Rev Per Year) - Rev of all flight group
    #       Rev of single flight group
    #       - Text_TR * Text_Factor + Browse_TR * Browse_Factor + Stream_TR * Stream_Factor
    :return:
    """
    rev_df = df['text_median_org'] * df['text_factor'] / 100 + \
             df['browse_median_org'] * df['browse_factor'] / 100 + \
             df['stream_median_org'] * df['stream_factor'] / 100
    res = rev_df.sum()
    return res


def calculate_total_mb(df):
    """
    calculate total MB
    :param df:
    :return:
    """
    # get total MB per group
    total_mb_df = df['text_MB'] * df['flight_count'] + \
          df['browse_MB'] * df['flight_count'] + \
          df['stream_MB'] * df['flight_count']
    total_mb = total_mb_df.sum()

    return total_mb

def calculate_total_cost(df):
    """
    calculate total cost with MB
    :param df:
    :return:
    """
    total_mb = calculate_total_mb(df)

    # get total cost with MB
    total_cost = total_mb * COST_FACTOR
    return total_cost

def calculate_total_profit(df):
    """
    calculate total profit
    :param df:
    :return:
    """
    rev = calculate_total_rev(df)
    cost = calculate_total_cost(df)
    res = rev - cost
    return res


def calculate_pac_rev_whole(df, share):
    """
    #   3.3.1 Calculate wholesale Rev
    :param df:
    :return:
    """
    total_mb = calculate_total_mb(df)
    whole_rev = total_mb * float(share[0].get('price_per_mb'))

    return whole_rev


def calculate_pac_rev_share(df, share):
    """
    #   3.3.2 Calculate share Rev
    :param df:
    :return:
    """
    total_rev = calculate_total_rev(df)

    share_rev_pac = total_rev * float(share[0].get('pac_pct')) / 100.0
    share_rev_air = total_rev * float(share[0].get('air_pct')) / 100.0
    share_rev_3rd = total_rev * float(share[0].get('wisp_pct')) / 100.0
    return share_rev_pac, share_rev_air, share_rev_3rd


def calculate_total_flight(df):
    """

    :param df:
    :return:
    """
    flight_cnt_df = df['flight_count']

    flight_cnt = flight_cnt_df.sum()
    return flight_cnt


def calculate_arpa(df, fleet):
    """

    :param df:
    :param fleet:
    :return:
    """
    print(fleet)
    ac_count = sum([int(f['AC_Count']) for f in fleet ])
    arpa = calculate_total_rev(df) / float(ac_count) / 12.0

    return arpa


def calculate_avg_usage_per_flight(df):
    """

    :param df:
    :return:
    """
    total_mb = calculate_total_mb(df)
    flight_cnt = calculate_total_flight(df)
    avg_mb = total_mb / flight_cnt

    return avg_mb

def calculate_total_profit(df):
    """
    calculate total profit: total revenue - total cost
    :param df:
    :return:
    """
    total_rev = calculate_total_rev(df)
    total_cost = calculate_total_cost(df)

    total_profit = total_rev - total_cost

    return total_profit

def calculate_session_tr(df):
    res = gen_summary_table(df)
    return res.total_TR

def calculate_suggestion(df, share, fleet):
    pac_rev_whole = calculate_pac_rev_whole(df, share)
    pac_rev_share = calculate_pac_rev_share(df, share)[0]
    total_cost = calculate_total_cost(df)
    ac_count = sum([int(f['AC_Count']) for f in fleet ])

    if pac_rev_share > pac_rev_whole:
        suggest = 'Revenue Share'
        profit = pac_rev_share - total_cost
        arpa = pac_rev_share / float(ac_count) / 12.0

    else:
        suggest = 'Wholesale-TB'
        profit = pac_rev_whole - total_cost
        arpa = pac_rev_whole / float(ac_count) / 12.0

    return suggest, profit, arpa

def final_output_(result, factor, input):
# def final_output_(result_text, result_browse, result_stream, factor, fleet, share, price):
#         res = output_merge(result_text, result_browse, result_stream)
#         detail_res, sum_res = final_output(res, df_factor, fleet.to_dict('records'), share.to_dict('records'), price.to_dict('records'))
    res_text = result.get('result_text')
    res_browse = result.get('result_browse')
    res_stream = result.get('result_stream')
    input_fleet = input.get('fleet')
    input_share = input.get('share')
    input_price = input.get('price')

    merged_output = output_merge(res_text, res_browse, res_stream)
    df = pd.merge(merged_output, factor, on=group_col)

    # s1 - append FOC information
    df = append_foc_value(df, input_share, input_price)

    # s2 - append summary information
    df = append_summary_information(df)

    # s3 - result calculation
    total_rev = calculate_total_rev(df)

    rev_pac_whole = calculate_pac_rev_whole(df, input_share)

    rev_share_pac, rev_share_air, rev_share_3rd = calculate_pac_rev_share(df, input_share)

    # arpa = calculate_arpa(df, input_fleet)

    usage_per_flight = calculate_avg_usage_per_flight(df)

    total_cost = calculate_total_cost(df)

    suggestion, profit, arpa = calculate_suggestion(df, input_share, input_fleet)

    session_tr = calculate_session_tr(df)

    # s_final - generate result set
    detail_list = ['Flight_Group', 'text_low', 'text_median', 'text_high', 'text_MB',
                   'browse_low', 'browse_median', 'browse_high', 'browse_MB', 'stream_low',
                   'stream_median', 'stream_high', 'stream_MB', 'total_low', 'total_median', 'total_high']


    summary_table = gen_summary_table(df)
    summary_res = summary_table.to_dict()

    summary_res['total_REV'] = output_value(total_rev)
    summary_res['total_REV_whole'] = output_value(rev_pac_whole)


    if int(input_share[0].get('pac_pct', 0)) + int(input_share[0].get('air_pct', 0)) + int(input_share[0].get('wisp_pct', 0)) > 0:
        summary_res['share'] = 1
    else:
        summary_res['share'] = 0
    summary_res['total_REV_pac'] = output_value(rev_share_pac)
    summary_res['total_REV_air'] = output_value(rev_share_air)
    summary_res['total_REV_3rd'] = output_value(rev_share_3rd)
    summary_res['arpa'] = output_value(arpa)
    summary_res['avg_MB'] = output_value(usage_per_flight)
    summary_res['total_COST'] = output_value(total_cost)
    summary_res['total_REV'] = output_value(total_rev)
    summary_res['Profit'] = output_value(profit)
    summary_res['Suggest'] = output_value(suggestion)
    summary_res['Session_TR'] = output_value(session_tr)

    # res_detail = df[detail_list].round(2).to_dict('records')
    #
    res_detail = df[detail_list]
    res_detail = res_detail.merge(factor[['Flight_Group', 'Flight_Type', 'Flight_Pct']], on='Flight_Group')
    res_detail['Group_Pct'] = res_detail.Flight_Pct / \
                              res_detail.groupby('Flight_Type')['Flight_Pct'].transform('sum') \
                              * 100
    cal_col = [c for c in list(res_detail.columns) if
               c.startswith('browse') or c.startswith('stream') or c.startswith('text') or c.startswith('total')]

    for c in cal_col:
        res_detail[c] = res_detail[c] * res_detail['Group_Pct'] / 100
    detail_res = res_detail.groupby('Flight_Type')[cal_col].sum().round(2).reset_index().to_dict('records')
    #
    # detail_res = df[detail_list].round(2).to_dict('records')
    #
    return detail_res, summary_res

def final_output(merged_output, factor, fleet, share, price):
    print(fleet)
    ac_count = sum([f['AC_Count'] for f in fleet ])
    airline_region = share[0]['airline_region']
    free_text = price[0]['free_text']
    free_browse = price[0]['free_browse']
    free_stream = price[0]['free_stream']

    df = pd.merge(merged_output, factor, on=group_col)
    print(df.to_dict('records'))

    # append tr and mb for free of cost
    df['append_text_tr'] = df.apply(lambda x: append_tr(free_text, airline_region, x.Flight_Duration), axis=1)
    df['append_text_mb'] = df.apply(lambda x: append_mb(free_text, airline_region, x.Flight_Duration), axis=1)

    df['append_browse_tr'] = df.apply(lambda x: append_tr(free_browse, airline_region, x.Flight_Duration), axis=1)
    df['append_browse_mb'] = df.apply(lambda x: append_mb(free_browse, airline_region, x.Flight_Duration), axis=1)

    df['append_stream_tr'] = df.apply(lambda x: append_tr(free_stream, airline_region, x.Flight_Duration), axis=1)
    df['append_stream_mb'] = df.apply(lambda x: append_mb(free_stream, airline_region, x.Flight_Duration), axis=1)


    df['text_low_org'] = df['text_low']
    df['text_median_org'] = df['text_median']
    df['text_high_org'] = df['text_high']
    df['text_MB_org'] = df['text_MB']

    df['browse_low_org'] = df['browse_low']
    df['browse_median_org'] = df['browse_median']
    df['browse_high_org'] = df['browse_high']
    df['browse_MB_org'] = df['browse_MB']

    df['stream_low_org'] = df['stream_low']
    df['stream_median_org'] = df['stream_median']
    df['stream_high_org'] = df['stream_high']
    df['stream_MB_org'] = df['stream_MB']

    df['text_low'] = df['text_low'] + df['append_text_tr']
    df['text_median'] = df['text_median'] + df['append_text_tr']
    df['text_high'] = df['text_high'] + df['append_text_tr']
    df['text_MB'] = df['text_MB'] + df['append_text_mb']

    df['browse_low'] = df['browse_low']+ df['append_browse_tr']
    df['browse_median'] = df['browse_median'] + df['append_browse_tr']
    df['browse_high'] = df['browse_high'] + df['append_browse_tr']
    df['browse_MB'] = df['browse_MB'] + df['append_browse_mb']

    df['stream_low'] = df['stream_low']+ df['append_stream_tr']
    df['stream_median'] = df['stream_median'] + df['append_stream_tr']
    df['stream_high'] = df['stream_high'] + df['append_stream_tr']
    df['stream_MB'] = df['stream_MB'] + df['append_stream_mb']

    print(df.to_dict('records'))

    # append total number for each type
    for k in out_map.keys():
        if k:
            df['_'.join(('total', k))] = df[['_'.join((c, k)) for c in out_cat]].sum(axis=1)

    # get weighted take rate for each cat
    for c in out_cat:
        df['_'.join((c, 'weight'))] = df['_'.join((c, 'median'))] * df['Flight_Pct'] / 100.0

    # get total MB per group

    # done
    df['total_MB'] = df['text_MB'] * df['flight_count'] + df['browse_MB'] * df['flight_count'] + df['stream_MB'] * df[
        'flight_count']

    # done
    df['total_REV'] = df['text_median_org'] * df['text_factor'] / 100 + df['browse_median_org'] * df['browse_factor'] / 100 + \
                      df['stream_median_org'] * df['stream_factor'] / 100
    # done
    df['total_COST'] = df['total_MB'] * COST_FACTOR
    # done
    df['total_PROFIT'] = df['total_REV'] - df['total_COST']


    df_detail = df[['Flight_Group', 'text_low', 'text_median', 'text_high', 'text_MB',
                    'browse_low', 'browse_median', 'browse_high', 'browse_MB', 'stream_low',
                    'stream_median', 'stream_high', 'stream_MB', 'total_low', 'total_median', 'total_high']]

    df_sum = df[['total_low', 'total_median', 'total_high', 'text_weight', 'browse_weight', 'stream_weight', 'total_MB',
                 'flight_count', 'total_REV', 'total_COST', 'total_PROFIT']]


    res_detail = df_detail.round(2)

    # calculate sum of all flight groups
    res_sum = df_sum.sum()

    res_sum['avg_MB'] = res_sum['total_MB'] / res_sum['flight_count']
    res_sum['arpa'] = res_sum['total_REV'] / float(ac_count) / 12.0
    res_sum['total_TR'] = res_sum['text_weight'] + res_sum['browse_weight'] + res_sum['stream_weight']
    res_sum = res_sum.round(2)
    print(res_sum.dtypes)

    res_dict = res_sum.to_dict()
    res_dict['total_REV_'] = res_dict['total_REV']
    # append whole sale rev
    res_dict['total_REV_whole'] = res_dict['total_MB'] * float(share[0].get('price_per_mb'))
    res_dict['total_PROFIT_whole'] = output_value(res_dict['total_REV_whole'] - res_dict['total_COST'])
    res_dict['total_REV_whole'] = output_value(res_dict['total_REV_whole'])

    res_dict['avg_MB_'] = res_dict['avg_MB']

    res_dict['total_REV'] = output_value(res_dict['total_REV'])
    res_dict['total_MB'] = output_value(res_dict['total_MB'])
    res_dict['avg_MB'] = output_value(res_dict['avg_MB'])

    res_dict['arpa'] = output_value(res_dict['arpa'])
    res_dict['total_COST'] = output_value(res_dict['total_COST'])
    res_dict['total_PROFIT'] = output_value(res_dict['total_PROFIT'])
    # SHARE_COL = ['whole','share','pac_pct', 'air_pct', 'wisp_pct']
    share = share[0]

    if int(share.get('pac_pct', 0)) + int(share.get('air_pct', 0)) + int(share.get('wisp_pct', 0)) > 0:
        print('share')
        res_dict['share'] = 1
        res_dict['total_REV_pac'] = output_value(res_dict['total_REV_'] * float(share.get('pac_pct')) / 100.0)
        res_dict['total_REV_air'] = output_value(res_dict['total_REV_'] * float(share.get('air_pct')) / 100.0)
        res_dict['total_REV_3rd'] = output_value(res_dict['total_REV_'] * float(share.get('wisp_pct')) / 100.0)
    else:
        print('no share')
        res_dict['share'] = 0


    share_ind = float(share.get('pac_pct')) * float(res_dict['total_REV_']) / 100.0 / float(res_sum['flight_count'])
    whole_ind = float(share.get('price_per_mb')) * float(res_dict['avg_MB_'])
    print('check ind')
    print(f'share_ind:{share_ind}')
    print(f'whole_ind:{whole_ind}')

    if share_ind > whole_ind:
        suggest = 'Revenue Share'
        profit = res_dict['total_PROFIT']
    else:
        suggest = 'Wholesale-TB'
        profit = res_dict['total_PROFIT_whole']

    res_dict['Suggest'] = suggest
    res_dict['Profit'] = profit

    # for new output - weight group sum
    res_detail = res_detail.merge(factor[['Flight_Group', 'Flight_Type', 'Flight_Pct']], on = 'Flight_Group')
    res_detail['Group_Pct'] = res_detail.Flight_Pct / \
                              res_detail.groupby('Flight_Type')['Flight_Pct'].transform('sum') \
                              * 100
    cal_col = [c for c in list(res_detail.columns) if
               c.startswith('browse') or c.startswith('stream') or c.startswith('text') or c.startswith('total')]
    res_detail[cal_col] = res_detail[cal_col].mul(res_detail.Group_Pct, axis=0).div(100)
    res_detail_group = res_detail.groupby('Flight_Type')[cal_col].sum().round(2).reset_index()

    return res_detail_group.to_dict('records'), res_dict




def test_detail_output():
    df = pd.read_csv(TEST_OUTPUT_PATH)
    df_ = df.copy()
    df_[out_col] += 1
    df__ = df.copy()
    df__[out_col] += 2
    res = output_merge(df, df_, df__)

    SAMPLE_OUTPUT['detail'] = res.to_dict('records')
    print(SAMPLE_OUTPUT)
    return SAMPLE_OUTPUT





if __name__ == '__main__':
    pass

    # pd.options.display.max_rows = 50
    #
    # from InputTranslation import fleet_sample, price_sample, flight_sample, RunModel, ui_translation
    # #
    # # print(fleet_sample)
    # # print(price_sample)
    # # print(flight_sample)
    #
    # df_input_text, df_input_browse, df_input_stream, df_factor = ui_translation()
    # # print(df_input_text.columns)
    # # print('--------------------------------------\n')
    # # print(df_input_text)
    #
    # result_text = RunModel(df_input_text)
    # result_browse = RunModel(df_input_browse)
    # result_stream = RunModel(df_input_stream)
    #
    # detail_res = output_merge(result_text, result_browse, result_stream)
    # print(df_factor)
    #
    # print(detail_res)
    # detail_res.to_csv(r'S:\Business_Intelligence\Private\BI-Team\Jinghan\merged datasets\UI & Model test\details_jimmy.csv')
    #
    # detile_res, sum_res = final_output(detail_res, df_factor)
    #
    # from pprint import pprint
    # pprint(detile_res)
    # pprint(sum_res)
    #
    #
    # {'browse_weight': 16.011,
    #  'stream_weight': 8.068,
    #  'text_weight': 0.0,
    #  'total_COST': 5068.463,
    #  'total_MB': 45053.004,
    #  'total_PROFIT': -4559.434,
    #  'total_REV': 509.028,
    #  'total_high': 35.488,
    #  'total_low': 9.722,
    #  'total_median': 24.079}
    #


    # i = 1000000000.11
    #
    #
    # print(output_value(i))
    #
    # a = pd.DataFrame([[100.023], [1000.222]])
    # a.columns = ['c1']
    # print(a)
    #
    # a['c1'] = a['c1'].apply(output_value)
    # print(a)


    print(result_col)
    print(out_cat)

