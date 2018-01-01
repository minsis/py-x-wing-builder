# -*- coding: utf-8 -*-
"""
xwing-data.py - Library for dealing with xwing-data source
Author: Dennis Whitney
Handle: minsis
Email: dwhitney@irunasroot.com
Version: 0.1.0
Copyright 2017, Dennis Whitney <dwhitney@irunasroot.com>
Licensed under GNU GENERAL PUBLIC LICENSE Version 3 (GNU v3)

xws-spec: v1.0.0
xwing-data: v0.59.0

https://github.com/elistevens/xws-spec
https://github.com/guidokessels/xwing-data
"""

from jsonschema import validate
from os.path import join, realpath
import json


class xwing_data:

    def __init__(self, data_files_path = None, schema_files_path = None):
        # Load up all the data from xwing-data files. Should you want to provide your own data... say from a database, you can then pass all that data as valid dictionaries that match the schema's

        if not data_files_path:
            data_files_path = join(realpath(__file__).rsplit("/", 1)[0], "xwing-data", "data")

        if not schema_files_path:
            schema_files_path = join(realpath(__file__).rsplit("/", 1)[0], "xwing-data", "schemas")

        self.conditions = json.loads(open(join(data_files_path, "conditions.js")).read())
        self.damage_deck_core_tfa = json.loads(open(join(data_files_path, "damage-deck-core-tfa.js")).read())
        self.damage_deck_core = json.loads(open(join(data_files_path, "damage-deck-core.js")).read())
        self.damage_deck_rebel_transport = json.loads(open(join(data_files_path, "damage-deck-rebel-transport.js")).read())
        self.pilots = json.loads(open(join(data_files_path, "pilots.js")).read())
        self.reference_cards = json.loads(open(join(data_files_path, "conditions.js")).read())
        self.ships = json.loads(open(join(data_files_path, "ships.js")).read())
        self.sources = json.loads(open(join(data_files_path, "sources.js")).read())
        self.upgrades = json.loads(open(join(data_files_path, "upgrades.js")).read())

        self.to_xws_slot_name = { "Astromech" : "amd",  "Bomb" : "bomb", "Cannon" : "cannon", "Cargo" : "cargo", "Crew" : "crew",
                               "Elite" : "ept", "Hardpoint" : "hardpoint", "Illicit" : "illicit", "Missile" : "missile", "Modification" : "mod",
                               "Salvaged Astromech" : "samd", "System" : "system", "Team" : "team", "Tech" : "tech", "Title" : "title",
                               "Torpedo" : "torpedo", "Turret" : "turret" }

        self.from_xws_slot_name = dict()
        for k, v in self.to_xws_slot_name.items():
            self.from_xws_slot_name.update({v : k})

    @property
    def conditions(self):
        return(self._conditions)

    @conditions.setter
    def conditions(self, conditions):
        self._conditions = conditions

    @property
    def damage_deck_core_tfa(self):
        return(self._damage_deck_core_tfa)

    @damage_deck_core_tfa.setter
    def damage_deck_core_tfa(self, damage_deck_core_tfa):
        self._damage_deck_core_tfa = damage_deck_core_tfa

    @property
    def damage_deck_core(self):
        return(self._damage_deck_core)

    @damage_deck_core.setter
    def damage_deck_core(self, damage_deck_core):
        self._damage_deck_core = damage_deck_core

    @property
    def damage_deck_rebel_transport(self):
        return(self._damage_deck_rebel_transport)

    @damage_deck_rebel_transport.setter
    def damage_deck_rebel_transport(self, damage_deck_rebel_transport):
        self._damage_deck_rebel_transport = damage_deck_rebel_transport

    @property
    def pilots(self):
        return(self._pilots)

    @pilots.setter
    def pilots(self, pilots):
        self._pilots = pilots

    @property
    def reference_cards(self):
        return(self._reference_cards)

    @reference_cards.setter
    def reference_cards(self, reference_cards):
        self._reference_cards = reference_cards

    @property
    def ships(self):
        return(self._ships)

    @ships.setter
    def ships(self, ships):
        self._ships = ships

    @property
    def sources(self):
        return(self._sources)

    @sources.setter
    def sources(self, sources):
        self._sources = sources

    @property
    def upgrades(self):
        return(self._upgrades)

    @upgrades.setter
    def upgrades(self, upgrades):
        self._upgrades = upgrades
