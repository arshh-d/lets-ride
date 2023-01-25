def filter_by_status(attribute, dict_list):
    res = []
    for ele in dict_list:
        if ele['status'] == attribute:
            res.append(ele)
    return res

def filter_by_asset_type(attribute, dict_list):
    res = []
    for ele in dict_list:
        if ele['asset_type'] == attribute:
            res.append(ele)
    return res

def filter_by_status_asset_type(status, asset_type, dict_list):
    res = []
    for ele in dict_list:
        if ele['asset_type'] == asset_type and ele['status'] == status:
            res.append(ele)
    return res

def filter_by(status, asset_type, dict_list):
    if status and not asset_type:
        return filter_by_status(status, dict_list)
    elif asset_type and not status:
        return filter_by_asset_type(asset_type, dict_list)
    elif status and asset_type:
        return filter_by_status_asset_type(status, asset_type, dict_list)
    else:
        return dict_list

def check_for_application(rider_query_set, applied_rides):

    applied_list = []
    for ride in applied_rides:
        applied_list.append(ride.rider_id.rider_id)

    ride_list = []
    for ride in rider_query_set:
        if ride['rider_id'] in applied_list:
            ride['applied'] = True
        else:
            ride['applied'] = False
        ride_list.append(ride)

    return ride_list