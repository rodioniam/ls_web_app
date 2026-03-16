from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import Card, Session


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
        card.refresh_from_db()
        # print(f"DEBUG card.id = {card.id}")
        # print(f"DEBUG card.name = {card.name}")
        total_used = sum(
            c.points for c in Card.objects.filter(session=session))
        points_remaining = session.total_points - total_used

        card_html = render_to_string(
            'card.html', {'card': card}, request=request)
        counter_html = render_to_string('points_remaining.html', {
                                        'points_remaining': points_remaining}, request=request)

        return HttpResponse(card_html + counter_html)

    return redirect('index', session_id=session.id)
