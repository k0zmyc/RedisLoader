from sqlalchemy import (Column,String,DateTime,Uuid,Boolean,Date,Float,Integer)
from sqlalchemy.orm import declarative_base
from uuid import uuid4, UUID

uuid = uuid4


import sqlalchemy



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


class AuthorModel(BaseModel):

    """
    Represents an Author entity in the database
    """
    
    __tablename__ = "publication_authors"

    id = UUIDColumn()
    order = Column(Integer)
    share = Column(Float)

    publication_id = UUIDFKey(nullable=True, comment="ID of the associated publication")#Column(Uuid, index=True)
    user_id = Column(Uuid, index=True)

    valid = Column(Boolean, default=True, comment="Indicates whether this entity is valid or invalid")
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")

class PublicationCategoryModel(BaseModel):

    """
    Represents a PublicationCategory entity in the database
    """

    __tablename__ = "publicationcategories"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)


    valid = Column(Boolean, default=True, comment="Indicates whether this entity is valid or invalid")
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True, comment="who's created the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True, comment="who's changed the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")


class PublicationTypeModel(BaseModel):

    """
    Represents a PublicationType entity in the database
    """

    __tablename__ = "publicationtypes"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    category_id = UUIDFKey(nullable=True)#Column(Uuid, index=True, nullable=True)
    #publication = relationship("PublicationModel", back_populates="publication_type")

    valid = Column(Boolean, default=True, comment="Indicates whether this entity is valid or invalid")
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")


class SubjectModel(BaseModel):

    """
    Represents a Subject entity in the database
    """

    __tablename__ = "publication_subjects"

    id = UUIDColumn()
    publication_id = UUIDFKey(nullable=True)#Column(ForeignKey("publications.id")index=True)
    subject_id = UUIDFKey(nullable=True)#Column(ForeignKey("plan_subjects.id"), index=True)

    #publication = relationship("PublicationModel")
    #subject = relationship("PlanSubjectModel")

    valid = Column(Boolean, default=True, comment="Indicates whether this entity is valid or invalid")
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True, comment="who's created the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True, comment="who's changed the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")