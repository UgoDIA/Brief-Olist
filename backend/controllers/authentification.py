import hug
import jwt
from hashlib import sha512
import secrets

from database.database     import session
from database.models.user  import Users

from database.getConf import getConfig

# Fonctions-------------------------------------------------------

# Vérifie le token => précisement comment ??
def token_verify(token):
    global secret_key
    try:
        return jwt.decode(token, secret_key, algorithms=['HS256'])
    except jwt.DecodeError:
        return False

# Hache un mdp
def hachage(mdp:str):
    # salt = secrets.token_hex(24).encode()
    salt = getConfig('salt').encode() # Permet d'augementer la "force" du hachage

    mdp = mdp.encode() # string => bytes
    
    # Hachage
    mdp_hache = sha512(salt + mdp).hexdigest()

    return mdp_hache

# Variables globales --------------------------------------------

secret_key = getConfig('secretKey')

token_key_authentication = hug.authentication.token(token_verify)

# API------------------------------------------------------------

# Authentification
@hug.post('/login')
def token_gen_call(username, password):
    """Authentifier et renvoyer un token"""
    global secret_key

    # Vérif que le username est présent dans la BDD
    usernameExist = session.query(Users.username).where(Users.username == username).count()
    if usernameExist == 0:
        return "Nom d'utilisateur et/ou mot de passe incorrect"
    
    elif usernameExist == 1:
        # Récuperer le vrai mdp
        realPwd = session.query(Users.password).where(Users.username == username).value(Users.password)

        # Vérifier la corespondance
        if secrets.compare_digest(realPwd, hachage(password)):
            return {"token" : jwt.encode({'user': username}, secret_key, algorithm='HS256')}
        else:
            return "Nom d'utilisateur et/ou mot de passe incorrect"

# Plus securisé que simple vraiMdp == mdpEntre car temps de comparaison constant (timing attacks)
# ", 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)" => Expiration du token

# Ajout d'utilisateur
@hug.post('/register', requires=token_key_authentication)
def register(username, password):
    ''' Enregistrer un nouvel utilisateur  '''
    # Vérif username n'éxiste pas déjà
    usernameAlreadyExist = session.query(Users).where(Users.username == username).count()
    if usernameAlreadyExist == 1:
        return 'Nom d\'utilisateur déja pris'
    # Enregistrements des identifiants
    else :
        session.add(Users(username = username, password = hachage(password)))
        session.commit()
        return 'ok'

@hug.get('/check', requires=token_key_authentication)
def authenticationCheck():
    ''' Vérifier si l'utilisateur est connecté '''
    return 'ok'

# Test restriction d'accès
@hug.get('/token_authenticated', requires=token_key_authentication)
def token_auth_call(user: hug.directives.user):
    ''' Test restriction d'accès, fonctionel '''
    return '"Test requête GET ": You are user: {0}'.format(user['user'])