from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to, respond_to
import datetime
import pendulum
import random
import json
import re
import schedule
from threading import Timer


class Tenets(MachineBasePlugin):
    ANNOUNCE_CHANNEL = "#labby_lives"  # "#general"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # schedule.every().monday.at("08:00").do(lambda: self.tenet())
        schedule.every().minute.do(lambda: self.tenet())

    def get_next_tenet(self):
        with open("./tenets.json", "r") as f:
            tenets = json.load(f)

        number_of_tenets = len(tenets)

        last_tenet_number = self.storage.get("tenet_number")
        last_tenet_number = last_tenet_number if last_tenet_number else random.randint(0, number_of_tenets-1)
        tenet_number = (last_tenet_number + 1) % number_of_tenets
        self.storage.set("tenet_number", tenet_number)

        tenet = tenets[tenet_number]

        return tenet

    def tenet(self):
        tenet = self.get_next_tenet()

        self.say(self.ANNOUNCE_CHANNEL,
f"""Welcome to work! This week's tenet of the week is:
{tenet}
Live your best Lab life, my Lab rats!""")

        for user in ["@niall"]: #self.users:
            self.send_dm_scheduled(pendulum.now()+datetime.timedelta(seconds=5), user,
f"""
Hey {user}, the tenet of the week has been:
{tenet}
How have you lived it this week?
""")

def tick():
        print("tick")
        schedule.run_pending()
        t = Timer(2, tick)
        t.start()
        print("tock")
tick()
