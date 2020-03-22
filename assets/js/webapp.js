import 'core-js/fn/string/includes';
import 'core-js/es7/array';
import 'core-js/fn/object/assign';

import React from "react";
import ReactDOM from "react-dom";

import Common from './Common';
import SearchTableStore from "./SearchTable/SearchTableStore";

import StoreMap from "./StoreMap";
import StoreGeocode from "./Helper/StoreGeocode";


$(document).ready(function () {
    window.common = new Common();
    if (document.getElementById('store-form')) {
        window.storeGeocode = new StoreGeocode();
    }

    if (document.getElementById('store-map')) {
        ReactDOM.render(
            <StoreMap ref={(storeMap) => {window.storeMap = storeMap}} />,
            document.getElementById("store-map")
        );
    }

    if (document.getElementById('store-search-results')) {
        ReactDOM.render(
            <SearchTableStore ref={(searchTableStore) => {window.searchTableStore = searchTableStore}} />,
            document.getElementById("store-search-results")
        );
    }
});
