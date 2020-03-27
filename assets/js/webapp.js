import 'core-js/fn/string/includes';
import 'core-js/es7/array';
import 'core-js/fn/object/assign';

import React from "react";
import ReactDOM from "react-dom";

import Common from './Common';
import SearchTableStore from "./SearchTable/SearchTableStore";
import SearchTableRegion from "./SearchTable/SearchTableRegion";

import StoreMap from "./StoreMap";
import StoreGeocode from "./Helper/StoreGeocode";
import OpeningTimesForm from "./OpeningTimesForm";
import SearchTableUser from "./SearchTable/SearchTableUser";


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

    if (document.getElementById('opening-times-form')) {
        ReactDOM.render(
            <OpeningTimesForm ref={(openingTimesForm) => {window.openingTimesForm = openingTimesForm}} />,
            document.getElementById("opening-times-form")
        );
    }

    if (document.getElementById('store-map')) {
        ReactDOM.render(
            <StoreMap ref={(storeMap) => {window.storeMap = storeMap}} />,
            document.getElementById("store-map")
        );
    }

    if (document.getElementById('user-search-results')) {
        ReactDOM.render(
            <SearchTableUser ref={(searchTableUser) => {window.searchTableUser = searchTableUser}} />,
            document.getElementById("user-search-results")
        );
    }
    if (document.getElementById('store-search-results')) {
        ReactDOM.render(
            <SearchTableStore ref={(searchTableStore) => {window.searchTableStore = searchTableStore}} />,
            document.getElementById("store-search-results")
        );
    }
    if (document.getElementById('region-search-results')) {
        ReactDOM.render(
            <SearchTableRegion ref={(searchTableRegion) => {window.searchTableRegion = searchTableRegion}} />,
            document.getElementById("region-search-results")
        );
    }
});
