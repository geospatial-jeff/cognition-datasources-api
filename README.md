# cognition-datasources-api

STAC compliant dynamic API for searching geospatial assets, powered by [cognition-datasources](https://github.com/geospatial-jeff/cognition-datasources).  Deployed with Flask and AWS Elasticbeanstalk.

Currently hosted at `http://cognition-datasources.wekg62sdma.us-east-1.elasticbeanstalk.com`

Supports the following datasets (more information [https://github.com/geospatial-jeff/cognition-datasources]):
- Digital Globe Open Data Program
- ElevationTiles
- CBERS
- Landsat8
- Microsoft Building Footprints
- NAIP
- Sentinel1
- Sentinel2
- SRTM
- USGS 3DEP

## Endpoints
- POST /stac/search - full STAC query

## Parameters
- **REQUIRED**: `datasources` and either `bbox` or `intersects`.

| Parameter | Type | Example |
|-------------|--------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| datasources | list | ["Landsat8", "NAIP", "Sentinel2"] |
| bbox | list | [-118, 34, -119, 35] |
| intersects | [GeoJSON Polygon](https://tools.ietf.org/html/rfc7946#section-3.1) | {"type": "Polygon", "coordinates": [[[-87.5390625, 32.84267363195431], [-81.9140625, 32.84267363195431], [-81.9140625, 37.43997405227057], [-87.5390625, 37.43997405227057], [-87.5390625, 32.84267363195431]]]} |
| time | str | "2018-02-12T00:00:00Z/2018-03-18T12:31:12Z" |
| properties | dict | {'eo:epsg': {'eq': 4326}, 'eo:gsd': {'lt': 30.0}} |
| limit | int | 20 |

## Example
```python
import requests
import json

endpoint = "http://cognition-datasources.wekg62sdma.us-east-1.elasticbeanstalk.com/stac/search"

geoj =  {"type": "Polygon", "coordinates": [[[-87.5390625, 32.84267363195431], [-81.9140625, 32.84267363195431], [-81.9140625, 37.43997405227057], [-87.5390625, 37.43997405227057], [-87.5390625, 32.84267363195431]]]}


payload = {"intersects": geoj,
           "datasources": ["Landsat8", "Sentinel2"]
           }


r = requests.post(endpoint, data=json.dumps(payload))
print(r.json())
```

#### Response
API response is a dictionary of feature collections, each containing a unique STAC Item for each asset returned by the query.  The above example will print:

```json
{
  "Landsat8": {
    "type": "FeatureCollection",
    "features": [STACItem, STACItem, STACItem]
  },
  "Sentinel2": {
    "type": "FeatureCollection",
    "features": [STACItem, STACItem, STACItem]
  }
}
```

View examples of STACItems returned by each datasource [here](https://github.com/geospatial-jeff/cognition-datasources/tree/master/docs/examples).

## Documentation
View documentation for the underlying library [here](https://github.com/geospatial-jeff/cognition-datasources).


