import os
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
from marshmallow import fields

from datasources import Manifest

application = Flask(__name__)
api = Api(application)
ma = Marshmallow(application)

"""Schemas"""
class GeojsonSchema(ma.Schema):
    type = fields.Str()
    coordinates = fields.List(fields.List(fields.List(fields.Number())))

class STACAPISchema(ma.Schema):
    bbox = fields.List(fields.Number())
    intersects = fields.Nested(GeojsonSchema)
    time = fields.String()
    properties = fields.Dict(keys=fields.String(), values=fields.Dict(keys=fields.String()))
    datasources = fields.List(fields.String())
    limit = fields.Int()

api_schema = STACAPISchema()


class STACAPI(Resource):

    def post(self):
        json_data = request.get_json(force=True)
        package, errors = api_schema.load(json_data)
        params = list(package)
        args = {}

        manifest = Manifest()

        if 'time' in params:
            args.update({'temporal': package['time'].split('/')})

        if 'intersects' in params:
            args.update({'spatial': package['intersects']})

        if 'bbox' in params:
            # Honor intersects over bbox
            if 'intersects' not in params:
                geoj = {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [package['bbox'][0], package['bbox'][3]],
                            [package['bbox'][2], package['bbox'][3]],
                            [package['bbox'][2], package['bbox'][1]],
                            [package['bbox'][0], package['bbox'][1]],
                            [package['bbox'][0], package['bbox'][3]]
                        ]
                    ]
                }
                args.update({'spatial': geoj})

        if 'properties' in params:
            args.update({'properties': package['properties']})

        if 'limit' in params:
            args.update({'limit': package['limit']})

        for source in package['datasources']:
            manifest[source].search(**args)

        response = manifest.execute()

        return jsonify(response)


api.add_resource(STACAPI, '/stac/search')

if __name__ == "__main__":
    application.run(debug=True)



