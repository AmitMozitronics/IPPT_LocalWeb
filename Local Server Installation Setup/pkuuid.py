from api.models import *                                                                                                              
import sys

index = 1
pd = PipeData.objects.all()                                                                                                           
for i in pd:
    sys.stdout.write("Data processing: " + str(index) + "\r")
    sys.stdout.flush()
    index += 1
    t = i.__dict__ 
    PipeData1.objects.create(mid=t["mid"], b = t["b"], c = t["c"], d = t["d"], e = t["e"], ts = t["ts"], count = t["count"], weight = t["weight"], ps = t["ps"], site_time = t["site_time"], shift = t["shift"]) 

index = 1
pdp = PipeDataProcessed.objects.all()
for i in pdp:
    sys.stdout.write("Data processing: " + str(index) + "\r")
    sys.stdout.flush()
    index += 1
    t = i.__dict__
    PipeDataProcessed1.objects.create(machine_id=t["machine_id"], basic_metarial=t["basic_metarial"], standard_type_classification=t["standard_type_classification"], pressure_type_specification=t["pressure_type_specification"], outer_diameter=t["outer_diameter"], outer_diameter_unit=t["outer_diameter_unit"], length = t["length"], length_unit = t["length_unit"], timestamp = t["timestamp"], count = t["count"], weight = t["weight"], maxweight = t["maxweight"], minweight = t["minweight"], weightgain = t["weightgain"], weightloss = t["weightloss"], pass_status = t["pass_status"], site_time = t["site_time"], shift = t["shift"])

