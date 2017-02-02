from pyramid.response import Response
from pyramid.view import view_config,view_defaults
import random
from pyramid.httpexceptions import (
HTTPFound,
HTTPNotFound,
)
import re
from sqlalchemy.exc import DBAPIError
from ..models import *

@view_config(route_name='tournament', renderer='templates/tournament.jinja2',permission = "view")
def view_tournament(request):
    if 'submitted' in request.params:
        if 'weight' in request.params:
            weight = request.params['weight']
        else:
            weight = ""

        if 'number_table' in request.params:
            number_table = request.params['number_table']
        else:
            number_table = 0
        build = request.params['build']
        address = request.params['address']

        if 'win' in request.params:
            if not request.params['win'].isdigit():
                score_win = 3
            else:
                score_win = int(request.params['win'])
        else:
            score_win = 0

        if 'draw' in request.params:
            if not request.params['draw'].isdigit():
                score_draw = 1
            else:
                score_draw = int(request.params['draw'])
        else:
            score_draw = 0

        if 'lose' in request.params:
            if not request.params['lose'].isdigit():
                score_lose = 0
            else:
                score_lose = int(request.params['lose'])
        else:
            score_lose = 0
        if 'number' in request.params:
            number = int(request.params['number'])
        else:
            number = 0
        nameTournament = request.params['nameTournament']
        city = request.params['city']
        kindName = request.params['kind']
        date = request.params['date']
        date2 = request.params['date2']
        if (date != ""):
            d = date.split('-')
            date = d[2] + "." + d[1] + "." + d[0]
        else:
            date = ""
        if (date2 != ""):
            d = date2.split('-')
            date2 = d[2] + "." + d[1] + "." + d[0]
        else:
            date2 = ""
        description = request.params['description']

        user = DBSession.query(User).filter_by(login = request.authenticated_userid).first()
        kind = DBSession.query(KindOfSport).filter_by(name = kindName).first()

        if 'type' in request.params:
            typeName = request.params['type']
        elif 'typePL' in request.params:
            typeName = request.params['typePL']
        elif kindName == 'Армспорт':
            typeName = ""
        else:
            typeName = "Гонка"

        type = DBSession.query(TypeTournament).filter_by(name=typeName).first()

        if 'group' in request.params:
            group = int(request.params['group'])
            fullList = []
            listTeams = []
            event = Event(building=build,address=address,scoreWin=score_win,scoreDraw=score_draw,scoreLose=score_lose,name=nameTournament,description=description, date=date,city=city, groupNumber=group, kind=kind, type=type, user=user)
            DBSession.add(event)
            i = 0
            while (i < number):
                inputName = "input" + str(i)
                input = request.params[inputName]
                listTeams.append(input)
                i += 1

            #numberInGroup = number / group
            nameGroup = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
            #number2 = number
            group2 = group

            if typeName == 'Групповой турнир с плей-офф':
                while (group > 0):
                    groupList = []
                    numberInGroup = number / group

                    while (numberInGroup > 0):
                        #rnd = random.randint(0, number - 1)
                        groupList.append(listTeams.pop(0))
                        numberInGroup -= 1
                        number -= 1

                    fullList.append(groupList)
                    group -= 1
            else:
                while (group > 0):
                    groupList = []
                    numberInGroup = number / group
                    while (numberInGroup > 0):
                        rnd = random.randint(0, number - 1)
                        groupList.append(listTeams[rnd])
                        listTeams.pop(rnd)
                        numberInGroup -= 1
                        number -= 1
                    fullList.append(groupList)
                    group -= 1

            #group = int(request.params['group'])
            i = 0
            while (i < group2):
                j = 0
                while (j < len(fullList[i])):
                    model = GroupTable(position=j + 1, event=event, name=fullList[i][j], games=0, wins=0, draws=0,
                                       lose=0, goalsScored=0, goalsAgainst=0, score=0, nameGroup=nameGroup[i])
                    DBSession.add(model)
                    j += 1
                i += 1

            return HTTPFound(location="my_tournaments")

        event = Event(weight = weight,numberTable=number_table,building=build,address=address,scoreWin=score_win,scoreDraw=score_draw,scoreLose=score_lose,
                      name=nameTournament,description=description, date=date,dateEnd=date2,city=city, groupNumber=0, kind=kind, type=type, user=user)
        DBSession.add(event)

        '''
        if typeName == "":
            return HTTPFound(location="my_tournaments")


        if typeName == 'Плей-офф (случайное распределение)':
            group = number/2
            fullList = []
            listTeams = []
            group2 = group

            i = 0
            while (i < number):
                inputName = "input" + str(i)
                input = request.params[inputName]
                listTeams.append(input)
                i += 1

            while (group > 0):
                groupList = []
                numberInGroup = number / group
                while (numberInGroup > 0):
                    rnd = random.randint(0, number - 1)
                    groupList.append(listTeams[rnd])
                    listTeams.pop(rnd)
                    numberInGroup -= 1
                    number -= 1
                fullList.append(groupList)
                group -= 1

            i = 0
            while (i < group2):
                model = PlayOff(event = event,date = "",playerOne = fullList[i][0],playerTwo = fullList[i][1],stage = group2)
                DBSession.add(model)
                i += 1

            group2 /= 2
            while(group2 >= 1):
                i = 0
                while(i< group2):
                    model = PlayOff(event = event,date = "",playerOne = "",playerTwo = "",stage = group2)
                    DBSession.add(model)
                    i+=1
                group2 /= 2

            return HTTPFound(location="my_tournaments")

        if typeName == 'Круговой турнир':
            i = 0
            while(i<number):
                inputName = "input" + str(i)
                input = request.params[inputName]
                model = Table(position=i+1,event=event, name= input, games=0, wins=0, draws=0,
                              lose=0, goalsScored = 0,goalsAgainst = 0, score=0)
                DBSession.add(model)
                i+=1
            return HTTPFound(location="my_tournaments")

        if typeName == 'Плей-офф':
            group = number / 2
            fullList = []
            listTeams = []
            group2 = group

            i = 0
            while (i < number):
                inputName = "input" + str(i)
                input = request.params[inputName]
                listTeams.append(input)
                i += 1

            while (group > 0):
                groupList = []
                numberInGroup = number / group

                while (numberInGroup > 0):
                    # rnd = random.randint(0, number - 1)
                    groupList.append(listTeams.pop(0))
                    numberInGroup -= 1
                    number -= 1

                fullList.append(groupList)
                group -= 1

            i = 0
            while (i < group2):
                model = PlayOff(event=event, date="", playerOne=fullList[i][0], playerTwo=fullList[i][1],
                                stage=group2)
                DBSession.add(model)
                i += 1

            group2 /= 2
            while (group2 >= 1):
                i = 0
                while (i < group2):
                    model = PlayOff(event=event, date="", playerOne="", playerTwo="", stage=group2)
                    DBSession.add(model)
                    i += 1
                group2 /= 2

            return HTTPFound(location="my_tournaments")

        i = 0
        while (i < number):
            inputName = "input" + str(i)
            input = request.params[inputName]
            model = RaceTable(position=i + 1, event=event, name=input, score="")
            DBSession.add(model)
            i += 1'''

        return HTTPFound(location="my_tournaments")

    return {}

