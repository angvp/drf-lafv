from rest_framework import generics


class ListAPIFilteredView(generics.ListAPIView):
    """
    View that allows you to filter through url params and defined fields
    """

    def get_queryset(self):
        queryset = super(ListAPIFilteredView, self).get_queryset()
        query_params = self.request.query_params
        params = query_params.keys()
        query_filters = []
        custom_filters = []

        try:
            query_filters = self.filter_fields
        except AttributeError:
            pass

        try:
            custom_filters = self.custom_filters
        except AttributeError:
            pass

        for field in query_filters:
            if field in params:
                value = query_params.getlist(field)

                if not value:
                    continue

                if len(value) > 1:
                    s = {'%s__in' % field: value}
                else:
                    s = {field: value[0]}
                queryset = queryset.filter(**s)

        for field in custom_filters:
            if field in params:
                try:
                    queryset = getattr(self, "filter_%s" % field)(queryset)
                except AttributeError:
                    continue

        return queryset
