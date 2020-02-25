var dt = JSON.parse(document.getElementById("region_ls").dataset.region);

var opt = ''
for (var key in dt){
    opt = opt + '<option value="' + dt[key] + '" >' + dt[key] + '</option> \n';
}
console.log(opt)


var short_fleet = '\
         <tr class="short_fleet_information">\
          <td>\
            <div class="form-group">\
              <select class="fleet_type" name="fleet_type">\
                <option value=0 selected >Short Haul</option>\
                  <option value=1 disabled>Long Haul</option>\
              </select>\
            </div>\
          </td>\
          <td>\
            <div class="form-group">\
               <input type="text" class="form-control" id="ac_type" name="ac_type" placeholder="type of aircraft" required="required">\
            </div>\
          </td>\
          <td>\
            <div class="form-group">\
                <input type="number" min= 0 max=999\
                   class="form-control" id="ac_cnt" name="ac_cnt" required="required">\
            </div>\
          </td>\
          <td>\
            <input type="number" min= {{ui_config.seat_count.min}} max={{ui_config.seat_count.max}}\
                   class="form-control" id="st_cnt" name="st_cnt" placeholder="" required="required">\
          </td>\
          <td>\
            <input type="number" min= {{ui_config.seat_count.min}} max={{ui_config.seat_count.max}}\
                   class="form-control" id="eco_cnt" name="eco_cnt" required="required">\
          </td>\
          <td>\
            <input type="number" min="0" max="30" step=".1"\
                   class="form-control" id="f_dur" name="f_dur" required="required">\
          </td>\
          <td>\
            <input type="number" min="0" max="5000"\
                   class="form-control" id="f_per" name="f_per" required="required">\
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
           <button id="fleet_del" class="btn btn-danger btn-sm" type="button" >\
           <span class="fa fa-minus" aria-hidden="true" color="white"></span></button>\
         </td>\
        </tr>\
          '


var long_fleet = '\
         <tr class="long_fleet_information">\
          <td>\
            <div class="form-group">\
              <select class="fleet_type" name="fleet_type">\
                <option value=0 disabled>long Haul</option>\
                  <option value=1 selected>Long Haul</option>\
              </select>\
            </div>\
          </td>\
          <td>\
            <div class="form-group">\
               <input type="text" class="form-control" id="ac_type" name="ac_type" placeholder="type of aircraft" required="required">\
            </div>\
          </td>\
          <td>\
            <div class="form-group">\
                <input type="number" min= 0 max=999\
                   class="form-control" id="ac_cnt" name="ac_cnt" required="required">\
            </div>\
          </td>\
          <td>\
            <input type="number" min= {{ui_config.seat_count.min}} max={{ui_config.seat_count.max}}\
                   class="form-control" id="st_cnt" name="st_cnt" placeholder="" required="required">\
          </td>\
          <td>\
            <input type="number" min= {{ui_config.seat_count.min}} max={{ui_config.seat_count.max}}\
                   class="form-control" id="eco_cnt" name="eco_cnt" required="required">\
          </td>\
          <td>\
            <input type="number" min="0" max="30" step=".1"\
                   class="form-control" id="f_dur" name="f_dur" required="required">\
          </td>\
          <td>\
            <input type="number" min="0" max="5000"\
                   class="form-control" id="f_per" name="f_per" required="required">\
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
           <button id="fleet_del" class="btn btn-danger btn-sm" type="button" >\
           <span class="fa fa-minus" aria-hidden="true" color="white"></span></button>\
         </td>\
        </tr>\
          '

//flight
  $(document).ready(function(){
//    $("#add_short_fleet").click(function(){
//        $(".short_fleet_form").append(
//            append_fleet
//        );
//    });

    $("#add_short_fleet").click(function(){
        $(".short_fleet_form").append(
            short_fleet
        );
    });
    $("#add_long_fleet").click(function(){
        $(".long_fleet_form").append(
            long_fleet
        );
    });
    $('tbody').on('click', '#fleet_del', function(){
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
