"""Directed convex-solid interference check for pedestal and coupled mechanism.

This records actual sampled solid intersections, not AABB penetration or a
continuous-sweep certificate. Uses the same scene state and vertices as export.
"""
import argparse
from itertools import product
from pathlib import Path
import numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
from unloading_sim.eco65.model import load_json,save_json
from unloading_sim.eco65.quarter_prototype import installation_support,mechanism_spec
from unloading_sim.eco65.coupled_scene import coupled_conveyor_state


def vertices(row):
    local=np.asarray(row['convex_mesh']['vertices']) if 'convex_mesh' in row else np.asarray(
        list(product(*[(-s/2,s/2) for s in row['size']])))
    pose=np.asarray(row['pose'])
    return local@pose[:3,:3].T+pose[:3,3]


def common_interior(a,b):
    if np.any(np.minimum(a.max(0),b.max(0))-np.maximum(a.min(0),b.min(0))<=1e-9):return None
    planes=np.vstack([ConvexHull(a).equations,ConvexHull(b).equations])
    # Positive inscribed-ball radius proves a common interior point in both
    # actual convex solids. It is NOT FCL penetration depth or surface gap.
    result=linprog([0,0,0,-1],A_ub=np.c_[planes[:,:3],np.linalg.norm(planes[:,:3],axis=1)],
                   b_ub=-planes[:,3],bounds=[(None,None)]*3+[(0,None)],method='highs')
    if not result.success or result.x[3]<=1e-8:return None
    return dict(common_interior_point_D_m=result.x[:3].tolist(),
                common_inscribed_radius_m=float(result.x[3]),reason='CONVEX_SOLIDS_SHARE_INTERIOR')


def check(config):
    spec=mechanism_spec(config,'INSTALLATION_STROKE_DIAGNOSTIC',{})
    mounts=[]
    for name,center,size in installation_support(config):
        pose=np.eye(4);pose[:3,3]=center
        mounts.append(dict(id=name,pose=pose.tolist(),size=list(size)))
    # Include mount vertical edges and midplanes as critical samples, in
    # addition to 10 mm spacing. Never claim unsampled sweep clearance.
    lo,hi=spec['low_height_m'],spec['high_height_m']
    heights=sorted(set([lo,hi,*np.arange(lo,hi,.01),*[z for m in mounts for z in
        (m['pose'][2][3]-m['size'][2]/2,m['pose'][2][3],m['pose'][2][3]+m['size'][2]/2) if lo<=z<=hi]]))
    failures=[]
    for h in heights:
        state=coupled_conveyor_state(spec,float(h))
        for mount in mounts:
            a=vertices(mount)
            for moving in state['world_objects']:
                witness=common_interior(a,vertices(moving))
                if witness:failures.append(dict(height_m=float(h),pair=[mount['id'],moving['id']],**witness))
    return dict(schema='eco65_installation_stroke_solid_check_v1',
                status='INTERFERENCE_FOUND' if failures else 'NO_INTERSECTION_AT_SAMPLES',
                scope='MOUNT_SOLIDS_VS_COUPLED_MECHANISM_ONLY',heights_m=heights,failures=failures,
                continuous_sweep_proven=False,structural_load_qualification='NOT_RUN')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--snapshot',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();snapshot=load_json(a.snapshot)
    report=check(snapshot['scene']['prototype']['configuration'])
    report['snapshot_fingerprint']=snapshot['fingerprint'];save_json(a.output,report)
    print(report['status'],len(report['failures']))