@view_config(route_name='profile', renderer='templates/profile.jinja2',permission = "view")
@view_config(route_name='apiMy', renderer='myjson')
def view_profile(request):
    user = DBSession.query(User).filter_by(login = request.authenticated_userid).first()
    events = DBSession.query(Event).filter_by(user = user).all()
    listContent = []
    if request.matched_route.name == 'apiMy':
        for event in events:
            listContent.append(event.id)
        return{"events":listContent}
    if 'sub' in request.params:
        message = ""
        stringKind = ""
        kindList = ['badminton', 'basketball', 'run', 'ski', 'cycle_racing', 'volleyball', 'handball', 'rowing',
                    'fighting', 'skating', 'tennis',
                    'table_tennis', 'swimming', 'rugby', 'football', 'hockey', 'snowboard', 'other']

        name = request.params['nameFilter']
        city = request.params['cityFilter']
        date = request.params['dateFilter']
        if (date != ""):
            d = date.split('-')
            date = d[2] + "." + d[1] + "." + d[0]
        else:
            date = ""

        if name and city and date:
            for kind in kindList:
                if kind in request.params:
                    sport = DBSession.query(KindOfSport).filter_by(name=request.params[kind]).first()
                    stringKind += request.params[kind] + ", "
                    events = DBSession.query(Event).filter_by(user=user,kind=sport, name=name, city=city, date=date).all()
                    for event in events:
                        list = fillList(event)
                        listContent.append(list)
            if stringKind == "":
                events = DBSession.query(Event).filter_by(user=user,date=date, city=city, name=name).all()
                for event in events:
                    list = fillList(event)
                    listContent.append(list)
            message = "Результат по поиску: название мероприятия - " + name + ", дата начала мероприятия - " + date + \
                      ", город проведения мероприятия - " + city
            if stringKind != "":
                message += ", виды спорта - " + stringKind[0:len(stringKind) - 2]

            if len(listContent) == 0:
                messageError = "Ваш запрос не дал результатов"
                return {"message": message,
                        "messageError": messageError}

            return {"message": message,
                    "listContent": listContent}
        if name and date:
            for kind in kindList:
                if kind in request.params:
                    sport = DBSession.query(KindOfSport).filter_by(name=request.params[kind]).first()
                    stringKind += request.params[kind] + ", "
                    events = DBSession.query(Event).filter_by(user=user,kind=sport, name=name, date=date).all()
                    for event in events:
                        list = fillList(event)
                        listContent.append(list)
            if stringKind == "":
                events = DBSession.query(Event).filter_by(user=user,date=date, name=name).all()
                for event in events:
                    list = fillList(event)
                    listContent.append(list)
            message = "Результат по поиску: название мероприятия - " + name + ", дата начала мероприятия - " + date
            if stringKind != "":
                message += ", виды спорта - " + stringKind[0:len(stringKind) - 2]

            if len(listContent) == 0:
                messageError = "Ваш запрос не дал результатов"
                return {"message": message,
                        "messageError": messageError}

            return {
                "message": message,
                "listContent": listContent}
        if name and city:
            for kind in kindList:
                if kind in request.params:
                    sport = DBSession.query(KindOfSport).filter_by(name=request.params[kind]).first()
                    stringKind += request.params[kind] + ", "
                    events = DBSession.query(Event).filter_by(user=user,kind=sport, name=name, city=city).all()
                    for event in events:
                        list = fillList(event)
                        listContent.append(list)
            if stringKind == "":
                events = DBSession.query(Event).filter_by(user=user,city=city, name=name).all()
                for event in events:
                    list = fillList(event)
                    listContent.append(list)
            message = "Результат по поиску: название мероприятия - " + name + ", город проведения мероприятия - " + city
            if stringKind != "":
                message += ", виды спорта - " + stringKind[0:len(stringKind) - 2]

            if len(listContent) == 0:
                messageError = "Ваш запрос не дал результатов"
                return {"message": message,
                        "messageError": messageError}

            return {
                "message": message,
                "listContent": listContent}
        if date and city:
            for kind in kindList:
                if kind in request.params:
                    sport = DBSession.query(KindOfSport).filter_by(name=request.params[kind]).first()
                    stringKind += request.params[kind] + ", "
                    events = DBSession.query(Event).filter_by(user=user,kind=sport, city=city, date=date).all()
                    for event in events:
                        list = fillList(event)
                        listContent.append(list)
            if stringKind == "":
                events = DBSession.query(Event).filter_by(user=user,city=city, date=date).all()
                for event in events:
                    list = fillList(event)
                    listContent.append(list)
            message = "Результат по поиску: дата начала мероприятия - " + date + ", город проведения мероприятия - " + city
            if stringKind != "":
                message += ", виды спорта - " + stringKind[0:len(stringKind) - 2]

            if len(listContent) == 0:
                messageError = "Ваш запрос не дал результатов"
                return {"message": message,
                        "messageError": messageError}

            return {
                "message": message,
                "listContent": listContent}
        if name:
            for kind in kindList:
                if kind in request.params:
                    sport = DBSession.query(KindOfSport).filter_by(name=request.params[kind]).first()
                    stringKind += request.params[kind] + ", "
                    events = DBSession.query(Event).filter_by(user=user,kind=sport, name=name).all()
                    for event in events:
                        list = fillList(event)
                        listContent.append(list)
            if stringKind == "":
                events = DBSession.query(Event).filter_by(user=user,name=name).all()
                for event in events:
                    list = fillList(event)
                    listContent.append(list)
            message = "Результат по поиску: название мероприятия - " + name
            if stringKind != "":
                message += ", виды спорта - " + stringKind[0:len(stringKind) - 2]

            if len(listContent) == 0:
                messageError = "Ваш запрос не дал результатов"
                return {"message": message,
                        "messageError": messageError}

            return {
                "message": message,
                "listContent": listContent}
        if date:
            for kind in kindList:
                if kind in request.params:
                    sport = DBSession.query(KindOfSport).filter_by(name=request.params[kind]).first()
                    stringKind += request.params[kind] + ", "
                    events = DBSession.query(Event).filter_by(user=user,kind=sport, date=date).all()
                    for event in events:
                        list = fillList(event)
                        listContent.append(list)
            if stringKind == "":
                events = DBSession.query(Event).filter_by(user=user,date=date).all()
                for event in events:
                    list = fillList(event)
                    listContent.append(list)
            message = "Результат по поиску: дата начала мероприятия - " + date
            if stringKind != "":
                message += ", виды спорта - " + stringKind[0:len(stringKind) - 2]

            if len(listContent) == 0:
                messageError = "Ваш запрос не дал результатов"
                return {"message": message,
                        "messageError": messageError}

            return {
                "message": message,
                "listContent": listContent}
        if city:
            for kind in kindList:
                if kind in request.params:
                    sport = DBSession.query(KindOfSport).filter_by(name=request.params[kind]).first()
                    stringKind += request.params[kind] + ", "
                    events = DBSession.query(Event).filter_by(user=user,kind=sport, city=city).all()
                    for event in events:
                        list = fillList(event)
                        listContent.append(list)
            if stringKind == "":
                events = DBSession.query(Event).filter_by(user=user,city=city).all()
                for event in events:
                    list = fillList(event)
                    listContent.append(list)
            message = "Результат по поиску: город проведения мероприятия - " + city
            if stringKind != "":
                message += ", виды спорта - " + stringKind[0:len(stringKind) - 2]

            if len(listContent) == 0:
                messageError = "Ваш запрос не дал результатов"
                return {"message": message,
                        "messageError": messageError}

            return {
                "message": message,
                "listContent": listContent}

        for kind in kindList:
            if kind in request.params:
                sport = DBSession.query(KindOfSport).filter_by(name=request.params[kind]).first()
                stringKind += request.params[kind] + ", "
                events = DBSession.query(Event).filter_by(user=user,kind=sport).all()
                for event in events:
                    list = fillList(event)
                    listContent.append(list)

        if stringKind != "":
            message += "Результат по поиску: виды спорта - " + stringKind[0:len(stringKind) - 2]

        if message == "":
            return HTTPFound(location="/my_tournaments")

        if len(listContent) == 0:
            messageError = "Ваш запрос не дал результатов"
            return {"message": message,
                    "messageError": messageError}

        return {"message": message,
                "listContent": listContent}

    for event in events:
        list = fillList(event)
        listContent.append(list)
    return {"listContent":listContent}

