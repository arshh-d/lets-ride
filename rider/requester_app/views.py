""" views for requester_app """
import uuid
import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest
from requester_app.models import Request, Requester, AppliedRequest
from requester_app.utils import filter_by, check_for_application
from rider_app.models import Rider
from rider.utils import handle_exc
from loguru import logger


@csrf_exempt
@require_http_methods(['POST'])
def create_request(request: HttpRequest) -> JsonResponse:
    """Create a new Asset transportation request

    Args:
        request (HttpRequest): request payload

    Returns:
        JsonResponse: creation status
    """
    payload = json.loads(request.body.decode('utf-8'))
    request_id = uuid.uuid4()
    datetime_str = payload.get('datetime')
    requester_id = payload.get('requester_id')

    logger.info(
        f"Creating a new request with id: {request_id}, for requester: {requester_id}")
    datetime_object = datetime.strptime(datetime_str, '%d/%m/%y %H:%M:%S')
    timestamp = datetime_object.timestamp()
    new_request = Request(
        request_id=request_id,
        source=payload.get('source'),
        destination=payload.get('destination'),
        datetime=datetime_object,
        timestamp=timestamp,
        quantity=payload.get('quantity'),
        asset_type=payload.get('asset_type'),
        sensitivity=payload.get('sensitivity')
    )
    new_request.save()
    logger.info(
        f"Created a new request with id: {request_id}, for requester: {requester_id}")
    new_requester = Requester(
        requester_id=requester_id,
        request_id=new_request
    )
    new_requester.save()
    logger.debug(
        f"Added mapping for request id: {request_id} to requester: {requester_id}")
    response = {
        "msg": "request created successfully",
        "request_id": request_id
    }
    return JsonResponse(response, status=200)


@require_http_methods(['GET'])
def get_requester_requests(request: HttpRequest, requester_id: int) -> JsonResponse:
    """Lists all the request created by a requester.

    Args:
        request (HttpRequest): request payload
        requester_id (int): special id assigned to each requester.

    Returns:
        JsonResponse: all request created by the requester. 
    """
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    status = request.GET['status']
    asset_type = request.GET['asset_type']
    sortby = request.GET['sortby']

    logger.info(f"Fetching requests for requester: {requester_id}")

    request_id_list = []
    requester_query_set = Requester.objects.filter(
        requester_id=requester_id).values()
    for req in requester_query_set:
        request_id_list.append(req['request_id_id'])

    logger.debug(f"Fetched all request ids for requester: {requester_id}")

    requests_list = []
    order = "datetime" if sortby == "ASC" else "-datetime"
    all_request = Request.objects.all()

    current_timestamp = datetime.now().timestamp()
    for req in all_request:
        if req.timestamp <= current_timestamp:
            req.status = "EX"
            req.save()
    requests_query_set = Request.objects.filter(
        request_id__in=request_id_list).order_by(order).values()[offset:limit]

    for req in requests_query_set:
        requests_list.append(req)

    logger.debug(f"Fetched all requests for requester: {requester_id}")

    requests_list = filter_by(status, asset_type, requests_list)
    logger.info(
        f"Filtered all requests matching the search criteria for requester: {requester_id}")
    response = {
        "request_list": requests_list
    }
    return JsonResponse(response, content_type='application/json', status=200)


@require_http_methods(['GET'])
def get_match(request: HttpRequest, request_id: uuid) -> JsonResponse:
    """List all riders relevant to the given request_id.

    Args:
        request (HttpRequest): request payload
        request_id (uuid): request uuid

    Returns:
        JsonResponse: returns matching rides for a request
    """
    try:
        request_data = Request.objects.get(request_id=request_id)
        requester = Requester.objects.get(request_id=request_id)
    except Exception as exception:
        response = handle_exc(exception)
        logger.error(
            f"Unable to fetch relevant requests for request id: {request_id}, cause: {exception}")
        return JsonResponse(response)

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
    logger.info(f"Fetched all riders relevant to request_id: {request_id}")

    logger.info(
        f"checking if requester: {requester.requester_id} has already applied for the request: {request_id}")
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
def apply(request: HttpRequest) -> JsonResponse:
    """Apply to the given rider with provides request_id.

    Args:
        request (HttpRequest): request payload with rider_id and request_id

    Returns:
        JsonResponse: application status
    """
    payload = json.loads(request.body.decode('utf-8'))
    rider_id = payload.get('rider_id')
    request_id = payload.get('request_id')

    try:
        rider = Rider.objects.get(rider_id=rider_id)
        requester = Requester.objects.get(request_id_id=request_id)
        request_to_apply = Request.objects.get(request_id=request_id)
    except Exception as exception:
        response = handle_exc(exception)
        logger.error(
            f"unable to apply for rider: {rider_id}, cause: {exception}")
        return JsonResponse(response, status=400)

    logger.info(
        f"checking if requster no. of asset is valid for rider: {rider_id}")
    if rider.quantity < request_to_apply.quantity:
        logger.error(
            f"asset request: {request_to_apply.quantity} not sufficient for completing the application for rider: {rider_id}")
        return JsonResponse({"msg": "asset limit not sufficient"}, status=400)

    rider.quantity -= request_to_apply.quantity
    rider.save()
    applied_ride = AppliedRequest(rider_id=rider, requester_id=requester)
    applied_ride.save()
    logger.info(
        f"request: {request_id} application successful for rider: {rider_id}")
    response = {
        "response_message": "applied successfully"
    }
    return JsonResponse(response, content_type='application/json', status=200)
