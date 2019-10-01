from mmpy_bot.bot import respond_to

@respond_to("^add all$")
def add_all_to_channel(message):
    print(message.get_channel_name())
