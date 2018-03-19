m = require('mithril');

require('./Claim.css');
config = require('../config');

const passwordIsValid = (password, password2) => {
    return password == password2 &&
        password.length > 0;
};

const Claim = () => {
    var mxid = m.route.param('mxid');
    var code = m.route.param('code');
    var password = '';
    var password2 = '';

    var loading = false;

    return {
        view: vnode => {
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
                                   m('span.value', mxid)
                               ])
                           ]),
                           m('h3', 'Choose a new password:'),
                           m('div.rows', [
                               m('div.row', [
                                   m('label', 'Password:'),
                                   m('span.value', m('input', {
                                       type: 'password',
                                       value: password,
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
                           m('button',
                             {
                                 class: passwordIsValid(password, password2) ? 'valid' : 'invalid',
                                 disabled: loading,
                                 onclick: event => {
                                     if (!passwordIsValid(password, password2)) {
                                         alert('Check yo passwords');
                                     }
                                     else {
                                         loading = true;
                                         m.request({
                                             method: 'POST',
                                             url: config.registrationApi + '/claim',
                                             data: {
                                                 mxid: mxid,
                                                 code: code,
                                                 password: password
                                             }
                                         })
                                         .then(result => {
                                             loading = false;
                                             console.log(result);
                                         });
                                     }
                                 }
                             },
                             'Claim my Riot.im account')
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

