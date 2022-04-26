import threading


class UnitOfWork:
    """Unit of Work for database"""
    _current = threading.local()

    def __init__(self):
        self.new_objects = set()
        self.modified_objects = set()
        self.removed_objects = set()
        self.MapperRegistry = None

    def set_mapper_registry(self, mapper_registry):
        """Sets registry mapper for unit of work"""
        from patterns.mappers import MapperRegistry
        mapper_registry: MapperRegistry
        self.MapperRegistry = mapper_registry

    def register_new(self, obj):
        """Registers new object"""
        self.new_objects.add(obj)

    def register_modified(self, obj):
        """Registers object as modified"""
        self.modified_objects.add(obj)

    def register_removed(self, obj):
        """Registers object as removed"""
        self.removed_objects.add(obj)

    def _insert_new(self):
        """Inserts all the objects registered as new"""
        for obj in self.new_objects:
            self.MapperRegistry.get_mapper(obj).insert(obj)
        self.new_objects.clear()

    def _update_modified(self):
        """Updates all the objects registered as modified"""
        for obj in self.modified_objects:
            self.MapperRegistry.get_mapper(obj).update(obj)
        self.modified_objects.clear()

    def _delete_removed(self):
        """Deletes all the objects registered as removed"""
        for obj in self.removed_objects:
            self.MapperRegistry.get_mapper(obj).delete(obj)
        self.removed_objects.clear()

    def commit(self):
        """
        Handles all registered
        actions in a single transaction
        """
        self._insert_new()
        self._update_modified()
        self._delete_removed()

    @classmethod
    def set_current(cls, unit_of_work):
        """Sets current unit of work"""
        cls._current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        """Gets current unit of work"""
        return cls._current.unit_of_work

    @classmethod
    def new_current(cls):
        """Sets new current unit of work"""
        cls.set_current(UnitOfWork())
