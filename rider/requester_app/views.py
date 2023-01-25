from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from requester_app.models import Request, Requester, AppliedRequest
from requester_app.utils import filter_by, check_for_application
from rider_app.models import Rider
from datetime import datetime, timedelta
from django.http import JsonResponse
import uuid

@csrf_exempt
@require_http_methods(['POST'])
def create_request(request):
    """
        Creates Asset Transportation Request (For Requester)

        Parameter
        ---------
        request_id : UUID: unique ID for each request generated
        requester_id: int: special ID given to requester to track user specific requests
        source: str: source location of transportation
        destination: str: destination location of transportation
        datetime: datetime: time of transportation
        quantity: int: nunber of assets
        asset_type: enum: type of asset
        sensitivity: enum: sensitivity of asset
    """
    payload = json.loads(request.body.decode('utf-8'))
    request_id = uuid.uuid4()
    requester_id = payload.get('requester_id')
    source = payload.get('source')
    destination = payload.get('destination')
    datetime_str = payload.get('datetime')
    quantity = payload.get('quantity')
    asset_type = payload.get('asset_type')
    sensitivity = payload.get('sensitivity')

    datetime_object = datetime.strptime(datetime_str, '%d/%m/%y %H:%M:%S')
    timestamp = datetime_object.timestamp()
    new_request = Request(
        request_id = request_id,
        source = source,
        destination = destination,
        datetime = datetime_object,
        timestamp = timestamp,
        quantity = quantity,
        asset_type = asset_type,
        sensitivity = sensitivity
    )
    new_request.save()

    new_requester = Requester(
        requester_id = requester_id,
        request_id = new_request
    )
    new_requester.save()

    return JsonResponse({"status_code": 200})

@require_http_methods(['GET'])
def get_requester_requests(request, requester_id):

    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    status = request.GET['status']
    asset_type = request.GET['asset_type']
    sortby = request.GET['sortby']

    request_id_list = []
    requester_query_set = Requester.objects.filter(requester_id=requester_id).values()
    for req in requester_query_set:
        request_id_list.append(req['request_id_id'])

    requests_list = []
    order = "datetime" if sortby == "ASC" else "-datetime" 
    all_request = Request.objects.all()

    current_timestamp = datetime.now().timestamp()
    for req in all_request:
        if req.timestamp <= current_timestamp:
            req.status = "EX"
            req.save()
    requests_query_set = Request.objects.filter(request_id__in = request_id_list).order_by(order).values()[offset:limit]

    for req in requests_query_set:
        requests_list.append(req)

    requests_list = filter_by(status, asset_type, requests_list)

    response = {
        "request_list": requests_list
    }
    return JsonResponse(response, content_type='application/json', status=200)

@require_http_methods(['GET'])
def get_match(request, request_id):
    
    request_data = Request.objects.get(request_id=request_id)
    requester = Requester.objects.get(request_id=request_id)
    request_quantity = request_data.quantity
    request_source = request_data.source
    request_destination = request_data.destination


    start = (request_data.datetime - timedelta(hours=12)).timestamp()
    end = (request_data.datetime + timedelta(days=1)).timestamp()
    rider_query_set = Rider.objects.filter(
        quantity__gte=request_quantity,
        timestamp__range=(start, end),
        source__contains=request_source,
        destination__contains=request_destination).values()
    
    applied_rides = AppliedRequest.objects.filter(requester_id=requester.id)

    ride_list = check_for_application(rider_query_set, applied_rides)

    response = {
        "request_id": request_id,
        "requester_id": requester.requester_id,
        "request_list": ride_list
    }
    return JsonResponse(response, content_type='application/json', status=200)

@csrf_exempt
@require_http_methods(['POST'])
def apply(request):
    payload = json.loads(request.body.decode('utf-8'))
    rider_id = payload.get('rider_id')
    request_id = payload.get('request_id')

    rider = Rider.objects.get(rider_id=rider_id)
    requester = Requester.objects.get(request_id_id=request_id)
    request_to_apply = Request.objects.get(request_id=request_id)

    if rider.quantity < request_to_apply.quantity:
        return JsonResponse({"status_code": 400})

    rider.quantity -= request_to_apply.quantity
    rider.save()
    applied_ride = AppliedRequest(rider_id=rider, requester_id=requester)
    applied_ride.save()

    response = {
        "response_message": "applied successfully"
    }

    return JsonResponse(response, content_type='application/json', status=200)

