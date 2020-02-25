from flask_wtf import Form, FlaskForm
from wtforms import StringField, IntegerField, DecimalField, FieldList, FormField, SelectField
from wtforms.validators import DataRequired, ValidationError
import datetime

QUARTER_LIST = [
    (1, '01')
    , (2, '02')
    , (3, '03')
    , (4, '04')
]

def gen_year_list():
    N = 30
    now = datetime.datetime.now()
    y = now.year

    year_ls = list()
    for i in range(0, N):
        v = i + y
        year_ls.append((v, str(v)))
    return year_ls


class ScheduleForm(FlaskForm):
    dep_y = SelectField('Deploy Year', validators=[DataRequired()]
                        , choices=gen_year_list())
    dep_q = SelectField('Deploy Quarter', validators=[DataRequired()]
                        , choices=QUARTER_LIST)
    dep_amt = IntegerField('Deploy Amount', validators=[DataRequired()]
                           , render_kw={"placeholder": "amount of deployment"})


class RoiForm(FlaskForm):
    ac_type = StringField('Aircraft Type', validators=[DataRequired()]
                          , render_kw={"placeholder": "type of aircraft"})
    ac_cnt = IntegerField('Aircraft Count', validators=[DataRequired()]
                          , render_kw={"placeholder": "count of aircraft"})
    flight_per_year = IntegerField('Flight Per Year', validators=[DataRequired()]
                                   , render_kw={"placeholder": "flight per year"})
    night_flight_per = DecimalField('Night Flight Percentage', validators=[DataRequired()]
                                    , render_kw={"placeholder": "percentage of night flights"})
    avg_flight_dur = IntegerField('Average Flight Duration(in hours)', validators=[DataRequired()]
                                  , render_kw={"placeholder": "average duration of flight"})
    busi_passenger_per = DecimalField('Business Passenger Percentage(Optional)'
                                      , render_kw={"placeholder": "percentage of business passengers"})

    dep_schedule = FieldList(FormField(ScheduleForm), min_entries=1)

    ori_region = StringField('Origin Region'
                             , render_kw={"placeholder": "origin region"})
    dest_region = StringField('Destination Region'
                              , render_kw={"placeholder": "destination region"})

    text_basic = IntegerField('Text(Basic)'
                              , render_kw={"placeholder": "price of text / basic package"})
    browse_mid = IntegerField('Browse(Mid)'
                              , render_kw={"placeholder": "price of browse / mid package"})
    stream_top = IntegerField('Browse(Mid)'
                              , render_kw={"placeholder": "price of stream / top package"})

#
# class ScheduleForm(FlaskForm):
#     dep_y = SelectField('Deploy Year', validators=[DataRequired()]
#                         , choices=gen_year_list())
#     dep_q = SelectField('Deploy Quarter', validators=[DataRequired()]
#                         , choices=QUARTER_LIST)
#     dep_amt = IntegerField('Deploy Amount', validators=[DataRequired()]
#                            , render_kw={"placeholder": "amount of deployment"})


# class RoiForm(FlaskForm):
#     ac_cnt = IntegerField('Aircraft Count', validators=[DataRequired()]
#                           # , render_kw={"placeholder": "count of aircraft"}
#                           )
#     flight_per_year = IntegerField('Flight Per Year', validators=[DataRequired()]
#                                    # , render_kw={"placeholder": "flight per year"}
#                                    )
#     age = DecimalRangeField('Age', default=0)
#
#     text_basic = DecimalRangeField('Text(Basic)', default=0, min=1, max=10
#                               , render_kw={"placeholder": "price of text / basic package"})
#     browse_mid = IntegerField('Browse(Mid)', default=0, min=1, max=10
#                               , render_kw={"placeholder": "price of browse / mid package"})
#     stream_top = IntegerField('Browse(Mid)', default=0, min=1, max=10
#                               , render_kw={"placeholder": "price of stream / top package"})
#
#
#     night_flight_per = DecimalField('Night Flight Percentage', validators=[DataRequired()]
#                                     , render_kw={"placeholder": "percentage of night flights"})
#     avg_flight_dur = IntegerField('Average Flight Duration(in hours)', validators=[DataRequired()]
#                                   , render_kw={"placeholder": "average duration of flight"})
#     busi_passenger_per = DecimalField('Business Passenger Percentage(Optional)'
#                                       , render_kw={"placeholder": "percentage of business passengers"})
#
#     dep_schedule = FieldList(FormField(ScheduleForm), min_entries=1)
#
#     ori_region = StringField('Origin Region'
#                              , render_kw={"placeholder": "origin region"})
#     dest_region = StringField('Destination Region'
#                               , render_kw={"placeholder": "destination region"})



