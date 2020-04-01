import React from "react";
import SearchTable from './SearchTable'

export default class StoreSearch extends SearchTable {
    params = {
        'sort-field': 'random',
        'sort-order': 'asc',
        page: 1
    };

    apiUrl = '/api/stores/search';
    formId = 'store-frontend-search-form';
    varPrefix = 'storeSearch';

    sortDef = [
        { key: 'random', name: 'Zufall'},
        { key: 'name.sort', name: 'Name' }
    ];
    loadParamsRegExp = [
        /\/store\/(.*)/g
    ];

    constructor(props) {
        super(props);
        this.params['random-seed'] = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
        $('#no_revisit_required').change(() => {
            this.updateData();
        });
    }


    getParams() {
        let params = Object.assign({}, this.params);
        if ($('#no_revisit_required').is(':checked')) {
            params['revisit-required'] = '0';
        }
        if (params.no_revisit_required) {
            delete params.no_revisit_required;
        }
        let object_keys = Object.keys(params);

        for (let i = 0; i < object_keys.length; i++) {
            params[object_keys[i].replace('_', '-')] = params[object_keys[i]];
        }
        return params
    }

    renderTable() {
        let rows = [];
        for (let i = 0; i < Math.ceil(this.state.data.length / 3); i++) {
            let row = [];
            for (let j = 0; j < 3; j++) {
                if (this.state.data.length > (i * 3) + j) {
                    row.push(this.renderStore(this.state.data[(i * 3) + j], i));
                }
            }
            rows.push(
                <div className="row row-form">
                    {row}
                </div>
            )
        }
        return (
            <div className="container">
                {rows}
            </div>
        )
    }

    renderStore(store, num) {
        return (
            <div className="col-md-4 col-6 tile">
                <div className={`bg-${(num % 2) + 1}`}>
                    <h2><a href={`/store/${store.id}`}>{store.name}</a></h2>
                    <p style={{color: '#999'}}>
                        {store.address !== null &&
                            <span>{store.address}, </span>
                        }
                        {store.postalcode !== null &&
                            <span>{store.postalcode} </span>
                        }
                        {(store.locality) ? store.locality : store.region_name}
                    </p>
                </div>
            </div>
        )
    }
}