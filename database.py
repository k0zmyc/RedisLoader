import redis
import json
import datetime

from redis_dict import RedisDict

from aiodataloader import DataLoader

import sqlalchemy
from sqlalchemy import (Column,String,DateTime,Uuid,Boolean,Date)

from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4, UUID
from sqlalchemy import Column, Uuid
uuid = uuid4


def UUIDColumn():

    return Column(
        Uuid, primary_key=True, default=uuid
    )


def UUIDFKey(comment = None, nullable=True, **kwargs):
    
    return Column(
        Uuid, index=True, nullable=nullable, **kwargs
    )
BaseModel = declarative_base()


class PublicationModel(BaseModel):

    """
    Represents a Publication entity in the database
    """

    __tablename__ = "publications"

    id = UUIDColumn()
    name = Column(String)
    published_date = Column(DateTime)
    reference = Column(String)
    valid = Column(Boolean)
    place = Column(String)

    publication_type_id = UUIDFKey(nullable=True, comment="ID of the publication type")#Column(Uuid, index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True, comment="who's created the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True, comment="who's changed the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")

#######################################################################
################## Serialization and deserialization ##################
#######################################################################


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

def deserialize_from_str(data):
    jsondata=json.loads(data)
    result = PublicationModel(**jsondata)

    return result

def serialize_to_str(dbModel):
    jsondata=serialize(dbModel)
    result=json.dumps(jsondata)

    return result

#######################################################################
##################  Insert data as using redis-dict####################
######################### ...as one string ############################
#######################################################################



def cache_dict(path, redis_dict):
    # Load the contents of the file into a dictionary
    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    # Separate Publication data and select the first publication
    publications = data["publications"]
    publication = publications[0]

    # Create publication class instance
    publicationobj=PublicationModel(**publication)
    print(publicationobj)
    print(serialize(publicationobj))
    #publication["created"]=datetime.datetime.now()

    # Create a RedisDict instance
    redis_dict = RedisDict(host='localhost', port=6379, db=0)

    # 
    redis_dict.transform[type(PublicationModel).__name__]=deserialize_from_str
    redis_dict.pre_transform[type(PublicationModel).__name__]=serialize_to_str

    # Store the JSON string in Redis
    #redis_dict['data'] = json_data
    #redis_dict[user["id"]]=json.dumps(user)
    #redis_dict[publication["id"]]=(publication)
    #entitystr=redis_dict[publication["id"]]
    redis_dict[publicationobj.id]=(publicationobj)
    entitymodel=redis_dict[publicationobj.id]
    #entity=json.loads(entitystr)
    entity=(entitymodel)
    print(entity)

class RedisLoader(DataLoader):
    def __init__(self, redis_dict):
        super().__init__()
        self.redis_dict = redis_dict

    async def batch_load_fn(self, keys):
        results = [self.redis_dict.get(key) for key in keys]
        return results


async def cache_dict_async(path, redis_dict):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    publications = data["publications"]
    publication = publications[0]
    publicationobj = PublicationModel(**publication)

    print(publicationobj)
    print(serialize(publicationobj))

    redis_dict.transform[type(PublicationModel).__name__] = deserialize_from_str
    redis_dict.pre_transform[type(PublicationModel).__name__] = serialize_to_str

    redis_loader = RedisLoader(redis_dict)

    await redis_loader.load(str(publicationobj.id))

    redis_dict[str(publicationobj.id)] = publicationobj
    entitymodel = await redis_loader.load(str(publicationobj.id))
    entity = entitymodel

    print(entity)