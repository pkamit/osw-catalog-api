"""
Views for articles api
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Article,
    Category,
)
from article import serializers


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'categories',
                OpenApiTypes.STR,
                description='Comma separated list of categories Ids to filter',
            ),

        ]
    )
)


class ArticleViewSet(viewsets.ModelViewSet):
    """ View for managing article api"""
    serializer_class = serializers.ArticleDetailSerializer
    queryset = Article.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def _params_to_ints(self, qs):
        """ coverts a list of strings to integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """ retrieve articles for aurthenticated user"""
        categories = self.request.query_params.get('categories')
        queryset = self.queryset
        if categories:
            cat_ids = self._params_to_ints(categories)
            queryset = queryset.filter(categories__id__in=cat_ids)
        return queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """ Return the serializer class for request"""
        if self.action == 'list':
            return serializers.ArticleSerializer
        elif self.action == 'upload_image':
            return serializers.ArticleImageSerializer
        elif self.action == 'uploadnew_image':
            return serializers.ArticleNewImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """ create a new article"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """ Upload an image to article"""
        article = self.get_object()
        serializer = self.get_serializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True, url_path='uploadnew-image')
    def uploadnew_image(self, request, pk=None):
        """ Upload an image to article"""
        article = self.get_object()
        serializer = self.get_serializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0,1],
                description='Filter by items to article.',
            )
        ]
    )
)

class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for article viewsets"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Filter queryset to authenticated_user"""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only',0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(article__isnull=False)
        return queryset.filter(user=self.request.user).order_by('-name').distinct()
       # return self.queryset.filter(user=self.request.user).order_by('-name').distinct()


class CategoryViewSet(BaseRecipeAttrViewSet):
    """ manage category in the database"""
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()

