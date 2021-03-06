from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from portal.models import LabourRequest, LABOUR_STATE_CHOICES


@login_required
def labour_list_finished(request):
    state_finished = LABOUR_STATE_CHOICES[4]
    state_paid = LABOUR_STATE_CHOICES[7]

    filter_states = (Q(state__exact=state_finished) | Q(state__exact=state_paid)) & \
                    (Q(worker__user__id=request.user.id) | Q(creator__user__id=request.user.id))

    labour_request_list = LabourRequest.objects.filter(filter_states)
    title = 'My finished labours'
    context = {'labour_request_list': labour_request_list, 'title': title}
    return render(request, 'labour_list.html', context)
