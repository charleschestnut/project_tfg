from django.shortcuts import render
from portal.models import *
from ..forms import RatingForm
from django.db.models import Q
from . import update_avg_rating as update


def worker_rating_create(request, id):
    labour = LabourRequest.objects.get(id=int(id))

    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        context={}
        if rating_form.is_valid():
            labour = LabourRequest.objects.get(id=int(id))
            description = rating_form.cleaned_data['description']
            puntuation = rating_form.cleaned_data['puntuation']
            rater = Profile.objects.get(user_id=request.user.id)
            rated = labour.worker

            rating = WorkerRating(
                puntuation=puntuation,
                description=description,
                labour=labour,
                rater_person=rater,
                rated_person=rated,
            )
            rating.save()
            # TODO: ACTUALIZAMOS LA VALORACIÓN MEDIA DEL RATED
            update.update_avg_rating(rated.user_id, 'WORKER')

            my_ratings_filter = Q(rater_person__id=request.user.id) | Q(rated_person__id=request.user.id)
            my_worker_ratings = WorkerRating.objects.filter(my_ratings_filter)
            context['rating_list'] = my_worker_ratings

            return render(request, 'rating_list.html', context)
    else:
        rating_form = RatingForm()
        rated = labour.worker
        context = {'form': rating_form, 'rated': rated, 'labour_id': labour.id}

    return render(request, 'worker_rating_create.html', context)
