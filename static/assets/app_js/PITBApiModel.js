AppPITBApiModel = function () {

    let me = this;
    me.appConstructor = function () {

    };

    //// RETRIEVE SINGLE VEHICLE TRIP HISTORY BY FILTER
    me.PushDataPITBServer_PostVTMSData = function (vehicle_id, selected_date) {
        // alert(vehicle_id + " --- " + start_date + " ---- " + end_date);

        let get_vehicle_code = "278905";
        let get_selected_date = "2025-05-06";

        let formdata = new FormData();
        formdata.append('vehicle_code', get_vehicle_code);
        formdata.append('selected_date', get_selected_date);
        var paramas = {
            url: push_pitb_server_post_vtms_data,
            data: formdata,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(paramas, function (data) {
            // console.log(data.tracker_raw_gprs_lists.length);

        });

    }

}