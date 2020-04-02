import React from "react";
const { Component } = React;
import { Map , Marker, Popup, TileLayer } from 'react-leaflet';
import  MarkerClusterGroup  from "react-leaflet-markercluster";
import $ from 'jquery';

export default class OsmMap extends Component {
    state = {
        initialized: false,
        geoJSON: {
            type: 'FeatureCollection',
            features: []
        }
    };
    baseBoxId = 'lokalwirkt-map';
    baseUrl = 'https://lokalwirkt.de';

    componentDidMount() {
        let box = $('#' + this.baseBoxId);
        if (box.data('base-url')) {
            this.baseUrl = box.data('base-url');
        }
        let regionSlug = box.data('region');
        if (!regionSlug)
            return;
        $.get(this.baseUrl + '/api/region/' + regionSlug)
            .then((data) => { this.loadMap(data) });
        this.setState({
            regionSlug: regionSlug,
            baseUrl: this.baseUrl,
        })
    }

    loadMap(data) {
        if (data.status !== 0)
            return;
        this.setState({
            region: data.data,
            initialized: true
        });
        let params = {
            'region-slug': data.data.slug
        };
        $.get(this.state.baseUrl + '/api/stores/geo', params)
            .then((data) => {
                this.setState({geoJSON: data});
            });
    }

    updateGeoJSON(data) {
        this.setState({
            geoJSON: data
        });
    }

    getOverlay(evt) {
        this.setState({
            storeLoading: true
        });
        $.get(this.state.baseUrl + '/api/store/' + evt.target.options.store)
            .then((data) => {
                if (data.status !== 0)
                    return;
                this.setState({
                    store: data.data,
                    storeLoading: false
                });
            });
    }

    closeOverlay() {
        this.setState({
            store: null
        });
    }

    render() {
        if (!this.state.initialized)
            return (<div>... wird geladen ...</div>);
        return (
            <div id="lokalwirkt-osm-box">
                <Map center={[this.state.region.lat, this.state.region.lon]} zoom="12" id="lokalwirkt-osm-map">
                    <TileLayer
                        attribution="&copy; <a href=&quot;https://osm.org/copyright&quot;>OpenStreetMap</a> contributors"
                        url="https://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png"
                    />
                    <MarkerClusterGroup>
                        {this.renderMarkers()}
                    </MarkerClusterGroup>
                </Map>
                {this.renderOverlay()}
            </div>
        )
    }

    renderMarkers() {
        let result = [];
        for (let i = 0; i < this.state.geoJSON.features.length; i++) {
            result.push(this.renderMarker(this.state.geoJSON.features[i]))
        }
        return result;
    }

    renderMarker(feature) {
        return(
            <Marker
                key={feature.properties.id}
                position={[feature.geometry.coordinates[1], feature.geometry.coordinates[0]]}
                onClick={this.getOverlay.bind(this)}
                store={feature.properties.id}
            >
            </Marker>
        );
    }

    renderOverlay() {
        if (!this.state.store && !this.state.storeLoading)
            return;
        if (this.state.storeLoading) {
            return (
                <div id="lokalwirkt-osm-overlay">
                    <div className="overlay-close" onClick={this.closeOverlay.bind(this)}>
                        X
                    </div>
                    <p>... wird geladen ...</p>
                </div>
            )
        }
        return (
            <div id="lokalwirkt-osm-overlay">
                <div className="overlay-close" onClick={this.closeOverlay.bind(this)}>
                    X
                </div>
                <h3>{this.state.store.name}</h3>
                <div id="lokalwirkt-osm-overay-container">
                    <div id="lokalwirkt-osm-overlay-left">
                        {this.state.store.address &&
                            <p>
                                {this.state.store.address &&
                                    <span>{this.state.store.address}<br/></span>
                                }
                                {this.state.store.postalcode &&
                                    <span>{this.state.store.postalcode} </span>
                                }
                                {this.state.store.locality &&
                                    <span>{this.state.store.locality}</span>
                                }
                            </p>
                        }
                        <p>
                            {this.state.store.phone &&
                                <span>
                                    Telefon:{' '}
                                    <a href={`mailto:${this.state.store.mobile}`}>
                                        {this.state.store.phone}
                                    </a><br/>
                                </span>
                            }
                            {this.state.store.mobile &&
                                <span>
                                    Mobil:{' '}
                                    <a href={`tel:${this.state.store.mobile}`}>
                                        {this.state.store.mobile}
                                    </a><br/>
                                </span>
                            }
                            {this.state.store.fax &&
                                <span>Fax: {this.state.store.fax}<br/></span>
                            }
                            {this.state.store.email &&
                                <span>Mail:{' '}
                                    <a href={`mailto:${this.state.store.email}`}>
                                        {this.state.store.email}
                                    </a><br/>
                                </span>
                            }
                            {this.state.store.website &&
                                <span>Web: <a href={this.state.store.website}>{this.state.store.website}</a><br/></span>
                            }
                            {this.state.store.brand &&
                                <span>Kette: {this.state.store.brand}<br/></span>
                            }
                            {this.state.store.wheelchair &&
                                <span>Rollstuhleignung: {this.formatWheelchair(this.state.store.wheelchair)}<br/></span>
                            }
                        </p>
                    </div>
                    <div id="lokalwirkt-osm-overlay-right">
                        {this.renderOpeningTimes(this.state.store['opening-time'])}
                    </div>
                </div>
            </div>
        )
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