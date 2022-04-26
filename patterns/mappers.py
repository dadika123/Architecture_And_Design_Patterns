import sqlite3
from abc import ABC, abstractmethod
from typing import Type

from patterns.creational_patterns import Student
from patterns.exceptions import RecordNotFoundException, DbCommitException, DbUpdateException, DbDeleteException


class Mapper(ABC):
    """Base mapper"""

    def __init__(self, table_name: str, connection: sqlite3.Connection):
        self._connection = connection
        self._cursor = connection.cursor()
        self._table_name = table_name.lower()

    def _select_all(self) -> list:
        """Select all from database"""
        statement = f'SELECT * from {self._table_name}'
        self._cursor.execute(statement)
        return self._cursor.fetchall()

    @abstractmethod
    def insert(self, obj):
        """Inserts object"""
        pass

    @abstractmethod
    def update(self, obj):
        """Updates object"""
        pass

    @abstractmethod
    def delete(self, obj):
        """Deletes object"""
        pass


class StudentMapper(Mapper):

    def __init__(self, connection: sqlite3.Connection):
        super().__init__(Student.__name__, connection)

    def all(self):
        """Gets all students"""
        students = []
        for student in self._select_all():
            student_id, name = student
            student = Student(name)
            student.id = student_id
            students.append(student)
        return students

    def get_by_id(self, student_id: int):
        """Gets student by id"""
        statement = f'SELECT id, name FROM {self._table_name} WHERE id=?'
        self._cursor.execute(statement, (student_id,))
        result = self._cursor.fetchone()
        if result:
            return Student(*result)
        raise RecordNotFoundException(f'id={student_id} not found')

    def insert(self, obj):
        statement = f'INSERT INTO {self._table_name} (name) VALUES (?)'
        self._cursor.execute(statement, (obj.name,))
        try:
            self._connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f'UPDATE {self._table_name} SET name=? WHERE id=?'
        self._cursor.execute(statement, (obj.name, obj.id))
        try:
            self._connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f'DELETE FROM {self._table_name} WHERE id=?'
        self._cursor.execute(statement, (obj.id,))
        try:
            self._connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


MappedClasses = Type[Student]

connection = sqlite3.connect('patterns.sqlite')


class MapperRegistry:
    _mappers = {
        Student.__name__.lower(): StudentMapper
    }

    @classmethod
    def get_mapper(cls, obj: MappedClasses):
        """Gets mapper according to class instance"""
        return cls._mappers[obj.__class__.__name__.lower()](connection)

    @classmethod
    def get_mapper_by_name(cls, name: str):
        """Gets mapper according to name"""
        return cls._mappers[name.lower()](connection)