def favoritesList(request):
    events = []
    user = DBSession.query(User).filter_by(login=request.authenticated_userid).first()
    favorites = DBSession.query(Favorites).filter_by(user=user).all()
    for e in favorites:
        event = DBSession.query(Event).filter_by(id=e.eventId).first()
        events.append(event)
    return events

def fillList(event):
    list = []
    list.append(event.id)
    list.append(event.name)
    kind = DBSession.query(KindOfSport).filter_by(id=event.kindId).first()
    list.append(kind.name)
    list.append(event.city)
    list.append(event.date)
    list.append(kind.name + ".png")
    return list

def fullFillList(event):
    list = []
    list.append(event.id)
    list.append(event.name)
    kind = DBSession.query(KindOfSport).filter_by(id=event.kindId).first()
    list.append(kind.name)
    list.append(event.city)
    list.append(event.date)
    list.append(event.description)
    list.append(event.typeId)
    list.append(event.userId)
    list.append(kind.name + ".png")
    list.append(event.building)
    list.append(event.address)
    list.append(event.scoreWin)
    list.append(event.scoreDraw)
    list.append(event.scoreLose)
    return list

@view_config(route_name='allTournaments', renderer='templates/allTournaments.jinja2')
@view_config(route_name='apiAllTournaments', renderer='myjson')
def at_view(request):
    listContent = []
    listFavorites = []
    if 'sub' in request.params:
        message = ""
        stringKind = ""
        kindList = ['badminton','basketball','run','ski','cycle_racing','volleyball','handball','rowing','fighting','skating','tennis',
                    'table_tennis','swimming','football','hockey','snowboard','other']

        name = request.params['nameFilter']
        city = request.params['cityFilter']
        date = request.params['dateFilter']

        if (date != ""):
            d = date.split('-')
            date = d[2] + "." + d[1] + "." + d[0]
        else:
            date = ""

        if name and city and date:
            for kind in kindList:
                if kind in request.params:
                    sport = DBSession.query(KindOfSport).filter_by(name=request.params[kind]).first()
                    stringKind += request.params[kind] + ", "
                    events = DBSession.query(Event).filter_by(kind=sport,name=name,city=city,date=date).all()
                    for event in events:
                        list = fullFillList(event)
                        if(event in favoritesList(request)):
                            listFavorites.append(list)
                        else:
                            listContent.append(list)
            if stringKind == "":
                events = DBSession.query(Event).filter_by(date=date,city=city,name=name).all()
                for event in events:
                    list = fullFillList(event)
                    if (event in favoritesList(request)):
                        listFavorites.append(list)
                    else:
                        listContent.append(list)
            message = "Результат по поиску: название мероприятия - " + name + ", дата начала мероприятия - " + date + \
                      ", город проведения мероприятия - " + city
            if stringKind != "":
                message += ", виды спорта - " + stringKind[0:len(stringKind)-2]

            if (len(listContent) == 0 and len(listFavorites) == 0):
                messageError = "Ваш запрос не дал результатов"
                return {"message": message,
                        "messageError": messageError}

            return {"message":message,
                    "listContent":listContent,
                    "listFavorites":listFavorites}
        if name and date:
            for kind in kindList:
                if kind in request.params:
                    sport = DBSession.query(KindOfSport).filter_by(name=request.params[kind]).first()
                    stringKind += request.params[kind] + ", "
                    events = DBSession.query(Event).filter_by(kind=sport, name=name, date=date).all()
                    for event in events:
                        list = fullFillList(event)
                        if (event in favoritesList(request)):
                            listFavorites.append(list)
                        else:
                            listContent.append(list)
            if stringKind == "":
                events = DBSession.query(Event).filter_by(date=date, name=name).all()
                for event in events:
                    list = fullFillList(event)
                    if (event in favoritesList(request)):
                        listFavorites.append(list)
                    else:
                        listContent.append(list)
            message = "Результат по поиску: название мероприятия - " + name + ", дата начала мероприятия - " + date
            if stringKind !="":
                message += ", виды спорта - " + stringKind[0:len(stringKind)-2]

            if (len(listContent) == 0 and len(listFavorites) == 0):
                messageError = "Ваш запрос не дал результатов"
                return {"message": message,
                        "messageError": messageError}

            return {
                "message": message,
                "listContent": listContent,
                "listFavorites":listFavorites}
        if name and city:
            for kind in kindList:
                if kind in request.params:
                    sport = DBSession.query(KindOfSport).filter_by(name=request.params[kind]).first()
                    stringKind += request.params[kind] + ", "
                    events = DBSession.query(Event).filter_by(kind=sport, name=name, city=city).all()
                    for event in events:
                        list = fullFillList(event)
                        if (event in favoritesList(request)):
                            listFavorites.append(list)
                        else:
                            listContent.append(list)
            if stringKind == "":
                events = DBSession.query(Event).filter_by(city=city, name=name).all()
                for event in events:
                    list = fullFillList(event)
                    if (event in favoritesList(request)):
                        listFavorites.append(list)
                    else:
                        listContent.append(list)
            message = "Результат по поиску: название мероприятия - " + name  + ", город проведения мероприятия - " + city
            if stringKind !="":
                message += ", виды спорта - " + stringKind[0:len(stringKind)-2]

            if (len(listContent) == 0 and len(listFavorites) == 0):
                messageError = "Ваш запрос не дал результатов"
                return {"message": message,
                        "messageError": messageError}

            return {
                "message": message,
                "listContent": listContent,
                "listFavorites":listFavorites}
        if date and city:
            for kind in kindList:
                if kind in request.params:
                    sport = DBSession.query(KindOfSport).filter_by(name=request.params[kind]).first()
                    stringKind += request.params[kind] + ", "
                    events = DBSession.query(Event).filter_by(kind=sport, city=city, date=date).all()
                    for event in events:
                        list = fullFillList(event)
                        if (event in favoritesList(request)):
                            listFavorites.append(list)
                        else:
                            listContent.append(list)
            if stringKind == "":
                events = DBSession.query(Event).filter_by(city=city, date=date).all()
                for event in events:
                    list = fullFillList(event)
                    if (event in favoritesList(request)):
                        listFavorites.append(list)
                    else:
                        listContent.append(list)
            message = "Результат по поиску: дата начала мероприятия - " + date + ", город проведения мероприятия - " + city
            if stringKind!="":
                message += ", виды спорта - " + stringKind[0:len(stringKind) - 2]

            if (len(listContent) == 0 and len(listFavorites) == 0):
                messageError = "Ваш запрос не дал результатов"
                return {"message": message,
                        "messageError": messageError}

            return {
                "message": message,
                "listContent": listContent,
                "listFavorites":listFavorites}
        if name:
            for kind in kindList:
                if kind in request.params:
                    sport = DBSession.query(KindOfSport).filter_by(name=request.params[kind]).first()
                    stringKind += request.params[kind] + ", "
                    events = DBSession.query(Event).filter_by(kind=sport, name=name).all()
                    for event in events:
                        list = fullFillList(event)
                        if (event in favoritesList(request)):
                            listFavorites.append(list)
                        else:
                            listContent.append(list)
            if stringKind == "":
                events = DBSession.query(Event).filter_by(name=name).all()
                for event in events:
                    list = fullFillList(event)
                    if (event in favoritesList(request)):
                        listFavorites.append(list)
                    else:
                        listContent.append(list)
            message = "Результат по поиску: название мероприятия - " + name
            if stringKind!="":
                message += ", виды спорта - " + stringKind[0:len(stringKind) - 2]

            if (len(listContent) == 0 and len(listFavorites) == 0):
                messageError = "Ваш запрос не дал результатов"
                return {"message": message,
                        "messageError": messageError}

            return {
                "message": message,
                "listContent": listContent,
                "listFavorites":listFavorites}
        if date:
            for kind in kindList:
                if kind in request.params:
                    sport = DBSession.query(KindOfSport).filter_by(name=request.params[kind]).first()
                    stringKind += request.params[kind] + ", "
                    events = DBSession.query(Event).filter_by(kind=sport, date=date).all()
                    for event in events:
                        list = fullFillList(event)
                        if (event in favoritesList(request)):
                            listFavorites.append(list)
                        else:
                            listContent.append(list)
            if stringKind == "":
                events = DBSession.query(Event).filter_by(date=date).all()
                for event in events:
                    list = fullFillList(event)
                    if (event in favoritesList(request)):
                        listFavorites.append(list)
                    else:
                        listContent.append(list)
            message = "Результат по поиску: дата начала мероприятия - " + date
            if stringKind != "":
                message += ", виды спорта - " + stringKind[0:len(stringKind) - 2]

            if (len(listContent) == 0 and len(listFavorites) == 0):
                messageError = "Ваш запрос не дал результатов"
                return {"message": message,
                        "messageError": messageError}

            return {
                "message": message,
                "listContent": listContent,
                "listFavorites":listFavorites}
        if city:
            for kind in kindList:
                if kind in request.params:
                    sport = DBSession.query(KindOfSport).filter_by(name=request.params[kind]).first()
                    stringKind += request.params[kind] + ", "
                    events = DBSession.query(Event).filter_by(kind=sport, city=city).all()
                    for event in events:
                        list = fullFillList(event)
                        if (event in favoritesList(request)):
                            listFavorites.append(list)
                        else:
                            listContent.append(list)
            if stringKind == "":
                events = DBSession.query(Event).filter_by(city=city).all()
                for event in events:
                    list = fullFillList(event)
                    if (event in favoritesList(request)):
                        listFavorites.append(list)
                    else:
                        listContent.append(list)
            message = "Результат по поиску: город проведения мероприятия - " + city
            if stringKind != "":
                    message += ", виды спорта - " + stringKind[0:len(stringKind) - 2]

            if (len(listContent) == 0 and len(listFavorites)):
                messageError = "Ваш запрос не дал результатов"
                return {"message": message,
                        "messageError": messageError}

            return {
                "message": message,
                "listContent": listContent,
                "listFavorites":listFavorites}

        for kind in kindList:
            if kind in request.params:
                sport = DBSession.query(KindOfSport).filter_by(name=request.params[kind]).first()
                stringKind += request.params[kind] + ", "
                events = DBSession.query(Event).filter_by(kind=sport).all()
                for event in events:
                    list = fullFillList(event)
                    if (event in favoritesList(request)):
                        listFavorites.append(list)
                    else:
                        listContent.append(list)

        if stringKind != "":
            message += "Результат по поиску: виды спорта - " + stringKind[0:len(stringKind) - 2]

        if message == "":
            return HTTPFound(location="/all_tournaments")

        if (len(listContent) == 0 and len(listFavorites) == 0):
            messageError = "Ваш запрос не дал результатов"
            return {"message": message,
                    "messageError": messageError}

        return {"message": message,
                "listContent":listContent,
                "listFavorites":listFavorites}

    events = DBSession.query(Event).filter_by().all()
    for event in events:
        list = fullFillList(event)
        if (event in favoritesList(request)):
            listFavorites.append(list)
        else:
            listContent.append(list)
    if request.matched_route.name == 'apiAllTournaments':
        apiList = []
        for list in listContent:
            apiList.append({"id":list[0],
                            "name":list[1],
                            "city":list[3],
                            "kind":list[2],
                            "date":list[4],
                            "description":list[5],
                            "type_id":list[6],
                            "user_id":list[7],
                            "building":list[9],
                            "address":list[10],
                            "score_win":list[11],
                            "score_draw":list[12],
                            "score_lose":list[13]})
        return {"events":apiList}
    return {"listContent":listContent,
            "listFavorites":listFavorites}

