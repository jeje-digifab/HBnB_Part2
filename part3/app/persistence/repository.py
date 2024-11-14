from abc import ABC, abstractmethod
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_


class RepositoryException(Exception):
    pass


class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        from app import db
        self.model = model
        self.db = db

    def add(self, obj):
        try:
            self.db.session.add(obj)
            self.db.session.commit()
            return obj
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise RepositoryException(f"Error adding object: {str(e)}")

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            try:
                for key, value in data.items():
                    setattr(obj, key, value)
                self.db.session.commit()
                return obj
            except SQLAlchemyError as e:
                self.db.session.rollback()
                raise RepositoryException(f"Error updating object: {str(e)}")
        return None

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            try:
                self.db.session.delete(obj)
                self.db.session.commit()
                return True
            except SQLAlchemyError as e:
                self.db.session.rollback()
                raise RepositoryException(f"Error deleting object: {str(e)}")
        return False

    def get_by_attribute(self, attr_name, attr_value):
        return (
            self.model.query
            .filter(getattr(self.model, attr_name) == attr_value)
            .first()
        )

    def get_by_attributes(self, attributes):
        query = self.model.query
        for attr_name, attr_value in attributes.items():
            query = query.filter(getattr(self.model, attr_name) == attr_value)
        return query.first()
