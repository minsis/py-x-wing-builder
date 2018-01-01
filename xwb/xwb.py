# -*- coding: utf-8 -*-
"""
xwb.py - X-Wing Builder. Build X-Wing lists using XWS format and export them
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

import json
from jsonschema import validate
from os.path import exists, realpath, join
import urllib.request
from .xwing_data import xwing_data

class xwb(object):

    def __init__(self, schema_source = None, vendor_key = None, **vendor_kwargs):

        self.xws_schema = schema_source
        self.xws_version = "1.0.0"
        self.xws_vendor = ""
        self.vendor_key = vendor_key
        self.vendor_kw = vendor_kwargs

    def import_xws(self, xws):
        """Import XWS formatted data as json and return properly formatted XWS JSON with all rules applied"""

        if type(xws) != dict:
            raise ValueError("XWS data is not of the correct type. Type: {}".format(type(xws)))

        # This is purely an import, check and cleasing of data. If points, vendor data, etc needs to be applied the export feature is needed here. This allows for a complete break down and cleansing of the data to conform to the XWS spec. This also allows for custom vendor specific information to be applied to the export.

        container_ignored_props = ["points", "vendor"]
        pilots_ignored_props = ["points", "vendor"]
        errors = list()

        xwing_data_conditions = xwing_data().conditions
        xwing_data_pilots = xwing_data().pilots
        xwing_data_ships = xwing_data().ships
        xwing_data_upgrades = xwing_data().upgrades

        conditions = list()
        for condition in xwing_data_conditions:
            conditions.append(condition["xws"])

        pilots = list()
        for pilot in xwing_data_pilots:
            pilots.append(pilot["xws"])

        ships = list()
        for ship in xwing_data_ships:
            ships.append(ship["xws"])

        upgrades = list()
        for upgrade in xwing_data_upgrades:
            upgrades.append(upgrade["xws"])

        upgrade_slots = list()
        for slot in xwing_data().to_xws_slot_name.items():
            upgrade_slots.append(slot[1])

        # validating the schmea
        validate(xws, self.xws_schema)

        if xws["version"] < "0.3.0":
            errors.append("Warning: XWS data version {} is older than 0.3.0. I cannot guarantee accuracy".format(xws["version"], self.xws_version))
        elif xws["version"] < self.xws_version:
            errors.append("XWS data version {} is older than {}".format(xws["version"], self.xws_version))

        elif xws["version"] > self.xws_version:
            errors.append("XWS data version {} is newer than {}.".format(xws["version"], self.xws_version))

        xws["version"] = self.xws_version

        # Remove any ignored items in the main squadron container.
        for prop in container_ignored_props:
            if prop in xws:

                # if you're the vendor keep the data.
                #if self.vendor_key and (self.vendor_key in str(xws[prop])):
                #    continue

                xws.pop(prop)

        # lets check to make sure we have valid pilots and ships
        for pilot in range(len(xws["pilots"])):

            if xws["pilots"][pilot]["name"] not in pilots:
                errors.append("Removing unknown pilot \"{}\"".format(xws["pilots"][pilot]["name"]))
                xws["pilots"].pop(pilot)
                continue

            if xws["pilots"][pilot]["ship"] not in ships:
                errors.append("Unknown ship removing pilot \"{}\"".format(xws["pilots"][pilot]["name"]))
                xws["pilots"].pop(pilot)
                continue

            # Remove any ignored items in the pilots container.
            for prop in pilots_ignored_props:
                if prop in xws["pilots"][pilot]:

                    # if you're the vendor keep the data.
                    #if self.vendor_key and (self.vendor_key in str(xws["pilots"][pilot][prop])):
                    #    continue

                    xws["pilots"][pilot].pop(prop)

            # clearing collision issues for r2d2 (prior to 0.3.0)
            if "amd" in xws["pilots"][pilot]["upgrades"]:
                if xws["pilots"][pilot]["upgrades"]["amd"].count("r2d2") > 1:
                    for i in range(xws["pilots"][pilot]["upgrades"]["amd"].count("r2d2")):

                        xws["pilots"][pilot]["upgrades"]["amd"].remove("r2d2")
                    errors.append("Removed r2d2 collision in Astromech Upgrade for \"{}\".".format(xws["pilots"][pilot]["name"]))

            # making sure we're not seeing old data prior to xws 0.30.0
            if "crew" in xws["pilots"][pilot]["upgrades"]:
                if "r2d2" in xws["pilots"][pilot]["upgrades"]["crew"]:

                    xws["pilots"][pilot]["upgrades"]["crew"].remove("r2d2")
                    xws["pilots"][pilot]["upgrades"]["crew"].append("r2d2-swx22")
                    errors.append("Corrected r2d2 in Crew Upgrade for \"{}\".".format(xws["pilots"][pilot]["name"]))

            # remove the slot if we dont know what it is
            for slot in list(xws["pilots"][pilot]["upgrades"].keys()):
                if slot not in upgrade_slots:

                    errors.append("Removing unknown slot type \"{}\" for Pilot \"{}\"".format(slot, xws["pilots"][pilot]["name"]))
                    xws["pilots"][pilot]["upgrades"].pop(slot)

            # add in the pilots xwing-data id
            if self.vendor_key and "vendor" not in xws["pilots"][pilot]:
                xws["pilots"][pilot]["vendor"] = { self.vendor_key : { "xwing_data_pilot_id" : xwing_data_pilots[pilots.index(xws["pilots"][pilot]["name"])]["id"] }}

            #add in total points value for each pilot and remove any unknown upgrade cards
            total_points = 0
            if "upgrades" in xws["pilots"][pilot]:
                for k, v in xws["pilots"][pilot]["upgrades"].items():
                    for upgrade in v:
                        if upgrade not in upgrades:

                            xws["pilots"][pilot]["upgrades"][k].remove(upgrade)
                            errors.append("Removing unknown Upgrade Card \"{}:{}\" for pilot \"{}\"".format(xwing_data().from_xws_slot_name[k],upgrade, xws["pilots"][pilot]["name"]))
                            continue

                        total_points += xwing_data_upgrades[upgrades.index(upgrade)]["points"]

            xws["pilots"][pilot]["points"] = xwing_data_pilots[pilots.index(xws["pilots"][pilot]["name"])]["points"] + total_points

        if self.vendor_key and ("vendor" not in xws) and (len(self.vendor_kw) != 0):
            xws["vendor"] = { self.vendor_key : {} }
            xws["vendor"][self.vendor_key].update(self.vendor_kw)
            #for k, v in self.vendor_kw:
            #    xws["vendor"][self.vendor_key][k] = v

        return((xws, errors))

    @property
    def xws_schema(self):
        return(self._xws_schema)

    @xws_schema.setter
    def xws_schema(self, schema_source):
        """Load the schema from either the URL or File provided. Default will be the file that ships with this."""

        #Offical schema for XWS: https://raw.githubusercontent.com/elistevens/xws-spec/master/schema.json

        def is_url(url):
            "Check to see if the URL actually exists"

            try:
                request = urllib.request.Request(url)
                request.get_method = lambda: 'HEAD'
                urllib.request.urlopen(request)
                return True
            except:
                return False

        # grab default schema file one wasn't passed in
        if not schema_source:
            schema_source = join(realpath(__file__).rsplit("/", 1)[0], "xws_schema.json")

        # see if the source a file, if not check to see if its a URL
        if exists(schema_source):
            try:
                schema = json.loads(open(schema_source, "r").read())
            except:
                raise ValueError("Unable to load schema from file {}".format(schema_source))

        elif is_url(schema_source):
            try:
                schema_site = json.loads(urllib.request.urlopen(schema_source))

                if schema_site.getcode() == 200:
                    schema = schema_site.read().decode("utf-8")

            except:
                raise ValueError("Unable to load schema from URL {}".format(schema_source))

        else:
            raise ValueError("Unable to determine the schema source {}".format(schema_source))

        self._xws_schema = schema