@view_config(route_name='tournamentDetail', renderer='templates/tournamentDetail.jinja2')
@view_config(route_name='apiTournamentDetail', renderer='myjson')
def td_view(request):
    id = request.matchdict['name']
    name = DBSession.query(Event).filter_by(id = id).first()
    if name:
        table = DBSession.query(Table).filter_by(event=name).all()
        #.order_by(Table.score.desc())
        playOff = DBSession.query(PlayOff).filter_by(event=name).all()
        race = DBSession.query(RaceTable).filter_by(event=name).all()
        group = DBSession.query(GroupTable).filter_by(event = name).all()
        games = DBSession.query(Game).filter_by(event=name).all()
        user = DBSession.query(User).filter_by(login=request.authenticated_userid).first()
        userTournament = DBSession.query(User).filter_by(id=name.userId).first()
        model = DBSession.query(Favorites).filter_by(event=name, user=user).first()
        type = DBSession.query(TypeTournament).filter_by(id=name.typeId)
        listWeight = []
        if model:
            favorites = True
        else:
            favorites = False
        root = False

        if user == userTournament:
            root = True

        if 'date' in request.params:
            date = request.params['date']
            if (date != ""):
                d = date.split('-')
                date = d[2] + "." + d[1] + "." + d[0]
            else:
                date = ""

        if request.matched_route.name == 'apiTournamentDetail':
            if table:
                list = []
                for t in table:
                    list.append(
                        {'position': t.position,
                         'name': t.name,
                         'games': t.games,
                         'wins': t.wins,
                         'draws': t.draws,
                         'lose': t.lose,
                         'goals_scored': t.goalsScored,
                         'goals_against': t.goalsAgainst,
                         'score': t.score})
                listGames = []
                for g in games:
                    listGames.append(
                        {'date': g.date,
                         'player_one': g.playerOne,
                         'player_two': g.playerTwo,
                         'score_player_one': g.playerOneScore,
                         'score_player_two': g.playerTwoScore}
                    )
                return {
                    'event_id': table[0].eventId,
                    'table': list,
                    'games': listGames
                }
            if group:
                groupList = []
                groupNumber = name.groupNumber
                nameGroup = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
                i = 0
                while (i < groupNumber):
                    table = DBSession.query(GroupTable).filter_by(event=name, nameGroup=nameGroup[i]).all()
                    list = []
                    for t in table:
                        list.append(
                            {'position': t.position,
                             'name': t.name,
                             'games': t.games,
                             'wins': t.wins,
                             'draws': t.draws,
                             'lose': t.lose,
                             'goals_scored': t.goalsScored,
                             'goals_against': t.goalsAgainst,
                             'score': t.score})
                    groupList.append({nameGroup[i]: list})
                    i += 1

                listGames = []
                for g in games:
                    listGames.append(
                        {'date': g.date,
                         'player_one': g.playerOne,
                         'player_two': g.playerTwo,
                         'score_player_one': g.playerOneScore,
                         'score_player_two': g.playerTwoScore}
                    )
                return {'event_id': group[0].eventId,
                        "groups": groupList,
                        "games": listGames
                        }
            if race:
                list = []
                for t in race:
                    list.append(
                        {'position': t.position,
                         'name': t.name,
                         'score': t.score})
                #listGames = []
                #for g in games:
                #    listGames.append(
                #        {'date': g.date,
                #         'player_one': g.playerOne,
                #         'player_two': g.playerTwo,
                #         'score_player_one': g.playerOneScore,
                #         'score_player_two': g.playerTwoScore}
                #    )

                return {'event_id': race[0].eventId,
                        'table': list}
            if playOff:
                playOffList = []
                stage = [64, 32, 16, 8, 4, 2, 1]
                i = 0
                while (i < len(stage)):
                    table = DBSession.query(PlayOff).filter_by(event=name, stage=stage[i]).all()
                    list = []
                    for t in table:
                        list.append(
                            {'date': t.date,
                             'player_one': t.playerOne,
                             'player_two': t.playerTwo,
                             'score_player_one': t.playerOneScore,
                             'score_player_two': t.playerTwoScore})
                    playOffList.append({stage[i]: list})
                    i += 1

                return{'event_id':playOff[0].eventId,
                       'grid':playOffList}

        if root:
            if 'delete' in request.params:
                if table:
                    for t in table:
                        DBSession.delete(t)
                if playOff:
                    for p in playOff:
                        DBSession.delete(p)
                if race:
                    for r in race:
                        DBSession.delete(r)
                if group:
                    for g in group:
                        DBSession.delete(g)
                if games:
                    for g in games:
                        DBSession.delete(g)
                DBSession.delete(name)

                return HTTPFound(location="/my_tournaments")
            if 'save' in request.params:
                if table:
                    table.sort(key=lambda x: x.score, reverse=True)
                    player1 = DBSession.query(Table).filter_by(event=name,name=request.params['player1']).first()
                    if not player1:
                        return {"message": "Первой команды не существует",
                                "event": name,
                                'table':table,
                                'games':games,
                                'root':root}
                    player2 = DBSession.query(Table).filter_by(event=name,name=request.params['player2']).first()
                    if not player2:
                        return {"message": "Второй команды не существует",
                                "event": name,
                                'table': table,
                                'games': games,
                                'root': root}
                    if player1 == player2:
                        return {"message": "Одна и таже команда по обе стороны",
                                "event": name,
                                'table': table,
                                'games': games,
                                'root': root}
                    score1 = request.params['score1']
                    if not score1.isdigit():
                        return {"message": "Неверно введены голы первой команды",
                                "event": name,
                                'table': table,
                                'games': games,
                                'root': root}
                    score2 = request.params['score2']
                    if not score2.isdigit():
                        return {"message": "Неверно введены голы второй команды",
                                "event": name,
                                'table': table,
                                'games': games,
                                'root': root}
                    score1 = int(score1)
                    score2 = int(score2)
                    game = Game(event=name, date=date, playerOne=player1.name, playerTwo=player2.name,
                                playerOneScore=score1,
                                playerTwoScore=score2)
                    DBSession.add(game)
                    player1.games += 1
                    player2.games += 1
                    player1.goalsScored += score1
                    player1.goalsAgainst += score2
                    player2.goalsScored += score2
                    player2.goalsAgainst += score1
                    if (score1 > score2):
                        player1.score += name.scoreWin
                        player2.score += name.scoreLose
                        player1.wins += 1
                        player2.lose += 1
                    elif (score1 == score2):
                        player1.score += name.scoreDraw
                        player2.score += name.scoreDraw
                        player1.draws += 1
                        player2.draws += 1
                    else:
                        player2.score += name.scoreWin
                        player1.score += name.scoreLose
                        player2.wins += 1
                        player1.lose += 1
                    table.sort(key=lambda x: x.score,reverse=True)
                    i=0
                    while(i<len(table)):
                        table[i].position = i+1
                        i+=1
                    return HTTPFound(location="/tournament/" + str(name.id))
                if group:
                    groupList = []
                    group = name.groupNumber
                    nameGroup = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]

                    player1 = DBSession.query(GroupTable).filter_by(event=name,name=request.params['player1']).first()
                    if not player1:
                        return {"message": "Первой команды не существует",
                                "event": name,
                                "groupList":groupList,
                                'games': games,
                                'root': root}
                    player2 = DBSession.query(GroupTable).filter_by(event=name,name=request.params['player2']).first()
                    if not player2:
                        return {"message": "Второй команды не существует",
                                "event": name,
                                "groupList": groupList,
                                'games': games,
                                'root': root}
                    if player1 == player2:
                        return {"message": "Одна и таже команда по обе стороны",
                                "event": name,
                                'table': table,
                                'games': games,
                                'root': root}
                    if player1.nameGroup != player2.nameGroup:
                        return{"message": "Команды из разных групп",
                                "event": name,
                                "groupList": groupList,
                                'games': games,
                                'root': root}
                    score1 = request.params['score1']
                    if not score1.isdigit():
                        return {"message": "Неверно введены голы первой команды",
                                "event": name,
                                "groupList": groupList,
                                'games': games,
                                'root': root}
                    score2 = request.params['score2']
                    if not score2.isdigit():
                        return {"message": "Неверно введены голы второй команды",
                                "event": name,
                                "groupList": groupList,
                                'games': games,
                                'root': root}
                    score1 = int(score1)
                    score2=int(score2)
                    game = Game(event=name, date=date, playerOne=player1.name, playerTwo=player2.name,
                                playerOneScore=score1,
                                playerTwoScore=score2)
                    DBSession.add(game)
                    player1.games += 1
                    player2.games += 1
                    player1.goalsScored += score1
                    player1.goalsAgainst += score2
                    player2.goalsScored += score2
                    player2.goalsAgainst += score1
                    if (score1 > score2):
                        player1.score += name.scoreWin
                        player2.score += name.scoreLose
                        player1.wins += 1
                        player2.lose += 1
                    elif (score1 == score2):
                        player1.score += name.scoreDraw
                        player2.score += name.scoreDraw
                        player1.draws += 1
                        player2.draws += 1
                    else:
                        player2.score += name.scoreWin
                        player1.score += name.scoreLose
                        player2.wins += 1
                        player1.lose += 1

                    i = 0
                    while (i < group):
                        table = DBSession.query(GroupTable).filter_by(event=name, nameGroup=nameGroup[i]).all()
                        table.sort(key=lambda x: x.score, reverse=True)
                        j = 0
                        while (j < len(table)):
                            table[j].position = j + 1
                            j += 1
                        groupList.append(table)
                        i += 1
                    return HTTPFound(location="/tournament/" + str(name.id))
                if race:
                    player = DBSession.query(RaceTable).filter_by(event=name,name=request.params['player']).first()
                    if not player:
                        return {"message": "Нет такого участника",
                                "event": name,
                                'race': race,
                                'root': root}
                    time = request.params['time']
                    if not time:
                        return{"message": "Введите время участника",
                               "event": name,
                               'race': race,
                                'root': root}
                    result = re.findall(r'\d{2}:\d{2}:\d{2}.\d{2,10}',time)
                    if not result:
                        result = re.findall(r'\d{2}:\d{2}.\d{2,10}',time)
                    if not result:
                        result = re.findall(r'\d{2}.\d{2,10}',time)
                    if not result:
                        return{"message": "Неверный формат время (нужно ввести ч:м:с.мс или м:с.мс или с.мс)",
                               "event": name,
                               'race': race,
                                'root': root}
                    player.score = time
                    race.sort(key=lambda x: x.score)
                    i=0
                    while (i < len(race)):
                        race[i].position = i + 1
                        i += 1
                    return HTTPFound(location="/tournament/" + str(name.id))
                if playOff:
                    playOffList = []
                    stage = [64, 32, 16, 8, 4, 2, 1]
                    i = 0
                    while (i < len(stage)):
                        table = DBSession.query(PlayOff).filter_by(event=name, stage=stage[i]).all()
                        playOffList.append(table)
                        i += 1
                    match = DBSession.query(PlayOff).filter_by(event=name,playerOne=request.params['player1'],playerTwo=request.params['player2']).first()
                    if not match:
                        return {"message": "Нет такого матча",
                                "event": name,
                                'tableP': playOffList,
                                'root': root}
                    if request.params['player1'] == request.params['player2']:
                        return {"message": "Одна и таже команда по обе стороны",
                                "event": name,
                                'table': table,
                                'games': games,
                                'root': root}
                    score1 = request.params['score1']
                    if not score1.isdigit():
                        return {"message": "Неверно введены голы первой команды",
                                "event": name,
                                'tableP': playOffList,
                                'root': root}
                    score2 = request.params['score2']
                    if not score2.isdigit():
                        return {"message": "Неверно введены голы второй команды",
                                "event": name,
                                'tableP': playOffList,
                                'root': root}
                    score1 = int(score1)
                    score2 = int(score2)
                    if(score1==score2):
                        return {"message": "Не может быть ничьи",
                                "event": name,
                                'tableP': playOffList,
                                'root': root}
                    match.date = date
                    match.playerOneScore = score1
                    match.playerTwoScore = score2
                    if (score1 > score2):
                        model1 = DBSession.query(PlayOff).filter_by(event=name,playerOne="",playerTwo="",stage=match.stage/2).first()
                        model2 = DBSession.query(PlayOff).filter(PlayOff.event==name,PlayOff.playerOne != "",PlayOff.playerTwo == "",PlayOff.stage == match.stage/2).first()
                        if model2:
                            model2.playerTwo = request.params['player1']
                        else:
                            model1.playerOne = request.params['player1']
                    if (score1 < score2):
                        model1 = DBSession.query(PlayOff).filter_by(event=name, playerOne="", playerTwo="",
                                                                    stage=match.stage / 2).first()
                        model2 = DBSession.query(PlayOff).filter(PlayOff.event == name, PlayOff.playerOne != "",
                                                                 PlayOff.playerTwo == "",
                                                                 PlayOff.stage == match.stage / 2).first()
                        if model2:
                            model2.playerTwo = request.params['player2']
                        else:
                            model1.playerOne = request.params['player2']

                    return HTTPFound(location="/tournament/" + str(name.id))
            if 'settings' in request.params:
                if not type:
                    if name.weight != "":
                        listWeight = name.weight.split(',')

                        return{
                            'event': name,
                            'weight': listWeight,
                            'root': root,
                            'favorites': favorites
                        }
                    return HTTPFound(location="/tournament/" + str(name.id))

        if table:
            if not root and 'favorites' in request.params:
                if favorites:
                    DBSession.delete(model)
                    favorites = False
                    return {'event': name,
                            'table': table,
                            'games': games,
                            'root':root,
                            'favorites':favorites}
                else:
                    model = Favorites(event=name, user=user)
                    DBSession.add(model)
                    favorites = True
                    return {'event': name,
                            'table': table,
                            'games': games,
                            'root': root,
                            'favorites': favorites}
            table.sort(key=lambda x: x.score, reverse=True)
            return {'event': name,
                    'table': table,
                    'games': games,
                    'root':root,
                    'favorites':favorites}
        if playOff:
            playOffList = []
            stage = [64,32,16,8,4,2,1]
            i = 0
            while(i<len(stage)):
                table = DBSession.query(PlayOff).filter_by(event=name,stage=stage[i]).all()
                playOffList.append(table)
                i+=1

            if not root and 'favorites' in request.params:
                if favorites:
                    DBSession.delete(model)
                    favorites = False
                    return {'event': name,
                            'tableP': playOffList,
                            'games': games,
                            'root': root,
                            'favorites': favorites}
                else:
                    model = Favorites(event=name, user=user)
                    DBSession.add(model)
                    favorites = True
                    return {'event': name,
                            'tableP': playOffList,
                            'games': games,
                            'root': root,
                            'favorites': favorites}
            return {'event': name,
                    'tableP': playOffList,
                    'games':games,
                    'root':root,
                    'favorites':favorites}
        if race:
            if not root and 'favorites' in request.params:
                if favorites:
                    DBSession.delete(model)
                    favorites = False
                    return {'event': name,
                            'root': root,
                            'race': race,
                            'favorites': favorites}
                else:
                    model = Favorites(event=name, user=user)
                    DBSession.add(model)
                    favorites = True
                    return {'event': name,
                            'race': race,
                            'root': root,
                            'favorites': favorites}
            race.sort(key=lambda x: x.score)
            return{'event':name,
                   'race':race,
                   'root':root,
                   'favorites':favorites}

        groupList = []
        group = name.groupNumber
        nameGroup = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
        i = 0
        while(i < group):
            table = DBSession.query(GroupTable).filter_by(event = name,nameGroup = nameGroup[i]).all()
            table.sort(key=lambda x: x.score, reverse=True)
            groupList.append(table)
            i+=1
        if not root and 'favorites' in request.params and user:
            if favorites:
                DBSession.delete(model)
                favorites = False
                return {'event': name,
                        'groupList': groupList,
                        'games': games,
                        'root': root,
                        'favorites': favorites}
            else:
                model = Favorites(event=name, user=user)
                DBSession.add(model)
                favorites = True
                return {'event': name,
                        'groupList': groupList,
                        'games': games,
                        'root': root,
                        'favorites': favorites}
        return{ 'event': name,
                'groupList': groupList,
                'games':games,
                'root':root,
                'favorites':favorites}
    else:
        return HTTPNotFound()

