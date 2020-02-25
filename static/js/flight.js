var dt = JSON.parse(document.getElementById("region_ls").dataset.region);

var opt = ''
for (var key in dt){
    opt = opt + '<option value="' + dt[key] + '" >' + dt[key] + '</option> \n';
}
console.log(opt)


var short_flight = '\
        <tr class="short_flight_information">\
          <td>\
            <div class="form-group">\
              <select class="flight_type" name="flight_type">\
                <option value=0 default  selected>Short Haul</option>\
                  <option value=1 disabled >Long Haul</option>\
              </select>\
            </div>\
          </td>\
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
           <input type="number" min= 0 max= 100\
                   class="form-control" id="tt_flt" name="tt_flt" placeholder="" required="required">\
          </td>\
          <td>\
            <input type="number" min= 0 max= 100\
                   class="form-control" id="ld_fct" name="ld_fct" placeholder="" required="required">\
          </td>\
          <td>\
            <input type="number" min= 0 max= 100\
                   class="form-control" id="nt_flt" name="nt_flt" placeholder="" required="required">\
          </td>\
          <td>\
            <button id="flight_del" class="btn btn-danger btn-sm" type="button" >\
            <span class="fa fa-minus" aria-hidden="true" color="white"></span></button>\
          </td>\
        </tr>\
          '


var long_flight = '\
        <tr class="long_flight_information">\
          <td>\
            <div class="form-group">\
              <select class="flight_type" name="flight_type">\
                <option value=0 disabled >Short Haul</option>\
                  <option value=1 default  selected >Long Haul</option>\
              </select>\
            </div>\
          </td>\
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
           <input type="number" min= 0 max= 100\
                   class="form-control" id="tt_flt" name="tt_flt" placeholder="" required="required">\
          </td>\
          <td>\
            <input type="number" min= 0 max= 100\
                   class="form-control" id="ld_fct" name="ld_fct" placeholder="" required="required">\
          </td>\
          <td>\
            <input type="number" min= 0 max= 100\
                   class="form-control" id="nt_flt" name="nt_flt" placeholder="" required="required">\
          </td>\
          <td>\
            <button id="flight_del" class="btn btn-danger btn-sm" type="button" >\
            <span class="fa fa-minus" aria-hidden="true" color="white"></span></button>\
          </td>\
        </tr>\
          '


//flight
  $(document).ready(function(){

    $("#add_short_flight").click(function(){
        $(".short_flight_form").append(
            short_flight
        );
    });
    $("#add_long_flight").click(function(){
        $(".long_flight_form").append(
            long_flight
        );
    });
    $('tbody').on('click', '#flight_del', function(){
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
