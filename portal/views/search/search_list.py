from django.core.paginator import Paginator
from django.shortcuts import render

from portal.models import *


def search_list(request):
    profession_choices = Profession.objects.all()
    profession_selected = request.GET.get('profession', '')
    city_selected = request.GET.get('city', '')
    rating_order = request.GET.get('rating_order', '')
    min_punctuation = request.GET.get('min_punctuation', '')
    page = request.GET.get('page', 1)
    workers_list = None
    context = {'profession_choices': profession_choices}

    if city_selected or rating_order or min_punctuation or profession_selected:
        if profession_selected:
            workers_list = Profile.objects.filter(professions__pk=profession_selected)

        if city_selected:
            if workers_list is None:
                workers_list = Profile.objects.filter(city__search=city_selected)
            else:
                workers_list = workers_list.filter(city__search=city_selected)
        if min_punctuation:
            if workers_list is None:
                workers_list = Profile.objects.filter(worker_rating_avg__gte=min_punctuation)
            else:
                workers_list = workers_list.filter(worker_rating_avg__gte=min_punctuation)

        if rating_order:
            if workers_list is None:
                workers_list = Profile.objects.order_by('-worker_rating_avg')
            else:
                workers_list = workers_list.order_by('-worker_rating_avg')

        if request.user.id and workers_list:
            workers_list = workers_list.exclude(user_id=request.user.id)

        paginator = Paginator(workers_list, 2)
        workers_list = paginator.get_page(page)

    context['workers_list'] = workers_list
    return render(request, 'search_list.html', context)
