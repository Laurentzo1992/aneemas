from django.shortcuts import redirect, render
from authentication.models import UserManager, User
from authentication.serializers import UserRegistrationSerializer, UserSerializer, UserLoginSerilizer
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import  login, logout, authenticate
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from paramettre.models import Demandeconventions, Formincidents, Cartartisants
from django.contrib.auth.decorators import login_required
from  django.views.decorators.cache import cache_control
from django.shortcuts import render
from django_pandas.io import read_frame
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from modules_externe.utils import get_plot
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator
import base64
from io import BytesIO
from django.core.exceptions import ValidationError





