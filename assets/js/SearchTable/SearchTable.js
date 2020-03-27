import React from "react";

const { Component } = React;

export default class SearchTable extends Component {
    state = {
        page: 1,
        data: [],
        resultCount: 0,
        initialized: false,
        itemsPerPage: 25
    };
    params = {
        sort_field: '',
        sort_order: '',
        page: 1
    };
    apiUrl = '';
    formId = '';
    varPrefix = '';
    loadParamsRegExp = [];
    capabilities = [];

    sortDef = [];
    colDef = [];
    submit_proceed = [];


    componentDidMount() {
        this.init();
        this.updateData();
    }

    init() {
        this.params.csrf_token = $('#csrf_token').val();
        this.loadParams();
        let form = $('#' + this.formId);
        if (form.data('capabilities')) {
            this.capabilities = form.data('capabilities').trim().split(' ');
        }
        $('#' + this.formId + ' select').change((event) => this.formSubmit(event));
        document.getElementById(this.formId).onsubmit = (event) => this.formSubmit(event)
    }

    updateData() {
        this.saveParams();
        $.post(this.apiUrl, this.params)
            .then(data => {
                if (data.status)
                    return;
                this.setState({
                    data: data.data,
                    aggs: data.aggs,
                    initialized: true,
                    page: this.params.page,
                    resultCount: data.count,
                    pageMax: (data.count) ? Math.ceil(data.count / this.state.itemsPerPage) : 1
                });
            });
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        $(".selectpicker").selectpicker('refresh');
        $('.btn-icon').tooltip()
    }

    loadParams() {
        if (!window.common.storageAvailable)
            return;
        if (!window.common.lastUrl)
            return;
        if (!this.loadParamsRegExpMatches())
            return;
        let params = localStorage.getItem(this.varPrefix + 'Data');
        if (!params)
            return;
        this.params = JSON.parse(params);
        for (let key of Object.keys(this.params)) {
            $('#' + key).val(this.params[key]);
        }
    }

    loadParamsRegExpMatches() {
        for (var i = 0; i < this.loadParamsRegExp.length; i++) {
            if (window.common.lastUrl.match(this.loadParamsRegExp[i]))
                return true;
        }
        return false;
    }

    formSubmit(event) {
        let active = $(document.activeElement);
        if (active) {
            if (this.submit_proceed.includes(active.attr('id'))) {
                return;
            }
        }
        event.preventDefault();
        this.params.page = 1;
        this.updateParams();
        this.updateData();
    }

    daterangepickerSubmit(start, end, label) {
        this.params.page = 1;
        this.updateParams({
            daterange: start.format('DD.MM.YYYY') + ' - ' + end.format('DD.MM.YYYY')
        });
        this.updateData();
    }

    updateParams(overwrite) {
        if (!overwrite) {
            overwrite = {};
        }
        let ids = [];
        $('#' + this.formId + ' select, #' + this.formId + ' input, #' + this.formId + ' textarea').each(function () {
            if ($(this).attr('id')) {
                ids.push($(this).attr('id'));
            }
        });
        for (let i = 0; i < ids.length; i++){
            let item = $('#' + ids[i]);
            if (item.attr('name') === 'csrf_token')
                continue;
            if (item.attr('name') === 'submit')
                continue;
            if (Object.keys(overwrite).includes(item.attr('name'))) {
                this.params[item.attr('name')] = overwrite[item.attr('name')];
                continue;
            }
            if (item.val() && item.val() !== '_default' && item.val() !== '_all') {
                this.params[item.attr('name')] = item.val();
                continue;
            }
            delete this.params[item.attr('name')];
        }
    }

    saveParams() {
        if (!window.common.storageAvailable)
            return;
        localStorage.setItem(this.varPrefix + 'Data', JSON.stringify(this.params))
    }


    setPage(page) {
        if (page < 1 || page > this.state.pageMax)
            return;
        this.params.page = page;
        this.updateData();
    }

    setSort(field) {
        let sort_field_dom = $('#sort_field');
        let sort_order_dom = $('#sort_order');
        if (sort_field_dom.val() !== field) {
            sort_field_dom.val(field);
            sort_order_dom.val('asc');
        }
        else if (sort_order_dom.val() === 'asc') {
            sort_order_dom.val('desc');
        }
        else {
            sort_order_dom.val('asc');
        }
        $(".selectpicker").selectpicker('refresh');
        this.updateParams();
        this.updateData();
    }

    render() {
        if (!this.state.initialized) {
            return (
                <div className={'search-table-loading'}>
                    ... wird geladen ...
                </div>
            );

        }
        return (
            <div className={'search-table'}>
                {this.renderStatusLineTop()}
                {this.renderTable()}
                {this.renderStatusLineBottom()}
            </div>
        )
    }

    renderStatusLineTop() {
        return (
            <div className="row">
                <div className="col-md-12 search-table-result-header">
                    <div className="d-flex justify-content-between bd-highlight">
                        {this.renderStatusLineText()}
                        <div className="d-flex justify-content-end">
                            {this.renderPagination()}
                        </div>
                    </div>
                </div>
            </div>
        )
    }

    renderStatusLineBottom() {
        return (
            <div className="row">
                <div className="col-md-12 search-table-result-footer">
                    <div className="d-flex justify-content-end">
                        {this.renderPagination()}
                    </div>
                </div>
            </div>
        )
    }

