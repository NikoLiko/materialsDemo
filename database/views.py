from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import pymongo
import json
import os
import time
import pymatgen as mg
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
            if each["lattice"]["a"] == float(latticeparameters[0]) and each["lattice"]["b"] == float(latticeparameters[1]) and each["lattice"]["c"] == float(latticeparameters[2]):
                selected = each
        structure = mg.Structure.from_dict(selected)
        space_group = structure.get_space_group_info()
        myclient.close()
        return render(request,"structure.html",{"element_name":name,"latticeparameters":selected,"space_group":space_group})