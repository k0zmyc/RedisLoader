import redis
import json
import asyncio

from redis_dict import RedisDict

from database import cache_dict, cache_dict_async

from Models import PublicationModel, AuthorModel, PublicationCategoryModel, PublicationTypeModel, SubjectModel

path = r'C:\Users\kozma\source\repos\RedisLoader\data.json'

redis_dict = RedisDict(host='localhost', port=6379, db=0)


#cache_dict(path, redis_dict)
asyncio.run(cache_dict_async(path, redis_dict, PublicationModel, PublicationCategoryModel, PublicationTypeModel, AuthorModel, SubjectModel))