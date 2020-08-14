from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from projects.models import TicketQR

def check_qr(request):

    # request.user.is_authenticated ?

    ticket_code = request.GET.get('ticket', '')

    if (ticket_code == '' or len(ticket_code) != 16):
      return JsonResponse({ 'success': False, 'error': 'Bad ticket code provided.' })

    ticket = get_object_or_404(TicketQR, validation_code=ticket_code)

    if not request.user.member_of(ticket.project.community.id):
      return JsonResponse({
        'success': False,
        'error': 'User is not a member of \'%s\' community.' % (ticket.project.community.name)})

    response = {
        'name': str(ticket.user),
        'email': ticket.user.email,
        'project': ticket.project.name,
        'code': ticket.validation_code,
        'validated_at': ticket.validated_at,
      }

    if (ticket.validated_at):
      response['error'] = 'Ticket already validated.'
      response['success'] = False
    else:
      response['validated_at'] = ticket.set_validated()
      response['success'] = True

    return JsonResponse(response)

def qr_reader(request):
  return render(request, 'reader.html')
