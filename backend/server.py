from hug.middleware import CORSMiddleware
import hug

from controllers.controllers import map, evolutions, annonce, data

api = hug.API(__name__)
# allow_origins à restreindre pour le déploiement
api.http.add_middleware(CORSMiddleware(api, allow_origins=['*']))

hug.get('/api/map', api=api)(map.getData)
hug.get('/api/evolutions', api=api)(evolutions.getDatas)
hug.get('/api/annonces', api=api)(annonce.getDatas)
hug.get('/api/date/minmax', api=api)(data.MinMaxYear)