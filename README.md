# concorde

## So you want to migrate fro Slack to Riot.im?

Great choice! This repo represents a toolkit of self-hostable bits and pieces to make that
easy for your Slack users.

The **main value of this toolkit** is that it allows you to:

- sync your Slack usernames intoa Matrix homeserver automatically
- expose a secure way for the original owners of those usernames to register them in Matrix

If the above isn't important to you then there are likely simpler flows you can try (e.g.
if you're not worried about users having the same username you might still want to use
`scripts/list_slack_users.py` script to fetch a list of user email addresses and then
rely on standard Matrix third party identifier invites to invite users by email).

If you do want to use this toolkit, there are a few bits you'll have to:

- register a slack bot
- find somewhere to host a Python Flask API (zappa deploy to AWS lambda supported)
- find somewhere to host a static JS mithril app (direct upload to S3 supported)
- be comfortable with some BASH/your-favourite-shell to glue the cli scripts together

1. Get the homeserver secret from the homserver config.yaml
1. Generate a `passgen_secret`
1. Generate a `migration_secret`
1. Build the python library
    - create a new virtualenv
    - `pip install -r requirements.txt`
    - cd concorde
    - python setup.py install
1. Build the API
    - cd /website/api
    - modify `config.yaml`
    - zappa init
    - put in sensible values for zappa
    - zappa deploy <env_name>
    - note the AWS API gateway URL
1. Build the static site
    - cd /website/ui
    - `npm run-script build -- --env.registrationApiUrl <API gateway URL> --env.homeserver <url of homeserver, cosmetic> --env.slackTeam <slack team name, cosmetic> --env.domain <mxid domain part, cosmetic>
    - `aws s3 sync ./dist s3://bucket_name/prod`
    - go into AWS and make /prod publicly accessible
    - get the public URL of /prod/index.html
1. Register a slack bot on your worksapce
    - go to https://api.slack.com/apps
    - register an app
    - click 'Add features and functionality'
    - click 'Bots'
    - click 'Add a bot user'
    - pick values that won't startle your users
    - click 'Add bot user'
    - Go to 'OAuth and Permissions'
    - Install the app to your workspace
    - Get the bot user oauth token
1. Get all the users from Slack
    - cd /scripts
    - ./list_slack_users.py --bot-oath-token <bot-oauth-token>
    - ./register_matrix_user.py --homeserver <homeserver_url> --homeserver-secret <homeserver_secret> --passgen-secret <passgen_secret> <mxid mxid mxid...>
    - ./generate_link.py --migration-secret <migration_secret> <S3 public url for index.html> <mxid>
    - ./send_slack_dm.py --bot-oauth-token <bot-oauth-token> <slack user id> <message (including the generated link)>

And Bob's your uncle.
