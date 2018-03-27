# concorde

## So you want to migrate from Slack to Riot.im?

Great choice! This repo represents a toolkit of self-hostable bits and pieces to make that
easy for your Slack users.

**XXX: Warning!** - These instructions are so far only of a quality that they might serve to jog my memory. Anyone else trying to work through these will find it difficult. If you want to try this in the wild, contact me at **@tom:lant.uk**.

<hr>
The **main value of this toolkit** is that it allows you to:

- sync your Slack usernames into a Matrix homeserver automatically (and before anyone gets a chance to register publicly)
- expose a secure way for the original owners of those usernames to register them in Matrix (so if you knew who @somebody was in Slack, you know who @somebody:domain.tld is in Matrix)

If the above isn't important to you then there are likely simpler flows you can try (e.g.
if you're not worried about users having the same username you might still want to use
`scripts/list_slack_users.py` to fetch a list of user email addresses and then
rely on standard Matrix third party identifier invites to invite users by email).

1. Get the homeserver `registration_shared_secret` from the homeserver homeserver.yaml
1. Generate a `passgen_secret` - a shared secret to transform mxids into passwords
1. Generate a `migration_secret` - a shared secret to validate that links for a user to claim their account were generated by us
1. Build the python library
    - create a new virtualenv
    - `cd concorde`
    - `pip install -r requirements.txt`
    - `python setup.py install`
1. Build the API
    - `cd website/api`
    - modify `config.yaml`
    - `zappa init`
    - put in sensible values for zappa
    - `zappa deploy <env_name>`
    - note the generated AWS API gateway URL
1. Build the static site
    - `cd website/ui`
    - `npm run-script build -- --env.registrationApiUrl <API gateway URL> --env.homeserver <url of homeserver, cosmetic> --env.slackTeam <slack team name, cosmetic>
    - `aws s3 sync ./dist s3://bucket_name/prod`
    - go into AWS and make /prod publicly accessible
    - get the public URL of /prod/index.html
1. Register a slack bot on your worksapce
    - go to https://api.slack.com/apps
    - register an app
    - click 'Add features and functionality'
    - click 'Bots'
    - click 'Add a bot user'
    - choose a name and avatar that won't startle your users
    - click 'Add bot user'
    - Go to 'OAuth and Permissions'
    - Install the app to your workspace
    - Get the bot user oauth token
1. Get all the users from Slack
    - `cd scripts`
    - `./list_slack_users.py --bot-oauth-token <bot-oauth-token>`
    - `./register_matrix_user.py --homeserver <homeserver_url> --homeserver-secret <homeserver_secret> --passgen-secret <passgen_secret> <mxid mxid mxid...>`
    - `./generate_link.py --migration-secret <migration_secret> <S3 public url for index.html> <mxid> --display-name <display name>`
    - `./send_slack_dm.py --bot-oauth-token <bot-oauth-token> <slack user id> <message (probably including the generated link)>`

And Bob's your uncle.
