AppVehicleModel = function () {

    let me = this;

    me.appConstructor = function () {

    };

    // //// THIS FUNCTION SHOW VEHICLE FEATURE ON MAP
    // me.ShowVehicleLiveMonitoringMap = function (feature_json) {
    //     // console.log(feature_json);
    //
    //     if (feature_json.length > 0) {
    //         for (let i = 0; i < feature_json.length; i++) {
    //             let register_no = feature_json[i].register_no;
    //             let latitude = feature_json[i].x;
    //             let longitude = feature_json[i].y;
    //
    //             let file_image = "vehicle";
    //
    //             // if (container_status === "Active") {
    //             //     file_image = "google_marker";
    //             // }
    //             // if (container_status === "Block") {
    //             //     // file_image = "/static/assets/images/toolbar/google-marker.png";
    //             //     file_image = "container_block";
    //             // }
    //
    //             let marker = '';
    //             marker = L.marker(new L.LatLng(longitude, latitude), {icon: DigitalArzModelJS.icons[file_image]});
    //
    //             marker.bindPopup('<div style="width: 300px;"' +
    //                 '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12" style="padding: 1px; text-align: center;">' +
    //                 '<strong style="font-size: 16px;">Vehicle Detail</strong></div></div>' +
    //                 '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
    //                 '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Register No.:</strong></div>' +
    //                 '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
    //                 '<div>' + register_no + '</div></div></div>' +
    //                 // '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
    //                 // '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Name:</strong></div>' +
    //                 // '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
    //                 // '<div>' + object.name + '</div></div></div>' +
    //                 // '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
    //                 // '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Status:</strong></div>' +
    //                 // '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
    //                 // '<div>' + object.working_status + '</div></div></div>' +
    //                 // '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
    //                 // '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Condition:</strong></div>' +
    //                 // '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
    //                 // '<div>' + object.asset_condition + '</div></div></div>' +
    //                 // '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
    //                 // '<div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 text-center" style="padding: 3px;">' +
    //                 // '<a type="button" class="btn btn-primary btn-xs"' +
    //                 // "onclick=AMSModelJS.OnClickAssetTypeTabularView('" + editParam + "');>" +
    //                 // '<i class="fa fa-eye"></i> More Details' +
    //                 // '</a>' +
    //                 // '</div></div>' +
    //                 '</div>');
    //
    //             DigitalArzModelJS.IndicatorFeature.addLayer(marker);
    //             // onloadMarkerLayer.addLayer(marker1);
    //             // DigitalArzModelJS.OnloadMarkerLayerOBJ[container_code + ":" + container_name] = marker.addTo(DigitalArzModelJS.map);
    //
    //
    //         } //// LOOP FOR FEATURE DATA
    //     } //// IF FEATURE EXIST THEN
    //
    // }

    //// FETCH VEHICLE LIST BY VEHICLE TYPE
    me.VehicleListWithTypeCodeView = function (cmd_id, condition_value, vehicle_status, selected_value) {

        let formdata = new FormData();
        formdata.append('vehicle_type', condition_value);
        formdata.append('vehicle_status', vehicle_status);
        var paramas = {
            url: vehicle_list_with_type_code,
            data: formdata,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(paramas, function (data) {
            // console.log(data);

            if (data.cmd_list.length > 0) {

                $('#cmd_vehicle_list').empty(); // Clear previous options
                $('#cmd_vehicle_list').append('<option value="NA">-- Select an Option --</option>');

                // Loop through response data and add options
                $.each(data.cmd_list, function (index, item) {
                    $('#cmd_vehicle_list').append(`<option value="${item.vehicle_code}">${item.register_no} - ${item.pitb_code}</option>`);
                });

                // Refresh the SelectPicker to update UI
                $('#cmd_vehicle_list').selectpicker('refresh');

            } else {
                $('#cmd_vehicle_list').empty(); // Clear previous options
                $('#cmd_vehicle_list').append('<option value="NA">-- Select an Option --</option>');
            }

        });

    }

    //// RETRIEVE SINGLE VEHICLE ROUTE BY FILTER
    me.RetrieveSingleVehicleRouteJS = function (vehicle_id, selected_date, timeFrom, timeTo) {
        // alert(vehicle_id + " --- " + start_date + " ---- " + end_date);

        let formdata = new FormData();
        formdata.append('vehicle_id', vehicle_id);
        formdata.append('selected_date', selected_date);
        formdata.append('time_from', timeFrom);
        formdata.append('time_to', timeTo);
        var paramas = {
            url: fetch_single_vehicle_route_data,
            data: formdata,
            type: "POST",
            dataType: 'json',
            timeout: 300000,  // 5 minutes in milliseconds
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(paramas, function (data) {
            // console.log(data.tracker_raw_gprs_lists.length);

            DigitalArzModelJS.VehicleLayer.clearLayers();
            DigitalArzModelJS.VehicleRadiusLayer.clearLayers();

            DigitalArzModelJS.IndicatorFeature.clearLayers();
            DigitalArzModelJS.GroupRouteNetworkLayer.clearLayers();
            if (data.tracker_raw_gprs_lists.length > 0) {

                debugger;

                let VehicleSpeed = [];
                let CoordinateOBJ = [];
                let tracker_raw_gprs_lists = data.tracker_raw_gprs_lists;
                for (let i = 0; i < tracker_raw_gprs_lists.length; i++) {
                    let veh_direction = tracker_raw_gprs_lists[i].direction;
                    let veh_speed = tracker_raw_gprs_lists[i].speed;
                    let vehicle_status = tracker_raw_gprs_lists[i].vehicle_status;
                    let latitude = tracker_raw_gprs_lists[i].x;
                    let longitude = tracker_raw_gprs_lists[i].y;

                    let shadowUrl = '/static/assets/images/legend/directions/shadex.png';
                    let pick_status = "";
                    let IconSize = 0;
                    if (i === 0) {
                        IconSize = 30;
                        pick_status = "START";
                    } else if (i === tracker_raw_gprs_lists.length - 1) {
                        IconSize = 30;
                        pick_status = "FINISH";
                    } else {
                        IconSize = 15;
                        pick_status = "STANDARD";
                    }

                    let xIcon = L.icon({
                        iconUrl: me.GetImage_IconUrl_VehicleTrip(pick_status, vehicle_status, veh_speed, veh_direction),
                        // shadowUrl: shadowUrl,
                        iconSize: [IconSize, IconSize],
                        shadowSize: [IconSize, IconSize]
                    });

                    let marker = '';
                    marker = L.marker(new L.LatLng(longitude, latitude), {icon: xIcon});

                    DigitalArzModelJS.IndicatorFeature.addLayer(marker);

                    //// GENERATE POLYLINE OBJECT PARAMETERS
                    VehicleSpeed.push(tracker_raw_gprs_lists[i].speed);
                    CoordinateOBJ.push(new L.LatLng(longitude, latitude));

                } //// LOOP END
                DigitalArzModelJS.map.fitBounds(new L.LatLngBounds(CoordinateOBJ));

                // //// ONLY FOR LINE DRAW WITH LENGTH
                // for (let l = 0; l < data.vehicle_tracks_length.length; l++) {
                //     let geojson = JSON.parse(data.vehicle_tracks_length[l].line_geojson);
                //     let line = L.geoJSON(geojson, {
                //         color: 'blue'
                //     }).addTo(DigitalArzModelJS.map);
                //     DigitalArzModelJS.map.fitBounds(line.getBounds());
                // }

                me.GeneratePolyline_VehicleTrip_Speed(CoordinateOBJ, VehicleSpeed);

            }

        });

    }

    //// RETRIEVE SINGLE VEHICLE TRIP HISTORY BY FILTER
    me.RetrieveSingleVehicleHistoryTrip = function (vehicle_id, start_date, end_date) {
        // alert(vehicle_id + " --- " + start_date + " ---- " + end_date);

        let formdata = new FormData();
        formdata.append('vehicle_id', vehicle_id);
        formdata.append('start_date', start_date);
        formdata.append('end_date', end_date);
        var paramas = {
            url: fetch_single_vehicle_trip_history_data,
            data: formdata,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(paramas, function (data) {
            // console.log(data.tracker_raw_gprs_lists.length);

            DigitalArzModelJS.IndicatorFeature.clearLayers();
            DigitalArzModelJS.GroupRouteNetworkLayer.clearLayers();
            if (data.tracker_raw_gprs_lists.length > 0) {

                let VehicleSpeed = [];
                let CoordinateOBJ = [];
                let tracker_raw_gprs_lists = data.tracker_raw_gprs_lists;
                for (let i = 0; i < tracker_raw_gprs_lists.length; i++) {
                    let veh_direction = tracker_raw_gprs_lists[i].direction;
                    let veh_speed = tracker_raw_gprs_lists[i].speed;
                    let vehicle_status = tracker_raw_gprs_lists[i].vehicle_status;
                    let latitude = tracker_raw_gprs_lists[i].x;
                    let longitude = tracker_raw_gprs_lists[i].y;

                    let shadowUrl = '/static/assets/images/legend/directions/shadex.png';
                    let pick_status = "";
                    let IconSize = 0;
                    if (i === 0) {
                        IconSize = 30;
                        pick_status = "START";
                    } else if (i === tracker_raw_gprs_lists.length - 1) {
                        IconSize = 30;
                        pick_status = "FINISH";
                    } else {
                        IconSize = 15;
                        pick_status = "STANDARD";
                    }

                    let xIcon = L.icon({
                        iconUrl: me.GetImage_IconUrl_VehicleTrip(pick_status, vehicle_status, veh_speed, veh_direction),
                        // shadowUrl: shadowUrl,
                        iconSize: [IconSize, IconSize],
                        shadowSize: [IconSize, IconSize]
                    });

                    let marker = '';
                    marker = L.marker(new L.LatLng(longitude, latitude), {icon: xIcon});

                    DigitalArzModelJS.IndicatorFeature.addLayer(marker);

                    //// GENERATE POLYLINE OBJECT PARAMETERS
                    VehicleSpeed.push(tracker_raw_gprs_lists[i].speed);
                    CoordinateOBJ.push(new L.LatLng(longitude, latitude));

                } //// LOOP END
                DigitalArzModelJS.map.fitBounds(new L.LatLngBounds(CoordinateOBJ));

                // //// ONLY FOR LINE DRAW WITH LENGTH
                // for (let l = 0; l < data.vehicle_tracks_length.length; l++) {
                //     let geojson = JSON.parse(data.vehicle_tracks_length[l].line_geojson);
                //     let line = L.geoJSON(geojson, {
                //         color: 'blue'
                //     }).addTo(DigitalArzModelJS.map);
                //     DigitalArzModelJS.map.fitBounds(line.getBounds());
                // }

                me.GeneratePolyline_VehicleTrip_Speed(CoordinateOBJ, VehicleSpeed);

            }

        });

    }

    me.GetImage_IconUrl_VehicleLiveMonitoring = function (vehicle_status, veh_speed, veh_direction) {
        let imgURL = "";
        if (vehicle_status === "Parked" && vehicle_status === "Idle" && veh_speed === 0) {
            imgURL = "/static/assets/images/legend/directions/blue_arrow/" + veh_direction + ".png";
        } else if (vehicle_status === "Moving" && veh_speed === 0) {
            imgURL = "/static/assets/images/legend/directions/blue_arrow/" + veh_direction + ".png";
        } else if (vehicle_status === "Moving" && veh_speed > 0) {
            imgURL = "/static/assets/images/legend/directions/green_arrow/" + veh_direction + ".png";
        } else {
            imgURL = "/static/assets/images/legend/directions/red_arrow/" + veh_direction + ".png";
        }

        return imgURL;


        // var imgURL = "";
        // if (car.Status == null) {
        //     imgURL = "images/directions/red_arrow/" + car.Direction + ".png";
        // }  else if (car.Status.toString().toLocaleUpperCase() == "IGNITION OFF") {
        //     imgURL = "images/directions/brown_arrow/" + car.Direction + ".png";
        // } else if (car.Status.toString().toLocaleUpperCase() == "IGNITION ON" && car.Speed == 0) {

        //     imgURL = "images/directions/blue_arrow/" + car.Direction + ".png";
        // } else if (car.Status.toString().toLocaleUpperCase() == "IGNITION ON" && car.Speed > 0) {
        //     imgURL = "images/directions/green_arrow/" + car.Direction + ".png";
        // } else {
        //     imgURL = "images/directions/red_arrow/" + car.Direction + ".png";
        // }
        // return imgURL;

    }

    me.GetImage_IconUrl_VehicleTrip = function (pick_status, vehicle_status, veh_speed, veh_direction) {
        let imgURL = "";
        if (pick_status === "") {
            // imgURL = "/static/assets/images/legend/directions/red_arrow/" + veh_direction + ".png";
            // imgURL = "/static/assets/images/toolbar/google-marker.png";
        } else if (pick_status === "START") {
            imgURL = "/static/assets/images/legend/toolbar/pickup-marker.png";
        } else if (pick_status === "FINISH") {
            imgURL = "/static/assets/images/legend/toolbar/destination-marker.png";
        } else if (vehicle_status === "Parked" && vehicle_status === "Idle" && veh_speed === 0) {
            imgURL = "/static/assets/images/legend/directions/blue_arrow/" + veh_direction + ".png";
        } else if (vehicle_status === "Moving" && veh_speed === 0) {
            imgURL = "/static/assets/images/legend/directions/blue_arrow/" + veh_direction + ".png";
        } else if (vehicle_status === "Moving" && veh_speed > 0) {
            imgURL = "/static/assets/images/legend/directions/green_arrow/" + veh_direction + ".png";
        } else {
            imgURL = "/static/assets/images/legend/directions/red_arrow/" + veh_direction + ".png";
        }

        return imgURL;


        // var imgURL = "";
        // if (car.Status == null) {
        //     imgURL = "images/directions/red_arrow/" + car.Direction + ".png";
        // }  else if (car.Status.toString().toLocaleUpperCase() == "IGNITION OFF") {
        //     imgURL = "images/directions/brown_arrow/" + car.Direction + ".png";
        // } else if (car.Status.toString().toLocaleUpperCase() == "IGNITION ON" && car.Speed == 0) {

        //     imgURL = "images/directions/blue_arrow/" + car.Direction + ".png";
        // } else if (car.Status.toString().toLocaleUpperCase() == "IGNITION ON" && car.Speed > 0) {
        //     imgURL = "images/directions/green_arrow/" + car.Direction + ".png";
        // } else {
        //     imgURL = "images/directions/red_arrow/" + car.Direction + ".png";
        // }
        // return imgURL;

    }

    me.GetColor_Tooltip_VehicleLiveMonitoring = function (vehicle_status, veh_speed) {
        let imgClass = "";
        if (vehicle_status === "Moving") {
            imgClass = "leaflet-tooltip-veh-moving";
        } else if (vehicle_status === "Idle") {
            imgClass = "leaflet-tooltip-veh-idle";
        } else if (vehicle_status === "Parked") {
            imgClass = "leaflet-tooltip-veh-park";
        } else if (vehicle_status === "Offline") {
            imgClass = "leaflet-tooltip-veh-offline";
        } else {
            imgClass = "leaflet-tooltip";
        }

        return imgClass;
    }

    me.GetColor_Radius_VehicleLiveMonitoring = function (vehicle_status, veh_speed) {
        let imgColor = "";
        if (vehicle_status === "Moving") {
            imgColor = "#65c15c";
        } else if (vehicle_status === "Idle") {
            imgColor = "#2cacec";
        } else if (vehicle_status === "Parked") {
            imgColor = "#FFA941";
        } else if (vehicle_status === "Offline") {
            imgColor = "#838383";
        } else {
            imgColor = "#7366ff";
        }

        return imgColor;
    }

    me.GeneratePolyline_VehicleTrip_Speed = function (CoordinateOBJ, VehicleSpeed) {

        // DigitalArzModelJS.IndicatorFeature.clearLayers();

        // Clear existing polylines
        DigitalArzModelJS.RouteLayerOJB.forEach(polyline => DigitalArzModelJS.map.removeLayer(polyline));
        DigitalArzModelJS.RouteLayerOJB = [];

        let Scolor = "#008000";
        let Greencolor = 'green';
        let YellowColor = 'orange';
        let RedColor = 'red';
        for (let j = 0; j < CoordinateOBJ.length - 1; j++) {
            let pointA = CoordinateOBJ[j];
            let pointB = CoordinateOBJ[j + 1];
            if (VehicleSpeed[j] > 0 && VehicleSpeed[j] < 50) {
                Scolor = Greencolor;
            } else if (VehicleSpeed[j] > 50 && VehicleSpeed[j] < 100) {
                Scolor = YellowColor;
            } else if (VehicleSpeed[j] > 100) {
                Scolor = RedColor;
            }
            let pointList = [pointA, pointB];
            // const polyline = new L.Polyline(pointList, {
            //     color: Scolor,
            //     weight: 3,
            //     opacity: 0.5,
            //     smoothFactor: 1
            // }).addTo(DigitalArzModelJS.map);

            const polyline = new L.Polyline(pointList, {
                color: Scolor,
                weight: 3,
                opacity: 0.5,
                smoothFactor: 1
            });
            DigitalArzModelJS.GroupRouteNetworkLayer.addLayer(polyline);

            DigitalArzModelJS.RouteLayerOJB.push(polyline);
        }

    }

    //// DISPLAY VEHICLE GEO LOCATION ON MAP
    me.DisplayVehicleAllGeoLocationOnMap = function (MakerCoordinate) {
        DigitalArzModelJS.IndicatorFeature.clearLayers();
        DigitalArzModelJS.GroupRouteNetworkLayer.clearLayers();
        if (MakerCoordinate.length > 0) {

            let VehicleSpeed = [];
            let CoordinateOBJ = [];
            let tracker_raw_gprs_lists = data.tracker_raw_gprs_lists;
            for (let i = 0; i < tracker_raw_gprs_lists.length; i++) {
                let veh_direction = tracker_raw_gprs_lists[i].direction;
                let veh_speed = tracker_raw_gprs_lists[i].speed;
                let vehicle_status = tracker_raw_gprs_lists[i].vehicle_status;
                let latitude = tracker_raw_gprs_lists[i].x;
                let longitude = tracker_raw_gprs_lists[i].y;

                //     let shadowUrl = '/static/assets/images/legend/directions/shadex.png';
                //     let pick_status = "";
                //     let IconSize = 0;
                //     if (i === 0) {
                //         IconSize = 30;
                //         pick_status = "START";
                //     } else if (i === tracker_raw_gprs_lists.length - 1) {
                //         IconSize = 30;
                //         pick_status = "FINISH";
                //     } else {
                //         IconSize = 15;
                //         pick_status = "STANDARD";
                //     }
                //
                //     let xIcon = L.icon({
                //         iconUrl: me.GetImage_IconUrl_VehicleTrip(pick_status, vehicle_status, veh_speed, veh_direction),
                //         // shadowUrl: shadowUrl,
                //         iconSize: [IconSize, IconSize],
                //         shadowSize: [IconSize, IconSize]
                //     });
                //
                //     let marker = '';
                //     marker = L.marker(new L.LatLng(longitude, latitude), {icon: xIcon});
                //
                //     DigitalArzModelJS.IndicatorFeature.addLayer(marker);
                //
                //     //// GENERATE POLYLINE OBJECT PARAMETERS
                //     VehicleSpeed.push(tracker_raw_gprs_lists[i].speed);
                //     CoordinateOBJ.push(new L.LatLng(longitude, latitude));
                //
            } //// LOOP END
            // DigitalArzModelJS.map.fitBounds(new L.LatLngBounds(CoordinateOBJ));
            //
            // // //// ONLY FOR LINE DRAW WITH LENGTH
            // // for (let l = 0; l < data.vehicle_tracks_length.length; l++) {
            // //     let geojson = JSON.parse(data.vehicle_tracks_length[l].line_geojson);
            // //     let line = L.geoJSON(geojson, {
            // //         color: 'blue'
            // //     }).addTo(DigitalArzModelJS.map);
            // //     DigitalArzModelJS.map.fitBounds(line.getBounds());
            // // }
            //
            // me.GeneratePolyline_VehicleTrip_Speed(CoordinateOBJ, VehicleSpeed);

        }


    }


}