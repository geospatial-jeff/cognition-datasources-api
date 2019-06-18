# cognition-datasources-api

STAC compliant dynamic API for searching geospatial assets, powered by [cognition-datasources](https://github.com/geospatial-jeff/cognition-datasources).

Currently hosted at **`https://uh2bdjpxkl.execute-api.us-east-1.amazonaws.com/dev/`**

Supports the following datasets:
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

This deployment was created with the following commands:
```
# Install library
git clone https://github.com/geospatial-jeff/cognition-datasources.git app
cd app
python setup.py develop

# Load drivers
cognition-datasources load -d DGOpenData -d ElevationTiles -d CBERS -d Landsat8 -d MicrosoftBuildingFootprints \
                           -d NAIP -d Sentinel1 -d Sentinel2 -d SRTM -d USGS3DEP

# Build Docker container
docker build . -t cognition-datasources-deploy:latest

# Package the layer
docker run --rm -v $PWD:/home/cognition-datasources -it cognition-datasources-deploy:latest package-service.sh

# Deploy to AWS
sls deploy -v
```

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

geoj =  {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -95.91064453125,
              28.825425374477224
            ],
            [
              -93.88916015625,
              28.825425374477224
            ],
            [
              -93.88916015625,
              30.44867367928756
            ],
            [
              -95.91064453125,
              30.44867367928756
            ],
            [
              -95.91064453125,
              28.825425374477224
            ]
          ]
        ]
      }


payload = {"intersects": geoj,
           "datasources": ["NAIP", "Landsat8", "Sentinel2", "SRTM"],
           }


r = requests.post('https://uh2bdjpxkl.execute-api.us-east-1.amazonaws.com/dev/stac/search', data=json.dumps(payload))
response = r.json()
print(response)
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


