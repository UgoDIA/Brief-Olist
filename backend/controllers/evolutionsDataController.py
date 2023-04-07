from controllers.functions import getTOP10states, getDataTOP10product

def evolutionsDataController(region, annee):
    dicoDatas = {}

    datas = getDataTOP10product(region, annee)
    dicoDatas['TOP10product'] = datas

    datas = getTOP10states(annee)
    dicoDatas['TOP10states'] = datas

    return dicoDatas