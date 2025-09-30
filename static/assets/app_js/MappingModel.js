AppMappingModel = function () {

    let me = this;
    me.intervalId = "";
    me.IsRunning = false;

    me.appConstructor = function () {

    };

    me.OnclickVehicleLiveMonitoring_Map = function (parameter, vehicle_status, vehicle_type, vehicle_code) {

        // alert(vehicle_status);

        let vehicle_monitoring = $("#ck_vehicle_monitoring").is(':checked');

        // //// FETCH VEHICLE LIVE MONITORING BY GPRS DATA
        // TOCLayerModelJS.FetchVehicleLiveMonitoringByGPRS();

        if (parameter === "ck_vehicle_monitoring" && vehicle_monitoring === false) {
            clearInterval(me.intervalId);
            console.log("Function stopped");
        }

        if (vehicle_monitoring === true) {
            // Start calling the function every 10 seconds
            me.intervalId = setInterval(function () {
                // method to be executed;
                //// FETCH VEHICLE LIVE MONITORING BY GPRS DATA
                TOCLayerModelJS.FetchVehicleLiveMonitoringByGPRS(vehicle_status, vehicle_type, vehicle_code);
            }, 5000);
        }


    }

}