
export default class StoreForm {
    baseUrl = 'https://nominatim.openstreetmap.org/search?';
    address = {
        country: 'Deutschland',
    };
    params = {
        format: 'json',
        q: ''
    };
    constructor() {
        return;
        $('#category').multiselect(window.common.multiselect_options);
        if (!document.getElementById('store-new-form'))
            return;
        document.getElementById('store-new-form').onsubmit = (evt) => this.submitData(evt);
        document.getElementById('address').onkeydown = (evt) => this.resetGeocode(evt);
        document.getElementById('postalcode').onkeydown = (evt) => this.resetGeocode(evt);
        document.getElementById('locality').onkeydown = (evt) => this.resetGeocode(evt);
    }

    resetGeocode() {
        document.getElementById('store-new-form').classList.remove('geocoded');
        document.getElementById('geocoding-error').style.display = 'none';
    }

    setGeocodeError() {
        document.getElementById('geocoding-error').style.display = 'block';
        document.getElementById('store-new-form').classList.add('geocoded');
    }

    submitData(evt) {
        if (document.getElementById('store-new-form').classList.contains('geocoded')) {
            return;
        }
        evt.preventDefault();
        let params = Object.assign({}, this.params);
        const addressParts = this.getAddressParts();
        if (addressParts.some(part => !part)) {
            this.setGeocodeError();
            return;
        }
        addressParts.push('Deutschland');
        params.q = addressParts.join(', ');
        $.get(this.baseUrl + $.param(params))
            .then((data) => this.handleGeocodingResults(data));
    }

    getAddressParts() {
        const addressParts = [];
        addressParts.push(document.getElementById('address').value);
        addressParts.push(document.getElementById('postalcode').value);
        addressParts.push(document.getElementById('locality').value);
        return addressParts;
    }

    handleGeocodingResults(data) {
        if (data.length === 0) {
            this.setGeocodeError();
            return;
        }
        let geocoded = data[0];
        if (!geocoded.lat || !geocoded.lon) {
            this.setGeocodeError();
            return;
        }
        document.getElementById('lat').value = String(geocoded.lat);
        document.getElementById('lon').value = String(geocoded.lon);
        document.getElementById('store-new-form').classList.add('geocoded');
        document.getElementById('submit').click();
    }


}