from rest_framework import mixins, viewsets

from config.pagination import DefaultPagination
from template.models import Template
from template.serializers import TemplateSerializer


class TemplateViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    pagination_class = DefaultPagination

    def retrieve(self, request, *args, **kwargs):
        """
        템플릿을 상세 조회합니다.
        """
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        템플릿 목록을 조회합니다.
        """
        return super().list(request, *args, **kwargs)
