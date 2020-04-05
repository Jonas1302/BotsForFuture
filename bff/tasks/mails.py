import logging
from bff.api import User, Team, Channel, respond_to, convert_to_post

logger = logging.getLogger(__name__)

mail_pattern = "{name} &lt;{email}&gt;"  # '<' and '>' would not be displayed by Mattermost Markdown
mail_separator = ", "


def post_mails(post, users):
    logger.info(f"post mails for users: {users}")
    addresses = []
    
    for user in users:
        addresses.append(mail_pattern.format(name=user.name, email=user.email))
    
    text = mail_separator.join(addresses)
    post.reply(text)
    return text

@respond_to("^mails$")
@convert_to_post
def post_mails_default(post):
    """Posts the mails of all users in the current team."""
    return post_mails(post, post.channel.team.users)

@respond_to("^mails( [\\S]+)+$")
@convert_to_post
def post_mails_specific(post, *targets):
    # targets may be users (with or without @) or team
    targets = list(map(str.strip, targets))
    logger.info(f"post mails for targets: {targets}")
    users = set()
    
    for target in targets:
        if target in ("all", "channel", "@all", "@channel"):
            # Note: this method is actually not called for '@all' and '@channel'
            # add all users in the current channel
            users.update(post.channel.users)
        elif target.startswith("@"):
            # add the specific user
            users.add(User.by_name(target[1:]))
        elif target.startswith("~"):
            # add all users in the specific channel
            users.update(Channel.by_team_and_name(post.channel.team, target[1:]).users)
        else:
            try:
                # try to find a user with the given name
                users.add(User.by_name(target))
            except Exception as e:
                print(e)
                logger.info(e.msg)
                # it's not a user therefore we assume it's a team name
                users.update(Team.by_name(target).users)
    return post_mails(post, users)
