from datetime import datetime, timedelta

from .models import Book
from lafv.views import ListAPIFilteredView
from .serializers import BookSerializer


class BookView(ListAPIFilteredView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_fields = ('author__nickname', 'isbn')
    custom_filters = ('new', )

    def filter_new(self, queryset):
        """
        get books that publication date is no longer than 1 month
        """
        last_month = datetime.today() - timedelta(days=30)
        queryset = queryset.filter(publication_date__gte=last_month)
        return queryset
