from django.shortcuts import render, get_object_or_404
from .models import Card, Session


def index(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    cards = Card.objects.filter(session=session)
    return render(request, 'allocation.html', {'cards': cards, 'session': session})
