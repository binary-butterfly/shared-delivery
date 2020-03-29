import 'core-js/fn/string/includes';
import 'core-js/es7/array';
import 'core-js/fn/object/assign';

import React from "react";
import ReactDOM from "react-dom";

import Common from './Common';
import SearchTableStore from "./SearchTable/SearchTableStore";
import SearchTableRegion from "./SearchTable/SearchTableRegion";

import StoreForm from "./Helper/StoreForm";
import UserForm from './Helper/UserForm';

import StoreMap from "./StoreMap";
import OpeningTimesForm from "./OpeningTimesForm";
import SearchTableUser from "./SearchTable/SearchTableUser";
import SearchTableStoreSuggestion from "./SearchTable/SearchTableStoreSuggestion";
import SearchTableCategory from './SearchTable/SearchTableCategory';
import StoreSearch from "./SearchTable/StoreSearch";

$(document).ready(function () {
    window.common = new Common();
    if (document.getElementById('user-form')) {
        window.userForm = new UserForm();
    }
    if (document.getElementById('store-new-form') || document.getElementById('store-form')) {
        window.storeForm = new StoreForm();
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

    if (document.getElementById('store-frontend-search-results')) {
        ReactDOM.render(
            <StoreSearch ref={(storeSearch) => {window.storeSearch = storeSearch}} />,
            document.getElementById("store-frontend-search-results")
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
    if (document.getElementById('region-search-results')) {
        ReactDOM.render(
            <SearchTableRegion ref={(searchTableRegion) => {window.searchTableRegion = searchTableRegion}} />,
            document.getElementById("region-search-results")
        );
    }
    if (document.getElementById('category-search-results')) {
        ReactDOM.render(
            <SearchTableCategory ref={(searchTableCategory) => {window.searchTableCategory = searchTableCategory}} />,
            document.getElementById("category-search-results")
        );
    }
    if (document.getElementById('store-search-results')) {
        ReactDOM.render(
            <SearchTableStore ref={(searchTableStore) => {window.searchTableStore = searchTableStore}} />,
            document.getElementById("store-search-results")
        );
    }
    if (document.getElementById('store-suggestion-search-results')) {
        ReactDOM.render(
            <SearchTableStoreSuggestion ref={(searchTableStoreSuggestion) => {window.searchTableStoreSuggestion = searchTableStoreSuggestion}} />,
            document.getElementById("store-suggestion-search-results")
        );
    }
});
