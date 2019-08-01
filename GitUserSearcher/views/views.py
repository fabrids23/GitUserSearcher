from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import permissions, viewsets
from rest_framework.utils import json
from rest_framework.views import APIView

from polls.integrations.api import make_request
from polls.models import GitHubUser


# Esta view va a buscar un usuario de github dependiendo del username que se le pase en la ruta
# class Detail(APIView):



