from django.shortcuts import render, get_object_or_404, redirect
from .models import Card, Session


def index(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    cards = Card.objects.filter(session=session)
    return render(request, 'allocation.html', {'cards': cards, 'session': session})


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
            # session.total_points -= 1
            # session.save()

        if action == 'remove':
            if card.points > 0:
                card.points -= 1
                card.save()
            # session.total_points += 1
            # session.save()

    return redirect('index', session_id=session.id)
