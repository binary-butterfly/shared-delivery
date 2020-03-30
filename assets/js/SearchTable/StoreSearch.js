import React from "react";
import SearchTable from './SearchTable'

export default class StoreSearch extends SearchTable {
    params = {
        sort_field: 'name',
        sort_order: 'asc',
        page: 1
    };

    apiUrl = '/api/stores/search';
    formId = 'store-frontend-search-form';
    varPrefix = 'storeSearch';

    sortDef = [
        { key: 'name', name: 'Name' }
    ];

    constructor(props) {
        super(props);
        $('#no_revisit_required').change(() => {
            this.updateData();
        });
    }


    getParams() {
        console.log(this.params);
        let params = Object.assign({}, this.params);
        if (params.region_id) {
            params['region-id'] = params.region_id;
            delete params.region_id;
        }
        if ($('#no_revisit_required').is(':checked')) {
            params['revisit-required'] = '0';
        }
        if (params.no_revisit_required) {
            delete params.no_revisit_required;
        }
        return params
    }

    render() {
        if (!this.state.initialized) {
            return (
                <div className={'search-table-loading'}>
                    ... wird geladen ...
                </div>
            );

        }
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
                </div>
            </div>
        )
    }
}