import logging
from sched import scheduler
import time
import datetime
import math

from bff.api import respond_to, listen_to, convert_to_post
from bff.api import Post, Channel, Team
from bff.storage import get_storage


logger = logging.getLogger(__name__)
storage = get_storage("to")
announcers = {}


def get_to_url(date):
    return f"https://pad.fridaysforfuture.de/p/TOPs-KA-{date.year%100}-{date.month}-{date.day}"


def get_next_plenum_datetime(weekday, time, skip_weeks=0):
    """
    Return the `datetime.date` of the next plenum, assuming its weekly on the given `weekday`.
    
    Parameters
    ----------
    weekday : int
        weekday of the plenum: 0 = Monday, 1 = Tuesday, ... . default is Monday
    """
    current_date = datetime.datetime.now().date()
    # from https://stackoverflow.com/a/6558571
    days_ahead = weekday - current_date.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    # TODO: check if it's the evening after the plenum
    days_ahead += 7 * skip_weeks
    plenum_date = current_date + datetime.timedelta(days_ahead)
    return datetime.datetime.combine(plenum_date, time)  # TODO: consider local timezone


def on_init():
    start()

@respond_to("^to start$")
def start(_=None):  # first argument (post) is not needed
    if storage.teams is None:
        logger.error("Invalid configuration for TO Announcer")
        return
    
    for team in storage.teams:
        announcer = Announcer(team)
        announcer.start()
        announcers[team["name"]] = announcer

@respond_to("^to stop$")
def stop(_=None):  # first argument (post) is not needed
    map(Announcer.stop, announcers.values())
    announcers = {}

@respond_to("^to skip (\\S*) (\\d*)$")
@convert_to_post
def skip(post, team_name, weeks):
    assert isinstance(weeks, int)
    if not team_name in announcers:
        post.reply(f"No TO announcer for team {team} configured.")
        return
    announcers[team_name].skip(weeks)


class Announcer:
    def __init__(self, settings):
        self.settings = settings
        self.scheduler = scheduler()
        self.announcement_event = None
        self.reminder_event = None
        self.team = Team.by_name(self.settings["name"])
        self.channel = Channel.by_team_and_name(self.team, self.settings["channel"])
    
    
    def get_event(self, settings, skip_weeks, method):
        """
        Return the timedelta until the announcement or reminder datetime is reached.
        
        The datetime is given as days and hours before the next plenum.
        If the datetime already passed, one or more weeks will be added so the
        returned delay is always positive (i. e. in the future).
        `days_in_advance` is the number of days before the plenum
        `hours_in_advance` is the number of hours before the plenum
        """
        now = datetime.datetime.now()  # TODO: consider local timezone
        time = datetime.time(hour=self.settings["hour"], minute=self.settings["minute"])
        next_plenum_datetime = get_next_plenum_datetime(self.settings["weekday"], time, skip_weeks)
        timedelta = datetime.timedelta(days=settings["days_in_advance"],
                                       hours=settings["hours_in_advance"])  # time between plenum and target
        target_datetime = next_plenum_datetime - timedelta
        delay = target_datetime - now  # time until target
        
        # if target is in the past, we add as many weeks as needed to get the next target
        if delay < datetime.timedelta():  # check if delay is in the past ("negative")
            delay += datetime.timedelta(weeks=math.ceil(delay.days/7))
        
        logger.info(f"current delay for '{method.__name__}' is {delay}")
        return self.scheduler.enter(delay.total_seconds(), 0, method, (next_plenum_datetime,))
    
    
    def announce(self, plenum_date):
        message = storage.announcement_message.format(day=plenum_date.day,
                                                      month=plenum_date.month,
                                                      year=plenum_date.year,
                                                      url=get_to_url(plenum_date))
        post = Post.post(self.channel, message)
        self.settings["announcement-post-id"] = post.id
        storage.save()
        
        self.announcement_event = self.get_event(self.settings["announcement"], 0, self.announce)
        self.scheduler.run(blocking=False)
    
    def remind(self, plenum_date):
        if not self.settings["announcement-post-id"]:
            logger.warn("Reminding failed because no announcement was made")
        else:
            message = storage.reminder_message.format(day=plenum_date.day,
                                                      month=plenum_date.month,
                                                      year=plenum_date.year,
                                                      url=get_to_url(plenum_date))
            Post.by_id(self.settings["announcement-post-id"]).reply(message)
        
        self.reminder_event = self.get_event(self.settings["reminder"], 0, self.remind)
        self.scheduler.run(blocking=False)
    
    def start(self, skip_weeks=0):
        logger.info("start announcer {name} (channel: {channel}, plenum: {weekday}, {hour}:{minute})"
                    .format(**self.settings))
        self.announcement_event = self.get_event(self.settings["announcement"], skip_weeks, self.announce)
        self.reminder_event = self.get_event(self.settings["reminder"], skip_weeks, self.remind)
        self.scheduler.run(blocking=False)
    
    def stop(self):
        logger.info(f"stop announcer {self.settings['name']}")
        if self.announcement_event:
            self.scheduler.cancel(self.announcement_event)
            self.announcement_event = None
        if self.reminder_event:
            self.scheduler.cancel(self.reminder_event)
            self.reminder_event = None
    
    def skip(self, skip_weeks):
        self.stop()
        self.start(skip_weeks)


"""
[Entry, Entry, ...]
Entry: {team, channel, weekday, announcement-datetime, reminder-datetime,
        announcement-post-id, next-plenum}
"""

