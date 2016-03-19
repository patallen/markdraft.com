var debug = process.env.NODE_ENV !== 'production';
var webpack = require('webpack');

module.exports = {
    context: __dirname + "/src",
    devtool: debug ? "inline-sourcemap" : null,
    entry: ['bootstrap-loader', "./js/client.js"],
    module: {
        loaders: [
            {
                test: /\.js?$/,
                exclude: /(node_modules|bower_components)/,
                loader: 'babel-loader',
                query: {
                    presets: ['react', 'es2015', 'stage-0'],
                    plugins: ['react-html-attrs', 'transform-class-properties', 'transform-decorators-legacy']
                }
            },
            {
                test: /\.scss$/,
                include: /src/,
                loaders: [
                    'style',
                    'css',
                    'sass'
                ]
            },
            {
                test: /\.(ttf|eot|svg|woff(2)?)(\?[a-z0-9]+)?$/,
                loader: 'file-loader',
            }
        ]
    },
    output: {
        path: __dirname + "/src",
        filename: "client.min.js"
    },
    plugins: debug ? [] : [
        new webpack.optimize.DedupePlugin(),
        new webpack.optimize.OccurenceOrderPlugin(),
        new webpack.optimize.UglifyJsPlugin({mangle: false, sourcemap: false})
    ],
};
