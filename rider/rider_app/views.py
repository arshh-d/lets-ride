from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from rider_app.models import Rider
from datetime import datetime
from loguru import logger
import uuid


@csrf_exempt
@require_http_methods(['POST'])
def create_ride(request):
    payload = json.loads(request.body.decode('utf-8'))
    source = payload.get('source')
    destination = payload.get('destination')
    datetime_str = payload.get('datetime')
    travel_medium = payload.get('travel_medium')
    quantity = payload.get('quantity')

    rider_id = uuid.uuid4()
    logger.info(f"creating new rider: {rider_id}")

    datetime_object = datetime.strptime(datetime_str, '%d/%m/%y %H:%M:%S')
    timestamp = datetime_object.timestamp()
    new_rider = Rider(rider_id=rider_id,source=source, destination=destination,datetime=datetime_object,timestamp=timestamp,travel_medium=travel_medium,quantity=quantity)
    new_rider.save()

    logger.info(f"created new rider: {rider_id}")
    return JsonResponse({"msg": "ride created"}, status=200)
