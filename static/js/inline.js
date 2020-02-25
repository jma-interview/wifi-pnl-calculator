var dt = JSON.parse(document.getElementById("region_ls").dataset.region);

var opt = ''
for (var key in dt){
    opt = opt + '<option value="' + dt[key] + '" >' + dt[key] + '</option> \n';
}
console.log(opt)


var append_html = '\
         <tr class="flight_information">\
          <td>\
            <div class="form-group">\
              <select class="orig_reg" name="orig_reg">\
                '+ opt +
                '\
                </select>\
            </div>\
          </td>\
          <td>\
           <div class="form-group">\
             <select class="dest_reg" name="dest_reg">\
                '+ opt +
                '\
             </select>\
           </div>\
         </td>\
         <td>\
           <input type="number" min= {{ui_config.seat_count.min}} max={{ui_config.seat_count.max}} \
                  class="form-control" id="st_cnt" name="st_cnt" placeholder="" required="required">\
         </td>\
          <td>\
                <input type="number" min= 0 max= 100 \
                   class="form-control" id="ld_fct" name="ld_fct" placeholder="" required="required">\
          </td>\
         <td>\
           <input type="number" min= {{ui_config.seat_count.min}} max={{ui_config.seat_count.max}} \
                  class="form-control" id="eco_cnt" name="eco_cnt" required="required">\
         </td>\
         <td>\
           <div class="form-check">\
             <input id="redeye_Hidden" type="hidden" value=0 name="redeye">\
             <input class="form-check-input" type="checkbox" name="redeye" id="redeye" value=1>\
             <label class="form-check-label" for="redeye">Night Flight</label>\
           </div>\
         </td>\
         <td>\
           <input type="number" min="0" max="30" step=".1"\
                  class="form-control" id="f_dur" name="f_dur" required="required">\
         </td>\
         <td>\
           <div class="form-check">\
             <input id="service_ife_Hidden" type="hidden" value=0 name="service_ife">\
             <input class="form-check-input" type="checkbox" name="service_ife" id="service_ife" value=1>\
             <label class="form-check-label" for="service_ife">IFE</label>\
           </div>\
           <div class="form-check">\
             <input id="service_tv_Hidden" type="hidden" value=0 name="service_tv">\
             <input class="form-check-input" type="checkbox" name="service_tv" id="service_tv" value=1>\
             <label class="form-check-label" for="service_tv">TV</label>\
           </div>\
           <div class="form-check">\
             <input id="service_phone_Hidden" type="hidden" value=0 name="service_phone">\
             <input class="form-check-input" type="checkbox" name="service_phone" id="service_phone" value=1>\
             <label class="form-check-label" for="service_phone">Phone</label>\
           </div>\
           <div class="form-check">\
             <input id="service_media_Hidden" type="hidden" value=0 name="service_media">\
             <input class="form-check-input" type="checkbox" name="service_media" id="service_media" value=1>\
             <label class="form-check-label" for="service_media">1Media</label>\
           </div>\
         </td>\
         <td>\
           <input type="number" min="0" max="1000"\
                  class="form-control" id="ac_cnt" name="ac_cnt" required="required">\
         </td>\
         <td>\
           <input type="number" min="0"  max="5000"\
                  class="form-control" id="f_per" name="f_per" required="required">\
         </td>\
         <td>\
           <button id="del_flight" class="btn btn-danger btn-sm" type="button" >\
           <span class="fa fa-minus" aria-hidden="true" color="white"></span></button>\
         </td>\
       </tr>\
         '
//flight
  $(document).ready(function(){
    $("#add_flight").click(function(){
        $(".flight_form").append(
            append_html
        );
    });

    $('#rmv_flight').click(function(){
      $('.flight_information').remove();
      });
    $('tbody').on('click', '#del_flight', function(){
      $(this).parent().parent().remove()
      })
    });

// 1 to 100 loop
    $(function(){
    var $select = $(".option_ls_100");
    for (i=1;i<=100;i++){
        $select.append($('<option></option>').val(i).html(i))
    }
  });

// schedule
  $(document).ready(function(){
    $("#add_schedule").click(function(){
        $("af_info").append(
        '\
        <div class="deployment_schedule">\
          <fieldset style="width:300px; display:inline-block; text-align:left;">\
            <div>\
              <label for="dep_year" class="ds_form_label">Year:</label>\
              <input name="dep_y" type="number" class="ds_form_input" min="2010" max="2100"></select>\
            </div>\
            <div>\
              <label for="dep_q" class="ds_form_label">Quarter:</label>\
              <select name="dep_q" class="ds_form_input">\
                <option value = "1">01</option>\
                <option value = "2">02</option>\
                <option value = "3">03</option>\
                <option value = "4">04</option>\
              </select>\
            </div>\
            <div>\
              <label for="dep_amt" class="ds_form_label">Amount:</label>\
              <input name="dep_amt" type="number" class="ds_form_input" min="1" max="9999">\
            </div>\
            <button id="del_schedule" class="btn btn-danger btn-sm" type="button"><span class="fa fa-minus" aria-hidden="true" color="white"></span></button>\
          </fieldset>\
        </div>\
        '
        );
    });
     $('#rmv_schedule').click(function(){
       $('.deployment_schedule').remove();
    })
    $('af_info').on('click', '#del_schedule', function(){
       $(this).parent().parent().remove()
    })
  });