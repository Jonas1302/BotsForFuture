from bff.api import respond_to, convert_to_post

@respond_to("^add all$")
@convert_to_post
def add_all_to_channel(post):
    post.reply(post.channel.name)
