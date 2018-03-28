const m = require('mithril');

require('./Claim.css');
const config = require('../config');

const Password = (() => {
    var minimumLength = 6;

    var E_PASSWORD_TOO_SHORT = 'Password must be at least ' + minimumLength + ' characters long';
    var E_PASSWORDS_DONT_MATCH = 'Please check your passwords to make sure they match';

    var passwordIsLongEnough = (password1) => {
        return password1.length >= minimumLength;
    };

    return {
        requirements: E_PASSWORD_TOO_SHORT,

        validate: (password1, password2) => {
            if (password1 != password2) {
                return E_PASSWORDS_DONT_MATCH;
            }
            else if (!passwordIsLongEnough(password1)) {
                return E_PASSWORD_TOO_SHORT;
            }
            return null;
        }
    };
})();

const Claim = () => {
    var username = m.route.param('username');
    var code = m.route.param('code');
    var displayName = m.route.param('displayName');
    var password = '';
    var password2 = '';

    var error = '';
    var feedback = '';

    var loading = false;

    return {
        view: () => {
            if (config.registrationApiUrl == '') {
                return m('div.error', 'The registration API has not been configured.');
            }
            else if (!username) {
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
                                   m('span.value', username)
                               ])
                           ]),
                           m('form', [
                               m('h3', 'Choose a password:'),
                               m('p.explanation', Password.requirements),
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
                                         var passwordValidationMessage = Password.validate(password, password2);
                                         if (passwordValidationMessage) {
                                             error = passwordValidationMessage;
                                         }
                                         else {
                                             loading = true;
                                             m.request({
                                                 method: 'POST',
                                                 url: config.registrationApiUrl + '/claim',
                                                 data: {
                                                     username: username,
                                                     /* This weird replace is because python's urllib encodes spaces as
                                                      * + (as is reasonable) but mithril doesn't translate those +'es
                                                      * back into real spaces (boo). Luckily, urllib does encode real +'es
                                                      * as %2B so display names containing a + will roundtrip safely. */
                                                     displayName: displayName.replace(/\+/g, ' '),
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

