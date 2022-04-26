from patterns.unit_of_work import UnitOfWork


class DomainObject:
    """Class to group registrations to Unit of Work"""

    def mark_new(self):
        """
        Marks object as new by
        registering it in Unit of Work
        """
        UnitOfWork.get_current().register_new(self)

    def mark_modified(self):
        """
        Marks object as modified by
        registering it in Unit of Work
        """
        UnitOfWork.get_current().register_modified(self)

    def mark_removed(self):
        """
        Marks object as removed by
        registering it in Unit of Work
        """
        UnitOfWork.get_current().register_removed(self)
