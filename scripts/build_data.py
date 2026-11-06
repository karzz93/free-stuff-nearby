#!/usr/bin/env python3
"""
Turns an osmium GeoJSON-sequence export into small grid files the app can load.

  python3 scripts/build_data.py places.geojsonseq _site/data "europe/netherlands"
"""
import json, math, os, sys
from datetime import datetime, timezone

CELL = 0.05  # degrees; about 5.5 km north-south, 3.3 km east-west in the Netherlands

KEEP = {
  'name','amenity','man_made','emergency','drinking_water','fee','access','opening_hours',
  'wheelchair','changing_table','bottle','capacity','maxstay','parking','indoor',
  'defibrillator:location','internet_access','internet_access:fee','unisex','male','female',
  'check_date','survey:date','survey_date'
}

def wanted(t):
  a = t.get('amenity')
  if a in ('drinking_water','water_point','toilets','parking'): return True
  if t.get('man_made') == 'water_tap' and t.get('drinking_water') == 'yes': return True
  if t.get('emergency') == 'defibrillator': return True
  ia = t.get('internet_access','')
  if any(v in ia for v in ('wlan','yes','wifi')) and t.get('internet_access:fee') in ('no','customers'): return True
  return False

def flatten(coords):
  if isinstance(coords[0], (int, float)): yield coords; return
  for c in coords: yield from flatten(c)

def center(geom):
  pts = list(flatten(geom['coordinates']))
  if geom['type'] == 'Point': return pts[0][1], pts[0][0]
  xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
  return (min(ys)+max(ys))/2, (min(xs)+max(xs))/2

def main(src, out, areas):
  cells, seen, count = {}, set(), 0
  bbox = [90, 180, -90, -180]
  with open(src, encoding='utf-8') as f:
    for line in f:
      line = line.strip().lstrip('\x1e')
      if not line: continue
      feat = json.loads(line)
      p = feat.get('properties') or {}
      tags = {k: v for k, v in p.items() if not k.startswith('@')}
      if not wanted(tags) or not feat.get('geometry'): continue
      typ, oid = p.get('@type'), p.get('@id')
      if typ is None or oid is None: continue
      key = f'{typ}/{oid}'
      if key in seen: continue
      seen.add(key)
      lat, lon = center(feat['geometry'])
      ts = p.get('@timestamp')
      if isinstance(ts, (int, float)):
        ts = datetime.fromtimestamp(ts, timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
      row = [typ[0], oid, round(lat, 6), round(lon, 6), ts,
             {k: v for k, v in tags.items() if k in KEEP}]
      cid = f'{math.floor(lat/CELL)}_{math.floor(lon/CELL)}'
      cells.setdefault(cid, []).append(row)
      bbox = [min(bbox[0], lat), min(bbox[1], lon), max(bbox[2], lat), max(bbox[3], lon)]
      count += 1

  os.makedirs(os.path.join(out, 'cells'), exist_ok=True)
  for cid, rows in cells.items():
    with open(os.path.join(out, 'cells', cid + '.json'), 'w', encoding='utf-8') as f:
      json.dump(rows, f, ensure_ascii=False, separators=(',', ':'))
  manifest = {
    'version': 1, 'cell': CELL, 'built': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'areas': areas, 'bbox': [round(v, 4) for v in bbox] if count else None,
    'cells': sorted(cells), 'places': count
  }
  with open(os.path.join(out, 'manifest.json'), 'w', encoding='utf-8') as f:
    json.dump(manifest, f, separators=(',', ':'))
  print(f'{count} places in {len(cells)} cells, written to {out}')

if __name__ == '__main__':
  if len(sys.argv) < 3: sys.exit(__doc__)
  main(sys.argv[1], sys.argv[2], [a for a in (sys.argv[3] if len(sys.argv) > 3 else '').split(',') if a])
