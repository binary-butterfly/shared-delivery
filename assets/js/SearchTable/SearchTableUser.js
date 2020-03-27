import React from "react";
import SearchTable from './SearchTable'

export default class SearchTableUser extends SearchTable {
    params = {
        sort_field: 'lastname',
        sort_order: 'asc',
        page: 1
    };
    apiUrl = '/api/admin/users';
    formId = 'user-search-form';
    varPrefix = 'searchTableUser';
    loadParamsRegExp = [
        /admin\/user\/(.*)/g,
    ];

    sortDef = [
        { key: 'lastname', name: 'lastname' },
        { key: 'created', name: 'Erstellt' }
    ];

    colDef = [
        { sortField: 'name', text: 'Name' },
        { text: 'Aktionen' }
    ];

    renderTableRow(row) {
        return (
            <tr key={`user-${row.id}`}>
                {this.renderTableCellName(row)}
                {this.renderTableCellActions(row)}
            </tr>
        )
    }

    renderTableCellName(row) {
        return(
            <td>
                {row.lastname}, {row.firstname}<br/>
                <small>{row.email}</small>
            </td>
        )
    }

    renderTableCellActions(row) {
        return(
            <td>
                {this.renderActionLink(`/admin/user/${row.id}/show`, 'info', true)}
                {this.renderActionLink(`/admin/user/${row.id}/edit`, 'edit', true)}
            </td>
        )
    }
}