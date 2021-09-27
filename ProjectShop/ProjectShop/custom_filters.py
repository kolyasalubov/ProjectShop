from django.contrib import admin


class DropdownChoicesFieldListFilter(admin.filters.ChoicesFieldListFilter):
    template = 'admin/custom_filters/dropdown_filter.html'


class MultipleChoiceListFilter(admin.SimpleListFilter):
    """
    Copied from https://github.com/ctxis/django-admin-multiple-choice-list-filter with a few changes
    """
    template = 'admin/custom_filters/checkboxes_filter.html'

    def lookups(self, request, model_admin):
        """
        Must be overridden to return a list of tuples (value, verbose value)
        """
        raise NotImplementedError(
            'The MultipleChoiceListFilter.lookups() method must be overridden to '
            'return a list of tuples (value, verbose value).'
        )

    def queryset(self, request, queryset):
        if request.GET.get(self.parameter_name):
            kwargs = {self.parameter_name: request.GET[self.parameter_name].split(',')}
            queryset = queryset.filter(**kwargs)
        return queryset

    def value_as_list(self):
        return self.value().split(',') if self.value() else []

    def amend_query_string(self, changelist, include=None, exclude=None):
        selections = self.value_as_list()
        if include and include not in selections:
            selections.append(include)
        if exclude and exclude in selections:
            selections.remove(exclude)
        if selections:
            csv = ','.join(selections)
            return changelist.get_query_string({self.parameter_name: csv})
        else:
            return changelist.get_query_string(remove=[self.parameter_name])

    def choices(self, changelist):
        yield {
            'selected': self.value() is None,
            'query_string': changelist.get_query_string(remove=[self.parameter_name]),
            'display': 'All',
            'reset': True,
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': str(lookup) in self.value_as_list(),
                'include_query_string': self.amend_query_string(changelist, include=str(lookup)),
                'exclude_query_string': self.amend_query_string(changelist, exclude=str(lookup)),
                'display': title,
            }
