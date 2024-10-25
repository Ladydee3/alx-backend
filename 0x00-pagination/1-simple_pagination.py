#!/usr/bin/env python3
""" Simple pagination
"""

import csv
from typing import List, Tuple


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # Skip the header row

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """ Finds the correct indexes to paginate dataset.
        """
        assert type(page) == int, "Page must be an integer"
        assert type(page_size) == int, "Page size must be an integer"
        assert page > 0, "Page must be greater than 0"
        assert page_size > 0, "Page size must be greater than 0"
        
        start, end = index_range(page, page_size)
        dataset = self.dataset()
        if start >= len(dataset):
            return []  # Return an empty list if the start index is out of bounds

        return dataset[start:end]


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """ Returns a tuple containing a start and end index.
    """
    return ((page - 1) * page_size, page * page_size)

