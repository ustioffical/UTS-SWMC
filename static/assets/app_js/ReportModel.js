AppReportModel = function () {

    let me = this;

    me.appConstructor = function (page_name) {

        if (page_name === "VehicleHistory") {

            let CurrentDateTime = UtilityModelJS.GetCurrentDateTime();
            document.getElementById("from_datetime").value = CurrentDateTime;
            document.getElementById("to_datetime").value = CurrentDateTime;

        }

        if (page_name === "VehicleRoute") {
        }

    };

    me.onClickVehicleRouteFilter = function () {
        let VehicleType = $("#cmd_vehicle_type").val();
        let VehicleID = $("#cmd_vehicle_list").val();
        // alert(VehicleType + " --- " + VehicleID);

        if (VehicleType === "NA") {
            UtilityModelJS.ToastSweetAlert("top-center", "warning", "Please Select Vehicle Type!!!");
            return true;
        } else if (VehicleID === "NA") {
            UtilityModelJS.ToastSweetAlert("top-center", "warning", "Please Select Vehicle Name!!!");
            return true;
        }

        //// FOR DATE TIME
        let dateFromPG = document.getElementById("selected_date").value;
        if (dateFromPG === "") {
            UtilityModelJS.ToastSweetAlert("top-center", "warning", "From date can not be empty");
            return true;
        }

        let today = new Date().toISOString().split('T')[0];  // Get today's date in YYYY-MM-DD
        if (dateFromPG > today) {
            UtilityModelJS.ToastSweetAlert("top-center", "warning", "Yor can not select Future Data!!!");
            return true;
        }
        //// FOR DATE TIME

        //// TIME DURATION START AND END DATE
        let timeFrom = $("#preloading-start-time").val();
        let timeTo = $("#preloading-end-time").val();

        let fromParts = timeFrom.split(':');
        let toParts = timeTo.split(':');

        let [year, month, day] = dateFromPG.split("-");
        let fromDate = new Date(year, month, day, fromParts[0], fromParts[1]);
        let toDate = new Date(year, month, day, toParts[0], toParts[1]);

        if (fromDate > toDate) {
            UtilityModelJS.ToastSweetAlert("top-center", "warning", "Start time must be earlier than end time.!!!");
            return true;
        }
        //// TIME DURATION START AND END DATE

        VehicleModelJS.RetrieveSingleVehicleRouteJS(VehicleID, dateFromPG, timeFrom, timeTo);

    }

    me.onClickVehicleHistoryFilter = function () {
        let VehicleType = $("#cmd_vehicle_type").val();
        let VehicleID = $("#cmd_vehicle_list").val();
        // alert(VehicleType + " --- " + VehicleID);

        if (VehicleType === "NA") {
            UtilityModelJS.ToastSweetAlert("top-center", "warning", "Please Select Vehicle Type!!!");
            return true;
        } else if (VehicleID === "NA") {
            UtilityModelJS.ToastSweetAlert("top-center", "warning", "Please Select Vehicle Name!!!");
            return true;
        }

        //// FOR DATE TIME
        let datetimeFrom = document.getElementById("from_datetime").value;
        let datetimeFromPG = datetimeFrom.replace("T", " ") + ":00"; // Convert to PG format
        let datetimeTo = document.getElementById("to_datetime").value;
        let datetimeToPG = datetimeTo.replace("T", " ") + ":00"; // Convert to PG format

        if (datetimeFrom === "NA") {
            UtilityModelJS.ToastSweetAlert("top-center", "warning", "From date can not be empty");
            return true;
        } else if (datetimeTo === "NA") {
            UtilityModelJS.ToastSweetAlert("top-center", "warning", "To date can not be empty!!!");
            return true;
        }

        let datetimeFrom_Replace = datetimeFromPG.replace(/-/g, " ");
        let datetimeFrom_New = new Date(datetimeFrom_Replace);

        let datetimeTo_Replace = datetimeToPG.replace(/-/g, " ");
        let datetimeTo_New = new Date(datetimeTo_Replace);
        let CurrentDateTime = new Date();

        if (datetimeFrom_New > datetimeTo_New) {
            UtilityModelJS.ToastSweetAlert("top-center", "warning", "Please Enter Valid Date and Time!!!");
            return true;
        } else if (datetimeFrom_New > CurrentDateTime) {
            UtilityModelJS.ToastSweetAlert("top-center", "warning", "Start Date should not be greater than today Date.!!!");
            return true;
        } else if (datetimeTo_New > CurrentDateTime) {
            UtilityModelJS.ToastSweetAlert("top-center", "warning", "End Date should not be greater than today Date.!!!");
            return true;
        }

        VehicleModelJS.RetrieveSingleVehicleHistoryTrip(VehicleID, datetimeFromPG, datetimeToPG);

    }

}