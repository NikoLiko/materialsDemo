# 这个脚本应该    复现matcloud中 BandStructure页面的内容。
# 将此计算的输入输出文件中信息提取并展示到网页。主要包括POSCAR  、 INCAR 、OSZICAR OUTCAR 、


from pymatgen.io.vasp import outputs, inputs
from pymatgen.core.structure import Structure
from pymatgen.vis.structure_vtk import StructureVis
import re

def ParsePOSCAR(POSCARorCIF):
    structure = Structure.from_file(POSCARorCIF)
    SpaceGroup = structure.get_space_group_info()
    Sites = structure.sites
    Lattice = structure.as_dict()['lattice']
    # print(structure.as_dict())
    return SpaceGroup, Sites, Lattice, structure

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

def ParseOUTCAR(OUTCAR):
    outcar = outputs.Outcar(OUTCAR)
    run_stats = outcar.run_stats

    with open(OUTCAR, 'r') as f:
        version = f.readline()
        f.readline()
        plat = re.findall('\s+(\w+)\s+', f.readline())[1]
    return run_stats, version, plat


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
    OUTCAR, INCAR, KPOINTS, OSZICAR, POSCAR, vasprun_path = getID('.')


    #解析晶体结构部分，输出三部分主要信息。
    input_spacegroup, input_sites, input_lattice, input_structure = ParsePOSCAR(POSCAR)
    print(input_spacegroup, input_sites, input_lattice)
    print("------------------------------------------------------------")


    # POSCAR 晶体结构可视化 , 可视化需要软件VTK
    input_poscarVis = StructureVis()
    input_poscarVis.set_structure(input_structure)
    input_poscarVis.show()


    # 画能代结构图 ,
    from pymatgen.io.vasp import Vasprun, BSVasprun
    from pymatgen.electronic_structure.plotter import BSPlotter
    vasprun = BSVasprun(vasprun_path)
    bankStructure = vasprun.get_band_structure(kpoints_filename=KPOINTS,line_mode=True)
    plt = BSPlotter(bankStructure)
    # print(plt.get_ticks())              #Get all ticks and labels for a band structure plot.    return A dictionary with ‘distance’
    plt.show(ylim=(-36, 5))             # 这一行有问题。就是这个范围参数该如何得到。


    # 解析INCAR部分,应该直接打印 INCAR 中所有参数信息也是没问题的。
    incar = ParseINCAR(INCAR)
    print("------------------------------------------------------------")
    print(incar.as_dict())

    # 解析KPOINTS 部分， 需要的参数有 kpoints，  nkpoints, label,
    kpoints  =  ParseKPOINTS(KPOINTS)

    kPoints = kpoints['kpoints']
    nkpoints = kpoints['nkpoints']
    label = kpoints['label']
    # print(kpoints.as_dict())

    #解析OSZICAR 部分。
    oszicar, ionic_steps,electronic_steps = ParseOSZICAR(OSZICAR)
    # print(ionic_steps,electronic_steps)

    #   画图 OSZICAR  中 electronic 部分。
    from matplotlib import pyplot

    N = []
    rms = []
    E = []
    for i in electronic_steps[0]:
        N.append(i['N'])
        rms.append(i['rms'])
        E.append(i['E'])

    #  打开plt的交互模式，平常是阻塞模式，无法同时显示两个图
    pyplot.ion()


    pyplot.figure()
    pyplot.plot(E)

    pyplot.figure()
    pyplot.plot(rms)

    #   关闭交互模式，并显示图片。
    pyplot.ioff()
    pyplot.show()


    # 解析OUTCAR ，获得 版本信息、 与 运行信息
    run_stats, version, platform = ParseOUTCAR(OUTCAR)

# ...