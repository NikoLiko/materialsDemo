# 这个脚本应该    复现matcloud中 StaticCalculation 页面的内容。
# 将此计算的输入输出文件中信息提取并展示到网页。主要包括POSCAR  、 INCAR 、OSZICAR OUTCAR 、等
# 在电子信息图中， 如何将 每个点 显示出来？ 目前只有一条平滑的曲线。

from pymatgen.io.vasp import outputs, inputs
from pymatgen.core.structure import Structure
from pymatgen.vis.structure_vtk import StructureVis
import re
from matplotlib import pyplot


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



if __name__ == '__main__':
    #   获得一个 文件夹 ID
    OUTCAR, INCAR, KPOINTS, OSZICAR, POSCAR, vasprun_path = getID('./5a28adf4bd1a248faf08545c')


    #解析晶体结构部分，输出三部分主要信息。
    input_spacegroup, input_sites, input_lattice, input_structure = ParsePOSCAR(POSCAR)
    print(input_spacegroup, input_sites, input_lattice)


    #  POSCAR 晶体结构可视化 , 可视化需要软件VTK
    input_poscarVis = StructureVis()
    input_poscarVis.set_structure(input_structure)
    input_poscarVis.show()

    # Properteis 部分 total energy
    oszicar, ionic_steps, electronic_steps = ParseOSZICAR(OSZICAR)
    totalEnergy = oszicar.final_energy

    # Convergency Part , 数据来源于 electronic_steps
    #   画图 OSZICAR  中 electronic 部分。
    N = []
    rms = []
    E = []
    for i in electronic_steps[0]:
        N.append(i['N'])
        rms.append(i['rms'])
        E.append(i['E'])

    # 打开plt的交互模式，平常是阻塞模式，无法同时显示两个图
    pyplot.ion()

    pyplot.figure()
    pyplot.plot(E)

    pyplot.figure()
    pyplot.plot(rms)

    #   关闭交互模式，并显示图片。
    pyplot.ioff()
    pyplot.show()

    # Software  部分 数据来源于OUTCAR  , run_stats 是 Resource usage 部分数据
    run_stats, version, plat, outcar = ParseOUTCAR(OUTCAR)
    print(run_stats, version, plat)

    # Parameters 部分 解析INCAR 文件, KPOINTS 文件
    incar = ParseINCAR(INCAR)
    Kpoints = ParseKPOINTS(KPOINTS)

    kpoints = Kpoints.as_dict()['kpoints']
    nkpoints = Kpoints.as_dict()['nkpoints']
    label = Kpoints.as_dict()['labels']
    print(kpoints, nkpoints, label)
    # print(Kpoints.as_dict())
    print(incar.as_dict())

    # Properties 部分  fermiEnergy
    fermiEnergy = outcar.efermi
    # print(fermiEnergy)