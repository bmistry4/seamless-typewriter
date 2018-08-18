from enum import Enum


class TABLE_HEADINGS(Enum):
    """
    Enums used for the search table column headings
    """
    __order__ = 'TIME TEXT'
    TIME = ("Time", 0)
    TEXT = ("Text", 1)


    @staticmethod
    def get_heading(value):
        """
        Returns the heading name
        :param value: Tuple of the enum values
        :return: The heading name
        """
        return value[0]


    @staticmethod
    def get_index(value):
        """
        Reutrns the index value of the column i.e. 2nd tuple value of the enum values
        :param value: enum value
        :return: 2nd tuple = index value
        """
        return value[1]
