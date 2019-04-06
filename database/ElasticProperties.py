# 这个脚本应该    复现matcloud中 ElasticProperties 页面的内容。
# 将此计算的输入输出文件中信息提取并展示到网页。主要包括POSCAR  、 INCAR 、OSZICAR OUTCAR 、等

from pymatgen.core.structure import Structure
from pymatgen.io.vasp import inputs,outputs
from pymatgen.vis.structure_vtk import StructureVis
from pymatgen.analysis.elasticity.elastic import ElasticTensor
import numpy as np
import re
from . import elastic as ela
import math


    # 解析 VASP 输入文件， 返回 空间信息 spacegroup  坐标信息 Sites
    #                           参数信息 lattice    晶体结构对象 structure
def ParsePOSCAR(POSCARorCIF):
    structure = Structure.from_file(POSCARorCIF)
    SpaceGroup = structure.get_space_group_info()
    Sites = structure.sites
    Lattice = structure.as_dict()['lattice']
    # print(structure.as_dict())
    return SpaceGroup, Sites, Lattice, structure


    # 解析 INCAR 文件 ， 返回 INCAR 对象
def ParseINCAR(INCAR):
    incar = inputs.Incar.from_file(INCAR)
    # print(incar.as_dict())
    return incar

    # 解析 KPOINTS 文件， 返回 KPOINTS 对象
def ParseKPOINTS(KPOINTS):
    kpoints = inputs.Kpoints.from_file(KPOINTS)

    return kpoints

    # 解析 OSZICAR 文件， 返回 OSZICAR 对象  离子步骤信息 ionic_steps  电子步骤信息 electronic_steps
def ParseOSZICAR(OSZICAR):
    oszicar = outputs.Oszicar(OSZICAR)
    ionic_steps = oszicar.as_dict()['ionic_steps']
    electronic_steps = oszicar.as_dict()['electronic_steps']

    return oszicar, ionic_steps, electronic_steps

    # 解析 OUTCAR 文件  返回 运行信息 run_stats   版本信息 version    平台信息 plat
def ParseOUTCAR(OUTCAR):
    outcar = outputs.Outcar(OUTCAR)
    run_stats = outcar.run_stats


    with open(OUTCAR, 'r') as f:
        version = f.readline()
        f.readline()
        plat = re.findall('\s+(\w+)\s+', f.readline())[1]
    return run_stats, version, plat, outcar

    # 从文件夹下读取各个文件的路径    返回 OUTCAR INCAR KPOINTS OSZICAR POSCAR vasprun 文件的路径
def getID(i):
    outcar_path = '%s/OUTCAR' %i
    incar_path = '%s/INCAR' %i
    kpoints_path = '%s/KPOINTS' %i
    oszicar_path = '%s/OSZICAR' %i
    poscar_path = '%s/POSCAR' %i
    vasprun_path = '%s/vasprun.xml' %i
    return outcar_path, incar_path, kpoints_path, oszicar_path, poscar_path, vasprun_path

    # 读取OUTCAR ，利用正则表达式，取出cpuTime 和 wallTime 数据 存入list 中并返回
def getAllTimeFromOutcar(outcarPath):
    with open(outcarPath, 'r') as f:
        content = f.read()
        cpuTimeAndRealTime = re.findall('LOOP\+:\s+cpu+\stime\s+([0-9]+\.[0-9]+):\sreal\stime\s+([0-9]+\.[0-9]+)', content, re.S)
    cpuTime = []
    wallTime = []
    for i in cpuTimeAndRealTime:
        cpuTime.append(float(i[0]))
        wallTime.append(float(i[1]))
    return cpuTime, wallTime

if __name__ == '__main__':
    #   获得一个 文件夹 ID
    OUTCAR, INCAR, KPOINTS, OSZICAR, POSCAR, vasprun_path = getID('./5a28adf4bd1a248faf08545d')

    # 解析晶体结构部分，输出三部分主要信息。
    input_spacegroup, input_sites, input_lattice, input_structure = ParsePOSCAR(POSCAR)
    print(input_spacegroup, input_sites, input_lattice)

    #  POSCAR 晶体结构可视化 , 可视化需要软件VTK
    input_poscarVis = StructureVis()
    input_poscarVis.set_structure(input_structure)
    input_poscarVis.show()

    # Software 部分
    run_stats, version, plat, outcar = ParseOUTCAR(OUTCAR)
    print('Version:',version)
    print('Platform:', plat)

    # Propreties 部分， 展示的是 Elastictiy Matrix  和 Average properties;  单位是K
    outcar.read_elastic_tensor()
    elaticityMatrix = outcar.data["elastic_tensor"]
    elas = ela.Elastic(elaticityMatrix)
    elas = ela.ElasticOrtho(elas)
    avg = elas.averages()
    print('Average Properties :', avg)
    k = avg[0][2] / avg[0][0]
    voigtHardness = 2 * math.pow((k * k * avg[0][2]), 0.585) - 3
    #  下面这个公式要  / 10  ，这样单位才是K
    meltingPoint = (482.8 + 8.172 * avg[0][0]) / 10
    print(voigtHardness, meltingPoint)

    # Parameters 部分(incar)
    incar = ParseINCAR(INCAR)
    Kpoints = ParseKPOINTS(KPOINTS)

    kpoints = Kpoints.as_dict()['kpoints']
    nkpoints = Kpoints.as_dict()['nkpoints']
    label = Kpoints.as_dict()['labels']
    print(kpoints, nkpoints, label)
    # print(Kpoints.as_dict())
    print(incar.as_dict())

    # Convergency 部分(oszicar. ionic)
    oszicar, ionic_steps, electronic_steps = ParseOSZICAR(OSZICAR)
    ionicTotalEnergy = []
    for i in ionic_steps:
        ionicTotalEnergy.append(i['F'])
    print(ionicTotalEnergy)

    # Resource usage 部分 (outcar.run_stats, 图中信息来源 outcar文件 ，关键字 为 Loop+: cpu time)
    print('Run Stats:', run_stats)
    cpuTime, wallTime = getAllTimeFromOutcar(OUTCAR)
    print('Cpu Time:', cpuTime)
    print('Real Time:', wallTime)
