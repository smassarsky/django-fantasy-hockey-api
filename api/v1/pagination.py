from rest_framework.pagination import LimitOffsetPagination


class SmallLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10