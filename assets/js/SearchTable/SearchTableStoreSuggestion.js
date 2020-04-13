import React from "react";
import SearchTable from './SearchTable'

export default class SearchTableStoreSuggestion extends SearchTable {
    params = {
        sort_field: 'created',
        sort_order: 'desc',
        page: 1
    };
    apiUrl = '/api/admin/store/suggestions';
    formId = 'store-suggestion-search-form';
    varPrefix = 'searchTableStoreSuggestion';
    loadParamsRegExp = [
    ];

    sortDef = [
        { key: 'created', name: 'Erstellt' }
    ];

    colDef = [
        {sortField: 'created', text: 'Datum'},
        { sortField: 'name', text: 'Name' },
        { text: 'Adresse' },
        { text: 'Aktionen' }
    ];

    renderTableRow(row) {
        return (
            <tr key={`store-${row.id}`}>
                {this.renderTableCellCreated(row)}
                {this.renderTableCellName(row)}
                {this.renderTableCellAddress(row)}
                {this.renderTableCellActions(row)}
            </tr>
        )
    }

    renderTableCellCreated(row) {
        return(
            <td>
                {window.common.datetimeify(row.created)}
            </td>
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
                {this.renderActionLink(`/admin/store/suggestion/${row.id}/show`, 'info', true)}
                {this.renderActionLink(`/admin/store/suggestion/${row.id}/delete`, 'delete', true)}
            </td>
        )
    }
}