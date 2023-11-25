from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'items_per_page': len(self.page),
            'results': data
        })
