import pymongo
import json
import os
import time
import pymatgen as mg
from . import GeometryOptimization as go
from . import VASP_output_BandStructure as bs
from . import StaticCalculation as sc

from . import ElasticProperties as ep
from . import MagneticProperties as mp
from pymatgen.io.vasp import outputs, inputs
from pymatgen.core.structure import Structure
from pymatgen.vis.structure_vtk import StructureVis
from django.shortcuts import render
from django.http import HttpResponse

def database(request):
    myclient = pymongo.MongoClient("mongodb://localhost:27017")
    mydb = myclient["materials"]
    my_col_materials = mydb["PureElements"]
    all = my_col_materials.find()
    pure_list = []
    for each in all:
        pure_list.append(each["sites"][0]["species"][0]["element"])
    pure_list = set(pure_list)
    pure_list = list(pure_list)
    pure_list.sort()
    myclient.close()
    return render(request, "database.html", {"pure_list": pure_list})

def select(request):
    if request.is_ajax():
        name = request.POST.get("element_name")
        # myclient = pymongo.MongoClient("mongodb://45.76.29.47:27017")
        myclient = pymongo.MongoClient("mongodb://localhost:27017")
        mydb = myclient["materials"]
        my_col_materials = mydb["PureElements"]
        selected = []
        for each in my_col_materials.find():
            if each["sites"][0]["label"] == name:
                selected.append(each)
        myclient.close()
        one  = selected[0]
        structure = mg.Structure.from_dict(one)
        space_info = structure.get_space_group_info()
        selected.append(space_info)
        return HttpResponse(json.dumps(selected))

def upload(request):
    return render(request, "Upload.html")

