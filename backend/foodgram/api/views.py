from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.decorators import action
# from rest_framework.response import Response

# from djoser.views import UserViewSet as Djoser

from recipes.models import Ingredients, Recipes, Tags
from users.models import User

from .serializers import (IngredientsSerializer, TagsSerializer,
                          UserSerializer, UserCreateSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """Users' viewset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer

    # @action(methods=['post'], detail=False)
    # def set_password(self, request):
    #     current_user_password = self.request.user.password
    #     if request.data.get('current_password') == current_user_password:
    #         self.request.user.password = request.data.get('new_password')
    #         pass
    # @action(methods=['post'], detail=False)
    # def set_password(self, request, *args, **kwargs):
    #     serializer = UserSerializer(data=request.data)
    #     serializer.is_valid()
    #     print(serializer.initial_data)
    #     self.request.user.set_password(serializer.initial_data["new_password"])
    #     self.request.user.save()
    #     return Response({'message': 'password changed'})


class UserMeViewSet(viewsets.ModelViewSet):
    """Users' viewset."""
    serializer_class = UserSerializer
    pagination_class = None

    def get_queryset(self):
        current_user = self.request.user
        return User.objects.filter(id=current_user.id)


class TagsViewSet(viewsets.ModelViewSet):
    """Tags' viewset."""
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    """Ingredients' viewset."""
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    """Ingredients' viewset."""
    queryset = Recipes.objects.all()
    serializer_class = IngredientsSerializer
    paginator_class = LimitOffsetPagination
