#!/usr/bin/env python3
"""Fetch official Zaber specs for one exact base part.

Usage:
  python fetch_zaber_specs.py X-LSQ X-LSQ150A
"""
import json
import sys
import urllib.parse
import urllib.request

if len(sys.argv) != 3:
    raise SystemExit("usage: fetch_zaber_specs.py <series> <base-part>")
series, part = sys.argv[1:]
url = "https://www.zaber.com/api/my-series/url/" + urllib.parse.quote(series)
with urllib.request.urlopen(url, timeout=30) as response:
    payload = json.load(response)
match = next((x for x in payload.get("base_parts", []) if x.get("base_part") == part), None)
if match is None:
    raise SystemExit(f"base part not found: {part}")
specs = {}
for item in match.get("base_part_specs", []):
    definition = item.get("definition", {})
    name = definition.get("spec")
    if name:
        specs[name] = {
            "raw_value": item.get("value"),
            "formatted_value": item.get("formatted", {}).get("formatted_value"),
            "unit": definition.get("unit"),
            "description": definition.get("description"),
        }
print(json.dumps({
    "source_url": url,
    "series_datasheet_url": "https://www.zaber.com" + payload.get("datasheet_url", ""),
    "part_datasheet_url": "https://www.zaber.com" + match.get("datasheet_url", ""),
    "series": series,
    "base_part": part,
    "description": match.get("description"),
    "specifications": specs,
}, indent=2))
