import base64

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Stone
from django.conf import settings
import qrcode
from io import BytesIO
from .forms import CommentForm, FinderCommentForm
from django.contrib import messages
from django.core.mail import send_mail


def home(request):
    stones = Stone.objects.filter(draft=False).order_by('-id')
    return render(request, 'index.html', {'stones': stones})


def contact(request):
    if request.method == "POST":
        email = request.POST.get("email")
        message = request.POST.get("message")

        subject = f"Wiadomość od {email}"
        body = f"Nadawca: {email}\n\nTreść wiadomości:\n{message}"

        send_mail(
            subject,
            body,
            "kamieniorze.auto@gmail.com",
            ["kamieniorze@gmail.com"],
            fail_silently=False,
        )

        messages.success(request, "Wiadomość została wysłana!")
        return redirect("contact")  # po wysłaniu wraca na stronę kontaktu

    return render(request, "contact.html")


def map(request):
    stones = list(
        Stone.objects.filter(draft=False)
        .values('id', 'latitude', 'longitude', 'title', 'found')
    )
    return render(request, 'map.html', {'stones': stones})


def stone_detail(request, pk):
    stone = get_object_or_404(Stone, pk=pk)
    comments = stone.comments.order_by("-created_at")

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.stone = stone
            comment.save()
            return redirect("stone_detail", pk=stone.pk)
    else:
        form = CommentForm()

    return render(request, "stone_detail.html", {
        "stone": stone,
        "comments": comments,
        "form": form,
    })


def mark_stone_found(request, token, pk):
    stone = get_object_or_404(Stone, token=token)

    if stone.finder_comment is not None:
        return redirect('stone_detail', pk=stone.pk)

    if not stone.found:
        stone.found = True
        from django.utils.timezone import now
        stone.found_at = now()
        stone.save()

    if request.method == "POST":
        form = FinderCommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.stone = stone
            comment.save()
            stone.finder_comment = comment
            stone.save()
            return redirect('stone_detail', pk=stone.pk)
    else:
        form = FinderCommentForm()

    return render(request, 'stone_found.html', {'stone': stone, "form": form})


@staff_member_required
def stone_qr_view(request, pk):
    stone = get_object_or_404(Stone, pk=pk)

    host = settings.SITE_DOMAIN
    url = f"{host}found/{stone.pk}/{stone.token}/"

    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'stone_qr_preview.html', {
        'stone': stone,
        'qr_base64': qr_base64,
        'qr_url': url
    })