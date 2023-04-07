from hug.middleware import CORSMiddleware
import hug

from controllers import mapDataController, evolutionsDataController

api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api, allow_origins=['*'])) # allow_origins à restreindre pour le déploiement

@hug.get('/api/map')
def getMapData():
    datas = mapDataController()
    return datas

# Non terminé
@hug.get('/api/evolutions/{region}/{annee}')
def getEvolutionsdatas(region,annee):
    dicoDatas = evolutionsDataController(region, annee)
    return dicoDatas