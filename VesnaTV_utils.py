import VesnaTV_config
import urllib.request
import json
import time
import _thread
from time import sleep


def mess(sock, message):
    sock.send("PRIVMSG #{} :{}\r\n".format(VesnaTV_config.CHAN, message).encode())


def make_str(lst):
    return ", ".join(lst)


def is_doctor(user):
    return user in VesnaTV_config.doctors


def change_names(lst):
    new_lst = lst.copy()
    for p in new_lst:
        p.replace("a", "а")
        p.replace("c", "с")
    return new_lst


# http://tmi.twitch.tv/group/user/luci0us/chatters
# http://tmi.twitch.tv/group/user/vesnatv/chatters
# http://tmi.twitch.tv/group/user/blue_screen_of_doom/chatters
def fillOpList():
    while True:
        try:
            url = "http://tmi.twitch.tv/group/user/vesnatv/chatters"
            req = urllib.request.Request(url, headers={"accept": "*/*"})
            res = urllib.request.urlopen(req).read()
            VesnaTV_config.oplist.clear()
            data = json.loads(res)
            for p in data["chatters"]["moderators"]:
                VesnaTV_config.oplist[p] = "mod"
            for p in data["chatters"]["global_mods"]:
                VesnaTV_config.oplist[p] = "global_mod"
            for p in data["chatters"]["admins"]:
                VesnaTV_config.oplist[p] = "admin"
            for p in data["chatters"]["staff"]:
                VesnaTV_config.oplist[p] = "staff"
            for p in data["chatters"]["broadcaster"]:
                VesnaTV_config.oplist[p] = "broadcaster"
                VesnaTV_config.broadcaster = p
            for p in data["chatters"]["vips"]:
                VesnaTV_config.viewers[p] = "vip"
            for p in data["chatters"]["viewers"]:
                if p == "luci0us":
                    VesnaTV_config.oplist[p] = "bot_leader"
                else:
                    VesnaTV_config.viewers[p] = "viewer"
        except:
            "Something wrong"
        sleep(5)


def add_schizo(user):
    ward_file = open("ward.txt", "w")
    VesnaTV_config.ward.append(user)
    for p in VesnaTV_config.ward:
        ward_file.write(p + " ")
    ward_file.close()


def remove_schizo(user):
    ward_file = open("ward.txt", "w")
    VesnaTV_config.ward.remove(user)
    for p in VesnaTV_config.ward:
        ward_file.write(p + " ")
    ward_file.close()


def add_wild(user):
    violent_file = open("violent.txt", "w")
    VesnaTV_config.violent.append(user)
    for p in VesnaTV_config.violent:
        violent_file.write(p + " ")
    violent_file.close()


def remove_wild(user):
    violent_file = open("violent.txt", "w")
    VesnaTV_config.violent.remove(user)
    for p in VesnaTV_config.violent:
        violent_file.write(p + " ")
    violent_file.close()


def amnistia():
    ward_file = open("ward.txt", "w").close()
    VesnaTV_config.ward.clear()
    violent_file = open("violent.txt", "w").close()
    VesnaTV_config.violent.clear()
