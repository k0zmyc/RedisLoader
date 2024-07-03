#######################################################################
################## Serialization and deserialization ##################
#######################################################################

import json
def serialize(dbModel):
    """ 
    Funkce umožňující serializaci(dbModel představuje hodnotu třídy)
    """
    result = {}
    for name in dir(dbModel):
        if name.startswith("_"):
            continue
        value = getattr(dbModel, name)
        if value is not None:
            result[name]=value

    return result

def deserialize(model, data):
    """Deserialize JSON data into an SQLAlchemy model instance."""
    return model(**data)

def deserialize_from_str(model, data):
    """Deserialize a JSON string into an SQLAlchemy model instance."""
    jsondata = json.loads(data)
    return deserialize(model, jsondata)

def serialize_to_str(dbModel):
    jsondata=serialize(dbModel)
    result=json.dumps(jsondata)

    return result