@view_config(route_name='apiFavorites', renderer='myjson')
def ft_view(request):
    user = DBSession.query(User).filter_by(login=request.authenticated_userid).first()
    events = DBSession.query(Favorites).filter_by(user=user).all()
    list = []
    for event in events:
        list.append(event.eventId)
    return {"events":list}

@view_config(route_name='apiType', renderer='myjson')
def type_view(request):
    list = []
    types = DBSession.query(TypeTournament).filter_by().all()
    for type in types:
        list.append({type.id:type.name})
    return {"types":list}
'''@view_config(route_name='favorites', renderer='templates/favorites.jinja2')
def ft_view(request):
    listContent = []
    if 'sub' in request.params:
        message = ""
        stringKind = ""
        kindList = ['badminton', 'basketball', 'run', 'ski', 'cycle_racing', 'volleyball', 'handball', 'rowing',
                    'fighting', 'skating', 'tennis',
                    'table_tennis', 'swimming', 'rugby', 'football', 'hockey', 'snowboard', 'other']
        for kind in kindList:
            if kind in request.params:
                sport = DBSession.query(KindOfSport).filter_by(name=request.params[kind]).first()
                stringKind += request.params[kind] + ", "
                events = DBSession.query(Event).filter_by(kind=sport)
                for event in events:
                    list = fillList(event)
                    listContent.append(list)
        name = request.params['nameFilter']
        city = request.params['cityFilter']
        date = request.params['dateFilter']
        if name and city and date:
            events = DBSession.query(Event).filter_by(date=date, city=city, name=name).all()
            for event in events:
                list = fillList(event)
                listContent.append(list)
            message = "Результат по поиску: название мероприятия - " + name + ", дата начала мероприятия - " + date + \
                      ", город проведения мероприятия - " + city
            if stringKind != "":
                message += ", виды спорта - " + stringKind[0:len(stringKind) - 2]
            return {"message": message,
                    "listContent": listContent}
        if name and date:
            events = DBSession.query(Event).filter_by(date=date, name=name).all()
            for event in events:
                list = fillList(event)
                listContent.append(list)
            message = "Результат по поиску: название мероприятия - " + name + ", дата начала мероприятия - " + date
            if stringKind != "":
                message += ", виды спорта - " + stringKind[0:len(stringKind) - 2]
            return {
                "message": message,
                "listContent": listContent}
        if name and city:
            events = DBSession.query(Event).filter_by(city=city, name=name).all()
            for event in events:
                list = fillList(event)
                listContent.append(list)
            message = "Результат по поиску: название мероприятия - " + name + ", город проведения мероприятия - " + city
            if stringKind != "":
                message += ", виды спорта - " + stringKind[0:len(stringKind) - 2]
            return {
                "message": message,
                "listContent": listContent}
        if date and city:
            events = DBSession.query(Event).filter_by(city=city, date=date).all()
            for event in events:
                list = fillList(event)
                listContent.append(list)
            message = "Результат по поиску: дата начала мероприятия - " + date + ", город проведения мероприятия - " + city
            if stringKind != "":
                message += ", виды спорта - " + stringKind[0:len(stringKind) - 2]

            return {
                "message": message,
                "listContent": listContent}
        if name:
            events = DBSession.query(Event).filter_by(name=name).all()
            for event in events:
                list = fillList(event)
                listContent.append(list)
            message = "Результат по поиску: название мероприятия - " + name
            if stringKind != "":
                message += ", виды спорта - " + stringKind[0:len(stringKind) - 2]
            return {
                "message": message,
                "listContent": listContent}
        if date:
            events = DBSession.query(Event).filter_by(date=date).all()
            for event in events:
                list = fillList(event)
                listContent.append(list)
            message = "Результат по поиску: дата начала мероприятия - " + date
            if stringKind != "":
                message += ", виды спорта - " + stringKind[0:len(stringKind) - 2]
            return {
                "message": message,
                "listContent": listContent}
        if city:
            events = DBSession.query(Event).filter_by(city=city).all()
            for event in events:
                list = fillList(event)
                listContent.append(list)
                message = "Результат по поиску: город проведения мероприятия - " + city
                if stringKind != "":
                    message += ", виды спорта - " + stringKind[0:len(stringKind) - 2]
            return {
                "message": message,
                "listContent": listContent}
        if stringKind != "":
            message += "Результат по поиску: виды спорта - " + stringKind[0:len(stringKind) - 2]
        return {"message": message,
                "listContent": listContent}

    events = []
    user = DBSession.query(User).filter_by(login=request.authenticated_userid).first()
    favorites = DBSession.query(Favorites).filter_by(user=user).all()
    for e in favorites:
        event = DBSession.query(Event).filter_by(id=e.eventId).first()
        events.append(event)

    for event in events:
        list = fullFillList(event)
        listContent.append(list)
    return {"listContent": listContent}'''