def uploaded(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no files for upload!")
        namepath = os.path.join(r"E:\Pycharm\models\myfile", myFile.name + str(time.time()))
        destination = open(os.path.join(r"E:\Pycharm\models\myfile", myFile.name + str(time.time())), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        myclient = pymongo.MongoClient("mongodb://localhost:27017")
        mydb = myclient["materials"]
        mycol = mydb["Structure"]
        structure = mg.Structure.from_file(namepath)
        print("已存入一条数据")
        mycol.insert_one(structure.as_dict())
        myclient.close()
        return HttpResponse("upload over!")

def query(request):
    if request.is_ajax():
        name = request.POST.get("element_name")
        myclient = pymongo.MongoClient("mongodb://localhost:27017")
        mydb = myclient["materials"]
        my_col_materials = mydb["PureElements"]
        selected = []
        for each in my_col_materials.find():
            if each["sites"][0]["label"] == name:
                selected.append(each)
        myclient.close()
        
        return HttpResponse(json.dumps(selected))

#返回struct页面需要的数据
# def struct(request):
#     if request.is_ajax():
#         name = request.POST.get("element_name")
#         latticeparameters = request.POST.get("latticeparameters")
#         latticeparameters = latticeparameters.split(",")
#         myclient = pymongo.MongoClient("mongodb://localhost:27017")
#         mydb = myclient["materials"]
#         my_col_materials = mydb["PureElements"]
#         select = []
#         for each in my_col_materials.find():
#             if each["sites"][0]["label"] == name:
#                 select.append(each)
#         for each in select:
#             if each["lattice"]["a"] == float(latticeparameters[0]) and each["lattice"]["b"] == float(latticeparameters[1]) and each["lattice"]["c"] == float(latticeparameters[2]):
#                 selected = each
#         structure = mg.Structure.from_dict(selected)
#         space_group = structure.get_space_group_info()
#         myclient.close()
#         return render(request,"structure.html",{"element_name":name,"latticeparameters":selected,"space_group":space_group})

def struct(request):
    if request.is_ajax():
        name = request.POST.get("element_name")
        latticeparameters = request.POST.get("latticeparameters")
        latticeparameters = latticeparameters.split(",")
        myclient = pymongo.MongoClient("mongodb://localhost:27017")
        mydb = myclient["materials"]
        my_col_materials = mydb["PureElements"]
        select = []
        for each in my_col_materials.find():
            if each["sites"][0]["label"] == name:
                select.append(each)
        for each in select:
            if each["lattice"]["a"] == float(latticeparameters[0]) and each["lattice"]["b"] == float(
                    latticeparameters[1]) and each["lattice"]["c"] == float(latticeparameters[2]):
                selected = each
        structure = mg.Structure.from_dict(selected)
        space_group = structure.get_space_group_info()
        id = selected['_id']
        sites = []
        index = 0
        for obj in (selected["sites"]):
            site = []
            abc = ""
            xyz = ""
            i = 0
            j = 0
            site.append(index)
            site.append(obj["label"])

            for a in (obj["abc"]):
                if i == 0:
                    abc = abc + "a:" + ("%.4f" % a) + "\r\n"
                    i = i + 1
                elif i == 1:
                    abc = abc + "b:" + ("%.4f" % a) + "\r\n"
                    i = i + 1
                else:
                    abc = abc + "c:" + ("%.4f" % a) + "\r\n"

            for a in (obj["xyz"]):
                if j == 0:
                    xyz = xyz + "x:" + ("%.4f" % a) + "\t"
                    j = j + 1
                elif j == 1:
                    xyz = xyz + "y:" + ("%.4f" % a) + "\r\n"
                    j = j + 1
                else:
                    xyz = xyz + "z:" + ("%.4f" % a) + "\r\n"
            site.append(abc)
            site.append(xyz)
            index = index + 1
            sites.append(site)
        myclient.close()  
        return render(request, "structure.html",locals())

def sites(request):
    if request.is_ajax():
        name = request.POST.get("element_name")
        latticeparameters = request.POST.get("latticeparameters")
        latticeparameters = latticeparameters.split(",")
        myclient = pymongo.MongoClient("mongodb://localhost:27017")
        mydb = myclient["materials"]
        my_col_materials = mydb["PureElements"]
        select = []
        for each in my_col_materials.find():
            if each["sites"][0]["label"] == name:
                select.append(each)
        for each in select:
            if each["lattice"]["a"] == float(latticeparameters[0]) and each["lattice"]["b"] == float(latticeparameters[1]) and each["lattice"]["c"] == float(latticeparameters[2]):
                selected = each
        sites = []
        for i in selected["sites"]:
            sites.append(i["abc"])
            sites.append(i["xyz"])
        return HttpResponse(json.dumps(sites))

def test(request):
    myclient = pymongo.MongoClient("mongodb://localhost:27017")
    mydb = myclient["materials"]
    my_col_materials = mydb["PureElements"]
    one = my_col_materials.find_one()
    structure = mg.Structure.from_dict(one)
    return render(request, "test.html", {"one":one})

def get_BandStructure(request):
    OUTCAR, INCAR, KPOINTS, OSZICAR, POSCAR, vasprun_path = bs.getID("E:\mat\data\BandStructure")
    input_spacegroup, input_sites, input_lattice, input_structure = bs.ParsePOSCAR(POSCAR)
    incar = bs.ParseINCAR(INCAR)
    incar = incar.as_dict()
    kpoints  =  bs.ParseKPOINTS(KPOINTS) 
    kpoints = kpoints.as_dict()
    run_stats, version, platform = bs.ParseOUTCAR(OUTCAR)
    software = []
    software.append(version)
    software.append(platform)
    oszicar, ionic_steps,electronic_steps = bs.ParseOSZICAR(OSZICAR)
    # print(ionic_steps,electronic_steps)
    N = []
    rms = []
    E = []
    for i in electronic_steps[0]:
        N.append(i['N'])
        rms.append(i['rms'])
        E.append(i['E'])
    return render(request,"BandStructure.html",{"structure":input_structure,"space_info":input_spacegroup,"parameters":incar,"resource":run_stats,"software":software,"N":N,"E":E,"rms":rms})

def get_GeometryOptimization(request):
    OUTCAR, INCAR, KPOINTS, OSZICAR, POSCAR, vasprun_path = bs.getID("E:\mat\data\GeometryOptimization")
    input_spacegroup, input_sites, input_lattice, output_Structure = bs.ParsePOSCAR(POSCAR)
    incar = bs.ParseINCAR(INCAR)
    incar = incar.as_dict()
    kpoints  =  bs.ParseKPOINTS(KPOINTS) 
    kpoints = kpoints.as_dict()
    run_stats, version, platform, cpuTime, realTime = go.ParseOUTCAR(OUTCAR)
    software = []
    software.append(version)
    software.append(platform)
    oszicar, ionic_steps, electronic_steps = go.ParseOSZICAR('OSZICAR')
    #   画图 OSZICAR  中 Ionic 部分。
    F = []
    for i in ionic_steps:
        F.append(i['F'])
    return render(request,"GeometryOptimization.html",{"structure":output_Structure,"space_info":input_spacegroup,"parameters":incar,"software":software,"resouce":run_stats,"F":F,"cputime":cpuTime,"realtime":realTime})

def get_StaticCalculation(request):
    OUTCAR, INCAR, KPOINTS, OSZICAR, POSCAR, vasprun_path = sc.getID("E:\mat\data\StaticCalculation")
    input_spacegroup, input_sites, input_lattice, output_Structure = sc.ParsePOSCAR(POSCAR)
    incar = bs.ParseINCAR(INCAR)
    incar = incar.as_dict()
    run_stats, version, plat, outcar = sc.ParseOUTCAR(OUTCAR)
    oszicar, ionic_steps, electronic_steps = sc.ParseOSZICAR(OSZICAR)
    totalEnergy = oszicar.final_energy
    fermiEnergy = outcar.efermi
    #这里是properties信息
    properties = []
    properties.append(totalEnergy)
    properties.append(fermiEnergy)
    #这里是software信息
    software = []
    software.append(version)
    software.append(plat)
    #这里是parameters信息
    incar = sc.ParseINCAR(INCAR)
    incar = incar.as_dict()
    #这里是rusource usage信息
    #这里是Convergency
    N = []
    rms = []
    E = []
    for i in electronic_steps[0]:
        N.append(i['N'])
        rms.append(i['rms'])
        E.append(i['E'])
    return render(request,"GeometryOptimization.html",{"structure":output_Structure,"space_info":input_spacegroup,"parameters":incar,"resource":run_stats,"software":software,"properties":properties,"N":N,"rms":rms,"E":E})

def get_DensityOfStates(request):
    OUTCAR, INCAR, KPOINTS, OSZICAR, POSCAR, vasprun_path = bs.getID("E:\mat\data\DensityOfStates")
    input_spacegroup, input_sites, input_lattice, output_Structure = sc.ParsePOSCAR(POSCAR)
    run_stats, version, plat, outcar = sc.ParseOUTCAR(OUTCAR)
    #这里显示的是properties
    fermiEnergy = outcar.efermi
    #DOS和Partial DOS先空出来

    #这里是software信息
    software = []
    software.append(run_stats)
    software.append(version)
    software.append(plat)
    #这里是parameters信息
    incar = sc.ParseINCAR(INCAR)
    incar = incar.as_dict()
    #这里是Convergency
    oszicar, ionic_steps, electronic_steps = sc.ParseOSZICAR(OSZICAR)
    N = []
    rms = []
    E = []
    for i in electronic_steps[0]:
        N.append(i['N'])
        rms.append(i['rms'])
        E.append(i['E'])
    return render(request,"DensityOfStates.html",{"structure":output_Structure,"space_info":input_spacegroup,"parameters":incar,"resource":run_stats,"software":software,"properties":fermiEnergy,"N":N,"rms":rms,"E":E})

def get_ElasticProperties(request):
    OUTCAR, INCAR, KPOINTS, OSZICAR, POSCAR, vasprun_path = ep.getID("E:\mat\data\ElasticProperties")
    input_spacegroup, input_sites, input_lattice, output_Structure = ep.ParsePOSCAR(POSCAR)
    incar = ep.ParseINCAR(INCAR)
    incar = incar.as_dict()
    run_stats, version, plat, outcar = ep.ParseOUTCAR(OUTCAR)
    #这里是properties信息
    
    #这里是software信息
    software = []
    software.append(version)
    software.append(plat)
    #这里是parameters信息
    incar = sc.ParseINCAR(INCAR)
    incar = incar.as_dict()
    #这里是convergency信息
    oszicar, ionic_steps, electronic_steps = ep.ParseOSZICAR(OSZICAR)
    ionicTotalEnergy = []
    for i in ionic_steps:
        ionicTotalEnergy.append(i['F'])
    #这里是resource信息，这里需要画图
    cpuTime, wallTime = ep.getAllTimeFromOutcar(OUTCAR)
    return render(request,"ElasticProperties.html",{"structure":output_Structure,"space_info":input_spacegroup,"parameters":incar,"resource":run_stats,"cputime":cpuTime,"walltime":wallTime,"software":software,"ionicTotalEnergy":ionicTotalEnergy})

def get_MagneticProperties(request):
    OUTCAR, INCAR, KPOINTS, OSZICAR, POSCAR, vasprun_path = mp.getID("E:\mat\data\MagneticProperties")
    input_spacegroup, input_sites, input_lattice, output_Structure = mp.ParsePOSCAR(POSCAR)
    incar = mp.ParseINCAR(INCAR)
    incar = incar.as_dict()
    run_stats, version, plat, outcar = mp.ParseOUTCAR(OUTCAR)
    #这里是properties信息
    oszicar, ionic_steps, electronic_steps = mp.ParseOSZICAR(OSZICAR)
    mag = ionic_steps[0]['mag']
    #这里是software信息
    software = []
    software.append(version)
    software.append(plat)
    #这里是parameters信息
    incar = sc.ParseINCAR(INCAR)
    incar = incar.as_dict()
    #这里是resource信息
    #这里是convergency信息
    N = []
    rms = []
    E = []
    for i in electronic_steps[0]:
        N.append(i['N'])
        rms.append(i['rms'])
        E.append(i['E'])
    return render(request,"MagneticProperties.html",{"structure":output_Structure,"space_info":input_spacegroup,"parameters":incar,"resource":run_stats,"software":software,"properties":mag,"N":N,"rms":rms,"E":E})