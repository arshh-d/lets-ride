from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from rider_app.models import Rider
from datetime import datetime

@csrf_exempt
@require_http_methods(['POST'])
def create_ride(request):
    payload = json.loads(request.body.decode('utf-8'))
    source = payload.get('source')
    destination = payload.get('destination')
    datetime_str = payload.get('datetime')
    travel_medium = payload.get('travel_medium')
    quantity = payload.get('quantity')

    datetime_object = datetime.strptime(datetime_str, '%d/%m/%y %H:%M:%S')
    timestamp = datetime_object.timestamp()
    new_rider = Rider(source=source, destination=destination,datetime=datetime_object,timestamp=timestamp,travel_medium=travel_medium,quantity=quantity)
    new_rider.save()

    return JsonResponse({"status_code": 200})
