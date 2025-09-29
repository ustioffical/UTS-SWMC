/**
 *
 * Created by FarhanTa on 5/23/2023.
 */

AppUtilityModel = function () {

    let me = this;
    me.PageTitle = "";

    me.appConstructor = function () {
    };

    me.FillCmdListByModel = function (table_name, column_name, column_code, cmd_id, selected_value) {
        let formdata = new FormData();
        formdata.append('table_name', table_name);
        formdata.append('column_name', column_name);
        formdata.append('column_code', column_code);
        var paramas = {
            url: cmd_list_model,
            data: formdata,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(paramas, function (data) {
            var sbox = document.getElementById(cmd_id);
            for (var i = 0; i < data.cmd_list.length; i++) {
                sbox.add(new Option(data.cmd_list[i][column_name], data.cmd_list[i][column_code]));
            }
            if (selected_value !== "") {
                $("#" + cmd_id).val(selected_value); // Select the option with a value of '1'
                $("#" + cmd_id).trigger('change'); // Notify any JS components that the value changed
            }
        });

    };

    me.FillCmdListByModelWithCode = function (table_name, condition_column, cmd_column, cmd_id, selected_value) {
        let formdata = new FormData();
        formdata.append('table_name', table_name);
        formdata.append('condition_column', condition_column);
        formdata.append('cmd_column', cmd_column);
        var paramas = {
            url: fill_cmd_model_with_code,
            data: formdata,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(paramas, function (data) {

            let column_split = cmd_column.split("^^")
            let column_code = column_split[0]
            let column_name = column_split[1]

            if (data.cmd_list.length > 0) {
                var sbox = document.getElementById(cmd_id);
                $("#" + cmd_id).empty();

                $("#" + cmd_id).append("<option value='NA'>Select</option>");
                $("#" + cmd_id + "> option").removeAttr("selected");
                for (var i = 0; i < data.cmd_list.length; i++) {
                    sbox.add(new Option(data.cmd_list[i][column_name], data.cmd_list[i][column_code]));
                }
                if (selected_value !== "") {
                    $("#" + cmd_id).val(selected_value); // Select the option with a value of '1'
                    $("#" + cmd_id).trigger('change'); // Notify any JS components that the value changed
                }
            } else {
                $("#" + cmd_id + "> option").removeAttr("selected");
                // $("#" + cmd_id).trigger("change");
                $('#' + cmd_id).empty();
                $('#' + cmd_id).append("<option value=''>No Record Found</option>");
            }
        })
    };

    //// FETCH GOOGLE ADDRESS BY COORDINATE
    me.SetGooglePlaceJSON = function (lat, lng) {
        let geocoder = new google.maps.Geocoder;
        let p = new L.LatLng(lat, lng);
        let latlng = {lat: lat, lng: lng};
        geocoder.geocode({'location': latlng}, function (results, status) {
            if (status === 'OK') {
                if (results[0]) {
                    me.FillFormattedAddressInputField(results[0], lat, lng);
                } else {
                    window.alert('No results found');
                }
            }
        });
    }

    me.FillFormattedAddressInputField = function (format_add, lat, lng) {

        $("#id_address").val(format_add.formatted_address);
        let p_len = format_add.address_components.length;
        $("#id_province").val(format_add.address_components[p_len - 2].long_name);
        $("#id_city").val(format_add.address_components[p_len - 3].long_name);

        // let markerType = $('#cmd_marker_type').val();
        // let fiberName = $('#cmd_fiber_type').val();
        //
        // if (markerType !== "NA") {
        //     $("#id__address").val(format_add.formatted_address);
        //     var p_len = format_add.address_components.length;
        //     $("#id__province").val(format_add.address_components[p_len - 2].long_name);
        //     $("#id__city").val(format_add.address_components[p_len - 3].long_name);
        //
        //     // var city_name = format_add.address_components[p_len - 3].long_name;
        //     // alert(city_name);
        //     // if (markerType === "ebs" || markerType === "so" || markerType === "sp") {
        //     //     var name = markerType + "_olt_name";
        //     //     var coordinate = "POINT(" + lng + " " + lat + ")";
        //     //     GlobalModelJS.FillCMDOLTsList(name, coordinate);
        //     // }
        //
        // }

        // if (feature_type !== "NA") {
        //     // $("#" + fiberName + "_dml").val();
        //     var fiber_status = $("#" + fiberName + "_dml").val();
        //     var part = fiber_status.split(":");
        //     if (part[0] !== "Updated") {
        //         var p_len = format_add.address_components.length;
        //         $("#id_" + fiberName + "_province").val(format_add.address_components[p_len - 2].long_name);
        //         $("#id_" + fiberName + "_city").val(format_add.address_components[p_len - 3].long_name);
        //     }
        // }
    };

    //// GET CURRENT DATE WITH TIME BY CODE
    me.GetCurrentDate = function () {
        let now = new Date();

        // Get local date and time components
        let year = now.getFullYear();
        let month = String(now.getMonth() + 1).padStart(2, '0'); // Months are 0-based
        let day = String(now.getDate()).padStart(2, '0');
        let hours = String(now.getHours()).padStart(2, '0');
        let minutes = String(now.getMinutes()).padStart(2, '0');

        // Format: YYYY-MM-DDTHH:MM (Required by datetime-local)
        let formattedDateTime = `${year}-${month}-${day}`;
        return formattedDateTime;
    }

    me.GetCurrentDateTime = function () {
        let now = new Date();

        // Get local date and time components
        let year = now.getFullYear();
        let month = String(now.getMonth() + 1).padStart(2, '0'); // Months are 0-based
        let day = String(now.getDate()).padStart(2, '0');
        let hours = String(now.getHours()).padStart(2, '0');
        let minutes = String(now.getMinutes()).padStart(2, '0');

        // Format: YYYY-MM-DDTHH:MM (Required by datetime-local)
        let formattedDateTime = `${year}-${month}-${day}T${hours}:${minutes}`;
        return formattedDateTime;
    }

    // Random color generator
    me.GetRandomColor = function () {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    ////SWEET ALERT
    me.ToastSweetAlert = function (directions, icon_title, msg) {

        const Toast = Swal.mixin({
            toast: true,
            position: directions, //// top-end, "top-start", bottom-start
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true,
            didOpen: (toast) => {
                toast.onmouseenter = Swal.stopTimer;
                toast.onmouseleave = Swal.resumeTimer;
            },
        });
        Toast.fire({
            icon: icon_title, //// "success"
            title: msg, //// "Signed in successfully"
        });

    }

}

setMissingParams = function (params, isAsync) {
    if (!params["type"]) {
        params["type"] = "GET";
    }
    if (!params["dataType"]) {
        params["dataType"] = "json";
    }
    if (!params["processData"]) {
        params["processData"] = false;
    }
    if (!params["contentType"]) {
        params["contentType"] = false;
    }

    if (!params["async"]) {
        params["async"] = isAsync;
    }
    return params;
}

callAJAX = function (params, callback) {
    // params in the form of {url:url,post:post} ets
    var params = setMissingParams(params, true);
    // if ($("#waiting-div").length) $("#waiting-div").css('visibility', 'visible');
    var delayInMilliseconds = 1000; //1 second
    setTimeout(function () {
        $.ajax(params).done(function (data) {
            // if ($("#waiting-div").length) $("#waiting-div").css('visibility', 'hidden');
            try {
                if (data.is_redirect) {
                    window.location.href = data.url
                }
            } catch (e) {
                console.log(e)
            }
            callback(data)
        }).fail(function (error, texStatus) {
            // console.log(error.responseText);
            // if ($("#waiting-div").length) $("#waiting-div").css('visibility', 'hidden');
            console.log(texStatus)
            errorMsg = "Fail to perform your request."
            // showAlertDialog(errorMsg, dialogTypes.error);
            // if (progressbarModel != null)
            //     progressbarModel.hideProgressBar()
        })
            , delayInMilliseconds
    })
}