const Path = require('path');

function create_config(options) {
    return {
        entry: "./src/index.js",
        output: {
            path: __dirname,
            filename: "./bin/app.js"
        },
        module: {
            loaders: [
                {
                    test: /\.css$/,
                    loader: "style-loader!css-loader"
                },
                {
                    test: /\.(jpg|png|svg)$/,
                    loader: "file-loader"
                },
                {
                    test: /config\.js$/,
                    loader: "string-replace-loader",
                    query: {
                        multiple: [
                            { search: 'REGISTRATION_API_URL', replace: options.registrationApiUrl },
                            { search: 'HOMESERVER', replace: options.homeserver },
                            { search: 'SLACK_TEAM', replace: options.slackTeam }
                        ]
                    }
                }
            ]
        },
        resolve: {
            alias: {
                Resources: Path.resolve(__dirname, 'resources')
            }
        }
    };
}

module.exports = function(env) {
    return create_config(env);
};
