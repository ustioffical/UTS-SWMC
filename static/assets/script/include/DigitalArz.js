/**
 *
 * Created by FarhanTa on 01/01/2025.
 */


AppDigitalArzModel = function (mapTarget) {

    let me = this;
    me.mapTarget = mapTarget;
    me.view = null;
    me.map = null;
    me.extent = "";
    me.minZoom = 13;
    me.maxZoom = 22;
    me.OSMStreetMap = "";
    me.googleStreets = "";
    me.googleHybrid = "";
    me.setLevel = 5;
    me.icons = [];

    //// DRAW FEATURE
    me.IndicatorFeature = undefined;
    me.DrumFeatureGroup = undefined;
    me.ContainerFeatureGroup = undefined;
    me.CollectionSiteFeatureGroup = undefined;
    me.DumpingSiteFeatureGroup = undefined;
    me.DumpingCoverageFeatureGroup = undefined;
    me.WeighingSiteFeatureGroup = undefined;
    me.WeighingCoverageFeatureGroup = undefined;
    me.ParkingSiteFeatureGroup = undefined;
    me.WorkshopFeatureGroup = undefined;
    me.FillingStationFeatureGroup = undefined;

    me.LanduseBoundaryFeatureGroup = undefined;
    me.AdminBoundaryFeatureGroup = undefined;
    me.UnionCouncilFeatureGroup = undefined;

    me.SelectedFeatureLayer = null;
    me.EditFeatureLayer = null;
    me.DrawFeatureLayer = null;
    me.MarkerDrawer = "";
    me.PolylineDrawer = "";
    me.polygonDrawer = "";
    me.rectangleDrawer = "";
    me.markerInputField = "";
    me.lineInputField = "";
    me.polygonInputField = "";
    me.IndicatorFiberLayer = undefined;
    me.GroupRouteNetworkLayer = undefined;
    me.VehicleLayer = undefined;
    me.VehicleRadiusLayer = undefined;
    me.OnEachNetworkLayer = undefined;
    me.OnEachPopupLayer = undefined;

    me.LeafIcon_highlight = "";
    me.LeafIcon_indicator = "";
    me.LeafIcon_AssetType = "";

    me.OnloadFiberLayerOBJ = [];
    me.RouteLayerOJB = []; // Store polylines for later removal
    me.RouteLayer = null;

    // Set up the OSM layer
    me.LoadMap = function (Editable, CenterZoom) {

        me.map = new L.Map(me.mapTarget, {
            center: new L.LatLng(31.500574, 74.328710),
            // center: new L.LatLng(CenterZoom),
            zoom: me.minZoom,
            maxZoom: me.maxZoom,
            editable: Editable,
            measureControl: true,
            'zoomControl': false
        });
        document.getElementById(me.mapTarget).style.cursor = 'pointer';
        // me.OSMStreetMapView();
        // me.googleStreetsView();
        me.googleHybridView();

        //// create a feature group for Leaflet Draw to hook into for delete functionality
        me.IndicatorFeature = L.featureGroup().addTo(me.map);
        me.DrumFeatureGroup = L.featureGroup().addTo(me.map);
        me.ContainerFeatureGroup = L.featureGroup().addTo(me.map);
        me.CollectionSiteFeatureGroup = L.featureGroup().addTo(me.map);
        me.DumpingSiteFeatureGroup = L.featureGroup().addTo(me.map);
        me.DumpingCoverageFeatureGroup = L.featureGroup().addTo(me.map);
        me.WeighingSiteFeatureGroup = L.featureGroup().addTo(me.map);
        me.WeighingCoverageFeatureGroup = L.featureGroup().addTo(me.map);
        me.ParkingSiteFeatureGroup = L.featureGroup().addTo(me.map);
        me.WorkshopFeatureGroup = L.featureGroup().addTo(me.map);
        me.FillingStationFeatureGroup = L.featureGroup().addTo(me.map);

        me.LanduseBoundaryFeatureGroup = L.featureGroup().addTo(me.map);
        me.AdminBoundaryFeatureGroup = L.featureGroup().addTo(me.map);
        me.UnionCouncilFeatureGroup = L.featureGroup().addTo(me.map);

        me.VehicleLayer = L.featureGroup().addTo(me.map);
        me.VehicleRadiusLayer = L.featureGroup().addTo(me.map);

        me.GroupRouteNetworkLayer = L.featureGroup().addTo(me.map);

        me.DrawFeatureLayer = new L.FeatureGroup();
        me.map.addLayer(me.DrawFeatureLayer);

        me.SelectedFeatureLayer = L.featureGroup().addTo(me.map);
        me.EditFeatureLayer = L.featureGroup().addTo(me.map);

        me.map.on('zoomend', function () {
            me.setLevel = me.map.getZoom();
        });

        me.map.on('click', function (e) {
            // alert(e.latlng);
            // if (me.selectedfeature) {
            //     me.map.removeLayer(me.selectedfeature)
            // }

        });

        me.LeafIcon_highlight = L.Icon.extend({
            options: {iconSize: [35, 35]}
        });

        me.LeafIcon_indicator = L.Icon.extend({
            options: {iconSize: [25, 25]}
        });

        me.LeafIcon_AssetType = L.Icon.extend({
            options: {iconSize: [25, 25]}
        });

        me.icons = {
            google_marker: new me.LeafIcon_highlight({iconUrl: '/static/assets/images/toolbar/google-marker.png'}),
            marker_conves: new me.LeafIcon_highlight({iconUrl: '/static/assets/images/toolbar/marker-conves.png'}),
            vehicle: new me.LeafIcon_AssetType({iconUrl: '/static/assets/images/legend/vehicle/vehicle.png'}),
            //     drawhighlight: new LeafIcon_highlight({iconUrl: '/static/das/assets/images/asset_logo/place-marker-sel.png'}),
            //
            //     excellent: new LeafIcon_indicator({iconUrl: '/static/das/assets/images/toolbar-icon/excellent.png'}),
            //     good: new LeafIcon_indicator({iconUrl: '/static/das/assets/images/toolbar-icon/good.png'}),
            //     fair: new LeafIcon_indicator({iconUrl: '/static/das/assets/images/toolbar-icon/fair.png'}),
            //     poor: new LeafIcon_indicator({iconUrl: '/static/das/assets/images/toolbar-icon/poor.png'}),
            //     failing: new LeafIcon_indicator({iconUrl: '/static/das/assets/images/toolbar-icon/failing.png'}),
            //     undefined: new LeafIcon_indicator({iconUrl: '/static/das/assets/images/toolbar-icon/marker-img.png'}),
            collection_site: new me.LeafIcon_indicator({iconUrl: '/static/assets/images/legend/asset_logo/collection_site.png'}),
            dumping_site_active: new me.LeafIcon_indicator({iconUrl: '/static/assets/images/legend/asset_logo/dumping_site.png'}),
            weighing_site: new me.LeafIcon_indicator({iconUrl: '/static/assets/images/legend/asset_logo/weighing-machine.png'}),
            parking_site_active: new me.LeafIcon_indicator({iconUrl: '/static/assets/images/legend/asset_logo/parking_site.png'}),
            workshop_active: new me.LeafIcon_indicator({iconUrl: '/static/assets/images/legend/asset_logo/workshop.png'}),
            fs_active: new me.LeafIcon_indicator({iconUrl: '/static/assets/images/legend/asset_logo/filling_station.png'}),

            container_active: new me.LeafIcon_indicator({iconUrl: '/static/assets/images/legend/container/green.png'}),
            container_block: new me.LeafIcon_indicator({iconUrl: '/static/assets/images/legend/container/red.png'}),

            container_visited: new me.LeafIcon_indicator({iconUrl: '/static/assets/images/legend/container/visited.png'}),
            container_to_be_visited: new me.LeafIcon_indicator({iconUrl: '/static/assets/images/legend/container/to_be_visited.png'}),
            container_visited_but_not_dumped: new me.LeafIcon_indicator({iconUrl: '/static/assets/images/legend/container/visited_but_not_dumped.png'}),

            drum_visited: new me.LeafIcon_indicator({iconUrl: '/static/assets/images/legend/drum/visited.png'}),
            drum_to_be_visited: new me.LeafIcon_indicator({iconUrl: '/static/assets/images/legend/drum/to_be_visited.png'}),
            drum_visited_but_not_dumped: new me.LeafIcon_indicator({iconUrl: '/static/assets/images/legend/drum/visited_but_not_dumped.png'}),

            //
            //     water_filtration_plant: new LeafIcon_AssetType({iconUrl: '/static/das/assets/images/map_icon/filterationplant.png'}),
            //     ohr: new LeafIcon_AssetType({iconUrl: '/static/das/assets/images/map_icon/ohr.png'}),
            //     tube_well: new LeafIcon_AssetType({iconUrl: '/static/das/assets/images/map_icon/tubewell.png'}),
            //     disposal_station: new LeafIcon_AssetType({iconUrl: '/static/das/assets/images/map_icon/disposalstation.png'}),
            //     solid_waste: new LeafIcon_AssetType({iconUrl: '/static/das/assets/images/map_icon/solidwaste.png'}),
            //     street_light: new LeafIcon_AssetType({iconUrl: '/static/das/assets/images/map_icon/streetlight.png'}),
            //     slaughter_house: new LeafIcon_AssetType({iconUrl: '/static/das/assets/images/map_icon/slaughterhouse.png'}),
            //     park: new LeafIcon_AssetType({iconUrl: '/static/das/assets/images/map_icon/park.png'}),
            //     graveyard: new LeafIcon_AssetType({iconUrl: '/static/das/assets/images/map_icon/graveyard.png'}),
            //     bus_stand: new LeafIcon_AssetType({iconUrl: '/static/das/assets/images/map_icon/busstand.png'}),
            //     mc_office: new LeafIcon_AssetType({iconUrl: '/static/das/assets/images/map_icon/building.png'}),
            //     shop: new LeafIcon_AssetType({iconUrl: '/static/das/assets/images/map_icon/shop.png'}),
        };

        ////FEATURE ONCLICK FUNCTION
        me.WMSFeatureOnclick();

        //// THIS CODE IS USED FOR NEW FEATURE EDITING
        me.DrawShapeControl();

    }

    me.googleStreetsView = function () {
        me.googleStreets = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        });

        // me.googleStreets = L.tileLayer('https://www.google.com/maps/vt?lyrs=m&x={x}&y={y}&z={z}', {
        //     attribution: '&copy; Google'
        // });
        me.map.addLayer(me.googleStreets);
        me.googleStreets.bringToBack();
    }

    me.googleHybridView = function () {
        me.googleHybrid = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {
            maxZoom: 22,
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
        });

        // me.googleHybrid = L.tileLayer('https://www.google.com/maps/vt?lyrs=y&x={x}&y={y}&z={z}', {
        //     attribution: '&copy; Google'
        // });
        me.map.addLayer(me.googleHybrid);
        me.googleHybrid.bringToBack();
    }

    me.OSMStreetMapView = function () {
        me.OSMStreetMap = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 22,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright"></a>'
        });
        me.map.addLayer(me.OSMStreetMap);
        // me.OSMStreetMap.bringToBack();
    }

    ////FEATURE ONCLICK FUNCTION
    me.WMSFeatureOnclick = function () {
        ////Feature onclick function
        L.TileLayer.BetterWMS = L.TileLayer.WMS.extend({

            onAdd: function (map) {
                // Triggered when the layer is added to a map.
                //   Register a click listener, then do all the upstream WMS things
                L.TileLayer.WMS.prototype.onAdd.call(this, map);
                me.map.on('click', this.getFeatureInfo, this);
            },

            onRemove: function (map) {
                // Triggered when the layer is removed from a map.
                //   Unregister a click listener, then do all the upstream WMS things
                L.TileLayer.WMS.prototype.onRemove.call(this, map);
                me.map.off('click', this.getFeatureInfo, this);
            },

            getFeatureInfo: function (evt) {
                // Make an AJAX request to the server and hope for the best
                var url = this.getFeatureInfoUrl(evt.latlng),
                    showResults = L.Util.bind(this.showGetFeatureInfo, this);
                let formdata = new FormData();
                formdata.append('url', url);
                var paramas = {
                    url: get_proxy_url,
                    data: formdata,
                    type: "POST",
                    dataType: 'json',
                    headers: {'X-CSRFToken': posttoken}
                };
                callAJAX(paramas, function (data) {
                    // console.log(data);
                    var err = typeof data.data === 'string' ? null : data.data;
                    showResults(err, evt.latlng, data.data);
                    // if (data.region.length > 0) {
                    //     $("#id_" + markerName + "_region").val(data.region[0].region);
                    // }
                })
            },

            getFeatureInfoUrl: function (latlng) {
                // Construct a GetFeatureInfo request URL given a point
                var point = this._map.latLngToContainerPoint(latlng, this._map.getZoom()),
                    size = this._map.getSize(),

                    params = {
                        request: 'GetFeatureInfo',
                        service: 'WMS',
                        srs: 'EPSG:4326',
                        styles: this.wmsParams.styles,
                        transparent: this.wmsParams.transparent,
                        version: this.wmsParams.version,
                        format: this.wmsParams.format,
                        bbox: this._map.getBounds().toBBoxString(),
                        height: size.y,
                        width: size.x,
                        layers: this.wmsParams.layers,
                        query_layers: this.wmsParams.layers,
                        info_format: 'application/json'
                        //info_format: 'text/html'
                    };

                // params[params.version === '1.3.0' ? 'i' : 'x'] = point.x;
                // params[params.version === '1.3.0' ? 'j' : 'y'] = point.y;

                params[params.version === '1.3.0' ? 'i' : 'x'] = Math.round(point.x);
                params[params.version === '1.3.0' ? 'j' : 'y'] = Math.round(point.y);

                //return this._url + L.Util.getParamString(params, this._url, true);

                var url = this._url + L.Util.getParamString(params, this._url, true);

                /**
                 * CORS workaround (using a basic php proxy)
                 *
                 * Added 2 new options:
                 *  - proxy
                 *  - proxyParamName
                 *
                 */

                // check if "proxy" option is defined (PS: path and file name)
                if (typeof this.wmsParams.proxy !== "undefined") {


                    // check if proxyParamName is defined (instead, use default value)
                    if (typeof this.wmsParams.proxyParamName !== "undefined")
                        this.wmsParams.proxyParamName = 'url';

                    // build proxy (es: "proxy.php?url=" )
                    _proxy = this.wmsParams.proxy + '?' + this.wmsParams.proxyParamName + '=';

                    //url = _proxy + encodeURIComponent(url);
                    //url = url;
                }

                return url;
            },

            showGetFeatureInfo: function (err, latlng, content) {
                if (err) {
                    console.log(err);
                    return;
                } // do nothing if there's an error
                // // Otherwise show the content in a popup, or something.
                // L.popup({maxWidth: 800})
                //     .setLatLng(latlng)
                //     .setContent(content)
                //     .openOn(this._map);

                if (JSON.parse(content).features[0] !== undefined) {

                    // if (me.MeasuringStatus) {
                    //     return true;
                    // }
                    // if (me.DrawingStatus) {
                    //     return true;
                    // }

                    let layerName_comb = JSON.parse(content).features[0].id;
                    let layerName_split = layerName_comb.split(".");
                    let layerName = layerName_split[0];
                    // console.log(layerName);

                    let tooltipContent = "";
                    let attributes = JSON.parse(content).features[0].properties;

                    let FeatureStatus = "NO";

                    //// SEWERAGE SYSTEM (START)

                    //// DISPOSAL STATION (START)
                    if (layerName === "tbl_disposal_station") {

                        tooltipContent = '<div style="width: 350px;"' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;"><div class="col-lg-12 col-md-12 col-sm-12 col-xs-12" style="padding: 1px; text-align: center;">' +
                            '<strong style="font-size: 16px;">Disposal Station</strong></div></div>' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                            '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Name:</strong></div>' +
                            '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                            '<div>' + attributes.name + '</div></div></div>' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                            '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Address:</strong></div>' +
                            '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                            '<div>' + attributes.address + '</div></div></div>' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                            '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Condition Assessment:</strong></div>' +
                            '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                            '<div>' + attributes.asset_condition + '</div></div></div>' +
                            '<div class="row rowMargin" style="border-bottom: 2px solid #555e72;">' +
                            '<div class="col-lg-5 col-md-6 col-sm-6 col-xs-6 text-left" style="padding: 3px;"><strong>Work Status:</strong></div>' +
                            '<div class="col-lg-7 col-md-6 col-sm-6 col-xs-6 text-left" style="font-size: 12px; padding: 3px;">' +
                            '<div>' + attributes.working_status + '</div></div></div>' +
                            '</div>';

                        FeatureStatus = "YES";
                    }
                    //// DISPOSAL STATION (END)


                    if (FeatureStatus === "YES") {

                        // if (GlobalModelJS.SchemeCode !== "0") {
                        //
                        //     let condition_column = " amis_code= '" + attributes.amis_code + "'";
                        //
                        //     let formdata = new FormData();
                        //     formdata.append('asset_shape_type', GlobalModelJS.SelectedAssetShape);
                        //     formdata.append('table_name', layerName);
                        //     formdata.append('condition_column', condition_column);
                        //     var paramas = {
                        //         url: single_asset_feature_info,
                        //         data: formdata,
                        //         type: "POST",
                        //         dataType: 'json',
                        //         headers: {'X-CSRFToken': posttoken}
                        //     };
                        //     callAJAX(paramas, function (data) {
                        //         var result_data = data.feature_info;
                        //         $("#feature_coordinate").val(result_data[0].asset_geom);
                        //
                        //         if (GlobalModelJS.SelectedAssetShape === "Line") {
                        //             $("#lattitude").val(JSON.parse(content).features[0].geometry.coordinates[0][0][1]);
                        //             $("#longitude").val(JSON.parse(content).features[0].geometry.coordinates[0][0][0]);
                        //         } else {
                        //             $("#lattitude").val(result_data[0].y);
                        //             $("#longitude").val(result_data[0].x);
                        //         }
                        //
                        //         //// FUNCTION SHOWS SELECTED VALUE OF ASSET TYPE ON MAP ON START PROJECT
                        //         DSSModelJS.AppendProjectAssetDetail_DrawFeature(attributes, "Existing", "");
                        //     });
                        //
                        //     // Otherwise show the content in a popup, or something.
                        //     L.popup({maxWidth: 500})
                        //         .setLatLng(latlng)
                        //         .setContent(tooltipContent)
                        //         .openOn(this._map);
                        // }

                    }

                } else {
                }
            }
        });

        L.tileLayer.betterWms = function (url, options) {
            return new L.TileLayer.BetterWMS(url, options);
        };
    }

    //// THIS CODE IS USED FOR NEW FEATURE EDITING
    me.DrawShapeControl = function () {

        me.AddDrawFeatureLayer();

        /*******************ADD MARKER FEATURE ON MAP***************/
        $('#add-marker-feature').click(function () {
            me.DrawingStatus = true;
            me.MarkerDrawer.enable();
            // polylineDrawer.disable();
            // polygonDrawer.disable();
            // // $("#ployline_vertex_deleted").css("display", "none");

            // me.DrawFeatureLayer.clearLayers();
            // $('#img-add-marker').attr('src', '/static/das/assets/images/toolbar-icon/marker-green-sel.png');
        });
        /*******************ADD POLYLINE FEATURE ON MAP***************/
        $('#add-polyline-feature').click(function () {
            me.DrawingStatus = true;
            // markerDrawer.disable();
            // polygonDrawer.disable();
            me.PolylineDrawer.enable();
            // $("#ployline_vertex_deleted").css("display", "block");
            // me.DrawFeatureLayer.clearLayers();
            $('#img-add-fiber').attr('src', '/static/das/assets/images/toolbar-icon/polyline-green-sel.png');
        });
        /*******************ADD POLYLINE FEATURE ON MAP***************/
        // $('#delete_current_vertex_polyline').click(function () {
        //     polylineDrawer.deleteLastVertex();
        // });
        /*******************ADD POLYGON FEATURE ON MAP***************/
        $('#add-polygon-feature').click(function () {
            // markerDrawer.disable();
            // polylineDrawer.disable();
            me.polygonDrawer.enable();
            // $("#ployline_vertex_deleted").css("display", "none");
            // addFeatureLayers.clearLayers();

            if (PMDFCModelJS.ProcessStatus === "LOS-Coverage") {
                me.DrawFeatureLayer.clearLayers();
            }

        });

        //// THIS CODE IS USED FOR NEW FEATURE EDITING
        me.map.on(L.Draw.Event.CREATED, function (e) {
            var type = e.layerType,
                layer = e.layer;

            if (type === 'marker') {
                me.DrawFeatureLayer.clearLayers();
                var coordinate = layer._latlng;
                var lat = coordinate.lat;
                var lng = coordinate.lng;
                $("#lattitude").val(lat);
                $("#longitude").val(lng);
                $("#feature_coordinate").val("POINT(" + lng + " " + lat + ")");
                $("#show_coordinate").html(lng.toFixed(6) + ", " + lat.toFixed(6));

                UtilityModelJS.SetGooglePlaceJSON(lat, lng);
            }
            if (type === 'polyline') {
                // $("#ployline_vertex_deleted").css("display", "none");
                // me.DrawFeatureLayer.clearLayers();
                var PROJECT_WKT = '';
                var latlngs = layer._latlngs;

                PROJECT_WKT = 'MULTILINESTRING((';
                var wkt_polyline = '';
                var polyline_point = 0;
                var lng = '';
                var lat = '';

                for (var i = 0; i < latlngs.length; i++) {
                    $("#lattitude").val(latlngs[0].lat);
                    $("#longitude").val(latlngs[0].lng);
                    if (polyline_point != 0) {
                        wkt_polyline = wkt_polyline + ",";
                    }
                    var test_point = latlngs[i].lng + " " + latlngs[i].lat;
                    var raw_polygon_point = (latlngs[i].toString().replace("LatLng(", "")).replace(")", "");
                    polyline_point = raw_polygon_point.replace(",", " ");
                    polyline_point = test_point;
                    wkt_polyline = wkt_polyline + polyline_point;
                }

                var lengthKM = 0;
                var lengthMeter = 0;
                for (var l = 0; l < latlngs.length - 1; l++) {
                    lengthMeter += latlngs[l].distanceTo(latlngs[l + 1]);
                }
                me.FibreLengthKM = lengthMeter / 1000;
                //// CHECK INPUT FIELD ID EXIST OR NOT IN PAGE ////
                var element = document.getElementById('id_pipe_length');
                if (typeof (element) != 'undefined' && element != null) {
                    // Exists.
                    alert("Exists");
                }
                // console.log(lengthKM);

                $('#img-add-fiber').attr('src', '/static/das/assets/images/toolbar-icon/polyline.png');
                PROJECT_WKT = PROJECT_WKT + wkt_polyline + "))";
                // alert(PROJECT_WKT);
                $("#feature_coordinate").val(PROJECT_WKT);

            }
            if (type === 'rectangle' || type === 'polygon') {

                let PROJECT_WKT = '';
                let latlngs = layer._latlngs[0];
                PROJECT_WKT = 'MULTIPOLYGON(((';
                let wkt_polygon = '';
                let polygon_point = 0;
                for (let i = 0; i < latlngs.length; i++) {
                    if (polygon_point !== 0) {
                        wkt_polygon = wkt_polygon + ",";
                    }
                    let test_point = latlngs[i].lng + " " + latlngs[i].lat;
                    let raw_polygon_point = (latlngs[i].toString().replace("LatLng(", "")).replace(")", "");
                    polygon_point = raw_polygon_point.replace(",", " ");
                    polygon_point = test_point;
                    wkt_polygon = wkt_polygon + polygon_point;
                }
                let close_ring = latlngs[0].lng + " " + latlngs[0].lat;
                wkt_polygon = wkt_polygon + "," + close_ring;
                PROJECT_WKT = PROJECT_WKT + wkt_polygon + ")))";
                //alert(PROJECT_WKT);
                $("#feature_coordinate").val(PROJECT_WKT);
            }

            me.DrawingStatus = false;
            me.DrawFeatureLayer.addLayer(layer);

            // if (GlobalModelJS.SchemeCode === "") {
            //     return true;
            // }
            // if (GlobalModelJS.SchemeCode !== "0") {
            //     //// FUNCTION SHOWS SELECTED VALUE OF ASSET TYPE ON MAP ON START PROJECT
            //     DSSModelJS.AppendProjectAssetDetail_DrawFeature("", "New", "");
            // }

        });

        me.map.on('draw:edited', function (e) {
            var layers = e.layers;
            layers.eachLayer(function (layer) {
                //do whatever you want; most likely save back to db
            });
        });

    }

    me.AddDrawFeatureLayer = function () {

        //// Define you draw handler somewhere where you click handler can access it. N.B. pass any draw options into the handler
        me.MarkerDrawer = new L.Draw.Marker(me.map, {icon: me.icons['marker_conves']});
        me.PolylineDrawer = new L.Draw.Polyline(me.map, {
            allowIntersection: false, repeatMode: false, drawError: {color: '#faa21c', timeout: 2500},
            icon: new L.DivIcon({iconSize: new L.Point(8, 8), className: 'leaflet-div-icon leaflet-editing-icon'}),
            touchIcon: new L.DivIcon({
                iconSize: new L.Point(20, 20), className: 'leaflet-div-icon leaflet-editing-icon leaflet-touch-icon'
            }),
            guidelineDistance: 20, maxGuideLineLength: 4000, metric: true, // Whether to use the metric measurement system or imperial
            showLength: true, // Whether to display distance in the tooltip
            feet: true, // When not metric, to use feet instead of yards for display.
            nautic: false, // When not metric, not feet use nautic mile for display
            zIndexOffset: 2000, // This should be > than the highest z-index any map layers
            factor: 1, // To change distance calculation
            shapeOptions: {stroke: true, color: 'red', weight: 4, opacity: 0.5, fill: false, clickable: true}
        });
        me.polygonDrawer = new L.Draw.Polygon(me.map, {
            allowIntersection: false, repeatMode: false, drawError: {color: '#faa21c', timeout: 2500},
            icon: L.icon({iconUrl: '/static/assets/images/toolbar/place-marker-sel.png', iconSize: [15, 15]}),
            showLength: true, // Whether to display distance in the tooltip
            feet: true, // When not metric, to use feet instead of yards for display.
            factor: 1, // To change distance calculation
            shapeOptions: {stroke: true, color: '#faa21c', weight: 3, opacity: 0.5, fill: true, clickable: true}
        });
        // me.rectangleDrawer = new L.Draw.Rectangle(me.map, {
        //     icon: L.icon({iconUrl: '/static/images/toobar/place-marker-sel.png', iconSize: [15, 15]}),
        //     shapeOptions: {stroke: true, color: '#faa21c', weight: 3, opacity: 0.5, fill: true, clickable: true}
        // });
        //

    }

    ////  THIS FUNCTION IS USED TO ZOOM THE LAYER  /////
    me.ZoomToFeature = function (type, extent) {
        // alert(extent);
        let part_extent = extent.split(',');
        ////  THIS FUNCTION IS USED TO ZOOM THE LAYER  ///////////////////
        me.map.fitBounds([
            [part_extent[1], part_extent[0]],
            [part_extent[3], part_extent[2]]
        ]);

        if (type === "Marker" || type === "Point") {
            me.map.setZoom(16);
        }
    }

    //// FIBER ON HOVER AND CLICK FEATURE (START)
    me.OnEachFeature = function (feature, layer) {
        //console.log('here')
        // alert("fff");
        layer.on({
            mouseover: me.OnEachHighlightFeature,
        });
    }

    me.OnEachFeature1 = function (feature, layer) {
        //console.log('here')
        layer.on({
            mouseout: me.OnEachResetHighlightFeature,
            click: me.OnEachFiberClickFeature,
        });
    }

    me.OnEachFiberClickFeature = function (e) {
        // myLines.setStyle(myStyle);

        let layer = e.target;

        if (me.OnEachNetworkLayer) {
            me.map.removeLayer(me.OnEachNetworkLayer);
        }
        let selectedfeaturejson = {
            "type": "FeatureCollection",
            "features": [e.target.feature]
        }

        me.OnEachNetworkLayer = L.geoJSON(selectedfeaturejson, {
            style: {
                "color": "#FFD700",
                weight: 5,
                opacity: 1,
                dashArray: 5
            }
        }).addTo(me.map);
        check = true;
        L.DomEvent.stopPropagation(e);

        // alert(UtilityModelJS.PageTitle);
        if (UtilityModelJS.PageTitle === "Create Network") {
            UtilityModelJS.SetGooglePlaceJSON(e.latlng.lat, e.latlng.lng);
            $("#hid_type").val("OSM");
            $("#hid_unique_id").val(e.target.feature.properties.id);
            $("#feature_coordinate").val(selectedfeaturejson);
            $("#lattitude").val(e.latlng.lat);
            $("#longitude").val(e.latlng.lng);

            debugger;
            //// SELECTED FEATURE DRAW ON MAP
            let PROJECT_WKT = 'MULTILINESTRING((';
            let wkt_polyline = '';
            let polyline_point = 0;

            let coordinate_array = selectedfeaturejson.features[0].geometry.coordinates;
            let Fiber_Array = [];
            for (let p = 0; p < coordinate_array.length; p++) {
                let latlng = coordinate_array[p];
                let lng = latlng[0];
                let lat = latlng[1];

                if (polyline_point !== 0) {
                    wkt_polyline = wkt_polyline + ",";
                }
                polyline_point = lng + " " + lat;
                wkt_polyline = wkt_polyline + polyline_point;

                Fiber_Array.push([lat, lng]);
            } //// FOR LOOP
            PROJECT_WKT = PROJECT_WKT + wkt_polyline + "))";
            // alert(PROJECT_WKT);
            $("#feature_coordinate").val(PROJECT_WKT);

            me.SelectedFeatureLayer = L.polyline(Fiber_Array, {color: "red", weight: 5}).addTo(me.map);

            setTimeout(function () {
                RouteModelJS.AddonCreateNetworkItem_Box();
            }, 800);
        }
    }

    me.OnEachHighlightFeature = function (e) {

        if (me.OnEachNetworkLayer) {
            me.map.removeLayer(me.OnEachNetworkLayer);
        }

        let selectedfeaturejson = {
            "type": "FeatureCollection",
            "features": [e.target.feature]
        }

        me.OnEachNetworkLayer = L.geoJSON(selectedfeaturejson, {
            style: {
                "color": "#FFD700",
                "weight": 18,
                "opacity": 0.5
            }, onEachFeature: me.OnEachFeature1
        }).addTo(me.map);

        let popup_title = e.target.feature.properties.name;
        if (popup_title === null) {
            popup_title = "Missing Name"
        }
        me.OnEachPopupLayer = L.popup()
            .setLatLng(e.latlng)
            .setContent(popup_title)
            .openOn(me.map);
    }

    me.OnEachResetHighlightFeature = function (e) {
        me.map.removeLayer(me.OnEachNetworkLayer);
        if (me.OnEachPopupLayer && me.map) {
            me.map.closePopup(me.OnEachPopupLayer);
            me.OnEachPopupLayer = null;
        }
    }
    //// FIBER ON HOVER AND CLICK FEATURE (END)

    me.OnclickAssetLayer_TOC = function (parameter) {

        let asset_container_layer = $("#asset_container_layer").is(':checked');
        let asset_drum_layer = $("#asset_drum_layer").is(':checked');

        let asset_collection_site_layer = $("#asset_collection_site_layer").is(':checked');

        let asset_dumping_site_layer = $("#asset_dumping_site_layer").is(':checked');
        let asset_weighing_site_layer = $("#asset_weighing_site_layer").is(':checked');

        let asset_parking_site_layer = $("#asset_parking_site_layer").is(':checked');
        let asset_workshop_layer = $("#asset_workshop_layer").is(':checked');
        let asset_filling_station_layer = $("#asset_filling_station_layer").is(':checked');

        let asset_landuse_boundary_layer = $("#asset_landuse_boundary_layer").is(':checked');
        let asset_admin_boundary_layer = $("#asset_admin_boundary_layer").is(':checked');
        let asset_union_council_layer = $("#asset_union_council_layer").is(':checked');


        if (parameter === "asset_container_layer" && asset_container_layer === false) {
            DigitalArzModelJS.ContainerFeatureGroup.clearLayers();
        }

        if (parameter === "asset_drum_layer" && asset_drum_layer === false) {
            DigitalArzModelJS.DrumFeatureGroup.clearLayers();
        }

        if (parameter === "asset_collection_site_layer" && asset_collection_site_layer === false) {
            DigitalArzModelJS.CollectionSiteFeatureGroup.clearLayers();
        }

        if (parameter === "asset_dumping_site_layer" && asset_dumping_site_layer === false) {
            DigitalArzModelJS.DumpingSiteFeatureGroup.clearLayers();
            DigitalArzModelJS.DumpingCoverageFeatureGroup.clearLayers();
        }

        if (parameter === "asset_weighing_site_layer" && asset_weighing_site_layer === false) {
            DigitalArzModelJS.WeighingSiteFeatureGroup.clearLayers();
            DigitalArzModelJS.WeighingCoverageFeatureGroup.clearLayers();
        }

        if (parameter === "asset_parking_site_layer" && asset_parking_site_layer === false) {
            DigitalArzModelJS.ParkingSiteFeatureGroup.clearLayers();
        }

        if (parameter === "asset_workshop_layer" && asset_workshop_layer === false) {
            DigitalArzModelJS.WorkshopFeatureGroup.clearLayers();
        }

        if (parameter === "asset_filling_station_layer" && asset_filling_station_layer === false) {
            DigitalArzModelJS.FillingStationFeatureGroup.clearLayers();
        }

        if (parameter === "asset_union_council_layer" && asset_union_council_layer === false) {
            DigitalArzModelJS.UnionCouncilFeatureGroup.clearLayers();
        }

        if (parameter === "asset_landuse_boundary_layer" && asset_landuse_boundary_layer === false) {
            DigitalArzModelJS.LanduseBoundaryFeatureGroup.clearLayers();
        }

        if (parameter === "asset_admin_boundary_layer" && asset_admin_boundary_layer === false) {
            DigitalArzModelJS.AdminBoundaryFeatureGroup.clearLayers();
        }

        me.OrderAssetLayerSetting();

    }

    me.OrderAssetLayerSetting = function () {

        let asset_container_layer = $("#asset_container_layer").is(':checked');
        let asset_drum_layer = $("#asset_drum_layer").is(':checked');
        let asset_collection_site_layer = $("#asset_collection_site_layer").is(':checked');
        let asset_dumping_site_layer = $("#asset_dumping_site_layer").is(':checked');
        let asset_weighing_site_layer = $("#asset_weighing_site_layer").is(':checked');
        let asset_parking_site_layer = $("#asset_parking_site_layer").is(':checked');
        let asset_workshop_layer = $("#asset_workshop_layer").is(':checked');
        let asset_filling_station_layer = $("#asset_filling_station_layer").is(':checked');

        let asset_landuse_boundary_layer = $("#asset_landuse_boundary_layer").is(':checked');
        let asset_admin_boundary_layer = $("#asset_admin_boundary_layer").is(':checked');
        let asset_union_council_layer = $("#asset_union_council_layer").is(':checked');

        if (asset_container_layer === true && DigitalArzModelJS.ContainerFeatureGroup.getLayers().length === 0) {
            //// FETCH CONTAINER FEATURE DATA
            TOCLayerModelJS.FetchContainerFeatureData();
        }
        if (asset_drum_layer === true && DigitalArzModelJS.DrumFeatureGroup.getLayers().length === 0) {
            //// FETCH DRUM FEATURE DATA
            TOCLayerModelJS.FetchDrumFeatureData();
        }
        if (asset_collection_site_layer === true && DigitalArzModelJS.CollectionSiteFeatureGroup.getLayers().length === 0) {
            //// FETCH FILLING STATION FEATURE DATA
            TOCLayerModelJS.FetchCollectionSiteData();
        }
        if (asset_dumping_site_layer === true && DigitalArzModelJS.DumpingSiteFeatureGroup.getLayers().length === 0) {
            //// FETCH DUMPING SITE FEATURE DATA
            TOCLayerModelJS.FetchDumpingSiteData();
            //// FETCH DUMPING COVERAGE FEATURE DATA
            TOCLayerModelJS.FetchDumpingCoverageData();
        }
        if (asset_weighing_site_layer === true && DigitalArzModelJS.WeighingSiteFeatureGroup.getLayers().length === 0) {
            //// FETCH DUMPING SITE FEATURE DATA
            TOCLayerModelJS.FetchWeighingSiteData();
            //// FETCH DUMPING COVERAGE FEATURE DATA
            TOCLayerModelJS.FetchWeighingCoverageData();
        }
        if (asset_parking_site_layer === true && DigitalArzModelJS.DumpingCoverageFeatureGroup.getLayers().length === 0) {
            //// FETCH FILLING STATION FEATURE DATA
            TOCLayerModelJS.FetchParkingSiteData();
        }
        if (asset_workshop_layer === true && DigitalArzModelJS.WorkshopFeatureGroup.getLayers().length === 0) {
            //// FETCH FILLING STATION FEATURE DATA
            TOCLayerModelJS.FetchWorkshopData();
        }
        if (asset_filling_station_layer === true && DigitalArzModelJS.FillingStationFeatureGroup.getLayers().length === 0) {
            //// FETCH FILLING STATION FEATURE DATA
            TOCLayerModelJS.FetchFillingStationData();
        }
        if (asset_landuse_boundary_layer === true && DigitalArzModelJS.LanduseBoundaryFeatureGroup.getLayers().length === 0) {
            //// FETCH LANDUSE BOUNDARY FEATURE DATA
            TOCLayerModelJS.FetchLanduseBoundaryFeatureData();
        }
        if (asset_admin_boundary_layer === true && DigitalArzModelJS.AdminBoundaryFeatureGroup.getLayers().length === 0) {
            //// FETCH ADMINISTRATIVE BOUNDARY FEATURE DATA
            TOCLayerModelJS.FetchAdministrativeBoundaryFeatureData();
        }
        if (asset_union_council_layer === true) {
            //// FETCH UNION COUNCIL FEATURE DATA
            TOCLayerModelJS.FetchUnionCouncilFeatureData();
        }

    }

}
