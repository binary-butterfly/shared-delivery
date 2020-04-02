'use strict';

import gulp from 'gulp';
import sass from 'gulp-sass';
import autoprefixer from 'gulp-autoprefixer';
import sourcemaps from 'gulp-sourcemaps';
import browserify from "browserify";
import rev from 'gulp-rev';
import cache from 'gulp-cached';
import remember from 'gulp-remember';
import concat from 'gulp-concat';
import gulpif from 'gulp-if';
import source from 'vinyl-source-stream';
import cssnanoe from 'gulp-cssnano';
import gulpWebpack from 'webpack-stream';
import webpack from 'webpack';
import "@babel/polyfill";

const basePaths = {
    packages: './node_modules',
    dest: './static',
    src: './assets'
};

const sassPaths = {
    src: [`${basePaths.src}/sass/base.scss`, `${basePaths.src}/sass/webapp.scss`],
    dest: `${basePaths.dest}/css/`
};

const sassClientPaths = {
    src: [`${basePaths.src}/client-sass/base.scss`, `${basePaths.src}/client-sass/webapp.scss`],
    dest: `${basePaths.dest}/css/`
};


const scriptPaths = {
    src: [`${basePaths.src}/js/base.js`, `${basePaths.src}/js/webapp.js`],
    dest: `${basePaths.dest}/js`
};

const webpackConfiguration = require('./assets/webpack.config.js');
const webpackConfigurationProduction = require('./assets/webpack.production.config');
const webpackClientConfiguration = require('./assets/webpack.client.config.js');
const webpackClientConfigurationProduction = require('./assets/webpack.client.production.config');


let handleError = function (err) {
    console.log(err.toString());
    this.emit('end');
};

let enabled = {
    rev: 0
};

gulp.task('setproduction', (done) => {
    enabled.rev = 1;
    done();
});

gulp.task('watch', () => {
    gulp.watch(`${basePaths.src}/js/**/**.js`, gulp.series('webpack'));
    gulp.watch(`${basePaths.src}/sass/**/**.*`, gulp.series('styles')).on('change', function(evt) {
        if (evt.type === 'deleted') {
            delete cache.caches.styles[evt.path];
            remember.forget('styles', evt.path);
        }
        if (cache.caches.styles) {
            if (cache.caches.styles['/app/assets/sass/webapp.scss']) {
                delete cache.caches.styles['/app/assets/sass/webapp.scss'];
            }
        }
    });
    gulp.watch(`${basePaths.src}/client-js/**/**.js`, gulp.series('clientWebpack'));
    gulp.watch(`${basePaths.src}/client-sass/**/**.*`, gulp.series('clientStyles')).on('change', function(evt) {
        if (evt.type === 'deleted') {
            delete cache.caches.clientStyles[evt.path];
            remember.forget('clientStyles', evt.path);
        }
        if (cache.caches.clientStyles) {
            if (cache.caches.clientStyles['/app/assets/client-sass/webapp.scss']) {
                delete cache.caches.clientStyles['/app/assets/client-sass/webapp.scss'];
            }
        }
    });
});

gulp.task('styles', () => {
    return gulp.src(sassPaths.src)
        .pipe(sourcemaps.init())
        .pipe(cache('styles'))
        .pipe(sass.sync().on('error', sass.logError))
        .pipe(autoprefixer())
        //.pipe(gulpif(enabled.rev, cssnanoe()))
        .pipe(remember('styles'))
        .pipe(concat('webapp' + ((enabled.rev) ? '.min' : '') + '.css'))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(sassPaths.dest));
});

gulp.task('clientStyles', () => {
    return gulp.src(sassClientPaths.src)
        .pipe(sourcemaps.init())
        .pipe(cache('clientStyles'))
        .pipe(sass.sync().on('error', sass.logError))
        .pipe(autoprefixer())
        .pipe(gulpif(enabled.rev, cssnanoe()))
        .pipe(remember('clientStyles'))
        .pipe(concat('client' + ((enabled.rev) ? '.min' : '') + '.css'))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(sassClientPaths.dest));
});

gulp.task('webpack', () => {
    return gulp.src(scriptPaths.src)
        .pipe(gulpWebpack((enabled.rev) ? webpackConfigurationProduction : webpackConfiguration, webpack).on('error', function() {this.emit('end');}))
        .pipe(concat('webapp' + ((enabled.rev) ? '.min' : '') + '.js'))
        .pipe(gulp.dest(scriptPaths.dest))
        .pipe(gulpif(enabled.rev, rev.manifest(scriptPaths.dest + '/manifest.json', {
            base: scriptPaths.dest,
            merge: true,
        })))
        .pipe(gulp.dest(scriptPaths.dest));
});


gulp.task('clientWebpack', () => {
    return gulp.src(scriptPaths.src)
        .pipe(gulpWebpack((enabled.rev) ? webpackClientConfigurationProduction : webpackClientConfiguration, webpack).on('error', function() {this.emit('end');}))
        .pipe(concat('client' + ((enabled.rev) ? '.min' : '') + '.js'))
        .pipe(gulp.dest(scriptPaths.dest))
        .pipe(gulpif(enabled.rev, rev.manifest(scriptPaths.dest + '/client-manifest.json', {
            base: scriptPaths.dest,
            merge: true,
        })))
        .pipe(gulp.dest(scriptPaths.dest));
});

gulp.task('scripts', () => {
    return browserify({entries: scriptPaths.src})
        .transform('babelify', {presets: ['@babel/env']})
        .bundle()
        .pipe(concat('webapp' + ((enabled.rev) ? '.min' : '') + '.js'))
        .pipe(gulp.dest(scriptPaths.dest))
        .pipe(gulpif(enabled.rev, rev.manifest(scriptPaths.dest + '/manifest.json', {
            base: scriptPaths.dest,
            merge: true,
        })))
        .pipe(gulp.dest(scriptPaths.dest));
});

gulp.task('deploy', gulp.series('setproduction', 'styles', 'webpack', 'clientStyles', 'clientWebpack'));