# Author: Vatsal Sanjay
# vatsalsanjay@gmail.com
# Physics of Fluids
# Last updated: 19-Nov-2020

import numpy as np
import os
import subprocess as sp
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.ticker import StrMethodFormatter
import sys

matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['text.usetex'] = True
#matplotlib.rcParams['text.latex.preamble'] = [r"\usepackage{amsmath}"]

def gettingFacets(filename):
    exe = ["./getFacet", filename]
    p = sp.Popen(exe, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    temp1 = stderr.decode("utf-8")
    temp2 = temp1.split("\n")
    segs = []
    skip = False
    if (len(temp2) > 1e2):
        for n1 in range(len(temp2)):
            temp3 = temp2[n1].split(" ")
            if temp3 == ['']:
                skip = False
                pass
            else:
                if not skip:
                    temp4 = temp2[n1+1].split(" ")
                    r1, z1 = np.array([float(temp3[1]), float(temp3[0])])
                    r2, z2 = np.array([float(temp4[1]), float(temp4[0])])
                    segs.append(((r1, z1),(r2,z2)))
                    segs.append(((r1, -z1),(r2,-z2)))
                    segs.append(((-r1, z1),(-r2,z2)))
                    segs.append(((-r1, -z1),(-r2,-z2)))
                    skip = True
    return segs

# ----------------------------------------------------------------------------------------------------------------------

nGFS = 27500
Ldomain = float(sys.argv[1])
tsnap = float(sys.argv[2])


rmin, rmax, zmin, zmax = [-Ldomain/2, Ldomain/2, 0, Ldomain]
lw = 2

folder = 'VideoD2_v1'  # output folder

if not os.path.isdir(folder):
    os.makedirs(folder)

for ti in range(nGFS):
    t = tsnap*ti
    place = "intermediate/snapshot-%5.4f" % t
    name = "%s/%8.8d.png" %(folder, int(t*1000))
    if not os.path.exists(place):
        print("%s File not found!" % place)
    else:
        if os.path.exists(name):
            print("%s Image present!" % name)
        else:
            segs = gettingFacets(place)
            if (len(segs) == 0):
                print("Problem in the available file %s" % place)
            else:
                # Part to plot
                AxesLabel, TickLabel = [50, 20]
                fig, ax = plt.subplots()
                fig.set_size_inches(19.20, 10.80)

                ax.plot([0, 0], [zmin, zmax],'-.',color='grey',linewidth=lw)

                ax.plot([rmin, rmin], [zmin, zmax],'-',color='black',linewidth=lw)
                ax.plot([rmin, rmax], [zmin, zmin],'-',color='black',linewidth=lw)
                ax.plot([rmin, rmax], [zmax, zmax],'-',color='black',linewidth=lw)
                ax.plot([rmax, rmax], [zmin, zmax],'-',color='black',linewidth=lw)

                ## Drawing Facets
                line_segments = LineCollection(segs, linewidths=4, colors='green', linestyle='solid')
                ax.add_collection(line_segments)

                print("Done %d" % ti)


                ax.set_aspect('equal')
                ax.set_xlim(rmin, rmax)
                ax.set_ylim(zmin, zmax)
                # t2 = t/tc
                ax.set_title('$V_0t/R_0$ = %4.3f' % t, fontsize=TickLabel)

                ax.axis('off')
                # plt.show()
                plt.savefig(name, bbox_inches="tight")
                plt.close()
