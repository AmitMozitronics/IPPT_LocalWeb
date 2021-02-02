import sys
import datetime

import requests as httpFetchRequests

from django.conf import settings

from api.models import PipeData

def check_all_field_is_not_empty_pipedata(pipeDataObj):
    if pipeDataObj.mid != '' and pipeDataObj.b != '' and pipeDataObj.c != '' and pipeDataObj.d != '' and pipeDataObj.e != '' and pipeDataObj.ts != '' and pipeDataObj.count != '' and pipeDataObj.weight != '' and pipeDataObj.ps != '' and pipeDataObj.site_time != '' and pipeDataObj.shift != '':
        return True
    return False

def sync_method(mid=None):
    if mid is None:
        pipeDataObjs = PipeData.objects.filter(synced=False)
    else:
        pipeDataObjs = PipeData.objects.filter(mid__in=mid, synced=False)
    sncpd = 0
    not_sncpd = 0    
    for pipeDataObj in pipeDataObjs:
        if check_all_field_is_not_empty_pipedata(pipeDataObj):
            apiUrl = "http://pipetrackerlive.com/api/Test/get_synced_data?a={0}&b={1}&c={2}&d={3}&e={4}&ts={5}&count={6}&weight={7}&ps={8}&site_time={9}&shift={10}"
            apiUrl = apiUrl.format(pipeDataObj.mid, pipeDataObj.b, pipeDataObj.c, pipeDataObj.d, pipeDataObj.e, pipeDataObj.ts, pipeDataObj.count, pipeDataObj.weight, pipeDataObj.ps, pipeDataObj.site_time, pipeDataObj.shift)
            fetchData = httpFetchRequests.get(url = apiUrl)
            if fetchData.status_code != 200:
                raise Exception("Bad network request")
        else:
            not_sncpd += 1
        pipeDataObj.synced = True
        pipeDataObj.save()
        sys.stdout.write("Data processing: " + str(sncpd) + "\r")
        sys.stdout.flush()
        sncpd += 1    
    sncpd_file = open(settings.BASE_DIR + '/' + "sync.log" , "a")
    sncpd_file.write(str(datetime.datetime.now()) + ": Data synced: " + str(sncpd) + "; Not synced: " + str(not_sncpd) + "\n")
    sncpd_file.close()
    if mid is not None:
        return sncpd