if __name__ == "__main__":
    pass

    print(gen_year_list())


  #
  #       <div class="card mb-4 shadow-sm">
  #         <div class="card-header">
  #           <strong class="section_header ">Price info: </strong>
  #         </div>
  #         <div class="card-body">
  #             <div class="form-group">
  #               <label class="form_label"  for="text_basic">Text(Basic): </label>
  #               <!--<input type="text" class="form-control" id="text_basic" name="text_basic" placeholder="price of text / basic package">-->
  #               <input type="range" min="1" max="10" value = "5" class="form-control-range"
  #                      class="form-control" id="text_range" name="text_range"><span id="text_basic"></span>
  #             </div>
  #             <script>
  #             var slider_txt = document.getElementById("text_range");
  #             var output_txt = document.getElementById("text_basic");
  #             output_txt.innerHTML = slider_txt.value;
  #             slider_txt.oninput = function() {
  #               output_txt.innerHTML = this.value;
  #             };
  #             </script>
  #
  #             <div class="form-group">
  #               <label class="form_label" for="browse_mid">Browse(Mid): </label>
  #               <!--<input type="text" class="form-control" id="browse_mid" name="browse_mid" placeholder="price of browse / mid package">-->
  #               <input type="range" min="11" max="30" value = "20" class="form-control-range"
  #                      class="form-control" id="browse_range" name="browse_range"><span id="browse_mid"></span>
  #             </div>
  #             <script>
  #             var slider_browse = document.getElementById("browse_range");
  #             var output_browse = document.getElementById("browse_mid");
  #             output_browse.innerHTML = slider_browse.value;
  #             slider_browse.oninput = function() {
  #               output_browse.innerHTML = this.value;
  #             };
  #             </script>
  #
  #             <div class="form-group">
  #               <label class="form_label"  for="stream_top">Stream(Top): </label>
  #               <!--<input type="text" class="form-control" id="stream_top" name="stream_top" placeholder="price of stream / top package">-->
  #               <input type="range" min="31" max="50" value = "40" class="form-control-range"
  #                      class="form-control" id="stream_range" name="stream_range"><span id="stream_top"></span>
  #             </div>
  #             <script>
  #             var slider_stream = document.getElementById("stream_range");
  #             var output_stream = document.getElementById("stream_top");
  #             output_stream.innerHTML = slider_stream.value;
  #             slider_stream.oninput = function() {
  #               output_stream.innerHTML = this.value;
  #             };
  #             </script>
  #         </div>
  #       </div>
  # </div>
  #
  # <hr>
  # <strong class="section_header ">Flight info: </strong>
  # <table class="table table-bordered table-condensed">
  #     <thead class="thead-light">
  #       <tr>
  #         <th scope="col">Orig</th>
  #         <th scope="col">Dest</th>
  #         <th scope="col">AC Type</th>
  #         <th scope="col">Seat Count</th>
  #         <th scope="col">Business Seat %</th>
  #         <th scope="col">Red Eye</th>
  #         <th scope="col">Flight Duration</th>
  #         <th scope="col">Other Services</th>
  #         <th scope="col">Product Cap</th>
  #         <th scope="col">% of Flight</th>
  #         <th scope="col">
  #           <button id="add_flight" class="btn btn-success btn-sm" type="button">
  #             <span class="fa fa-plus" aria-hidden="true" color="white"></span>
  #           </button>
  #           <!--<button id="rmv_flight" class="btn btn-danger btn-sm" type="button">-->
  #             <!--<span class="fa fa-remove" aria-hidden="true" color="white"></span>-->
  #           <!--</button>-->
  #         </th>
  #       </tr>
  #     </thead>
  #     <tbody>
  #       <tr>
  #         <td>
  #           <div class="form-group">
  #             <select class="orig_reg">
  #               <option value="usa">USA</option>
  #               <option value="eu">EU</option>
  #               <option value="asia">Asia</option>
  #             </select>
  #           </div>
  #         </td>
  #         <td>
  #           <div class="form-group">
  #             <select class="dest_reg">
  #               <option value="usa">USA</option>
  #               <option value="eu">EU</option>
  #               <option value="asia">Asia</option>
  #             </select>
  #           </div>
  #         </td>
  #         <td>
  #           <div class="form-group">
  #             <select class="ac_tp">
  #               <option value="wide">Wide</option>
  #               <option value="narrow">Narrow</option>
  #             </select>
  #           </div>
  #         </td>
  #         <td>
  #           <input type="number" min="30" max="500"
  #                  class="form-control" id="st_cnt" name="st_cnt" placeholder="" required="required">
  #         </td>
  #         <td>
  #           <input type="number" min="0" max="100"
  #                  class="form-control" id="b_per" name="b_per" required="required">
  #         </td>
  #         <td>
  #
  #           <div class="form-check">
  #             <input class="form-check-input" type="checkbox" name="redeye" id="redeye" value=1>
  #             <label class="form-check-label" for="redeye">Redeye</label>
  #           </div>
  #
  #         </td>
  #
  #         <td>
  #           <input type="number" min="0" max="30"
  #                  class="form-control" id="f_dur" name="f_dur" required="required">
  #         </td>
  #
  #         <td>
  #
  #           <div class="form-check">
  #             <input class="form-check-input" type="checkbox" name="service" id="service_ife" value=1>
  #             <label class="form-check-label" for="service_ife">IFE</label>
  #           </div>
  #           <div class="form-check">
  #             <input class="form-check-input" type="checkbox" name="service" id="service_tv" value=2>
  #             <label class="form-check-label" for="service_tv">TV</label>
  #           </div>
  #           <div class="form-check">
  #             <input class="form-check-input" type="checkbox" name="service" id="service_phone" value=3>
  #             <label class="form-check-label" for="service_phone">Phone</label>
  #           </div>
  #           <div class="form-check">
  #             <input class="form-check-input" type="checkbox" name="service" id="service_media" value=4>
  #             <label class="form-check-label" for="service_media">1Media</label>
  #           </div>
  #
  #         </td>
  #
  #         <td>
  #             <div class="form-check">
  #             <input class="form-check-input" type="checkbox" name="prod_cap" id="prod_time" value=1>
  #             <label class="form-check-label" for="prod_time">Time</label>
  #           </div>
  #           <div class="form-check">
  #             <input class="form-check-input" type="checkbox" name="prod_cap" id="prod_mb" value=2>
  #             <label class="form-check-label" for="prod_mb">MB</label>
  #           </div>
  #         </td>
  #
  #         <td>
  #           <input type="number" min="0" max="100"
  #                  class="form-control" id="f_per" name="f_per" required="required">
  #         </td>