import 'core-js/fn/string/includes';
import 'core-js/es7/array';
import 'core-js/fn/object/assign';

import React from "react";
import ReactDOM from "react-dom";

import Common from "./Common";
import OsmMap from "./OsmMap";

document.write('<link rel="stylesheet" type="text/css" href="https://lokalwirkt.de/static/css/client.min.css" />');

$(document).ready(function () {
    window.common = new Common();
    if (document.getElementById('lokalwirkt-map')) {
        ReactDOM.render(
            <OsmMap ref={(osmMap) => {
                window.osmMap = osmMap
            }}/>,
            document.getElementById("lokalwirkt-map")
        );
    }
});