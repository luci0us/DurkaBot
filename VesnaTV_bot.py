import VesnaTV_config
import VesnaTV_utils
import socket
import re
import time
import _thread
import random
from time import sleep


def main():
    last_escape = time.time() - 30
    vesna_escape = time.time() - 10
    catch_time = time.time() - 60
    durka_time = time.time()
    fight_time = time.time() - 60
    s = socket.socket()
    s.connect((VesnaTV_config.HOST, VesnaTV_config.PORT))
    s.send("PASS {}\r\n".format(VesnaTV_config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(VesnaTV_config.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(VesnaTV_config.CHAN).encode("utf-8"))

    chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

    f = open("ward.txt", "r")
    VesnaTV_config.ward = f.read().split()
    f.close()

    d = open("violent.txt", "r")
    VesnaTV_config.violent = d.read().split()
    d.close()

    VesnaTV_utils.mess(s, "/color #d946b6")

    _thread.start_new_thread(VesnaTV_utils.fillOpList, ())
    while True:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("POND :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0).lower()
            message = chat_message.sub("", response)
            print(response)

            mes = message.strip()
            words = mes.split()
            VesnaTV_config.counter[username] = VesnaTV_config.counter.get(username, 0) + 1

            # Общие команды для всех участников трансляции
            if time.time() - durka_time > 300:  # список комманд для чата
                durka_time = time.time()
                VesnaTV_utils.mess(s,
                           "/me Чат, напоминаем, что команды для дурки бота находятся тут https://github.com/luci0us/DurkaBot/blob/main/README.md")

            if mes == "!главврач":  # Показать главврача(стримера), выделения не будет
                VesnaTV_utils.mess(s, "/me " + VesnaTV_config.main_doctor[:].replace("a", "а") + " DurkaEbt")

            elif mes == "!санитары":  # Показать модерацию, выделения не будет
                VesnaTV_utils.mess(s, "/me Санитары: " + VesnaTV_utils.make_str(VesnaTV_utils.change_names(VesnaTV_config.sanitars)) + " DurkaEbt")

            elif mes == "!ботовод":  # Показать ботовода, выделения не будет
                VesnaTV_utils.mess(s, "/me За заведющего будет: " + VesnaTV_config.bot_leader[:].replace("c", "с") + " DurkaEbt")

            elif mes == "!лох":
                VesnaTV_utils.mess(s, "/me Ну да, я лох. И что? KappaPride")

            elif mes == "!хома":
                VesnaTV_utils.mess(s, "/me moderHom А? ЧТО? Я ЖИВ!")

            elif mes == "!голубь":
                VesnaTV_utils.mess(s, "/me Не скажу я вам инсайды, отстаньте! vesnaLeave")

            elif mes == "!побег" and time.time() - last_escape > 30.0 and username in VesnaTV_config.ward:
                last_escape = time.time()
                chance = random.uniform(0, 100)
                if username == "vovarium":
                    chance += 10
                if chance <= 25:
                    VesnaTV_utils.remove_schizo(username)
                    VesnaTV_utils.mess(s, "/me " + username + " сбежал из палаты")
                    VesnaTV_config.counter.clear()
                else:
                    VesnaTV_utils.mess(s, "/me Ну не везёт получается")

            elif mes == "!шизик" and time.time() - catch_time > 60:
                catch_time = time.time()
                chance1 = random.uniform(0, 100)
                if chance1 < 95:
                    for user in sorted(VesnaTV_config.counter, key=lambda x: (-VesnaTV_config.counter[x], x)):
                        if user not in VesnaTV_config.ward and not VesnaTV_utils.is_doctor(user) and username in VesnaTV_config.viewers:
                            VesnaTV_utils.add_schizo(user)
                            VesnaTV_config.counter.clear()
                            VesnaTV_utils.mess(s, "/me " + user + " ЭТО ГГ! SwiftRage")
                            break
                elif VesnaTV_config.CHAN not in VesnaTV_config.ward:
                    VesnaTV_utils.add_schizo(VesnaTV_config.CHAN)
                    VesnaTV_utils.mess(s, "/me  " + VesnaTV_config.CHAN + " ЭТО ГГ! SwiftRage")
                else:
                    VesnaTV_utils.mess(s, "/me ЭЭЭ, как не поймали никого???")

            elif mes == "!бой" and username in VesnaTV_config.ward:
                if time.time() - fight_time > 30:
                    fight_time = time.time()
                    if len(VesnaTV_config.ward) > 1:
                        second_fighter = random.choice(VesnaTV_config.ward)
                        while second_fighter == username:
                            second_fighter = random.choice(VesnaTV_config.ward)
                        winner = random.choice([username, second_fighter])
                        VesnaTV_utils.mess(s, "/me " + username + " решил побиться, а рядом оказался только " + second_fighter +
                                   ". По итогу победил " + winner + " и выбрался на свободу, второй сидит BloodTrail")
                        VesnaTV_utils.remove_schizo(winner)
                    else:
                        VesnaTV_utils.mess(s, "/me " + username + " решил побиться, а рядом оказалась только стена и " +
                                           username + " проиграл непобедимой стене BloodTrail")
                else:
                    VesnaTV_utils.mess(s, "/me Ещё не прибрано, ждите Kappa")

            # Комманды для модерации и Люци(для работников дурки)
            if VesnaTV_utils.is_doctor(username):
                if mes == "!палата":  # Показать участников палаты
                    VesnaTV_utils.mess(s, "/me Главные шизики: " + VesnaTV_utils.make_str(VesnaTV_config.ward))
                elif mes == "!карцер":  # Показать буйных шизов
                    VesnaTV_utils.mess(s, "/me Особо буйные дурики: " + VesnaTV_utils.make_str(VesnaTV_config.violent))
                elif words[0] == "!шизик" and len(words) == 2 and words[1][0] == "@":  # Добавить зрителя в палату
                    usr = words[1][1:].lower()
                    if usr in VesnaTV_config.viewers and not VesnaTV_utils.is_doctor(usr) and usr not in VesnaTV_config.ward:
                        VesnaTV_utils.add_schizo(usr)
                        VesnaTV_utils.mess(s, "/me ЭТО ГГ! SwiftRage")
                elif words[0] == "!здоров" and len(words) == 2 and words[1][0] == "@":  # Выпустить человека из палаты
                    usr = words[1][1:].lower()
                    if usr in VesnaTV_config.viewers and usr in VesnaTV_config.ward:
                        VesnaTV_utils.remove_schizo(usr)
                        VesnaTV_utils.mess(s, "/me ББ Squid1 Squid3 Squid2 Squid4")
                elif words[0] == "!рубашка" and len(words) == 2 and words[1][0] == "@":  # Добавить зрителя в карцер
                    usr = words[1][1:].lower()
                    if usr in VesnaTV_config.viewers and not VesnaTV_utils.is_doctor(usr) and usr not in VesnaTV_config.violent:
                        VesnaTV_utils.add_wild(usr)
                        VesnaTV_utils.mess(s, "/me Ну всё попался теперь не побегаешь StinkyCheese")
                elif words[0] == "!снять" and len(words) == 2 and words[1][0] == "@":  # Выпустить зрителя из карцера
                    usr = words[1][1:].lower()
                    if usr in VesnaTV_config.viewers and usr in VesnaTV_config.violent:
                        VesnaTV_utils.remove_wild(usr)
                        VesnaTV_utils.mess(s, "/me Больше не буянь Kappa")
                elif mes == "!предупреждение":
                    VesnaTV_utils.mess(s, "/me Не буянь VesnaTV, а то получишь по жопе KappaPride")
                elif words[0] == "!бан" and len(words) == 2 and words[1][0] == "@":  # Просто сообщение
                    usr = words[1][1:].lower()
                    VesnaTV_utils.mess(s, usr + ", может бан тебе выдать, а?")

                # Команды для стримера
                if username == VesnaTV_config.CHAN:
                    if mes == "!амнистия":
                        VesnaTV_utils.mess(s, "/me Амнистия! Дурики, далеко не разбегайтесь, будем вас ждать Kappa")
                        VesnaTV_utils.amnistia()
                    elif words[0] == "!спать" and len(words) == 2:
                        VesnaTV_utils.mess(s, "/me Ложусь спать")
                        sleep(float(words[1]) * 60)
                        VesnaTV_utils.mess(s, "/me Я поспал BloodTrail")
                    elif mes == "!подкоп":
                        if time.time() - vesna_escape > 10.0:
                            if username in VesnaTV_config.ward:
                                vesna_escape = time.time()
                                chance = random.uniform(0, 100)
                                if chance <= 50:
                                    VesnaTV_utils.remove_schizo(username)
                                    VesnaTV_utils.mess(s, "/me " + username + " сбежала по подкопу и скрылась")
                                else:
                                    VesnaTV_utils.mess(s, "/me Ну не везёт получается," + VesnaTV_config.CHAN + " KappaPride")
                        elif username in VesnaTV_config.ward:
                            VesnaTV_utils.mess(s, "/me Ещё рано копать VesnaTV")
                        else:
                            VesnaTV_utils.mess(s, "VesnaTV, ты не в палате, АЛОООО")

                # Команды для Люци
                if username == "luci0us":
                    if words[0] == "!шизик" and len(words) == 2 and words[1][0] == "@":  # Добавить зрителя в палату
                        usr = words[1][1:].lower()
                        if usr not in VesnaTV_config.ward:
                            VesnaTV_utils.add_schizo(usr)
                            VesnaTV_utils.mess(s, "/me ЭТО ГГ! SwiftRage")
                    elif words[0] == "!здоров" and len(words) == 2 and words[1][
                        0] == "@":  # Выпустить человека из палаты
                        usr = words[1][1:].lower()
                        if usr in VesnaTV_config.ward:
                            VesnaTV_utils.remove_schizo(usr)
                            VesnaTV_utils.mess(s, "/me ББ Squid1 Squid3 Squid2 Squid4")
                    elif words[0] == "!повязать" and len(words) == 2 and words[1][
                        0] == "@":  # Добавить человека в карцер
                        usr = words[1][1:].lower()
                        if usr not in VesnaTV_config.violent:
                            VesnaTV_utils.add_wild(usr)
                            VesnaTV_utils.mess(s, "/me Ну ты совсем озверел, тебя только так! BloodTrail")
                    elif words[0] == "!развязать" and len(words) == 2 and words[1][
                        0] == "@":  # Выпустить человека из карцера
                        usr = words[1][1:].lower()
                        if usr in VesnaTV_config.violent:
                            VesnaTV_utils.remove_wild(usr)
                            VesnaTV_utils.mess(s, "/me Мы следим за тобой! Kappa")
                    elif mes == "!амнистия":
                        VesnaTV_utils.mess(s, "/me Амнистия! Дурики, далеко не разбегайтесь, будем вас ждать Kappa")
                        VesnaTV_utils.amnistia()
                    elif mes == "!таблетки":
                        VesnaTV_utils.mess(s, "/me Так, дурики, а ну пить таблетки Vesnyam , а то получите по жопе SMOrc")
                    elif words[0] == "!спать" and len(words) == 2:
                        VesnaTV_utils.mess(s, "/me Ложусь спать")
                        sleep(float(words[1]) * 60)
                        VesnaTV_utils.mess(s, "/me Я поспал BloodTrail")
                    elif mes == "!подкоп" and time.time() - vesna_escape > 10.0 and username in VesnaTV_config.ward:
                        vesna_escape = time.time()
                        chance = random.uniform(0, 100)
                        if chance <= 50:
                            VesnaTV_utils.remove_schizo(username)
                            VesnaTV_utils.mess(s, "/me " + username + " сбежал через подкоп и зарыл обратно")
                        else:
                            VesnaTV_utils.mess(s, "/me Ну не везёт получается. Копай дальше")

                    elif words[0] == "!вызов" and len(words) == 2 and words[1][0] == "@":
                        usr = words[1][1:].lower()
                        VesnaTV_utils.mess(s, "/me " + usr + " был вызван в кабинет, идут разбирательства KappaPride")

        sleep(1)


if __name__ == "__main__":
    main()
