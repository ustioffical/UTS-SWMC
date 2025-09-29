/**
 *
 * Created by FarhanTa on 5/23/2023.
 */

AppTOCLayerModel = function () {

    let me = this;
    me.GroupColorJson = {}

    me.TownBoundaryLayer;
    me.ZoneBoundaryLayer;
    me.UCBoundaryLayer;
    me.OSMRoadNetwork;

    me.cqlQuery;

    me.appConstructor = function () {

    };

    //// DISPLAY TOWN BOUNDARY ////
    me.DisplayTownBoundaryLayer = function () {
        if (me.TownBoundaryLayer !== undefined) {
            DigitalArzModelJS.map.removeLayer(me.TownBoundaryLayer);
        }

        me.TownBoundaryLayer = L.tileLayer.betterWms('http://167.99.158.1:8080/geoserver/LWMC/wms?', {
            layers: 'LWMC:tbl_town_boundary',
            format: 'image/png',
            transparent: true,
            version: '1.1.0',
            proxy: 'getProxyUrl',
            // CQL_FILTER: me.cqlQuery,
            proxyParamName: 'url',
            maxZoom: 22
        }).addTo(DigitalArzModelJS.map);
        me.TownBoundaryLayer.bringToFront();
    }

    //// DISPLAY ZONE BOUNDARY ////
    me.DisplayZoneBoundaryLayer = function () {
        if (me.ZoneBoundaryLayer !== undefined) {
            DigitalArzModelJS.map.removeLayer(me.ZoneBoundaryLayer);
        }

        me.ZoneBoundaryLayer = L.tileLayer.betterWms('http://167.99.158.1:8080/geoserver/LWMC/wms?', {
            layers: 'LWMC:tbl_zone_boundary',
            format: 'image/png',
            transparent: true,
            version: '1.1.0',
            proxy: 'getProxyUrl',
            // CQL_FILTER: me.cqlQuery,
            proxyParamName: 'url',
            maxZoom: 22
        }).addTo(DigitalArzModelJS.map);
        me.ZoneBoundaryLayer.bringToFront();
    }

    //// DISPLAY UC BOUNDARY ////
    me.DisplayUCBoundaryLayer = function () {
        if (me.UCBoundaryLayer !== undefined) {
            DigitalArzModelJS.map.removeLayer(me.UCBoundaryLayer);
        }

        me.UCBoundaryLayer = L.tileLayer.betterWms('http://167.99.158.1:8080/geoserver/LWMC/wms?', {
            layers: 'LWMC:tbl_uc_boundary',
            format: 'image/png',
            transparent: true,
            version: '1.1.0',
            proxy: 'getProxyUrl',
            // CQL_FILTER: me.cqlQuery,
            proxyParamName: 'url',
            maxZoom: 22
        }).addTo(DigitalArzModelJS.map);
        me.UCBoundaryLayer.bringToFront();
    }

    //// DISPLAY OSM Road Network ////
    me.DisplayOSMRoadNetworkLayer = function () {
        if (me.OSMRoadNetwork !== undefined) {
            DigitalArzModelJS.map.removeLayer(me.OSMRoadNetwork);
        }

        me.OSMRoadNetwork = L.tileLayer.betterWms('http://167.99.158.1:8080/geoserver/LWMC/wms?', {
            layers: 'LWMC:tbl_osm_road_network',
            format: 'image/png',
            transparent: true,
            version: '1.1.0',
            proxy: 'getProxyUrl',
            // CQL_FILTER: me.cqlQuery,
            proxyParamName: 'url',
            maxZoom: 22
        }).addTo(DigitalArzModelJS.map);
        me.OSMRoadNetwork.bringToFront();
    }

    //// ASSET LIST ////

    //// FETCH COLLECTION SITE FEATURE DATA
    me.FetchCollectionSiteData = function () {
        let params = {
            url: fetch_collection_site_feature_data,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(params, function (data) {
            // console.log(data);
            if (data.message === "Success") {

                if (data.feature_lists.length > 0) {
                    for (let i = 0; i < data.feature_lists.length; i++) {

                        let code = data.feature_lists[i].tcp_code;
                        let name = data.feature_lists[i].tcp_name;
                        let status = data.feature_lists[i].status;
                        let latitude = data.feature_lists[i].x;
                        let longitude = data.feature_lists[i].y;

                        let file_image = "";
                        if (status === "Active") {
                            file_image = "collection_site";
                        }

                        let marker = "";
                        marker = L.marker(new L.LatLng(longitude, latitude), {icon: DigitalArzModelJS.icons[file_image]});

                        marker.bindPopup('<div style="width: 300px;"' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12" style="padding: 1px; text-align: center;">' +
                            '<strong style="font-size: 16px;">Filling Station Detail</strong></div></div>' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                            '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Name:</strong></div>' +
                            '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                            '<div>' + name + '</div></div></div>' +
                            '</div>');
                        DigitalArzModelJS.CollectionSiteFeatureGroup.addLayer(marker);

                    } //// LOOP FOR FEATURE DATA
                } //// IF FEATURE EXIST THEN

            }

        });

    }

    //// FETCH DUMPING SITE FEATURE DATA
    me.FetchDumpingSiteData = function () {
        let params = {
            url: fetch_dumping_site_feature_data,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(params, function (data) {
            // console.log(data);
            if (data.message === "Success") {

                if (data.feature_lists.length > 0) {
                    for (let i = 0; i < data.feature_lists.length; i++) {

                        let code = data.feature_lists[i].code;
                        let name = data.feature_lists[i].name;
                        let status = data.feature_lists[i].status;
                        let latitude = data.feature_lists[i].x;
                        let longitude = data.feature_lists[i].y;

                        let file_image = "";
                        if (status === "Active") {
                            file_image = "dumping_site_active";
                        }
                        //         if (container_status === "Block") {
                        //             file_image = "container_block";
                        //         }

                        let marker = "";
                        marker = L.marker(new L.LatLng(longitude, latitude), {icon: DigitalArzModelJS.icons[file_image]});

                        marker.bindPopup('<div style="width: 300px;"' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12" style="padding: 1px; text-align: center;">' +
                            '<strong style="font-size: 16px;">Filling Station Detail</strong></div></div>' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                            '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Name:</strong></div>' +
                            '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                            '<div>' + name + '</div></div></div>' +
                            '</div>');
                        DigitalArzModelJS.DumpingSiteFeatureGroup.addLayer(marker);

                    } //// LOOP FOR FEATURE DATA
                } //// IF FEATURE EXIST THEN

            }

        });

    }

    //// FETCH DUMPING COVERAGE FEATURE DATA
    me.FetchDumpingCoverageData = function () {
        let params = {
            url: fetch_dumping_coverage_feature_data,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(params, function (data) {
            if (data.message === "Success") {
                let features = data.feature_lists[0].geojson.features;
                if (features === null) {
                } else {

                    for (let f = 0; f < features.length; f++) {

                        let coordinates = features[f].geometry.coordinates[0][0];
                        const coordinates_2d = []; // Create inner array for each row
                        for (let i = 0; i < coordinates.length; i++) {
                            let lat = coordinates[i][1];
                            let lng = coordinates[i][0];
                            coordinates[i][0] = lat;
                            coordinates[i][1] = lng;
                        }

                        const polygon = L.polygon(coordinates, {
                            fillColor: "transparent",  // No fill color
                            fillOpacity: 0,           // Completely transparent fill
                            color: "#3388ff",         // Border color
                            weight: 3,                // Border width
                            opacity: 1,               // Border opacity
                            dashArray: "5, 5"         // Optional: dashed border
                        });
                        DigitalArzModelJS.DumpingCoverageFeatureGroup.addLayer(polygon);

                    } //// LOOP FOR FEATURE DATA

                } //// IF FEATURE EXIST THEN

            }

        });

    }

    //// FETCH WEIGHING SITE FEATURE DATA
    me.FetchWeighingSiteData = function () {
        let params = {
            url: fetch_weighing_site_feature_data,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(params, function (data) {
            // console.log(data);
            if (data.message === "Success") {

                if (data.feature_lists.length > 0) {
                    for (let i = 0; i < data.feature_lists.length; i++) {

                        let code = data.feature_lists[i].code;
                        let name = data.feature_lists[i].name;
                        let status = data.feature_lists[i].status;
                        let latitude = data.feature_lists[i].x;
                        let longitude = data.feature_lists[i].y;

                        let file_image = "";
                        if (status === "Active") {
                            file_image = "weighing_site";
                        }
                        //         if (container_status === "Block") {
                        //             file_image = "container_block";
                        //         }

                        let marker = "";
                        marker = L.marker(new L.LatLng(longitude, latitude), {icon: DigitalArzModelJS.icons[file_image]});

                        marker.bindPopup('<div style="width: 300px;"' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12" style="padding: 1px; text-align: center;">' +
                            '<strong style="font-size: 16px;">Filling Station Detail</strong></div></div>' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                            '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Name:</strong></div>' +
                            '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                            '<div>' + name + '</div></div></div>' +
                            '</div>');
                        DigitalArzModelJS.WeighingSiteFeatureGroup.addLayer(marker);

                    } //// LOOP FOR FEATURE DATA
                } //// IF FEATURE EXIST THEN

            }

        });

    }

    //// FETCH WEIGHING COVERAGE FEATURE DATA
    me.FetchWeighingCoverageData = function () {
        let params = {
            url: fetch_weighing_coverage_feature_data,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(params, function (data) {
            if (data.message === "Success") {
                let features = data.feature_lists[0].geojson.features;
                if (features === null) {
                } else {

                    for (let f = 0; f < features.length; f++) {

                        let coordinates = features[f].geometry.coordinates[0][0];
                        const coordinates_2d = []; // Create inner array for each row
                        for (let i = 0; i < coordinates.length; i++) {
                            let lat = coordinates[i][1];
                            let lng = coordinates[i][0];
                            coordinates[i][0] = lat;
                            coordinates[i][1] = lng;
                        }

                        const polygon = L.polygon(coordinates, {
                            fillColor: "transparent",  // No fill color
                            fillOpacity: 0,           // Completely transparent fill
                            color: "#FF0A0A",         // Border color
                            weight: 3,                // Border width
                            opacity: 1,               // Border opacity
                            dashArray: "5, 5"         // Optional: dashed border
                        });
                        DigitalArzModelJS.WeighingCoverageFeatureGroup.addLayer(polygon);

                    } //// LOOP FOR FEATURE DATA

                } //// IF FEATURE EXIST THEN

            }

        });

    }

    //// FETCH PARKING SITE FEATURE DATA
    me.FetchParkingSiteData = function () {
        let params = {
            url: fetch_parking_site_feature_data,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(params, function (data) {
            // console.log(data);
            if (data.message === "Success") {

                if (data.feature_lists.length > 0) {
                    for (let i = 0; i < data.feature_lists.length; i++) {

                        let code = data.feature_lists[i].code;
                        let name = data.feature_lists[i].name;
                        let status = data.feature_lists[i].status;
                        let latitude = data.feature_lists[i].x;
                        let longitude = data.feature_lists[i].y;

                        let file_image = "";
                        if (status === "Active") {
                            file_image = "parking_site_active";
                        }
                        //         if (container_status === "Block") {
                        //             file_image = "container_block";
                        //         }

                        let marker = "";
                        marker = L.marker(new L.LatLng(longitude, latitude), {icon: DigitalArzModelJS.icons[file_image]});

                        marker.bindPopup('<div style="width: 300px;"' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12" style="padding: 1px; text-align: center;">' +
                            '<strong style="font-size: 16px;">Filling Station Detail</strong></div></div>' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                            '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Name:</strong></div>' +
                            '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                            '<div>' + name + '</div></div></div>' +
                            '</div>');
                        DigitalArzModelJS.ParkingSiteFeatureGroup.addLayer(marker);

                    } //// LOOP FOR FEATURE DATA
                } //// IF FEATURE EXIST THEN

            }

        });

    }

    //// FETCH WORKSHOP FEATURE DATA
    me.FetchWorkshopData = function () {
        let params = {
            url: fetch_workshop_feature_data,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(params, function (data) {
            // console.log(data);
            if (data.message === "Success") {

                if (data.feature_lists.length > 0) {
                    for (let i = 0; i < data.feature_lists.length; i++) {

                        let code = data.feature_lists[i].code;
                        let name = data.feature_lists[i].name;
                        let status = data.feature_lists[i].status;
                        let latitude = data.feature_lists[i].x;
                        let longitude = data.feature_lists[i].y;

                        let file_image = "";
                        if (status === "Active") {
                            file_image = "workshop_active";
                        }
                        //         if (container_status === "Block") {
                        //             file_image = "container_block";
                        //         }

                        let marker = '';
                        marker = L.marker(new L.LatLng(longitude, latitude), {icon: DigitalArzModelJS.icons[file_image]});

                        marker.bindPopup('<div style="width: 300px;"' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12" style="padding: 1px; text-align: center;">' +
                            '<strong style="font-size: 16px;">Filling Station Detail</strong></div></div>' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                            '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Name:</strong></div>' +
                            '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                            '<div>' + name + '</div></div></div>' +
                            '</div>');
                        DigitalArzModelJS.WorkshopFeatureGroup.addLayer(marker);

                    } //// LOOP FOR FEATURE DATA
                } //// IF FEATURE EXIST THEN

            }

        });

    }

    //// FETCH FILLING STATION FEATURE DATA
    me.FetchFillingStationData = function () {
        let params = {
            url: fetch_filling_station_feature_data,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(params, function (data) {
            // console.log(data);
            if (data.message === "Success") {

                if (data.feature_lists.length > 0) {
                    for (let i = 0; i < data.feature_lists.length; i++) {

                        let code = data.feature_lists[i].code;
                        let name = data.feature_lists[i].name;
                        let status = data.feature_lists[i].status;
                        let latitude = data.feature_lists[i].x;
                        let longitude = data.feature_lists[i].y;

                        let file_image = "";
                        if (status === "Active") {
                            file_image = "fs_active";
                        }
                        //         if (container_status === "Block") {
                        //             file_image = "container_block";
                        //         }

                        let marker = '';
                        marker = L.marker(new L.LatLng(longitude, latitude), {icon: DigitalArzModelJS.icons[file_image]});

                        marker.bindPopup('<div style="width: 300px;"' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12" style="padding: 1px; text-align: center;">' +
                            '<strong style="font-size: 16px;">Filling Station Detail</strong></div></div>' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                            '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Name:</strong></div>' +
                            '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                            '<div>' + name + '</div></div></div>' +
                            '</div>');
                        DigitalArzModelJS.FillingStationFeatureGroup.addLayer(marker);

                    } //// LOOP FOR FEATURE DATA
                } //// IF FEATURE EXIST THEN

            }

        });

    }

    //// FETCH CONTAINER FEATURE DATA
    me.FetchContainerFeatureData = function () {
        var params = {
            url: fetch_container_feature_data,
            // data: formdata,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(params, function (data) {
            if (data.message === "Success") {

                if (data.feature_lists.length > 0) {
                    for (let i = 0; i < data.feature_lists.length; i++) {

                        let container_code = data.feature_lists[i].container_code;
                        let container_name = data.feature_lists[i].container_name;
                        let container_status = data.feature_lists[i].status;
                        let latitude = data.feature_lists[i].x;
                        let longitude = data.feature_lists[i].y;

                        let file_image = "container_to_be_visited";

                        // if (container_status === "Active") {
                        //     file_image = "container_active";
                        // }
                        // if (container_status === "Block") {
                        //     // file_image = "/static/assets/images/toolbar/google-marker.png";
                        //     file_image = "container_block";
                        // }

                        let marker = '';
                        marker = L.marker(new L.LatLng(longitude, latitude), {icon: DigitalArzModelJS.icons[file_image]});

                        marker.bindPopup('<div style="width: 300px;"' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12" style="padding: 1px; text-align: center;">' +
                            '<strong style="font-size: 16px;">Container Detail</strong></div></div>' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                            '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Name:</strong></div>' +
                            '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                            '<div>' + container_name + '</div></div></div>' +
                            '</div>');
                        DigitalArzModelJS.ContainerFeatureGroup.addLayer(marker);

                    } //// LOOP FOR FEATURE DATA
                } //// IF FEATURE EXIST THEN

            }

        });

    }

    //// FETCH DRUM FEATURE DATA
    me.FetchDrumFeatureData = function () {
        var params = {
            url: fetch_drum_feature_data,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(params, function (data) {
            if (data.message === "Success") {

                if (data.feature_lists.length > 0) {
                    for (let i = 0; i < data.feature_lists.length; i++) {

                        let drum_code = data.feature_lists[i].drum_code;
                        let drum_name = data.feature_lists[i].drum_name;
                        let drum_status = data.feature_lists[i].status;
                        let latitude = data.feature_lists[i].x;
                        let longitude = data.feature_lists[i].y;

                        let file_image = "drum_to_be_visited";

                        // if (drum_status === "Active") {
                        //     file_image = "drum_to_be_visited";
                        // }
                        // if (drum_status === "Block") {
                        //     // file_image = "/static/assets/images/toolbar/google-marker.png";
                        //     file_image = "container_block";
                        // }

                        let marker = '';
                        marker = L.marker(new L.LatLng(longitude, latitude), {icon: DigitalArzModelJS.icons[file_image]});

                        marker.bindPopup('<div style="width: 300px;"' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12" style="padding: 1px; text-align: center;">' +
                            '<strong style="font-size: 16px;">Drum Detail</strong></div></div>' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                            '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Name:</strong></div>' +
                            '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                            '<div>' + drum_name + '</div></div></div>' +
                            '</div>');
                        DigitalArzModelJS.DrumFeatureGroup.addLayer(marker);

                    } //// LOOP FOR FEATURE DATA
                } //// IF FEATURE EXIST THEN

            }

        });

    }

    //// FETCH CONTAINER FEATURE BASED ON PROCESS TYPE
    me.FetchContainerFeatureData_ProcessType = function () {
        // alert("ffff");

        // let town_code = $("#cmd_town").val();
        //
        // let formdata = new FormData();
        // formdata.append('town_code', town_code);

        var params = {
            url: fetch_container_feature_process_type_data,
            // data: formdata,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(params, function (data) {
            if (data.message === "Success") {

                if (data.feature_lists.length > 0) {
                    for (let i = 0; i < data.feature_lists.length; i++) {

                        let container_code = data.feature_lists[i].container_code_id;
                        let container_name = data.feature_lists[i].container_name;
                        let cont_proc_type_name = data.feature_lists[i].cont_proc_type_name;
                        let latitude = data.feature_lists[i].x;
                        let longitude = data.feature_lists[i].y;

                        let file_image = "";

                        if (cont_proc_type_name === "Visited") {
                            file_image = "container_visited";
                        }
                        if (cont_proc_type_name === "To be Visited") {
                            // file_image = "/static/assets/images/toolbar/google-marker.png";
                            file_image = "container_to_be_visited";
                        }
                        if (cont_proc_type_name === "Visited but Not Dumped") {
                            // file_image = "/static/assets/images/toolbar/google-marker.png";
                            file_image = "container_visited_but_not_dumped";
                        }

                        let marker = '';
                        marker = L.marker(new L.LatLng(longitude, latitude), {icon: DigitalArzModelJS.icons[file_image]});

                        marker.bindPopup('<div style="width: 300px;"' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12" style="padding: 1px; text-align: center;">' +
                            '<strong style="font-size: 16px;">Container Detail (Code : ' + container_code + ')</strong></div></div>' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                            '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Name:</strong></div>' +
                            '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                            '<div>' + container_name + '</div></div></div>' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                            '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Name:</strong></div>' +
                            '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                            '<div>' + container_name + '</div></div></div>' +
                            '</div>');
                        DigitalArzModelJS.ContainerFeatureGroup.addLayer(marker);

                    } //// LOOP FOR FEATURE DATA
                } //// IF FEATURE EXIST THEN

            }

        });

    }

    //// FETCH ROAD NETWORK SCHEDULE FEATURE
    me.FetchRouteNetworkScheduleFeature = function () {
        // alert("ffff");

        // let town_code = $("#cmd_town").val();
        //
        // let formdata = new FormData();
        // formdata.append('town_code', town_code);

        var params = {
            url: fetch_route_network_schedule_feature,
            // data: formdata,
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
                                let assign_color = me.GroupColorJson[feature.properties.sche_group_code];
                                return {
                                    fillColor: assign_color,  // Fill color of the polygon
                                    weight: 1,          // Border weight
                                    color: assign_color,     // Border color
                                    fillOpacity: 0.9    // Fill opacity
                                };
                            }, onEachFeature: DigitalArzModelJS.OnEachFeature
                        }).addTo(DigitalArzModelJS.map);
                    }
                }

            }

        });

    }

    //// FETCH VEHICLE FEATURE DATA
    me.FetchVehicleFeatureData = function (action, feature_json) {

        if (action === "Onload") {

            if (feature_json.length > 0) {
                for (let i = 0; i < feature_json.length; i++) {

                    let register_no = feature_json[i].register_no;
                    let latitude = feature_json[i].x;
                    let longitude = feature_json[i].y;

                    let file_image = "vehicle";

                    let marker = '';
                    marker = L.marker(new L.LatLng(longitude, latitude), {icon: DigitalArzModelJS.icons[file_image]});

                    marker.bindPopup('<div style="width: 300px;"' +
                        '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12" style="padding: 1px; text-align: center;">' +
                        '<strong style="font-size: 16px;">Vehicle Detail</strong></div></div>' +
                        '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                        '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>PITB Code:</strong></div>' +
                        '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                        '<div>' + feature_json[i].pitb_code + '</div></div></div>' +
                        '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                        '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Register No.:</strong></div>' +
                        '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                        '<div>' + register_no + '</div></div></div>' +
                        '</div>');
                    DigitalArzModelJS.VehicleLayer.addLayer(marker);

                    //// VEHICLE RADIUS
                    let radius = 50;
                    let marker_circle = L.circle([longitude, latitude], {
                        radius: radius, // radius in meters
                        color: '#b5ea9a', // optional: circle color
                        fillColor: '#b5ea9a', // optional: fill color
                        fillOpacity: 0.3 // optional: fill opacity
                    });
                    DigitalArzModelJS.VehicleRadiusLayer.addLayer(marker_circle);

                } //// LOOP FOR FEATURE DATA
                // 5. Fit map to the bounds of the FeatureGroup
                DigitalArzModelJS.map.fitBounds(DigitalArzModelJS.VehicleRadiusLayer.getBounds());
            } //// IF FEATURE EXIST THEN
        }

        if (action === "Ajax") {
            var params = {
                url: fetch_vehicle_feature_data,
                // data: formdata,
                type: "POST",
                dataType: 'json',
                headers: {'X-CSRFToken': posttoken}
            };
            callAJAX(params, function (data) {
                if (data.message === "Success") {

                    if (data.feature_lists.length > 0) {
                        for (let i = 0; i < data.feature_lists.length; i++) {

                            let register_no = data.feature_lists[i].register_no;
                            let latitude = data.feature_lists[i].x;
                            let longitude = data.feature_lists[i].y;

                            let file_image = "vehicle";

                            let marker = '';
                            marker = L.marker(new L.LatLng(longitude, latitude), {icon: DigitalArzModelJS.icons[file_image]});

                            marker.bindPopup('<div style="width: 300px;"' +
                                '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12" style="padding: 1px; text-align: center;">' +
                                '<strong style="font-size: 16px;">Vehicle Detail</strong></div></div>' +
                                '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                                '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Register No.:</strong></div>' +
                                '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                                '<div>' + register_no + '</div></div></div>' +
                                '</div>');
                            DigitalArzModelJS.VehicleLayer.addLayer(marker);

                            //// VEHICLE RADIUS
                            let radius = 50;
                            let marker_circle = L.circle([longitude, latitude], {
                                radius: radius, // radius in meters
                                color: '#b5ea9a', // optional: circle color
                                fillColor: '#b5ea9a', // optional: fill color
                                fillOpacity: 0.3 // optional: fill opacity
                            });
                            DigitalArzModelJS.VehicleRadiusLayer.addLayer(marker_circle);

                        } //// LOOP FOR FEATURE DATA
                        // 5. Fit map to the bounds of the FeatureGroup
                        DigitalArzModelJS.map.fitBounds(DigitalArzModelJS.VehicleRadiusLayer.getBounds());
                    } //// IF FEATURE EXIST THEN

                }

            });
        }

    }

    //// FETCH VEHICLE LIVE MONITORING BY GPRS DATA
    me.FetchVehicleLiveMonitoringByGPRS = function (vehicle_status, vehicle_type, vehicle_code) {
        let formdata = new FormData();
        formdata.append('vehicle_status', vehicle_status);
        formdata.append('vehicle_type', vehicle_type);
        formdata.append('vehicle_code', vehicle_code);
        var params = {
            url: fetch_vehicle_live_monitoring_gprs,
            data: formdata,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(params, function (data) {
            if (data.message === "Success") {
                if (data.feature_lists.length > 0) {
                    DigitalArzModelJS.VehicleLayer.clearLayers();
                    DigitalArzModelJS.VehicleRadiusLayer.clearLayers();
                    for (let i = 0; i < data.feature_lists.length; i++) {

                        let register_no = data.feature_lists[i].register_no;
                        let pitb_code = data.feature_lists[i].pitb_code;
                        let veh_type = data.feature_lists[i].vehicle_type;
                        let veh_direction = data.feature_lists[i].direction;
                        let veh_speed = data.feature_lists[i].speed;
                        let vehicle_status = data.feature_lists[i].g_status;
                        let latitude = data.feature_lists[i].x;
                        let longitude = data.feature_lists[i].y;

                        let IconSize = 20;
                        let xIcon = L.icon({
                            iconUrl: VehicleModelJS.GetImage_IconUrl_VehicleLiveMonitoring(vehicle_status, veh_speed, veh_direction),
                            // shadowUrl: shadowUrl,
                            iconSize: [IconSize, IconSize],
                            shadowSize: [IconSize, IconSize]
                        });

                        let marker = '';
                        marker = L.marker(new L.LatLng(longitude, latitude), {icon: xIcon});

                        let vehicle_live_label_html = $("#vehicle_live_label").is(':checked');
                        if (vehicle_live_label_html === true) {
                            marker.bindTooltip("<div>" + veh_type + " - " + pitb_code + " - " + veh_speed + "</div>", {
                                permanent: true,
                                direction: 'top',
                                offset: [0, -10],
                                className: VehicleModelJS.GetColor_Tooltip_VehicleLiveMonitoring(vehicle_status, veh_speed),
                            });
                        }

                        DigitalArzModelJS.VehicleLayer.addLayer(marker);

                        // let file_image = "vehicle";
                        //
                        // let marker = '';
                        // marker = L.marker(new L.LatLng(longitude, latitude), {icon: DigitalArzModelJS.icons[file_image]});

                        // marker.bindPopup('<div style="width: 300px;"' +
                        //     '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12" style="padding: 1px; text-align: center;">' +
                        //     '<strong style="font-size: 16px;">Vehicle Detail</strong></div></div>' +
                        //     '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                        //     '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Register No.:</strong></div>' +
                        //     '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                        //     '<div>' + register_no + '</div></div></div>' +
                        //     '</div>');
                        // DigitalArzModelJS.VehicleLayer.addLayer(marker);
                        //
                        //// VEHICLE RADIUS
                        let radius = 30;
                        let marker_circle = L.circle([longitude, latitude], {
                            radius: radius, // radius in meters
                            color: VehicleModelJS.GetColor_Radius_VehicleLiveMonitoring(vehicle_status, veh_speed), // optional: circle color
                            fillColor: VehicleModelJS.GetColor_Radius_VehicleLiveMonitoring(vehicle_status, veh_speed), // optional: fill color
                            fillOpacity: 0.3 // optional: fill opacity
                        });
                        DigitalArzModelJS.VehicleRadiusLayer.addLayer(marker_circle);


                    } //// LOOP FOR FEATURE DATA
                } //// IF FEATURE EXIST THEN

                //// VEHICLE SUMMARY ////
                if (data.vehicle_g_status.length > 0) {

                    let vehicle_moving = 0;
                    let vehicle_idle = 0;
                    let vehicle_stop_park = 0;
                    let vehicle_offline = 0;
                    let vehicle_total = 0;

                    for (let i = 0; i < data.vehicle_g_status.length; i++) {
                        let vehicle_g_status = data.vehicle_g_status[i].g_status;
                        if (vehicle_g_status === "Moving") {
                            vehicle_moving = parseInt(data.vehicle_g_status[i].count);
                        } else if (vehicle_g_status === "Idle") {
                            vehicle_idle = parseInt(data.vehicle_g_status[i].count);
                        } else if (vehicle_g_status === "Parked") {
                            vehicle_stop_park = parseInt(data.vehicle_g_status[i].count);
                        } else if (vehicle_g_status === "Offline") {
                            vehicle_moving = parseInt(data.vehicle_g_status[i].count);
                        }
                        vehicle_total += parseInt(data.vehicle_g_status[i].count);
                    }

                    document.getElementById("summary_total_vehicle").innerHTML = vehicle_total.toLocaleString();
                    document.getElementById("summary_moving_vehicle").innerHTML = vehicle_moving.toLocaleString();
                    document.getElementById("summary_idle_vehicle").innerHTML = vehicle_idle.toLocaleString();
                    document.getElementById("summary_stop_park_vehicle").innerHTML = vehicle_stop_park.toLocaleString();
                    document.getElementById("summary_offline_vehicle").innerHTML = vehicle_offline.toLocaleString();

                }
                //// VEHICLE SUMMARY ////

            }

        });

    }

    //// FETCH LANDUSE BOUNDARY FEATURE DATA
    me.FetchLanduseBoundaryFeatureData = function () {
        let params = {
            url: fetch_landuse_boundary_feature_data,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(params, function (data) {
            if (data.message === "Success") {
                let features = data.feature_lists[0].geojson.features;
                if (features === null) {
                } else {

                    for (let f = 0; f < features.length; f++) {

                        let coordinates = features[f].geometry.coordinates[0][0];
                        const coordinates_2d = []; // Create inner array for each row
                        for (let i = 0; i < coordinates.length; i++) {
                            let lat = coordinates[i][1];
                            let lng = coordinates[i][0];
                            coordinates[i][0] = lat;
                            coordinates[i][1] = lng;
                        }

                        const polygon = L.polygon(coordinates, {
                            color: '#a19af4',
                            dashArray: '5, 5', // Creates a dashed effect
                            fillColor: UtilityModelJS.GetRandomColor(),
                            // fillOpacity: 0.35, // set fill opacity
                            // opacity: 0.35, // set desired opacity
                            fillOpacity: 0, // set fill opacity
                            opacity: 1, // set desired opacity
                            width: 1
                        });
                        DigitalArzModelJS.LanduseBoundaryFeatureGroup.addLayer(polygon);

                    } //// LOOP FOR FEATURE DATA

                } //// IF FEATURE EXIST THEN

            }

        });

    }

    //// FETCH ADMINISTRATIVE BOUNDARY FEATURE DATA
    me.FetchAdministrativeBoundaryFeatureData = function () {
        let params = {
            url: fetch_admin_boundary_feature_data,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(params, function (data) {
            if (data.message === "Success") {
                let features = data.feature_lists[0].geojson.features;
                if (features === null) {
                } else {

                    for (let f = 0; f < features.length; f++) {

                        let coordinates = features[f].geometry.coordinates[0][0];
                        const coordinates_2d = []; // Create inner array for each row
                        for (let i = 0; i < coordinates.length; i++) {
                            let lat = coordinates[i][1];
                            let lng = coordinates[i][0];
                            coordinates[i][0] = lat;
                            coordinates[i][1] = lng;
                        }

                        const polygon = L.polygon(coordinates, {
                            color: '#FFFAFA', fillColor: UtilityModelJS.GetRandomColor(),
                            opacity: 0.35, // set desired opacity
                            fillOpacity: 0.35, // set fill opacity
                            width: 1
                        });

                        //// Add label at the center
                        polygon.bindTooltip(features[f].properties.admin_name, {
                            permanent: true,
                            direction: 'center',
                            className: 'polygon-label'
                        });

                        DigitalArzModelJS.AdminBoundaryFeatureGroup.addLayer(polygon);

                    } //// LOOP FOR FEATURE DATA

                } //// IF FEATURE EXIST THEN

            }

        });

    }

    //// FETCH UNION COUNCIL FEATURE DATA
    me.FetchUnionCouncilFeatureData = function () {
        let params = {
            url: fetch_union_council_feature_data,
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': posttoken}
        };
        callAJAX(params, function (data) {
            if (data.message === "Success") {
                let features = data.feature_lists[0].geojson.features;
                if (features === null) {
                } else {

                    for (let f = 0; f < features.length; f++) {

                        let coordinates = features[f].geometry.coordinates[0][0];
                        const coordinates_2d = []; // Create inner array for each row
                        for (let i = 0; i < coordinates.length; i++) {
                            let lat = coordinates[i][1];
                            let lng = coordinates[i][0];
                            coordinates[i][0] = lat;
                            coordinates[i][1] = lng;
                        }

                        const polygon = L.polygon(coordinates, {
                            color: '#FFFAFA', fillColor: UtilityModelJS.GetRandomColor(),
                            opacity: 0.35, // set desired opacity
                            fillOpacity: 0.35, // set fill opacity
                            width: 1
                        });
                        DigitalArzModelJS.UnionCouncilFeatureGroup.addLayer(polygon);

                    } //// LOOP FOR FEATURE DATA

                } //// IF FEATURE EXIST THEN

            }

        });

    }

}