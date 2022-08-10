from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from http import HTTPStatus
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.pdfgen import canvas

from recipes.models import (Carts, Favorites, Follows, Ingredients,
                            IngredientsInRecipe, Recipes, Tags)
from users.models import User
from .serializers import (CartsSerializer, FollowsSerializer,
                          IngredientsSerializer, RecipesSerializer,
                          TagsSerializer, UserSerializer, UserCreateSerializer)
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .filters import IngredientsFilter, RecipesFilter


class UserViewSet(viewsets.ModelViewSet):
    """Users' viewset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer

    @action(
        methods=['POST'],
        detail=False
    )
    def set_password(self, request):
        """Password changing."""
        current_user = self.request.user
        if not current_user.check_password(
            request.data.get('current_password')
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
        follows = Follows.objects.filter(user=user)
        pages = self.paginate_queryset(follows)
        serializer = FollowsSerializer(
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
            if Follows.objects.filter(
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
            follow = Follows.objects.create(
                user=user,
                author=author
            )
            serializer = FollowsSerializer(
                follow,
                context={'request': request},
            )
            return Response(serializer.data)
        follow = Follows.objects.filter(
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


class UserMeViewSet(viewsets.ModelViewSet):
    """Users' viewset."""
    serializer_class = UserSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        return User.objects.filter(id=current_user.id)


class TagsViewSet(viewsets.ModelViewSet):
    """Tags' viewset."""
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
    permission_classes = [IsAdminOrReadOnly]


class IngredientsViewSet(viewsets.ModelViewSet):
    """Ingredients' viewset."""
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ('^name',)
    pagination_class = None
    filter_backends = IngredientsFilter


class RecipesViewSet(viewsets.ModelViewSet):
    """Ingredients' viewset."""
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    paginator_class = LimitOffsetPagination
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = RecipesFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipes, pk=pk)
        cart = Carts.objects.filter(
                user=request.user,
                recipe=recipe
        )
        if request.method == 'POST':
            if cart.exists():
                return Response(
                    {'errors': 'Этот рецепт уже есть в списке покупок'},
                    status=HTTPStatus.BAD_REQUEST,
                )
            Carts.objects.create(
                user=request.user,
                recipes=recipe
            )
            serializer = CartsSerializer(recipe)
            return Response(serializer.data)
        if not cart.exists():
            return Response(
                {'errors': 'Этого рецепта нет в списке покупок'},
                status=HTTPStatus.BAD_REQUEST,
            )
        cart.delete()
        return Response(status=HTTPStatus.NO_CONTENT)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipes, pk=pk)
        favorite_recipe = Favorites.objects.filter(
            user=request.user,
            recipe=recipe
        )
        if request.method == 'POST':
            if favorite_recipe.exists():
                return Response(
                    {'errors': 'Рецепт уже в избранном'},
                    status=HTTPStatus.BAD_REQUEST
                )
            Favorites.objects.create(user=request.user, recipe=recipe)
            serializer = CartsSerializer(recipe)
            return Response(serializer.data)
        if not favorite_recipe.exists():
            return Response(
                {'errors': 'Такого рецепта нет в Избранном'},
                status=HTTPStatus.BAD_REQUEST,
            )
        favorite_recipe.delete()
        return Response(status=HTTPStatus.NO_CONTENT)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        user = request.user
        shopping_list = {}
        ingredients = IngredientsInRecipe.objects.filter(
            recipe__cart__user=user).values_list(
                'ingredient__name',
                'amount',
                'ingredient__measurement_unit',
                named=True)
        for ingredient in ingredients:
            name = ingredient.ingredient__name
            measurement_unit = ingredient.ingredient__measurement_unit
            amount = ingredient.amount
            if name not in shopping_list:
                shopping_list[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount,
                }
            else:
                shopping_list[name]['amount'] += amount
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
        for name, data in shopping_list.items():
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
