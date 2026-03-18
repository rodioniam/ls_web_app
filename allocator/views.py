from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import Card, Session


def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')
    elif request.method == 'POST':
        if any(not name for name in request.POST.values()) or any(len(name) > 10 for name in request.POST.values()):
            return render(request, 'home.html')
        else:
            session = Session.objects.create()
            Card.objects.create(
                session=session,
                name=request.POST['fcard']
            )
            Card.objects.create(
                session=session,
                name=request.POST['scard']
            )
        return redirect('index', session_id=session.id)


def index(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    cards = Card.objects.filter(session=session)
    total_used = sum(
        c.points for c in Card.objects.filter(session=session))
    points_remaining = session.total_points - total_used
    return render(request, 'allocation.html', {'cards': cards, 'session': session, 'points_remaining': points_remaining})


def change_points(request, card_id, action):
    card = get_object_or_404(Card, id=card_id)
    session = card.session

    if request.method == "POST":
        total_used = sum(
            c.points for c in Card.objects.filter(session=session))

        if action == 'add':
            if total_used < session.total_points:
                card.points += 1
                card.save()

        if action == 'remove':
            if card.points > 0:
                card.points -= 1
                card.save()

    if request.headers.get('HX-Request'):
        total_used = sum(
            c.points for c in Card.objects.filter(session=session))
        points_remaining = session.total_points - total_used

        card_html = render_to_string(
            'card.html', {'card': card}, request=request)
        counter_html = render_to_string('points_remaining.html', {
                                        'points_remaining': points_remaining}, request=request)

        return HttpResponse(card_html + counter_html)

    return redirect('index', session_id=session.id)
