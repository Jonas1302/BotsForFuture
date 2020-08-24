import logging
import caldav
from datetime import datetime, timedelta
from threading import Timer

from bff.api import User, Team, Channel, Post, at_start, listen_to, respond_to, convert_to_post, me
from bff.settings import settings
from bff.exceptions import DoNotLoadModuleException
from bff import storage


logger = logging.getLogger(__name__)


# check if this module shall be loaded
if settings["modules"] and __name__ not in settings["modules"]:
	logger.info(f"{__name__} shall not be loaded")
	raise DoNotLoadModuleException(__name__)

"""
data: {
	url,
	username,
	password,
	calendars,
	offsets: [(offset, message)],  // in minutes
}
"""

data = storage.get_storage("calendar")
default_team = Team.by_name(data.team)

client = caldav.DAVClient(url=data.url, username=data.username, password=data.password)
principal = client.principal()
calendars = principal.calendars()


def get_channel(title):
	return Channel.by_name(default_team, title)


def schedule(when, func, *args, **kwargs):
	if type(when) is timedelta:
		delay = when.total_seconds()
	else:  # should be datetime
		now = datetime.now()
		delay = (when - now).total_seconds()
	
	if delay < 0:
		logger.warn(f"Don't schedule because {when} is already over.")
		# maybe it's just a little error due to lazy programming
		if delay > -60:
			delay = 0
		else:
			return
	
	timer = Timer(delay, func, args, kwargs)
	timer.daemon = True
	timer.start()

@at_start
def check_calendars(startdt=None):
	for calendar in calendars:
		if len(data.calendars) > 0 and calendar.name not in data.calendars:
			continue
		
		if startdt is None:
			startdt = datetime.today()
		enddt= startdt + timedelta(days=1)
		events = calendar.date_search(start=startdt, end=enddt)
		
		for event in events:
			vevent = event.vobject_instance.vevent
			start = vevent.dtstart.value  # datetime
			title = vevent.summary.value  # string
			
			for offset, message in data.offsets:
				when = start - timedelta(minutes=offset)
				message = message.format(title)
				channel = get_channel(title)
				
				# only consider channels the bot was added to
				if channel not in me.channels:
					continue
				
				schedule(when, channel.post, (message,))
	
	# check calendar again since we just considered the next 24h
	schedule(enddt, check_calendars, (enddt,))
