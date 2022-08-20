from http import HTTPStatus
from typing import Union

from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.pdfgen import canvas

from recipes.models import (Cart, Favorite, Follow, Ingredient,
                            IngredientInRecipe, Recipe, Tag)
from users.models import User
from .serializers import (CartSerializer, FollowSerializer,
                          IngredientSerializer, RecipePostSerializer,
                          RecipeSerializer, SetPasswordSerializer,
                          TagSerializer, UserSerializer, UserCreateSerializer)
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .filters import IngredientSearchFilter, RecipeFilter
from .pagination import LimitPageNumberPagination


class UserViewSet(viewsets.ModelViewSet):
    """Users' viewset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer

    @action(
        methods=['POST'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def set_password(self, request):
        """Password changing."""
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_user = self.request.user
        if not current_user.check_password(
            serializer.validated_data.get('current_password')
        ):
            return Response(
                {'errors': 'Неверный текущий пароль'},
                status=HTTPStatus.BAD_REQUEST
            )
        current_user.set_password(request.data.get('new_password'))
        current_user.save()
        return Response(
            {'message': 'Пароль изменен'},
            status=HTTPStatus.OK
        )

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        """Getting all subscriptions with recipes limit."""
        user = request.user
        follows = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(follows)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, pk):
        """Create/delete subscribe."""
        user = request.user
        author = get_object_or_404(User, id=pk)
        if request.method == 'POST':
            if Follow.objects.filter(
                user=user,
                author=author
            ).exists():
                return Response(
                    {'errors': 'Вы уже подписаны на этого автора'},
                    status=HTTPStatus.BAD_REQUEST,
                )
            if user == author:
                return Response(
                    {'errors': 'Нельзя подписаться на себя'},
                    status=HTTPStatus.BAD_REQUEST,
                )
            follow = Follow.objects.create(
                user=user,
                author=author
            )
            serializer = FollowSerializer(
                follow,
                context={'request': request},
            )
            return Response(serializer.data)
        follow = Follow.objects.filter(
            user=user,
            author=author
        )
        if follow.exists():
            follow.delete()
            return Response(status=HTTPStatus.NO_CONTENT)
        return Response(
            {'errors': 'Вы не подписаны на данного автора'},
            status=HTTPStatus.BAD_REQUEST
        )

    @action(detail=False,
            pagination_class=None,
            url_path='me',
            )
    def current_user_information(self, request):
        """Current user information."""
        current_user = request.user
        if not current_user:
            return Response(
                    {'errors': 'Ни один пользователь не авторизован'},
                    status=HTTPStatus.BAD_REQUEST,
                )
        serializer = self.get_serializer(current_user)
        return Response(serializer.data, status=HTTPStatus.OK)


class TagViewSet(viewsets.ModelViewSet):
    """Tag' viewset."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [IsAdminOrReadOnly]


class IngredientViewSet(viewsets.ModelViewSet):
    """Ingredient' viewset."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (IngredientSearchFilter, )
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Ingredient' viewset."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    paginator_class = LimitPageNumberPagination
    permission_classes = [IsAuthorOrReadOnly]
    filter_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return RecipePostSerializer
        return RecipeSerializer

    def create_object(self, model, user, pk):
        """Create new object."""
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response(
                {'errors': 'Рецепт уже в списке.'},
                status=HTTPStatus.BAD_REQUEST,
                )
        recipe = get_object_or_404(Recipe, pk=pk)
        model.objects.create(
            user=user,
            recipe=recipe
        )
        serializer = CartSerializer(recipe)
        return Response(
            serializer.data,
            status=HTTPStatus.CREATED,
            )

    def delete_object(self, model, user, pk):
        """Delete object."""
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=HTTPStatus.NO_CONTENT)
        return Response(
            {'errors': 'Рецепт уже удален'},
            status=HTTPStatus.BAD_REQUEST,
            )

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        """Add or delete recipe from shoping cart."""
        if request.method == 'POST':
            return self.create_object(
                model=Cart,
                user=self.request.user,
                pk=pk,
            )
        return self.delete_object(
            model=Cart,
            user=self.request.user,
            pk=pk,
        )

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        """Add or delete recipe from favorites list."""
        if request.method == 'POST':
            return self.create_object(
                model=Favorite,
                user=self.request.user,
                pk=pk,
            )
        return self.delete_object(
            model=Favorite,
            user=self.request.user,
            pk=pk,
        )

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        user = request.user
        purchases: dict[str, Union[str, int]] = {}
        ingredients = IngredientInRecipe.objects.filter(
            recipe__cart__user=user).values(
                'ingredient__name',
                'ingredient__measurement_unit'
                ).annotate(amount_in_cart=Sum('amount'))
        for ingredient in ingredients:
            name = ingredient.get('ingredient__name')
            measurement_unit = ingredient.get('ingredient__measurement_unit')
            amount = ingredient.get('amount_in_cart')
            purchases[name] = {
                'measurement_unit': measurement_unit,
                'amount': amount,
            }
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="shoping_list.pdf"')
        pdfmetrics.registerFont(TTFont('GOST', 'GOST type A.ttf', 'UTF-8'))
        pdf = canvas.Canvas(response)
        pdf.setFont('GOST', 40)
        pdf.setFillColor(colors.black)
        pdf.drawCentredString(300, 770, 'Список покупок')
        pdf.setFillColor(colors.black)
        pdf.setFont('GOST', 24)
        height = 700
        for name, data in purchases.items():
            pdf.drawString(
                60,
                height,
                f"- {name} ({data['measurement_unit']}) - {data['amount']}"
            )
            height -= 25
            if height == 50:
                pdf.showPage()
                pdf.setFont('Neocyr', 24)
                height = 700
        pdf.showPage()
        pdf.save()
        return response
