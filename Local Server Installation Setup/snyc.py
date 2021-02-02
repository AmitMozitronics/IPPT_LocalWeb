from api.models import *
import sys
import datetime
import pytz
from django.utils import timezone


def fun():
    basicmetarialobjects = BasicMetarialStandard.objects.all()
    standardtypeclassificationobjects = StandardTypeClassification.objects.all()
    pressuretypespecificationobjects = PressureTypeSpecification.objects.all()
    pipeouterdiameterobjects = PipeOuterDiameter.objects.all()
    pipelengthobjects = PipeLength.objects.all()

    index = 1
    sync_log = open("snyc.log", "a+")
    for j in PipeData.objects.all():
        sys.stdout.write("Data processing: " + str(index) + "\r")
        sys.stdout.flush()
        t = j.toDic()
        if t["ts"] != '999':
            try:
                c = t["c"]
                if len(c) == 2:
                    outer_diameter_code = c[0]
                    pipe_length_code = c[1]
                elif len(c) == 4:
                    outer_diameter_code = c[0] + c[1]
                    pipe_length_code = c[2] + c[3]
                elif len(c) == 3:
                    if int(c[0] + c[1]) > 19:
                        outer_diameter_code = c[0]
                        pipe_length_code = c[1] + c[2]
                else:
                    outer_diameter_code = c[0] + c[1]
                    pipe_length_code = c[2]
            except Exception as e:
                sync_log.write(str(index) + ": " + str(e) + "\r\n")
                outer_diameter_code = None
                pipe_length_code = None
            try:
                bms = None
                for i in basicmetarialobjects:
                    if i.toDic()['code'] == t["b"][0]:
                        bms = i
                        break
            except Exception as e:
                sync_log.write(str(index) + ": " + str(e) + "\r\n")
                bms = None
            try:
                stc = None
                for i in standardtypeclassificationobjects:
                    idic = i.toDic()
                    if idic['code'] == t["b"][1] and idic["basic_metarial"] == bms:
                        stc = i
                        break
            except Exception as e:
                sync_log.write(str(index) + ": " + str(e) + "\r\n")
                stc = None
            try:
                pts = None
                for i in pressuretypespecificationobjects:
                    idic = i.toDic()
                    if idic['code'] == t["b"][2] and idic["basic_metarial"] == bms and idic["standard_type_classification"] == stc:
                        pts = i
                        break
            except Exception as e:
                sync_log.write(str(index) + ": " + str(e) + "\r\n")
                pts = None
            try:
                pod = None
                for i in pipeouterdiameterobjects:
                    idic = i.toDic()
                    if idic['code'] == outer_diameter_code and idic["standard_type_classification"] == stc:
                        pod = i
                        break
            except Exception as e:
                sync_log.write(str(index) + ": " + str(e) + "\r\n")
                pod = None
            try:
                pl = None
                for i in pipelengthobjects:
                    idic = i.toDic()
                    if idic['code'] == pipe_length_code and idic["standard_type_classification"] == stc:
                        pl = i
                        break
            except Exception as e:
                sync_log.write(str(index) + ": " + str(e) + "\r\n")
                pl = None

            try:
                machine_id = str(t["a"])
            except:
                machine_id = None
            try:
                basic_metarial = bms.toDic().get("basic_metarial")
            except:
                basic_metarial = None
            try:
                standard_type_classification = stc.toDic().get("standard_type_classification")
            except:
                standard_type_classification = None
            try:
                pressure_type_specification = pts.toDic().get("pressure_type_specification")
            except:
                pressure_type_specification = None
            try:
                pod_dic = pod.toDic()
                outer_diameter = float(pod_dic.get("outer_diameter"))
                outer_diameter_unit = str(pod_dic.get("unit"))
            except:
                outer_diameter = None
                outer_diameter_unit = None
            try:
                pl_dic = pl.toDic()
                length = float(pl_dic.get("length"))
                length_unit = str(pl_dic.get("unit"))
            except:
                length = None
                length_unit = None
            try:
                maxweight = int(t["d"])
            except:
                maxweight = None
            try:
                minweight = int(t["e"])
            except:
                minweight = None
            try:
                timestamp = int(t["ts"])
            except:
                timestamp = None
            try:
                count = int(t["count"])
            except:
                count = None
            try:
                weight = int(t["weight"])
            except:
                weight = None
            try:
                if t["ps"] == '0':
                    pass_status = 'Underweight'
                elif t["ps"] == '1':
                    pass_status = 'Overweight'
                elif t["ps"] == '2':
                    pass_status = 'Passed'
            except:
                pass_status = None
            try:
                site_time = datetime.datetime.fromtimestamp(
                    timestamp, tz=pytz.timezone("Asia/Kolkata"))
            except:
                site_time = None
            try:
                shift = t["shift"]
            except:
                shift = None
            try:
                if maxweight - weight < 0:
                    weightloss = maxweight - weight
                    weightgain = 0
                else:
                    weightgain = maxweight - weight
                    weightloss = 0
            except:
                weightgain = None
                weightloss = None
            try:
                sync_log.write(str(index) + ": " + str(machine_id) + ' ' + str(basic_metarial) + ' ' + str(standard_type_classification) + ' ' + str(pressure_type_specification) + ' ' + str(outer_diameter) + ' ' + str(outer_diameter_unit) + ' ' + str(length) + ' ' + str(
                    length_unit) + ' ' + str(timestamp) + ' ' + str(count) + ' ' + str(weight) + ' ' + str(maxweight) + ' ' + str(minweight) + ' ' + str(weightgain) + ' ' + str(weightloss) + ' ' + str(pass_status) + ' ' + str(site_time) + ' ' + str(shift) + ' ' + str("\r\n"))
                PipeDataProcessed.objects.create(machine_id=machine_id, basic_metarial=basic_metarial, standard_type_classification=standard_type_classification, pressure_type_specification=pressure_type_specification, outer_diameter=outer_diameter, outer_diameter_unit=outer_diameter_unit,
                                                 length=length, length_unit=length_unit, timestamp=timestamp, count=count, weight=weight, maxweight=maxweight, minweight=minweight, weightgain=weightgain, weightloss=weightloss, pass_status=pass_status, site_time=site_time, shift=shift)
            except Exception as identifier:
                #print(machine_id, basic_metarial, standard_type_classification, pressure_type_specification, outer_diameter, outer_diameter_unit, length, length_unit, timestamp, count, weight, maxweight, minweight, weightgain, weightloss, pass_status, site_time, shift)
                sync_log.write(str(index) + ": " + str(identifier) + "\r\n")
        index += 1
    sync_log.close()
