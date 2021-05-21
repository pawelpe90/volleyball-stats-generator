import datetime
import json
import os


def current_time(format):
    t = datetime.datetime.now()
    return t.strftime(format)


def save_to_file(content, file):
    for element in content:
        if len(element) == 4:
            file.write("[{}-{}] Point for {}! {}\n".format(element["score"]["team_a"], element["score"]["team_b"],
                                                           element["team"], element["ptype"]))
        else:
            file.write(element["info"])


def save_to_json(content, path):
    with open(path, "a") as json_outfile:
        json.dump(content, json_outfile)


def add_record(team, score_team_a, score_team_b, ptype, type="record"):
    return {"type": type, "team": team, "score": {"team_a": score_team_a, "team_b": score_team_b}, "ptype": ptype}


def add_event(info, type="event"):
    return {"type": type, "info": info}


def choose_type():
    while True:
        print("Choose type:\n[1] - attack \n[2] - block\n[3] - ace\n[4] - opponent error")
        ptype = input("Type: ")
        if ptype == "1":
            return choose_subtype_attack()
        elif ptype == "2":
            return "Block"
        elif ptype == "3":
            return "Ace"
        elif ptype == "4":
            return choose_subtype_opponent_error()
        else:
            print("Incorrect Input")


def choose_subtype_attack():
    while True:
        print("Choose type:\n[1] - zone 1 (serve) \n[2] - zone 2 (right)\n[3] - zone 3 (middle)\n"
              "[4] - zone 4 (left)\n[5] - zone 5\n[6] - zone 6 (pipe)")
        ptype = input("Type: ")
        if ptype == "1":
            return "Attack: zone1"
        elif ptype == "2":
            return "Attack: zone2"
        elif ptype == "3":
            return "Attack: zone3"
        elif ptype == "4":
            return "Attack: zone4"
        elif ptype == "5":
            return "Attack: zone5"
        elif ptype == "6":
            return "Attack: zone6"
        else:
            print("Incorrect Input")


def choose_subtype_opponent_error():
    while True:
        print("Choose type:\n[1] - faulty attack\n[2] - faulty serve\n[3] - net foul\n"
              "[4] - foot foul\n[5] - positional foul\n[6] - pass foul\n[7] - hand interlay\n[8] - setter disturbance"
              "\n[9] - other")
        ptype = input("Type: ")
        if ptype == "1":
            return "OpponentError: attackFoul"
        elif ptype == "2":
            return "OpponentError: serveFoul"
        elif ptype == "3":
            return "OpponentError: netFoul"
        elif ptype == "4":
            return "OpponentError: footFoul"
        elif ptype == "5":
            return "OpponentError: positionalFoul"
        elif ptype == "6":
            return "OpponentError: passFoul"
        elif ptype == "7":
            return "OpponentError: handInterlay"
        elif ptype == "8":
            return "OpponentError: setterDisturbance"
        elif ptype == "9":
            return "OpponentError: other"
        else:
            print("Incorrect Input")


def event_creator(team_a, team_b):
    team = team_picker(team_a, team_b)
    print("Choose event:\n[1] - time-out\n[2] - substitution\n")
    ptype = input("Type: ")

    while True:
        if ptype == "1":
            return f"Game event: time-out for {team}\n"
        elif ptype == "2":
            return f"Game event: substitution for {team}\n"
        else:
            print("Incorrect Input")


def team_picker(team_a, team_b):
    print(f"Pick team: \n[1] - {team_a}\n[2] - {team_b}")
    team = input("Team: ")

    while True:
        if team == "1":
            return team_a
        elif team == "2":
            return team_b
        else:
            print("Incorrect Input")


def main():
    team_a = "BioEden"
    team_b = "Ortomed"
    setno = 1
    tmp = []
    score = {team_a: 0, team_b: 0}
    path = r"C:\Users\pruszyns\Google Drive\volleyballStatistics"
    fname = "matchLog_{}_setNo{}_{}_{}".format(current_time("%d-%m-%Y %H-%M-%S"), setno, team_a, team_b)

    f = open(os.path.join(path, fname + ".txt"), "a")

    while True:
        print("\nScore: {} {} - {} {}".format(team_a, score[team_a], team_b, score[team_b]))
        print("[1] - log action \n[2] - remove previous record\n[3] - log event\n[4] - save and exit\n")
        action = input("Option: ")

        if action == "1":
            print("Point for: [1] - {}, [2] - {}".format(team_a, team_b))
            point = input("Team: ")
            if point == "1":
                score[team_a] += 1
                ptype = choose_type()
                tmp.append(add_record(team_a, score[team_a], score[team_b], ptype))
            elif point == "2":
                score[team_b] += 1
                ptype = choose_type()
                tmp.append(add_record(team_b, score[team_a], score[team_b], ptype))
            else:
                print("Incorrect input!")

        elif str(action) == "2":
            try:
                prev_score = tmp[-2]['score']
                score[team_a] = prev_score['team_a']
                score[team_b] = prev_score['team_b']
                del tmp[-1]

            except IndexError:
                prev_score = tmp[-1]['score']
                score[team_a] = prev_score['team_a']
                score[team_b] = prev_score['team_b']
                del tmp[-1]

        elif str(action) == "3":
            event = event_creator(team_a, team_b)
            tmp.append(add_event(event))

        elif str(action) == "4":
            save_to_file(tmp, f)
            save_to_json(tmp, os.path.join(path, fname + ".json"))
            print("End of the session")
            break

        else:
            print("Incorrect input!")

    f.close()

main()