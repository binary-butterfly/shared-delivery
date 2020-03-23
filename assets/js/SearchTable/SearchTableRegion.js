import React from "react";
import SearchTable from './SearchTable'

export default class SearchTableStore extends SearchTable {
    params = {
        sort_field: 'name',
        sort_order: 'asc',
        page: 1
    };
    apiUrl = '/api/admin/regions';
    formId = 'region-search-form';
    varPrefix = 'searchTableRegion';
    loadParamsRegExp = [
        /store\/(.*)/g,
        /\/admin\/region\/(.*)/g
    ];

    sortDef = [
        { key: 'name', name: 'Name' },
        { key: 'created', name: 'Erstellt' }
    ];

    colDef = [
        { sortField: 'name', text: 'Name' },
        { text: 'Aktionen' }
    ];

    renderTableRow(row) {
        return (
            <tr key={`store-${row.id}`}>
                {this.renderTableCellName(row)}
                {this.renderTableCellActions(row)}
            </tr>
        )
    }

    renderTableCellName(row) {
        return(
            <td>
                {row.name}
            </td>
        )
    }

    renderTableCellActions(row) {
        return(
            <td>
                {this.renderActionLink(`/admin/region/${row.id}/show`, 'info', true)}
                {this.renderActionLink(`/admin/region/${row.id}/edit`, 'edit', true)}
            </td>
        )
    }
}