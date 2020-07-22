from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


import json

from .models import Category, Products, ProductCategory
from .serializers import CategorySerializer, ProductSerializer
from .forms import CategoryForm, ProductForm



class CategoryAPI(APIView):
    """
    List all category, or create a new category.
    """
    permission_classes = [IsAuthenticated]


    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        cat_obj = Category.objects.filter(is_active=True).all()
        serializer = CategorySerializer(cat_obj,many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        To create categories.
        :param request:
        :param format:
        :return: Status 200 on success else 404 for bad request
        """
        serializer = CategorySerializer(data=request.data)
        payload = request.data
        form = CategoryForm(payload)
        if form.is_valid():
            if serializer.is_valid():
                get_parent_id = 0
                name = form.data.get('name')
                subcategory_of = form.data.get('subcategory_of')
                if name and subcategory_of:
                    get_parent_id = Category.objects.filter(name__iexact=subcategory_of.strip().lower()).first()
                    if get_parent_id:
                        get_parent_id = get_parent_id.id
                    else:
                        return Response({'Warning': 'Please create first Parent Category.'}, status=status.HTTP_400_BAD_REQUEST)
                serializer.validated_data['parent_id'] = get_parent_id
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductAPI(APIView):
    """
    List all product, or create a new product.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        cat_obj = Products.objects.filter(is_active=True).all()
        product_list = []
        for each in cat_obj:
            product_list.append({each.id:each.name})
        return Response(product_list, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        payload = request.data
        form = ProductForm(payload)
        if form.is_valid():
            if serializer.is_valid():
                if payload.get("categories"):
                    prod = Products.objects.create(name=payload.get("name"))
                    cat_not_exist_list = []
                    cat_exist_list = []
                    for each_cat in payload.get("categories"):
                        check_cat_exist = Category.objects.filter(id=each_cat).first()
                        if check_cat_exist:
                            prod_cat = ProductCategory.objects.create(category_id=each_cat, product_id=prod.id)
                            cat_exist_list.append(each_cat)
                        else:
                            cat_not_exist = cat_not_exist_list.append(each_cat)
                    if cat_not_exist_list:
                        context = {'message':'successfully product {0} created'.format(payload.get("name")),
                                   'product attached to categories':cat_exist_list,
                                   'error':'Not creates for categories {0}'.format(cat_not_exist_list)}
                    else:
                        context = {'message':'successfully product {0} created'.format(payload.get("name")),
                                   'product attached to categories':cat_exist_list}
                    return Response(context, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class GetPrductsByCategoryAPI(APIView):
    """
    List all product, by category.
    """
    permission_classes = [IsAuthenticated]


    def get(self, request, category_id, format=None):
        prod_list = ProductCategory.objects.filter(category_id=category_id).values('product_id')
        product_list = Products.objects.filter(id__in=prod_list).values('name')
        cat_obj = Category.objects.filter(id=category_id).first()
        prod_dict = []
        if cat_obj.parent_id:
            parent_cat = Category.objects.filter(id=cat_obj.parent_id).first()
            prod_dict.append({parent_cat.name:{cat_obj.name:product_list}})
        else:
            prod_dict.append({cat_obj.name:product_list})
        return Response(prod_dict , status=status.HTTP_200_OK)

class GetCategoryByProductAPI(APIView):
    """
    List all category, by product.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id, format=None):
        prod_list = ProductCategory.objects.filter(product_id=product_id).values('category_id')
        prod_obj = Products.objects.filter(id=product_id).first()
        cat_list = Category.objects.filter(id__in=prod_list).values('id','name')
        prod_dict = [{'product_name':prod_obj.name,'categories':cat_list}]
        return Response(prod_dict , status=status.HTTP_200_OK)

class UpdateProductAPI(APIView):
    """
    List all product, or create a new product.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        cat_obj = Products.objects.filter(id=id, is_active=True).all()
        product_list = []
        for each in cat_obj:
            product_list.append({each.id:each.name})
        return Response(product_list, status=status.HTTP_200_OK)

    def post(self, request, id, format=None):
        serializer = ProductSerializer(data=request.data)
        payload = request.data
        payload['id'] = id
        form = ProductForm(payload)
        if form.is_valid():
            if serializer.is_valid():
                if payload.get("categories"):
                    prod = Products.objects.filter(id=id).update(name=payload.get('name'), price=payload.get('price'))
                    cat_not_exist_list = []
                    cat_exist_list = []
                    for each_cat in payload.get("categories"):
                        check_cat_exist = Category.objects.filter(id=each_cat).first()
                        if check_cat_exist:
                            if_prod_cat_present = ProductCategory.objects.filter(category_id=each_cat,
                                                                                 product_id=id).first()
                            if if_prod_cat_present:
                                continue
                            prod_cat = ProductCategory.objects.create(category_id=each_cat, product_id=id)
                            cat_exist_list.append(each_cat)
                        else:
                            cat_not_exist = cat_not_exist_list.append(each_cat)
                    if cat_not_exist_list:
                        context = {'message':'successfully product {0} created'.format(payload.get("name")),
                                   'product attached to categories':cat_exist_list,
                                   'error':'Not creates for categories {0}'.format(cat_not_exist_list)}
                    else:
                        context = {'message':'successfully product {0} created'.format(payload.get("name")),
                                   'product attached to categories':cat_exist_list}
                    return Response(context, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
