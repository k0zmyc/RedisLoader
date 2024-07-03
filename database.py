import redis
import json
import datetime

from redis_dict import RedisDict

from aiodataloader import DataLoader


from serialize import *

#######################################################################
##################  Insert data using redis-dict ######################
#######################################################################



def cache_dict(path, redis_dict, model):
    """Cache data from a JSON file into Redis using a specified SQLAlchemy model."""
    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    entities = data[model.__tablename__]

    redis_dict.transform[model.__name__] = lambda x: deserialize_from_str(model, x)
    redis_dict.pre_transform[model.__name__] = lambda obj: serialize_to_str(model, obj)

    for entity_data in entities:
        entity = model(**entity_data)
        redis_dict[str(entity.id)] = entity
        print(f"Cached entity {model.__tablename__}:", serialize(entity))


class RedisLoader(DataLoader):
    def __init__(self, redis_dict):
        super().__init__()
        self.redis_dict = redis_dict

    async def batch_load_fn(self, keys):
        results = [self.redis_dict.get(key) for key in keys]
        return results


async def cache_dict_async(path, redis_dict, *models):
    with open(path, encoding='utf-8') as file:
        data = json.load(file)

    redis_loader = RedisLoader(redis_dict)

    ids = []

    for model in models:
        entities = data[model.__tablename__]

        for entity in entities:
            entity_obj = model(**entity)
            redis_dict[str(entity_obj.id)] = entity_obj
            ids.append(str(entity_obj.id))

            #print(f"Cached entity {model.__tablename__}: {serialize(entity_obj)}")

    entities = await redis_loader.load_many(ids)

    for entity in entities:
        print(entity)
