import React from "react";
import SearchTable from './SearchTable'

export default class SearchTableStore extends SearchTable {
    params = {
        sort_field: 'name',
        sort_order: 'asc',
        page: 1
    };
    apiUrl = '/api/admin/stores';
    formId = 'store-search-form';
    varPrefix = 'searchTableStore';
    loadParamsRegExp = [
        /store\/(.*)/g,
        /\/admin\/store\/(.*)/g
    ];

    sortDef = [
        { key: 'name', name: 'Name' },
        { key: 'created', name: 'Erstellt' }
    ];

    colDef = [
        { sortField: 'name', text: 'Name' },
        { text: 'Adresse' },
        { text: 'Aktionen' }
    ];

    renderTableRow(row) {
        return (
            <tr key={`store-${row.id}`}>
                {this.renderTableCellName(row)}
                {this.renderTableCellAddress(row)}
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

    renderTableCellAddress(row) {
        return(
            <td>
                {row.address}<br/>
                {row.postalcode} {row.locality}
            </td>
        )
    }

    renderTableCellActions(row) {
        return(
            <td>
                {this.renderActionLink(`/admin/store/${row.id}/show`, 'show', true)}
                {this.renderActionLink(`/admin/store/${row.id}/edit`, 'edit', true)}
            </td>
        )
    }
}