from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from http import HTTPStatus

from recipes.models import (Carts, Favorites, Follows, Ingredients, Recipes,
                            Tags)
from users.models import User
from .serializers import (CartsSerializer, FollowsSerializer,
                          IngredientsSerializer, RecipesSerializer,
                          TagsSerializer, UserSerializer, UserCreateSerializer)
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """Users' viewset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    # permission_classes = IsAuthenticated

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer

    @action(methods=['post'], detail=False)
    def set_password(self, request):
        current_user = self.request.user
        if not current_user.check_password(
            request.data.get('current_password')
        ):
            return Response(
                {'message': 'Incorrect current password'},
                status=HTTPStatus.BAD_REQUEST
            )
        current_user.set_password(request.data.get('new_password'))
        current_user.save()
        return Response(
            {'message': 'Password changed'},
            status=HTTPStatus.OK
        )

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        follows = Follows.objects.filter(user=user)
        pages = self.paginate_queryset(follows)
        serializer = FollowsSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST', 'DELETE'], detail=True,
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk):
        user = request.user
        author = get_object_or_404(User, id=pk)
        if request.method == 'POST':
            follow = Follows.objects.create(user=user, author=author)
            serializer = FollowsSerializer(follow,
                                           context={'request': request})
            return Response(serializer.data)
        follow = Follows.objects.filter(user=user, author=author)
        if follow.exists():
            follow.delete()
            return Response(status=HTTPStatus.NO_CONTENT)
        return Response({'errors': 'Вы не подписаны на данного автора'},
                        status=HTTPStatus.BAD_REQUEST)


class UserMeViewSet(viewsets.ModelViewSet):
    """Users' viewset."""
    serializer_class = UserSerializer
    pagination_class = None
    permission_classes = IsAuthenticated

    def get_queryset(self):
        current_user = self.request.user
        return User.objects.filter(id=current_user.id)


class TagsViewSet(viewsets.ModelViewSet):
    """Tags' viewset."""
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
    permission_classes = IsAdminOrReadOnly


class IngredientsViewSet(viewsets.ModelViewSet):
    """Ingredients' viewset."""
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = IsAdminOrReadOnly


class RecipesViewSet(viewsets.ModelViewSet):
    """Ingredients' viewset."""
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    paginator_class = LimitOffsetPagination
    permission_classes = IsAuthorOrReadOnly

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipes, pk=pk)
        if request.method == 'POST':
            Carts.objects.create(user=request.user, recipes=recipe)
            serializer = CartsSerializer(recipe)
            return Response(serializer.data)
        cart = Carts.objects.filter(user=request.user, recipes=recipe)
        cart.delete()
        return Response(status=HTTPStatus.NO_CONTENT)

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipes, pk=pk)
        if request.method == 'POST':
            Favorites.objects.create(user=request.user, recipe=recipe)
            serializer = CartsSerializer(recipe)
            return Response(serializer.data)
        favorite = Favorites.objects.filter(user=request.user, recipe=recipe)
        favorite.delete()
        return Response(status=HTTPStatus.NO_CONTENT)