    renderStatusLineText() {
        let sort_list = [];
        for (let i = 0; i < this.sortDef.length; i++) {
            let attrib = {};
            if (this.params.sort_field === this.sortDef[i].key) {
                attrib['selected'] = 'selected';
            }
            sort_list.push(
                <option value={this.sortDef[i].key} {...attrib}>{this.sortDef[i].name}</option>
            )
        }
        let attrib_asc = {};
        let attrib_desc = {};
        if (this.params.sort_order === 'asc') {
            attrib_asc['selected'] = 'selected';
        }
        else {
            attrib_desc['selected'] = 'selected';
        }
        return (
            <div className="d-flex justify-content-start search-table-result-header-text">
                <span>
                    {this.state.resultCount} Ergebnis{this.state.resultCount === 1 ? '' : 'se'}
                </span>
                <select id="sort_order" name="sort_order" onChange={(event) => this.formSubmit(event)} className="selectpicker" data-width="fit">
                    <option value="asc" {...attrib_asc}>aufsteigend</option>
                    <option value="desc" {...attrib_desc}>absteigend</option>
                </select>
                <span>
                    sortiert nach
                </span>
                <select id="sort_field" name="sort_field" onChange={(event) => this.formSubmit(event)} className="selectpicker" data-width="fit" data-showIcon="false">
                    {sort_list}
                </select>
            </div>
        )
    }

    renderTable() {
        return(
            <div className="row">
                <div className="col-md-12">
                    <table className="table table-striped table-bordered">
                        <thead>
                        {this.renderTableHead()}
                        </thead>
                        <tfoot>
                        {this.renderTableHead()}
                        </tfoot>
                        {this.renderTableRows()}
                    </table>
                </div>
            </div>
        )
    }

    renderTableHead() {
        let cols = [];
        for (let i = 0; i < this.colDef.length; i++) {
            let click = false;
            let classes = [];
            if (this.colDef[i].sortField) {
                classes.push('sortable');
                click = this.setSort.bind(this, this.colDef[i].sortField);
                if (this.params.sort_field === this.colDef[i].sortField) {
                    classes.push('active');
                    classes.push(this.params.sort_order);
                }
            }
            cols.push(
                <th onClick={click} className={classes.join(' ')}>{this.colDef[i].text}</th>
            )
        }
        return(
            <tr>
                {cols}
            </tr>
        )
    }

    renderPagination() {
        return(
            <nav aria-label="pagination">
                <ul className="pagination justify-content-end">
                    <li className={'page-item' + (this.state.page === 1 ? ' disabled' : '')}>
                        <a className="page-link" href="#" aria-label="first" onClick={this.setPage.bind(this, 1)}>
                            <span aria-hidden="true">&laquo;</span>
                        </a>
                    </li>
                    <li className={'page-item' + (this.state.page === 1 ? ' disabled' : '')}>
                        <a className="page-link" href="#" aria-label="previous" onClick={this.setPage.bind(this, this.state.page - 1)}>
                            <span aria-hidden="true">&lsaquo;</span>
                        </a>
                    </li>
                    <li className="page-item disabled">
                        <span className="page-link">{this.state.page}/{this.state.pageMax}</span>
                    </li>
                    <li className={'page-item' + (this.state.page >= this.state.pageMax ? ' disabled' : '')}>
                        <a className="page-link" href="#" aria-label="next" onClick={this.setPage.bind(this, this.state.page + 1)}>
                            <span aria-hidden="true">&rsaquo;</span>
                        </a>
                    </li>
                    <li className={'page-item' + (this.state.page >= this.state.pageMax ? ' disabled' : '')}>
                        <a className="page-link" href="#" aria-label="last" onClick={this.setPage.bind(this, this.state.pageMax)}>
                            <span aria-hidden="true">&raquo;</span>
                        </a>
                    </li>
                </ul>
            </nav>
        )
    }

    renderTableCellActionIcon(url, icon, label, condition) {
        if (!condition)
            return '';
        return(
            <a href={url} className="btn btn-default btn-icon" data-toggle="tooltip" data-placement="top" title={label}>
                <i className={`fa fa-${icon}`} aria-hidden="true"></i>
            </a>
        )
    }
    renderTableRows() {
        let rows = [];
        for (let i = 0; i < this.state.data.length; i++) {
            rows.push(this.renderTableRow(this.state.data[i]))
        }
        return (
            <tbody>
            {rows}
            </tbody>
        )
    }

    renderStatusIcon(icon, condition) {
        if (!condition)
            return '';
        return(
            <i className={`fa fa-${icon}`} aria-hidden="true"></i>
        )
    }

    renderActionLink(url, type, condition) {
        if (!condition)
            return '';
        if (type === 'info')
            return(
                <a href={url} className="btn btn-default btn-icon" data-toggle="tooltip" data-placement="top" title="anzeigen">
                    <i className={`fa fa-info`} aria-hidden="true"></i>
                </a>
            );
        if (type === 'edit')
            return(
                <a href={url} className="btn btn-default btn-icon" data-toggle="tooltip" data-placement="top" title="bearbeiten">
                    <i className={`fa fa-pencil-square-o`} aria-hidden="true"></i>
                </a>
            );
        if (type === 'delete')
            return(
                <a href={url} className="btn btn-default btn-icon" data-toggle="tooltip" data-placement="top" title="löschen">
                    <i className={`fa fa-trash-o`} aria-hidden="true"></i>
                </a>
            );
    }
}

