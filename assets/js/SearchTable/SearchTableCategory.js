import React from "react";
import SearchTable from './SearchTable'

export default class SearchTableStore extends SearchTable {
    params = {
        sort_field: 'name',
        sort_order: 'asc',
        page: 1
    };
    apiUrl = '/api/admin/categories';
    formId = 'category-search-form';
    varPrefix = 'searchTableCategory';
    loadParamsRegExp = [
        /\/admin\/category\/(.*)/g
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
                {this.renderActionLink(`/admin/category/${row.id}/show`, 'info', true)}
                {this.renderActionLink(`/admin/category/${row.id}/edit`, 'edit', this.capabilities.includes('edit'))}
            </td>
        )
    }
}