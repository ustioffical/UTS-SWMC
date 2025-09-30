AppRouteModel = function () {

    let me = this;
    me.selItemCount = 1;
    me.Item_OBJ = [];

    me.appConstructor = function () {

    };

    //// FETCH OSM ROAD NETWORK BY FILTER
    me.FetchOSMRoadNetworkByFilter = function () {
        // alert("ffff");

        let town_code = $("#cmd_town").val();
        let zone_code = $("#cmd_zone").val();
        let mc_code = $("#cmd_mc").val();

        if (town_code === "NA") {
            UtilityModelJS.ToastSweetAlert("top-end", "warning", "Please Select At-least One System Hierarchy!!!");
            return true;
        }

        let formdata = new FormData();
        formdata.append('town_code', town_code);
        formdata.append('zone_code', zone_code);
        formdata.append('mc_code', mc_code);

        var params = {
            url: fetch_osm_network_by_filter,
            data: formdata,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(params, function (data) {

            if (data.message === "Success") {
                let feature_geojson = data.feature_lists[0].geojson.features;
                if (feature_geojson !== null) {
                    var osm_feature_lists = data.feature_lists;
                    if (osm_feature_lists.length > 0) {
                        GroupRouteNetworkLayer = L.geoJSON(osm_feature_lists[0].geojson, {
                            // style: myStyle, onEachFeature: onEachFeature
                            style: function (feature) {
                                return {color: "#1F6ED4"};
                            }, onEachFeature: DigitalArzModelJS.OnEachFeature
                        }).addTo(DigitalArzModelJS.map);
                    }
                }

            }

        });

    }

    me.AddonCreateNetworkItem_Box = function () {
        //// TYPE OSM, Draw, Google

        let type = $("#hid_type").val();
        let unique_code = $("#hid_unique_id").val();
        let address = $("#id_address").val();
        let address_split = address.split('::');
        let feature_coordinate = $("#feature_coordinate").val();

        $("#tbody-create-network-item-table").append('<tr>' +
            '<td>' + me.selItemCount + '</td>' +
            '<td><h6 class="f-14 mb-0">' + type + '</h6></td>' +
            '<td>' +
            '<input class="form-control" id="input_asset_name_' + me.selItemCount + '" name="input_asset_name[]" type="text" placeholder="Road name" ' +
            "oninput=me.UpdateSelectedRouteName_CR('" + me.selItemCount + "'); value='" + address_split[0] + "'>" +
            '</td>' +
            '<td><h6 class="f-14 mb-0">' + address + '</h6></td>' +
            '<td><div class="common-align gap-2 justify-content-end">' +
            '<a class="square-white" href="add-user.html">' +
            '<svg><use href="/static/assets/svg/icon-sprite.svg#edit-content"></use></svg>' +
            '</a>' +
            '<a class="square-white" href="add-user.html">' +
            '<svg><use href="/static/assets/svg/icon-sprite.svg#trash1"></use></svg>' +
            '</a>' +
            '<a class="square-white" href="add-user.html">' +
            '<svg><use href="/static/assets/svg/icon-sprite.svg#view-member"></use></svg>' +
            '</a></div></td></tr>');

        me.Item_OBJ.push({
            sl: me.selItemCount,
            type: type,
            unique_code: unique_code,
            route_name: address_split[0],
            feature_coordinate: feature_coordinate
        });

        me.selItemCount++;
    }

    // ON INPUT NAME UPDATE ROUTE NETWORK NAME
    me.UpdateSelectedRouteName_CR = function (selected_index) {
        let get_asset_type_item_name = $("#input_asset_name_" + selected_index).val();

        // Remove leading spaces
        let asset_name_start_spaces = get_asset_type_item_name.replace(/^\s+/, '');
        // Remove trailing spaces except for one space at the end
        let asset_name_end_spaces = asset_name_start_spaces.replace(/\s{2,}$/, ' ');
        // Remove Special Chracters
        let asset_name_outString = asset_name_end_spaces.replace(/[`~!@#$%^&*()_|+\-=?;:'",.<>\[\]\/]/gi, '');

        for (let p = 0; p < me.Item_OBJ.length; p++) {
            if (me.Item_OBJ[p].sl === parseInt(selected_index)) {
                me.Item_OBJ[p].route_name = asset_name_outString;
            }
        }

    }

}