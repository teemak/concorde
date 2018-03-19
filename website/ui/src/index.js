m = require('mithril')

c = require('./Claim.js')

const Claim = {
    view: vnode => {
        return m(c);
    }

};

m.route(document.body, '/', {
    '/': Claim
});
