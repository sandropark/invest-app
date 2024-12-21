from typing import List, Type, TypeVar
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from src.domain.exception import ExeptionType, InvestAppException
from src.domain.port import Repository
from src.infra.persistance.mapper.mapper import Mapper


E = TypeVar("E")
M = TypeVar("M")


class SqlalchemyRepository[E, M](Repository[M]):
    def __init__(self, session: Session, mapper: Mapper[E, M], entity_type: Type[E]):
        self.session = session
        self.mapper = mapper
        self.entity_type = entity_type

    def save(self, model: M) -> M:
        with self.session as session:
            entity = self.mapper.to_entity(model)
            session.add(entity)
            session.commit()
            return model

    def update(self, id: int, model: M) -> M:
        with self.session as session:
            stmt = update(self.entity_type).where(self.entity_type.id == id).values(model.__dict__)
            session.execute(stmt)
            session.commit()
            return model

    def delete_by_id(self, id: int) -> int:
        with self.session as session:
            stmt = delete(self.entity_type).where(self.entity_type.id == id)
            session.execute(stmt)
            session.commit()
            return id

    def find_all(self) -> List[M]:
        with self.session as session:
            stmt = select(self.entity_type)
            return [self.mapper.to_model(entity) for entity in session.scalars(stmt).all()]

    def find_by_id(self, id: int) -> M | None:
        with self.session as session:
            stmt = select(self.entity_type).where(self.entity_type.id == id)
            entity = session.scalars(stmt).one_or_none()
            if not entity:
                raise InvestAppException(ExeptionType.ENTITY_NOT_FOUND, id)
            return self.mapper.to_model(entity)
