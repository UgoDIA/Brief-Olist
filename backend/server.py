from hug.middleware import CORSMiddleware
import hug

from controllers.controllers import map, evolutions

router = hug.route.API(__name__)

router.get('/api/map')(map.getData)
router.get('/api/evolutions')(evolutions.getDatas)