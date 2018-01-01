# -*- coding: utf-8 -*-

import json

#Sample

from xwb import xwb, xwing_data

vendor_info = {"url" : "https://somewhere.com", "list_url" : "https://somewhere.com/thislist"}
xwing_list = xwb.xwb(vendor_key = "pyxwb", **vendor_info)

results = xwing_list.import_xws(json.loads(open("sample-list.json").read()))

print(json.dumps(results[0], indent = 2, separators=(',', ':')))

for error in results[1]:
    print(error)
