import pandas as pd

try:
    from exception import EmptyInputError, DataTypeException, DataRangeException
    from constant import UI_CONFIG
except:
    from .exception import EmptyInputError, DataTypeException, DataRangeException
    from .constant import UI_CONFIG

ADD_COL = ['airline_region', 'price_per_mb', 'pac_pct', 'air_pct', 'wisp_pct']
PRICE_COL = ['text', 'num_text', 'unit_text', 'free_text', 'browse', 'num_browse', 'unit_browse', 'free_browse',
             'stream', 'num_stream', 'unit_stream', 'free_stream']

FLIGHT_COL = ['Flight_ID', 'Flight_Type', 'Orig_Region', 'Dest_Region', 'per_Total_Flight', 'Load_Factor', 'per_Night_Flight']
FLEET_COL = ['Fleet_ID', 'Fleet_Type', 'AC_Type', 'AC_Count',  'Seat_Count', 'Eco_Count', 'Flight_Duration', 'Flight_Per_AC'
    , 'IFE', 'TV', 'Phone', 'OneMedia']

class RoiInput:
    """A simple class for dep scheduler"""

    def __init__(self,
                 airline_region,
                 price_text, num_text, unit_text, text_free,
                 price_browse, num_browse, unit_browse, browse_free,
                 price_stream, num_stream, unit_stream, stream_free,
                 price_per_mb, pac_pct, air_pct, wisp_pct):

        self.airline_region = airline_region

        self.price_text = price_text
        self.num_text = num_text
        self.unit_text = unit_text
        self.text_free = text_free

        self.price_browse = price_browse
        self.num_browse = num_browse
        self.unit_browse = unit_browse
        self.browse_free = browse_free

        self.price_stream = price_stream
        self.num_stream = num_stream
        self.unit_stream = unit_stream
        self.stream_free = stream_free

        self.price_per_mb = price_per_mb
        self.pac_pct = pac_pct
        self.air_pct = air_pct
        self.wisp_pct = wisp_pct

    def __str__(self):
        return f"Fleet: - airline_region: {self.airline_region}\n" \
               f"Price: " \
               f"-- price_text: {self.price_text} -  num_text: {self.num_text} -  unit_text: {self.unit_text} " \
               f"-  free_text: {self.text_free} \n" \
               f"-- price_browse: {self.price_browse} -  num_browse: {self.num_browse} - unit_browse: {self.unit_browse}" \
               f"-  free_browse: {self.browse_free} \n" \
               f"-- price_stream: {self.price_stream} -  num_stream: {self.num_stream} -  unit_stream: {self.unit_stream}" \
               f"-  free_stream: {self.stream_free} \n"\
               f"Revenue Share: - price_per_mb: {self.price_per_mb} \n" \
               f"pac_pct: {self.pac_pct} - air_pct: {self.air_pct} - wisp_pct: {self.wisp_pct}\n"

    @staticmethod
    def load_request(jsonData):
        airline_region = jsonData.get('airline_region', None)

        price_text = jsonData.get('price_text', None)
        num_text = jsonData.get('num_text', None)
        unit_text = jsonData.get('unit_text', None)
        text_free = jsonData.getlist('text_free', None)[-1]

        price_browse =  jsonData.get('price_browse', None)
        num_browse =  jsonData.get('num_browse', None)
        unit_browse =  jsonData.get('unit_browse', None)
        browse_free = jsonData.getlist('browse_free', None)[-1]

        price_stream = jsonData.get('price_stream', None)
        num_stream = jsonData.get('num_stream', None)
        unit_stream = jsonData.get('unit_stream', None)
        stream_free = jsonData.getlist('stream_free', None)[-1]

        price_per_mb = jsonData.get('price_per_mb', None)
        pac_pct = jsonData.get('pac_pct', None)
        air_pct =  jsonData.get('air_pct', None)
        wisp_pct = jsonData.get('wisp_pct', None)

        input_validation('Price_Text', price_text, 'float'
                         , UI_CONFIG.get('price').get('text').get('min')
                         , UI_CONFIG.get('price').get('text').get('max'))
        input_validation('Price_Browse', price_browse, 'float'
                         , UI_CONFIG.get('price').get('browse').get('min')
                         , UI_CONFIG.get('price').get('browse').get('max'))
        input_validation('Price_Stream', price_stream, 'float'
                         , UI_CONFIG.get('price').get('stream').get('min')
                         , UI_CONFIG.get('price').get('stream').get('max'))

        price_str = f'price input: Text: {price_text} - Browse: {price_browse} - Stream: {price_stream}'

        if float(price_text) > float(price_browse):
            raise DataRangeException(f'price of Text package should NOT greater than price of Browse package: '
                                     f'{price_str}')
        if float(price_browse) > float(price_stream):
            raise DataRangeException(f'price of Browse package should NOT greater than price of Stream package: '
                                     f'{price_str}')

        form_input = RoiInput(airline_region,
                              price_text, num_text, unit_text, text_free,
                              price_browse, num_browse, unit_browse, browse_free,
                              price_stream, num_stream, unit_stream, stream_free,
                              price_per_mb, pac_pct, air_pct, wisp_pct)

        return form_input

    def gen_df(self):
        additional = pd.DataFrame(data=[[self.airline_region
                                            , self.price_per_mb
                                            , self.pac_pct
                                            , self.air_pct
                                            , self.wisp_pct]]
                                  , columns = ADD_COL)
        price = pd.DataFrame(data=[[self.price_text,self.num_text, self.unit_text, self.text_free,
                                    self.price_browse, self.num_browse, self.unit_browse, self.browse_free,
                                    self.price_stream, self.num_stream, self.unit_stream, self.stream_free]]
                             , columns = PRICE_COL)

        return additional, price


