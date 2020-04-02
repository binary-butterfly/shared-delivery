const path = require('path');
const webpack = require('webpack');

module.exports = {
    entry: [
        `./assets/client-js/base.js`,
        `./assets/client-js/webapp.js`
    ],
    mode: 'production',
    output: {
        path: path.join(__dirname, '..', 'static', 'js'),
        publicPath: '/static/js/client.min.js',
        filename: 'client.js',
    },
    optimization: {
        minimize: false
    },
    performance:{
        hints: false
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
                query: {
                    presets: ['@babel/preset-env', '@babel/preset-react']
                }
            },
        ]
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            moment: 'moment'
        }),
        new webpack.ContextReplacementPlugin(/moment[\/\\]locale$/, /de|en/)
    ]
};