## Python x-wing-builder (pyxwb)
Build X-Wing lists using XWS format

X-Wing library to import, clean and export an X-Wing list for use in some other application. The X-Wing data being used is from [https://github.com/guidokessels/xwing-data](xwing-data). As of now I'm not creating this as an installable module with pip... for now.

## Classes
### **xwb**
xwb.**_xwb_**(schema_source = None, vendor_key = None, \*\*vendor_kwargs)

(optionalish) schema_source is a file path or url to a json schema to check if the importing XWS data is compliant. By default I'm using the "official" schema from xws-spec that is in "xws_schema.json" which ships with this library. If this file is missing and no file or URL is specified then the app will fail.

(optional) vendor_key is a unique identifier for the developer using this library in their apps. Right now when importing the vendor info is completely dropped, but future iterations might ignore this and allow the vendor info to stay if it matches your key.

(optional) vendor_kwargs info is a kwargs dictionary passed in. Anything in this dictionary will be added to the main container's vendor info. If vendor_key is not specified then this is ignored.

xwb.xwb.**_import_xws_**(xws)
Pass in a a properly formatted XWS dictionary. The result is a returned tuple with cleaned up data following the xws-spec and a list of errors for any issues that may have been encountered.

xwb.xwb.**_xws_schema_**(schema_source = None)
If you need access to the imported schema outside of the library you can access it here. If you need to change the schema you can also set it. To set you need to pass in a new file or url source.

### **xwing_data**
xwing_data library gives you access to all the data files that ship with xwing_data. This has all information about every ship, card, dials, etc. Its also the source of all the images for those ships and cards if you want to include that in something.

xwing_data.**_xwing_data_**(data_files_path = None, schema_files_path = None)

data_files_path. By default this library ships with xwing-data. If for some reason you want host these files elsewhere you'll have to specify that.

schema_files_path. Currently not used right now.

xwing_data.xwing_data.**_conditions_**
Passes back all the condition cards

xwing_data.xwing_data.**_damage_deck_core_tfa_**
Passes back all the damage cards from The Force Awakens Core Set

xwing_data.xwing_data.**_damage_deck_core_**
Passes back all the damage cards from the Original Core Set

xwing_data.xwing_data.**_damage_deck_rebel_transport_**
Passes back all the damage cards from the Rebel Transport Expansion

xwing_data.xwing_data.**_pilots_**
Passes back all the pilot cards

xwing_data.xwing_data.**_reference_cards_**
Passes back all the reference cards

xwing_data.xwing_data.**_ships_**
Passes back all the ships

xwing_data.xwing_data.**_sources_**
Passes back all the Expansions and what came in them

xwing_data.xwing_data.**_upgrades_**
Passes back all the upgrade cards

xwing_data.xwing_data.**_to_xws_slot_name_**
Passes back a dictionary that consists of the xwing_data:xws naming nomcalture for upgrade slots. (e.g. xwing_data upgrade slot called Astromech is named amd in XWS format)

xwing_data.xwing_data.**_from_xws_slot_name_**
Same as above but in reverse.

## Installation
```
git clone git@github.com:minsis/x-wing-builder.git
cd x-wing-builder
pip install -r requirements.txt

```


## Examples
Included in the library is a sample list with errors in it. You can also run test.py to run some the test.

```
import json

#Sample

from xwb import xwb, xwing_data

vendor_info = {"url" : "https://somewhere.com", "list_url" : "https://somewhere.com/thislist"}
xwing_list = xwb.xwb(vendor_key = "pyxwb", **vendor_info)

results = xwing_list.import_xws(json.loads(open("sample-list.json").read()))

print(json.dumps(results[0], indent = 2, separators=(',', ':')))

for error in results[1]:
    print(error)
```

Results:
```
{
  "name":"2 A-Wings, 2 X-Wings",
  "faction":"rebel",
  "version":"1.0.0",
  "description":"Tycho leads a flight",
  "obstacles":[
    "core-asteroid-5",
    "vt49decimator-debris-2",
    "yt2400-debris-0"
  ],
  "pilots":[
    {
      "name":"tychocelchu",
      "ship":"awing",
      "upgrades":{
        "title":[
          "awingtestpilot"
        ],
        "missile":[
          "chardaanrefit"
        ],
        "ept":[
          "pushthelimit",
          "experthandling"
        ],
        "mod":[
          "experimentalinterface"
        ]
      },
      "vendor":{
        "pyxwb":{
          "xwing_data_pilot_id":29
        }
      },
      "points":32
    },
    {
      "name":"rookiepilot",
      "ship":"xwing",
      "upgrades":{
        "amd":[
          "r2astromech"
        ]
      },
      "vendor":{
        "pyxwb":{
          "xwing_data_pilot_id":3
        }
      },
      "points":22
    },
    {
      "name":"rookiepilot",
      "ship":"xwing",
      "upgrades":{
        "amd":[
          "r2astromech"
        ]
      },
      "vendor":{
        "pyxwb":{
          "xwing_data_pilot_id":3
        }
      },
      "points":22
    },
    {
      "name":"greensquadronpilot",
      "ship":"awing",
      "upgrades":{
        "title":[
          "awingtestpilot"
        ],
        "missile":[
          "chardaanrefit"
        ],
        "ept":[
          "experthandling"
        ],
        "mod":[
          "stealthdevice"
        ]
      },
      "vendor":{
        "pyxwb":{
          "xwing_data_pilot_id":31
        }
      },
      "points":20
    },
    {
      "name":"bluesquadronpilot",
      "ship":"xwing",
      "upgrades":{
        "ept":[
          "elusiveness",
          "experthandling"
        ],
        "mod":[
          "stealthdevice"
        ],
        "amd":[],
        "crew":[
          "r2d2-swx22"
        ]
      },
      "vendor":{
        "pyxwb":{
          "xwing_data_pilot_id":44
        }
      },
      "points":33
    }
  ],
  "vendor":{
    "pyxwb":{
      "url":"https://somewhere.com",
      "list_url":"https://somewhere.com/thislist"
    }
  }
}
XWS data version 0.3.0 is older than 1.0.0
Removing unknown Upgrade Card "Elite:unknownupgrade" for pilot "greensquadronpilot"
Removed r2d2 collision in Astromech Upgrade for "bluesquadronpilot".
Corrected r2d2 in Crew Upgrade for "bluesquadronpilot".
Removing unknown slot type "wrongupgrade" for Pilot "bluesquadronpilot"
Removing unknown pilot "unknownpilot"
```
