import {Decimal} from 'decimal.js';

export default class Common {
    daterangepicker_locale = {
        format: 'DD.MM.YYYY',
        applyLabel: "wählen",
        cancelLabel: "abbrechen",
        customRangeLabel: 'Eigener Bereich',
        daysOfWeek: [
            "So",
            "Mo",
            "Di",
            "Mi",
            "Do",
            "Fr",
            "Sa"
        ],
        monthNames: [
            "Januar",
            "Februar",
            "März",
            "April",
            "mai",
            "Juni",
            "Juli",
            "August",
            "September",
            "Oktober",
            "November",
            "Dezember"
        ]
    };

    daterangepicker_ranges = {
       'heute': [moment(), moment()],
       'gestern': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
       'letzte 7 Tage': [moment().subtract(6, 'days'), moment()],
       'letzte 30 Tage': [moment().subtract(29, 'days'), moment()],
       'dieser Monat': [moment().startOf('month'), moment().endOf('month')],
       'letzter Monat': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
    };

    multiselect_options = {
        numberDisplayed: 0,
        includeSelectAllOption: true,
        allSelectedText: 'alles ausgewählt',
        nonSelectedText: 'bitte wählen',
        selectAllText: 'alles auswählen',
        nSelectedText: 'ausgewählt',
        buttonClass: 'form-control',
        buttonContainer: '<div class="btn-group bootstrap-multiselect" />'
    };

    constructor() {
        window.onunload = function(){};
        this.storageAvailable = this.getStorageAvailable();
        this.setLastUrl();
        $('.btn-icon').tooltip()
    }

    setLastUrl() {
        if (!this.storageAvailable)
            return;
        this.lastUrl = localStorage.getItem('lastUrl');
        localStorage.setItem('lastUrl', window.location.pathname);
    }

    getStorageAvailable() {
        try {
            let x = '__storage_test__';
            localStorage.setItem(x, x);
            localStorage.removeItem(x);
            return true;
        }
        catch(e) {
            return e instanceof DOMException && (
                // everything except Firefox
                e.code === 22 ||
                // Firefox
                e.code === 1014 ||
                // test name field too, because code might not be present
                // everything except Firefox
                e.name === 'QuotaExceededError' ||
                // Firefox
                e.name === 'NS_ERROR_DOM_QUOTA_REACHED') &&
                // acknowledge QuotaExceededError only if there's something already stored
                storage.length !== 0;
        }
    }


    eurofy (value) {
        if (!value) {
            return '0,00 €'
        }
        if (value || value === 0) {
            value = new Decimal(value);
            value = value.toFixed(2);
            return value.replace('.', ',') + ' €';
        }
        return value;
    }

    zerofy (value) {
        if (value < 10)
            return '0' + String(value);
        return String(value);
    };

    datetimeify(value) {
        if (!value)
            return '';
        let date = new Date(Date.parse(value));
        let result = String(date.getDate()) + '.' + String(date.getMonth() + 1) + ', ';
        result += this.zerofy(date.getHours()) + ':' + this.zerofy(date.getMinutes());
        return result
    }

    getURLParams() {
        let search = window.location.search;
        const hashes = search.slice(search.indexOf("?") + 1).split("&");
        return hashes.reduce((params, hash) => {
            const split = hash.indexOf("=");

            if (split < 0) {
                return Object.assign(params, {
                    [hash]: null
                });
            }

            const key = hash.slice(0, split);
            const val = hash.slice(split + 1);

            return Object.assign(params, {[key]: decodeURIComponent(val)});
        }, {});
    }
}