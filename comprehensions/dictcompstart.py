"""
    Usage of comprehensions on dictionaries 
    and lists
"""


def main():
    ctemps = [0, 12, 34, 100]
    
    # TODO: Use comprehension to build a dictionary
    # tempDict = { t: (t*9/5)  + 32 for t in ctemps if t < 100 }
    # print(tempDict)
    # print(tempDict[12])
    
    # TODO: Merge below teams with a comprehension
    ## Note: This is as complicated as comprehensions should get
    ## should further code be required to a comprehension -> Create a function
    newTeam = {k:v for team in (team1, team2) for k,v in team.items()}
    
    # print(newTeam)
    
team1 = {
    "Jones": 24,
    "Jameson": 18,
    "Smith": 58,
    "Burns": 7
}

team2 = {
    "White": 12,
    "Macke": 88,
    "Perce": 4
}

if __name__ == '__main__':
    main()