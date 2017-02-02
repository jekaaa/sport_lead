import os
import sys
import transaction
import http.client
import json

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import *

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def table(position,name,wins,draws,lose,goals):
    model = Table(position=position,name=name,games=wins+draws+lose,wins=wins,draws=draws,lose=lose,goals=goals,score=wins*3+draws)
    DBSession.add(model)

#заполнение KindOfSport
def KOS():
    armsport = KindOfSport(name = "Армспорт")
    badminton = KindOfSport(name = "Бадминтон")
    basketball = KindOfSport(name = "Баскетбол")
    run = KindOfSport(name = "Бег")
    ski = KindOfSport(name = "Лыжи")
    bicycling = KindOfSport(name = "Велоспорт")
    volleyball = KindOfSport(name = "Волейбол")
    handball = KindOfSport(name = "Гандбол")
    rowing = KindOfSport(name = "Гребля")
    fight = KindOfSport(name = "Единоборства")
    skating = KindOfSport(name = "Конькобежный спорт")
    tennis = KindOfSport(name = "Теннис")
    tableTennis = KindOfSport(name = "Настольный теннис")
    swimming = KindOfSport(name = "Плавание")
    snowboard = KindOfSport(name = "Сноуборд")
    football = KindOfSport(name = "Футбол")
    hockey = KindOfSport(name = "Хоккей")
    drugoe =KindOfSport(name = "Другое")
    DBSession.add_all([armsport,badminton,basketball,run,ski,bicycling,volleyball,handball,rowing,
                fight,skating,tennis,tableTennis,swimming,snowboard,football,hockey,drugoe])

#заполнение TypeTournament
def TT():
    rrt = TypeTournament(name = "Круговой турнир")
    gpt = TypeTournament(name = "Групповой турнир с плей-офф")
    gptr = TypeTournament(name = "Групповой турнир с плей-офф (случайное распределение)")
    pt = TypeTournament(name = "Плей-офф")
    ptr = TypeTournament(name ="Плей-офф (случайное распределение)")
    race = TypeTournament(name = "Гонка")

    DBSession.add_all([rrt,gpt,pt,gptr,ptr,race])

def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        KOS()
        TT()