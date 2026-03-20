from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import Card, Session, Multiplier, CardMultiplier


def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')
    elif request.method == 'POST':
        fcard = request.POST['fcard']
        scard = request.POST['scard']
        if not fcard or not scard or len(fcard) > 10 or len(scard) > 10:
            return render(request, 'home.html')
        else:
            session = Session.objects.create()
            Card.objects.create(
                session=session,
                name=fcard
            )
            Card.objects.create(
                session=session,
                name=scard
            )
        return redirect('index', session_id=session.id)


def index(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    cards = Card.objects.filter(session=session)
    card_1 = cards[0]
    card_2 = cards[1]
    multipliers = Multiplier.objects.all()
    card_1_multipliers = CardMultiplier.objects.filter(
        parent_card_id=card_1.id)
    card_2_multipliers = CardMultiplier.objects.filter(
        parent_card_id=card_2.id)
    card_1_result = card_1.points
    card_2_result = card_2.points
    for m in card_1_multipliers:
        card_1_result *= m.assigned_mults.value
    for m in card_2_multipliers:
        card_2_result += m.assigned_mults.value

    total_used = sum(c.points for c in cards)
    points_remaining = session.total_points - total_used

    return render(request,
                  'allocation.html',
                  {
                      'card_1': card_1,
                      'card_2': card_2,
                      'session': session,
                      'points_remaining': points_remaining,
                      'multipliers': multipliers,
                      'card_1_result': card_1_result,
                      'card_2_result': card_2_result
                  }
                  )


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

        card_multipliers = CardMultiplier.objects.filter(parent_card=card)
        card_result = card.points

        for m in card_multipliers:
            card_result *= m.assigned_mults.value

        card_html = render_to_string(
            'card.html', {'card': card, 'points': card_result}, request=request)
        counter_html = render_to_string('points_remaining.html', {
                                        'points_remaining': points_remaining}, request=request)

        return HttpResponse(card_html + counter_html)

    return redirect('index', session_id=session.id)


def reset_points(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    cards = Card.objects.filter(session=session)
    card_multipliers = CardMultiplier.objects.filter(parent_card__in=cards)

    if request.method == "POST":
        for card in cards:
            card.points = 0
            card.save()
        card_multipliers.delete()

    return redirect('index', session_id=session.id)


def assign_multiplier(request, session_id):
    card_id = request.POST['card_id']
    multiplier_id = request.POST['multiplier_id']
    card = get_object_or_404(Card, id=card_id)
    multiplier = get_object_or_404(Multiplier, id=multiplier_id)

    if request.POST.get('left-card') or request.POST.get('right-card'):
        CardMultiplier.objects.create(
            parent_card=card,
            assigned_mults=multiplier
        )
        card_multipliers = CardMultiplier.objects.filter(parent_card=card)
        card_result = card.points
        for m in card_multipliers:
            card_result *= m.assigned_mults.value
        return render(request, 'card.html', {'card': card, 'points': card_result})
    else:
        CardMultiplier.objects.filter(
            parent_card=card,
            assigned_mults=multiplier
        ).delete()

        card_multipliers = CardMultiplier.objects.filter(parent_card=card)
        card_result = card.points
        for m in card_multipliers:
            card_result *= m.assigned_mults.value
        return render(request, 'card.html', {'card': card, 'points': card_result})
