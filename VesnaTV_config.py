HOST = "irc.twitch.tv"
PORT = 6667
NICK = "botlucious"
PASS = "oauth:r9yrpwsv3fi1353yulh15oip2yn4fb"
CHAN = "vesnatv"  # vesnatv, luci0us, blue_screen_of_doom
RATE = (20/30)


oplist = {}
viewers = {}
ward = list()
violent = list()
broadcaster = ""
main_doctor = "VesnaTV"
bot_leader = "luci0us"
sanitars = ["sent1ma", "ToTCaMbINXoma"]
doctors = list(oplist.keys())
doctors = doctors + [bot_leader, NICK] + ["sent1ma".lower(), "ToTCaMbINXoma".lower(), main_doctor.lower(), "streamelements"]
counter = dict()
