import React from "react";
const { Component } = React;
import io from 'socket.io-client';
import mapboxgl from 'mapbox-gl';
import $ from 'jquery';

export default class StoreMap extends Component {
    state = {
        initialized: false
    };

    geoApiUrl = '/api/stores/geo';

    componentDidMount() {
        mapboxgl.accessToken = map_config.token;

        this.map = new mapboxgl.Map({
            container: 'store-map-box',
            style: 'mapbox://styles/mapbox/light-v9',
            center: [map_config.lon, map_config.lat],
            zoom: map_config.zoom
        });
        this.map.addControl(new mapboxgl.NavigationControl(), 'top-left');

        var deref_map = new $.Deferred();
        var deref_data = new $.Deferred();

        $.when(deref_map, deref_data).done((mapready, data) => this.initMapData(mapready, data));
        this.map.on('load', function (data) {
            deref_map.resolve(data);
        });

        $.get(this.geoApiUrl, this.getParams(), (data) => {
            if (map_config.highlighted) {
                for (let i = 0; i <  data.features.length; i++) {
                    if (data.features[i].properties.id === map_config.highlighted) {
                        data.features[i].properties.highlighted = true;
                    }
                }
            }
            deref_data.resolve(data);
        });

        $('#store-map-search-form').submit((evt) => {
            evt.preventDefault();
            this.updateData();
        });
        $('#region_id').change(() => this.updateData());
    };

    updateData() {
        $.get(this.geoApiUrl, this.getParams(), (data) => {
            if (map_config.highlighted) {
                for (let i = 0; i <  data.features.length; i++) {
                    if (data.features[i].properties.id === map_config.highlighted) {
                        data.features[i].properties.highlighted = true;
                    }
                }
            }
            this.map.getSource('store-source').setData(data);
        });
    }

    getParams() {
        let data = {};
        if (map_config['region-slug']) {
            data['region-slug'] = map_config['region-slug'];
        }
        if (map_config['category-slug']) {
            data['category-slug'] = map_config['category-slug'];
        }
        if (document.getElementById('store-map-search-form')) {
            data['revisit-required'] = 0;
            if (document.getElementById('q').value) {
                data.q = document.getElementById('q').value;
            }
            if (document.getElementById('region_id').value && document.getElementById('region_id').value !== '_all') {
                data['region-id'] = document.getElementById('region_id').value;
            }
        }
        return data;
    }

    initMapData(mapready, data) {
        this.map.addSource('store-source', {
            type: 'geojson',
            data: data
        });
        let point_paint = {
            'circle-radius': 6,
            'circle-color': '#5cb85c',
            'circle-stroke-width': 1,
            'circle-stroke-color': '#89f789'
        };

        if (map_config.highlighted) {
            point_paint['circle-color'] = ['case', ['has', 'highlighted'], '#5cb85c', '#ffc107'];
            point_paint['circle-stroke-color'] = ['case', ['has', 'highlighted'], '#5cb85c', '#ffc107'];
        }

        this.map.addLayer({
            id: 'store-points',
            type: 'circle',
            source: 'store-source',
            paint: point_paint
        });

        this.map.addLayer({
            id: 'store-text',
            type: 'symbol',
            source: 'store-source',
            layout: {
                'text-field': '{name}',
                'text-offset': [0, 1.2],
                'text-size': 12
            },
            paint: {
                'text-color': '#000000'
            }
        });

        this.map.on('click', 'store-points', (e) => {
            this.setOverlayId(e.features[0].properties.id);
        });

        this.map.on('mouseenter', 'store-points', () => {
            this.map.getCanvasContainer().style.cursor = 'pointer';
        });

        this.map.on('mouseleave', 'store-points', () => {
            this.map.getCanvasContainer().style.cursor = '';
        });
    };

    setOverlayId(store_id) {
        $.get('/api/store/' + store_id)
            .then((data) => {
                this.setState({
                    overlayData: data.data
                });
            });
    }

    updateGeojson() {
        $.get('/api/stores/geo')
            .then((data) => {
                this.map.getSource('store-source').setData(this.geojson);
            });

    }


    unsetOverlayId() {
        this.setState({
            overlayData: null
        });
    }

    render() {
        return [
            <div id="store-map-box"></div>,
            <div id="store-map-overlay" style={{display: (this.state.overlayData) ? 'block' : 'none'}}>
                {this.renderOverlay()}
            </div>
        ];
    }