def input_validation(field_name, field_value, field_type, start=None, end=None):

    if field_value is None:
        raise EmptyInputError(f'input of {field_name} is None')

    if field_type.lower() == 'int':
        try:
            field_value = int(field_value)
        except:
            raise DataTypeException(f"input of {field_name} is not a {field_type}: {field_value}")
    if field_type.lower() == 'float':
        try:
            field_value = float(field_value)
        except:
            raise DataTypeException(f"input of {field_name} is not a {field_type}: {field_value}")

    if start is None:
        pass
    else:
        if start <= field_value:
            pass
        else:
            raise DataRangeException(f"input of {field_name} is out of range: value: {field_value}, start - end: {start} - {end}")
    if end is None:
        pass
    else:
        if field_value <= end:
            pass
        else:
            raise DataRangeException(f"input of {field_name} is out of range: value: {field_value}, start - end: {start} - {end}")


class RoiFleet:
    """A simple class for dep scheduler"""

    def __init__(self, fleet_type, ac_type, ac_cnt, st_cnt, eco_cnt, f_dur, f_per,
                 service_ife, service_tv, service_phone, service_media):
        self.fleet_type = fleet_type
        self.ac_type = ac_type
        self.ac_cnt = ac_cnt
        self.st_cnt = st_cnt
        self.eco_cnt = eco_cnt
        self.f_dur = f_dur
        self.f_per = f_per
        self.service_ife = service_ife
        self.service_tv = service_tv
        self.service_phone = service_phone
        self.service_media = service_media

    def __str__(self):
        return f"Basic:\n - type{self.fleet_type} - {self.ac_type}\n" \
               f"- ac_cnt: {self.ac_cnt} - seat_cnt: {self.st_cnt} - eco_cnt: {self.eco_cnt}\n" \
               f"- flight_duration: {self.f_dur} - f_per_ac: {self.f_per}\n" \
               f"Services: - service_ife: {self.service_ife} " \
               f"- service_tv: {self.service_tv} " \
               f"- service_phone: {self.service_phone} "\
               f"- service_media: {self.service_media}\n  " \

    def to_list(self):
        return [ self.fleet_type
                , self.ac_type
                , self.ac_cnt
                , self.st_cnt
                , self.eco_cnt
                , self.f_dur
                , self.f_per
                , self.service_ife
                , self.service_tv
                , self.service_phone
                , self.service_media]

    @staticmethod
    def load_input(flight_zip):
        output_ls = list()
        for s in flight_zip:
            print(s)
            output_ls.append(RoiFleet(*s))
        return output_ls

    @staticmethod
    def load_request(jsonData):
        print('load json from UI')
        fleet_zip = zip(
            jsonData.getlist('fleet_type')
            , jsonData.getlist('ac_type')
            , jsonData.getlist('ac_cnt')
            , jsonData.getlist('st_cnt')
            , jsonData.getlist('eco_cnt')
            , check_list_reform(jsonData.getlist('f_dur'))
            , jsonData.getlist('f_per')
            , check_list_reform(jsonData.getlist('service_ife'))
            , check_list_reform(jsonData.getlist('service_tv'))
            , check_list_reform(jsonData.getlist('service_phone'))
            , check_list_reform(jsonData.getlist('service_media'))
        )
        return list(fleet_zip)


