AppContainerModel = function () {
    let me = this;

    me.appConstructor = function () {

    };

    //// THIS FUNCTION SHOW CONTAINER FEATURE ON MAP (CONDITION STATUS)
    me.ShowContainerFeatureMapBaseStatus = function (feature_json) {
        // console.log(feature_json);

        if (feature_json.length > 0) {
            for (let i = 0; i < feature_json.length; i++) {
                let container_code = feature_json[i].container_code;
                let container_name = feature_json[i].container_name;
                let container_status = feature_json[i].status;
                let latitude = feature_json[i].x;
                let longitude = feature_json[i].y;

                let file_image = "";

                if (container_status === "Active") {
                    file_image = "container_active";
                }
                if (container_status === "Block") {
                    // file_image = "/static/assets/images/toolbar/google-marker.png";
                    file_image = "container_block";
                }

                let marker = '';
                marker = L.marker(new L.LatLng(longitude, latitude), {icon: DigitalArzModelJS.icons[file_image]});

                marker.bindPopup('<div style="width: 300px;"' +
                    '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12" style="padding: 1px; text-align: center;">' +
                    '<strong style="font-size: 16px;">Container Detail</strong></div></div>' +
                    '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                    '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Name:</strong></div>' +
                    '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                    '<div>' + container_name + '</div></div></div>' +
                    // '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                    // '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Name:</strong></div>' +
                    // '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                    // '<div>' + object.name + '</div></div></div>' +
                    // '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                    // '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Status:</strong></div>' +
                    // '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                    // '<div>' + object.working_status + '</div></div></div>' +
                    // '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                    // '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Condition:</strong></div>' +
                    // '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                    // '<div>' + object.asset_condition + '</div></div></div>' +
                    // '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                    // '<div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 text-center" style="padding: 3px;">' +
                    // '<a type="button" class="btn btn-primary btn-xs"' +
                    // "onclick=AMSModelJS.OnClickAssetTypeTabularView('" + editParam + "');>" +
                    // '<i class="fa fa-eye"></i> More Details' +
                    // '</a>' +
                    // '</div></div>' +
                    '</div>');

                DigitalArzModelJS.ContainerFeatureGroup.addLayer(marker);
                // onloadMarkerLayer.addLayer(marker1);
                // DigitalArzModelJS.OnloadMarkerLayerOBJ[container_code + ":" + container_name] = marker.addTo(DigitalArzModelJS.map);


            } //// LOOP FOR FEATURE DATA
        } //// IF FEATURE EXIST THEN

    }

}