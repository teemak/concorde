m = require('mithril');

require('./Claim.css');
config = require('../config');

const passwordIsValid = (password, password2) => {
    return password == password2 &&
        password.length >= 6;
};

const Claim = () => {
    var mxid = m.route.param('mxid');
    var code = m.route.param('code');
    var password = '';
    var password2 = '';

    var error = '';
    var feedback = '';

    var loading = false;

    return {
        view: vnode => {
            if (config.registrationApiUrl == '') {
                return m('div.error', 'The registration API has not been configured.');
            }
            else if (!mxid) {
                return m('div.error', 'No username was provided.');
            }
            else if (!code) {
                return m('div.error', 'No migration request validation code was provided.');
            }
            return m('div.center', [
                       m('div.header', [
                           m('img', {src: require('Resources/slack.png')}),
                           m('img', {src: require('Resources/arrow.png')}),
                           m('img', {src: require('Resources/riot.png')})
                       ]),
                       m('div.content-title',
                           m('h1', 'Import account settings')
                       ),
                       m('div.content', [
                           m('h3', 'Welcome'),
                           m('p', 'Welcome to Riot.im, the free and open source collaboration tool ' +
                                  'built on top of Matrix, the open protocol for decentralised, ' +
                                  'federated, encrypted messaging.'),
                           m('h3', 'Migration details:'),
                           m('div.rows', [
                               config.slackTeam != 'SLACK_TEAM' ? m('div.row', [
                                   m('label', 'Slack Team:'),
                                   m('span.value', config.slackTeam)
                               ]) : null,
                               config.homeserver != 'HOMESERVER' ? m('div.row', [
                                   m('label', 'Matrix Home Server:'),
                                   m('span.value', config.homeserver)
                               ]) : null,
                               m('div.row', [
                                   m('label', 'Matrix ID:'),
                                   m('span.value', '@' + mxid + ':' + config.domain)
                               ])
                           ]),
                           m('form', [
                               m('h3', 'Choose a password:'),
                               m('p.explanation', 'Passwords must be 6 characters or longer.'),
                               m('div.rows', [
                                   m('div.row', [
                                       m('label', 'Password:'),
                                       m('span.value', m('input', {
                                           type: 'password',
                                           value: password,
                                           autofocus: true,
                                           oninput: m.withAttr('value', value => {
                                               password = value;
                                           })
                                       }))
                                   ]),
                                   m('div.row', [
                                       m('label', 'Confirm Password:'),
                                       m('span.value', m('input', {
                                           type: 'password',
                                           value: password2,
                                           oninput: m.withAttr('value', value => {
                                               password2 = value;
                                           })
                                       }))
                                   ]),
                               ]),
                               feedback != '' ? m('div.feedback', feedback) : null,
                               error != '' ? m('div.error', error) : null,
                               m('button',
                                 {
                                     class: passwordIsValid(password, password2) ? 'valid' : 'invalid',
                                     disabled: loading,
                                     onclick: event => {
                                         event.preventDefault();
                                         feedback = ''; error = '';
                                         if (!passwordIsValid(password, password2)) {
                                             if (password != password2) {
                                                 error = 'Please check your passwords to make sure they match';
                                             }
                                             else if (password.length < 7) {
                                                 error = 'Password must be at least 6 characters long';
                                             }
                                         }
                                         else {
                                             loading = true;
                                             m.request({
                                                 method: 'POST',
                                                 url: config.registrationApiUrl + '/claim',
                                                 data: {
                                                     mxid: mxid,
                                                     code: code,
                                                     password: password
                                                 }
                                             })
                                             .then(result => {
                                                 loading = false;
                                                 if (result.response_code == 200) {
                                                     feedback = result.message;
                                                 }
                                                 else {
                                                     error = result.message;
                                                 }
                                             })
                                             .catch(error => {
                                                 loading = false;
                                                 error = 'Sorry, something went wrong. Please try again later';
                                             });
                                         }
                                     }
                                 },
                                 'Claim my Riot.im account')
                             ]),
                       ]),
                       m('div.footer', [
                           m('span', 'Powered by'),
                           m('a', {href: 'https://riot.im/app'}, 'riot.im'),
                           m('span', 'and'),
                           m('a', {href: 'https://matrix.org'}, 'matrix.org')
                       ])
                   ]);
        }
    };
};

module.exports = Claim;

