from controllers    import authentification
from hug.middleware import CORSMiddleware
import hug

api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api, allow_origins=['*'])) # allow_origins à restreindre pour le déploiement

api.extend(authentification, '/api/authentication')