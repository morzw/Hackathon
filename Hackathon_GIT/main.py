import operator
import random


winners = []


def random_teams(teams_list):
    """
    :param teams_list: list of four team names (list of string)
    :return: prints the random division into two groups in the desired format
    """
    team1 = []
    team2 = []
    random_name = random.choice(teams_list)
    team1.append(random_name)
    teams_list.remove(random_name)
    random_name2 = random.choice(teams_list)
    team1.append(random_name2)
    teams_list.remove(random_name2)
    team2.extend(teams_list)
    print(u"\u001B[31m*~*~*Welcome to Keyboard Spamming Battle Royal*~*~*\n"
          u"\u001B[35mGroup 1:\n"
          "==")
    for name in team1:
        print(name)
    print(u"\u001B[33mGroup 2:\n"
          "==")
    for name2 in team2:
        print(name2)
    print(u"\u001B[31mStart pressing keys on your keyboard as fast as you can!!")
    fun_facts()


def winners_statistics(score1, score2):
    """
    :param score1: tuple of the first team results - (team name, score)
    :param score2: tuple of the second team results - (team name, score)
    :return: prints the best team ever to play on this server
    """
    winners.append(score1)
    winners.append(score2)
    winners.sort(key=operator.itemgetter(1), reverse=True)
    print(u"\u001B[32mThe Best Team EVER Played On This Server Is....")
    print("    " + "\U0001f451")
    print(winners[0])
    fun_facts()


def fun_facts():
    """
    :return: prints randomly a fun fact :)
    """
    list_of_facts = ["The First Computer Weighed More Than 27 Tons", "The First Computer Mouse was Made of Wood",
                     "The First Known Computer Programmer was a Woman, her name was Ada Lovelace",
                     "People Blink Less When They Use Computers", "Hackers Write About 6,000 New Viruses Each Month",
                     "More Than 80% of Daily Emails in the U.S. are Spam",
                     "The Parts for the Modern Computer Were First Invented in 1833",
                     "The First Gigabyte Drive Cost $40,000", "MIT Has Computers That can Detect Fake Smiles"]
    fact = random.choice(list_of_facts)
    print(u"\u001B[36mFun Fact:\n" + fact)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    random_teams(['Ori', 'Noa', 'Raz', 'Mor'])
    winners_statistics(('Ori', 100), ('Mor', 50))
    winners_statistics(('Noa', 200), ('Raz', 150))
    fun_facts()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
