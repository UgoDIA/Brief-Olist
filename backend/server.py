from hug.middleware import CORSMiddleware
import hug

from controllers.controllers import map, evolutions

api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api, allow_origins=['*'])) # allow_origins à restreindre pour le déploiement

hug.get('/api/map', api=api)(map.getData)
hug.get('/api/evolutions', api=api)(evolutions.getDatas)