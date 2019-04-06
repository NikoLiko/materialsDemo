# 这个脚本应该    复现matcloud中 GeometryOptimization 页面的内容。
# 将此计算的输入输出文件中信息提取并展示到网页。主要包括 POSCAR  、 INCAR 、OSZICAR OUTCAR 、

from pymatgen.io.vasp import outputs, inputs
from pymatgen.core.structure import Structure
from pymatgen.vis.structure_vtk import StructureVis
import matplotlib.pyplot as plt
import re
import matplotlib.animation as animation



def ParsePOSCAR(POSCARorCIF):
    structure = Structure.from_file(POSCARorCIF)
    SpaceGroup = structure.get_space_group_info()
    Sites = structure.sites
    Lattice = structure.as_dict()['lattice']
    # print(structure.as_dict())
    return SpaceGroup, Sites, Lattice, structure

def ParseXDATCAR(XDATCAR):
    xdatcar = outputs.Xdatcar(XDATCAR)
    return xdatcar


# 缺少两个图。可用搜索关键字（LOOP+）的方式将数据搜集。
def ParseOUTCAR(OUTCAR):
    outcar = outputs.Outcar(OUTCAR)
    run_stats = outcar.run_stats

    with open(OUTCAR, 'r') as f:
        version = f.readline()
        f.readline()
        plat = re.findall('\s+(\w+)\s+', f.readline())[1]

        # LOOP+  画图部分的数据, 得到一个list， 里面是 元祖数据， 一个元祖包括两个字符串， 第一个数据是CPU Time ， 第二个是 real time 。 类型是字符串，还需要转换为 float
        cpuTime = re.findall('LOOP\+.+([0-9].+\.[0-9]+).+([0-9].+\.[0-9]+)', f.read())

    # 将cpuTime 中  String 转换为  Float

    cputime = []
    realtime = []
    for i in list(map(list, cpuTime)):
        cputime.append(float(i[0]))
        realtime.append(float(i[1]))


    return run_stats, version, plat, cputime, realtime


def ParseINCAR(INCAR):
    incar = inputs.Incar.from_file(INCAR)
    # print(incar.as_dict())
    return incar

def ParseKPOINTS(KPOINTS):
    kpoints = inputs.Kpoints.from_file(KPOINTS)
    return kpoints


def ParseOSZICAR(OSZICAR):
    oszicar = outputs.Oszicar(OSZICAR)
    ionic_steps = oszicar.as_dict()['ionic_steps']
    electronic_steps = oszicar.as_dict()['electronic_steps']

    return oszicar, ionic_steps, electronic_steps


def getID(i):
    outcar_path = '%s/OUTCAR' %i
    incar_path = '%s/INCAR' %i
    kpoints_path = '%s/KPOINTS' %i
    oszicar_path = '%s/OSZICAR' %i
    poscar_path = '%s/POSCAR' %i
    vasprun_path = '%s/vasprun.xml' %i
    return outcar_path, incar_path, kpoints_path, oszicar_path, poscar_path, vasprun_path


if __name__ == '__main__':
    # # 打开 画图 交互模式。可同时显示多张图。
    # plt.ion()
    #
    # #   获得一个 文件夹 ID
    # OUTCAR, INCAR, KPOINTS, OSZICAR, POSCAR, vasprun_path = getID('../59bf2e3aeedad7533a7a2dc3')
    #
    # #解析晶体结构部分，输出三部分主要信息。
    # input_spacegroup, input_sites, input_lattice, input_structure = ParsePOSCAR(POSCAR)
    # output_spacegroup, output_sites, output_lattice, output_structure = ParsePOSCAR(CONTCAR)
    # print(input_spacegroup, input_sites, input_lattice)
    #
    # #  POSCAR 晶体结构可视化 , 可视化需要软件VTK
    # poscarVis = StructureVis()
    # poscarVis.set_structure(input_structure)
    # poscarVis.show()
    #
    # output_contcarVis = StructureVis()
    # output_contcarVis.set_structure(output_structure)
    # output_contcarVis.show()
    #
    # 缺少 XDATCAR 的采集信息和 晶体结构可视化(采集信息应该与Contcar 一样， 晶体结构可视化图 就是POSCAR 到 Contcar 的动图)(动图代码部分还需要测试。)
    # Xdatcar = ParseXDATCAR('XDATCAR')
    # fig = plt.figure()
    # ims = []
    # for i in Xdatcar.structures:                #   Xdatcar.structures 应该是一个list ，里面每个元素都是Structure
    #     vis = StructureVis()
    #     vis.set_structure(i)
    #     ims.append(vis)
    # ani = animation.ArtistAnimation(fig, ims, interval=200, repeat_delay=1000)


    # # 解析OUTCAR ，获得 版本信息、 与 运行信息
    run_stats, version, platform, cpuTime, realTime = ParseOUTCAR('OUTCAR')

    # OUTCAR 画图部分。
    for i in range(len(cpuTime)):
        plt.figure(1)

        ax1 = plt.subplot(1, 2, 1)
        ax2 = plt.subplot(1, 2, 2)

        plt.sca(ax1)
        plt.plot(cpuTime, marker = 'o', color='red', s = 30, label = 'cpuTime')

        plt.sca(ax2)
        plt.plot(realTime, color='red', marker = 'o', s = 30, label = 'realTime')

        plt.show()




    # # 解析INCAR部分,应该直接打印 INCAR 中所有参数信息也是没问题的。
    # incar = ParseINCAR(INCAR)
    # print(incar.as_dict())



    # # 解析KPOINTS 部分， 需要的参数有 kpoints，  nkpoints, label,
    # kpoints  =  ParseKPOINTS(KPOINTS)
    #
    # kPoints = kpoints['kpoints']
    # nkpoints = kpoints['nkpoints']
    # label = kpoints['label']



    # 解析OSZICAR 部分。
    # oszicar, ionic_steps, electronic_steps = ParseOSZICAR('OSZICAR')
    # print(ionic_steps,electronic_steps)
    #
    # #   画图 OSZICAR  中 Ionic 部分。
    # F = []
    # for i in ionic_steps:
    #     F.append(i['F'])
    #
    # plt.figure()
    # plt.plot(F)
    #
    # plt.show()



