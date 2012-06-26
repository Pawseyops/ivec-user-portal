# -*- coding: utf-8 -*-
import operator
from ivecallocation.allocation.models import *
from django.contrib import admin
from django import forms
from admin_forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.db.models import Q


def test():
    pass

def get_querylist(request=None):
    # TODO hardcoded
    
    try:
        reviewers_astronomy = Group.objects.get(name='reviewers_astronomy')
    except ObjectDoesNotExist, e:
        reviewers_astronomy = None

    try:
        reviewers_geosciences = Group.objects.get(name='reviewers_geosciences')
    except ObjectDoesNotExist, e:
        reviewers_geosciences = None

    try:
        reviewers_directors = Group.objects.get(name='reviewers_directors')
    except ObjectDoesNotExist, e:
        reviewers_directors = None

    try:
        reviewers_partner = Group.objects.get(name='reviewers_partner')
    except ObjectDoesNotExist, e:
        reviewers_partner = None

    try:
        reviewers_national = Group.objects.get(name='reviewers_national')
    except ObjectDoesNotExist, e:
        reviewers_national = None


    query_list = []

    # build up query objects and test if user is a reviewer in any area
    if reviewers_astronomy and reviewers_astronomy in request.user.groups.all():
        query_list.append(Q(priority_area__code='astronomy'))

    if reviewers_geosciences and reviewers_geosciences in request.user.groups.all():
        query_list.append(Q(priority_area__code='geosciences'))

    if reviewers_directors and reviewers_directors in request.user.groups.all():
        query_list.append(Q(priority_area__code='director'))

    if reviewers_partner and reviewers_partner in request.user.groups.all():
        query_list.append(Q(priority_area__code='partner'))

    if reviewers_national and reviewers_national in request.user.groups.all():
        query_list.append(Q(priority_area__code='national'))

    #assert(False)
    return query_list
