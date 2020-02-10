const webpack = require('webpack');
const config ={
    entry: {
        schedule: './js/schedule.jsx',
    },
    output: {
        path: __dirname + '/dist',
        filename: '[name].bundle.js',
    },
    resolve:{
        extensions:[
            '.js',
            '.jsx',
            '.css'
        ]
    },
    module:{
        rules:[
            {
                test:/\.jsx?/,
                exclude:/node_modules/,
                use:'babel-loader'
            },
            {
                test:/\.(jpe?g|png|gif|svg)$/i,
                loader:"file-loader?name=/public/[name].[ext]",

            },
            {
                test:/\.css$/,
                use:[
                    'css-loader'
                ],

            },

        ]
    }
};


module.exports = config;
