from authentication.models import UserManager, User
from authentication.serializers import UserRegistrationSerializer, UserSerializer, UserLoginSerilizer
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import  login, logout, authenticate
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from paramettre.models import Demandeconventions, Formincidents, Cartartisants
from django.contrib.auth.decorators import login_required
from  django.views.decorators.cache import cache_control
from django.shortcuts import render
from django_pandas.io import read_frame
from django.db.models import Sum, F, Count
from django.db.models.functions import TruncMonth
from modules_externe.utils import get_plot
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator
import base64
from io import BytesIO
from django.core.exceptions import ValidationError
import requests
import json
from django.core import serializers
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from authentication.serializers import UserRegistrationSerializer, UserSerializer, UserLoginSerilizer
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from technique.forms import *
from django.core.serializers import serialize
from modules_externe.api_enrolment import get_data_by_api_enrolement, get_api_data_id_enrolement
from modules_externe.api_convention import get_data_by_api_convention, get_api_data_id_convention
from modules_externe.api_accident import get_data_by_api_accident, get_api_data_id_accident
from modules_externe.api_rapport import get_data_by_api_rapport, get_api_data_id_rapport
from modules_externe.api_url import FICHE_ENROLMENT_URL, FICHE_CONVENTION_URL, FICHE_ACCIDENT_URL, FICHE_RAPPORT_URL
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import csv
from django.views.generic import View