class RoiFlight:
    """A simple class for dep scheduler"""

    def __init__(self, flight_type, orig_reg, dest_reg, tt_flt, ld_fct, nt_flt):
        self.flight_type = flight_type
        self.orig_reg = orig_reg
        self.dest_reg = dest_reg
        self.tt_flt = tt_flt
        self.ld_fct = ld_fct
        self.nt_flt = nt_flt

    def __str__(self):
        return f"Basic:\n - flight_type: {self.flight_type} - orig: {self.orig_reg} - dest: {self.dest_reg} " \
               f"- per of tt flight: {self.tt_flt} - load factor: {self.ld_fct} - night light per: {self.nt_flt} \n" \

    def to_list(self):
        return [ self.flight_type
                , self.orig_reg
                , self.dest_reg
                , self.tt_flt
                , self.ld_fct
                , self.nt_flt]

    @staticmethod
    def load_input(flight_zip):
        output_ls = list()
        for s in flight_zip:
            print(s)
            output_ls.append(RoiFlight(*s))
        return output_ls

    @staticmethod
    def load_request(jsonData):
        print('load json from UI')
        flight_zip = zip(
            jsonData.getlist('flight_type')
            , jsonData.getlist('orig_reg')
            , jsonData.getlist('dest_reg')
            , jsonData.getlist('tt_flt')
            , jsonData.getlist('ld_fct')
            , jsonData.getlist('nt_flt')
        )
        return list(flight_zip)

def fleet_list_gen_df(fleet):

    l = [f.to_list() for f in fleet]
    df = pd.DataFrame(l)
    df.reset_index(level=0, inplace=True)
    print(df)
    df.columns= FLEET_COL
    return df

def flight_list_gen_df(flight):

    l = [f.to_list() for f in flight]
    df = pd.DataFrame(l)
    df.reset_index(level=0, inplace=True)
    print(df)
    df.columns= FLIGHT_COL
    return df


def check_list_reform(input_list):
    out = list()
    for i in range(len(input_list)):
        if input_list[i]=='1':
            out.pop()
        out.append(input_list[i])
    return out


if __name__ == "__main__":
    pass


    # print(price)
    #
    # price.columns= ['c1', 'c2', 'c3']
    print(flight)

    [
        ('airline_region', 'Americas'),
        fleet
        ('fleet_type', '0'), ('fleet_type', '0'), ('fleet_type', '1'), ('fleet_type', '1'),
        ('ac_type', 't1'), ('ac_type', 't2'), ('ac_type', 't3'), ('ac_type', 't4'),
        ('ac_cnt', '10'), ('ac_cnt', '20'), ('ac_cnt', '30'), ('ac_cnt', '40'),
        ('st_cnt', '100'), ('st_cnt', '200'), ('st_cnt', '300'), ('st_cnt', '400'),
        ('eco_cnt', '80'), ('eco_cnt', '160'), ('eco_cnt', '200'), ('eco_cnt', '300'),
        ('f_dur', '2'), ('f_dur', '10'), ('f_dur', '5'), ('f_dur', '10'),
        ('f_per', '10'), ('f_per', '20'), ('f_per', '30'), ('f_per', '40'),
        ('service_ife', '0'), ('service_ife', '0'), ('service_ife', '0'), ('service_ife', '0'),
        ('service_tv', '0'), ('service_tv', '0'), ('service_tv', '0'), ('service_tv', '0'),
        ('service_phone', '0'), ('service_phone', '0'), ('service_phone', '0'), ('service_phone', '0'),
        ('service_media', '0'), ('service_media', '0'), ('service_media', '0'), ('service_media', '0'),
        flight
        ('flight_type', '0'), ('flight_type', '0'), ('flight_type', '0'), ('flight_type', '1'), ('flight_type', '1'),
        ('orig_reg', 'Americas'), ('orig_reg', 'Europe'), ('orig_reg', 'Japan'), ('orig_reg', 'Americas'),
        ('orig_reg', 'Japan'),
        ('dest_reg', 'Americas'), ('dest_reg', 'Europe'), ('dest_reg', 'Japan'), ('dest_reg', 'Americas'),
        ('dest_reg', 'Japan'),
        ('tt_flt', '50'), ('tt_flt', '30'), ('tt_flt', '20'), ('tt_flt', '40'), ('tt_flt', '60'),
        ('ld_fct', '50'), ('ld_fct', '80'), ('ld_fct', '80'), ('ld_fct', '80'), ('ld_fct', '80'),
        ('nt_flt', '10'), ('nt_flt', '10'), ('nt_flt', '20'), ('nt_flt', '10'), ('nt_flt', '10'),

        ('price_per_mb', '10'), ('pac_pct', '40'), ('air_pct', '30'), ('wisp_pct', '30'),

        ('price_text', '10'), ('num_text', '10'), ('unit_text', 'mb'), ('text_free', '0'),
        ('price_browse', '20'), ('num_browse', '20'), ('unit_browse', 'mb'), ('browse_free', '0'),
        ('price_stream', '75'), ('num_stream', '100'), ('unit_stream', 'mb'), ('stream_free', '0')
    ]