    renderOverlay() {
        if (!this.state.overlayData)
            return;
        return ([
            <div className="overlay-close" onClick={this.unsetOverlayId.bind(this)}>
                <i className="fa fa-3x fa-times-circle-o" aria-hidden="true"></i>
            </div>,
            <div className="container">
                <div className="row">
                    <div className="col-md-12">
                        <h2>{this.state.overlayData.name}</h2>
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-6">
                        {this.state.overlayData.address &&
                            <p>
                                {this.state.overlayData.address &&
                                    <span>{this.state.overlayData.address}<br/></span>
                                }
                                {this.state.overlayData.postalcode &&
                                    <span>{this.state.overlayData.postalcode} </span>
                                }
                                {this.state.overlayData.locality &&
                                    <span>{this.state.overlayData.locality}</span>
                                }
                            </p>
                        }
                        <p>
                            {this.state.overlayData.phone &&
                                <span>
                                    Telefon:{' '}
                                    <a href={`mailto:${this.state.overlayData.mobile}`}>
                                        {this.state.overlayData.phone}
                                    </a><br/>
                                </span>
                            }
                            {this.state.overlayData.mobile &&
                                <span>
                                    Mobil:{' '}
                                    <a href={`tel:${this.state.overlayData.mobile}`}>
                                        {this.state.overlayData.mobile}
                                    </a><br/>
                                </span>
                            }
                            {this.state.overlayData.fax &&
                                <span>Fax: {this.state.overlayData.fax}<br/></span>
                            }
                            {this.state.overlayData.email &&
                                <span>Mail:{' '}
                                    <a href={`mailto:${this.state.overlayData.email}`}>
                                        {this.state.overlayData.email}
                                    </a><br/>
                                </span>
                            }
                            {this.state.overlayData.website &&
                                <span>Web: <a href={this.state.overlayData.website}>{this.state.overlayData.website}</a><br/></span>
                            }
                            {this.state.overlayData.brand &&
                                <span>Kette: {this.state.overlayData.brand}<br/></span>
                            }
                            {this.state.overlayData.wheelchair &&
                                <span>Rollstuhleignung: {this.formatWheelchair(this.state.overlayData.wheelchair)}<br/></span>
                            }
                        </p>
                    </div>
                    <div className="col-md-6">
                        {(!(this.state.overlayData.revisited_government || this.state.overlayData.revisited_store || this.state.overlayData.revisited_user || this.state.overlayData.revisited_admin)) &&
                        <p className="map-not-revisited">
                            Die angezeigten Daten wurden noch nicht für Corona aktualisiert. Kannst Du uns dabei helfen?<br/>
                            <a href={`/store/${this.state.overlayData.id}/suggest`} className="btn btn-primary">
                                Ich kenne die aktuellen Öffnungszeiten
                            </a>
                        </p>
                        }
                        {this.renderOpeningTimes(this.state.overlayData['opening-time'])}
                    </div>
                </div>
            </div>
        ])
    }

    renderOpeningTimes(times) {
        if (!times)
            return;
        times = times.sort((a, b) => (a.weekday > b.weekday) ? 1 : (a.weekday === b.weekday) ? ((a.open > b.open) ? 1 : -1) : -1 );
        let result = [];
        for (let i = 0; i < times.length; i++) {
            result.push(
                <li>
                    {this.formatWeekday(times[i].weekday)}{' '}
                    {this.formatTime(times[i].open)} - {this.formatTime(times[i].close)}
                </li>
            );
        }
        return (
            <ul>
                {result}
            </ul>
        );
    }

    formatWeekday(weekday_id) {
        if (weekday_id === 1)
            return 'Montag';
        if (weekday_id === 2)
            return 'Dienstag';
        if (weekday_id === 3)
            return 'Mittwoch';
        if (weekday_id === 4)
            return 'Donnerstag';
        if (weekday_id === 5)
            return 'Freitag';
        if (weekday_id === 6)
            return 'Samstag';
        if (weekday_id === 7)
            return 'Sonntag';
    }

    formatTime(time) {
        return (String(Math.floor(time / 3600)) + ':' + this.prependZero(Math.floor((time % 60) / 60)));
    }
    prependZero(value) {
        if (value < 10)
            return '0' + String(value);
        return String(value);
    }

    formatWheelchair(value) {
        if (value === 'yes')
            return 'ja';
        if (value === 'no')
            return 'nein';
        if (value === 'yes')
            return 'ja';

    }
}


