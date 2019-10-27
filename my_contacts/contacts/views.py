from django.shortcuts import render, get_object_or_404, Http404
from django.core.paginator import Paginator
from .models import Contact

def index(request):
    contacts = Contact.objects.order_by('-id').filter(
        show=True
    )

    paginator = Paginator(contacts, 2)
    page = request.GET.get('p')
    contacts = paginator.get_page(page)

    return render(request, 'contacts/index.html', {
        'contacts': contacts
    })

def see_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if not contact.show:
        raise Http404()

    return render(request, 'contacts/see_contact.html', {
        'contact': contact
    })
