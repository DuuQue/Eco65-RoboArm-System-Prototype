"""Selected upper-layer tasks keep the complete physical inventory."""
from copy import deepcopy
from pathlib import Path
import numpy as np
import pytest
import yaml
from unloading_sim.eco65.quarter_prototype import carton_grid, mechanism_spec
from unloading_sim.eco65.transverse_process import corners, process_options
from unloading_sim.eco65.coupled_task import CoupledTask
from unloading_sim.eco65.batch_task import BatchTask, SELECTED_CARTONS


def test_eight_layers_preserve_lower_stack_and_all_equipment_dimensions():
    root=Path('configs/workcells')
    old=yaml.safe_load((root/'eco65_lab_prototype_4c4l_fixed_candidate_v2.yaml').read_text())
    new=yaml.safe_load((root/'eco65_lab_prototype_4c8l_fixed_candidate_v2.yaml').read_text())
    for key in ('installation','receiver','trailer','chassis','external_translation_m'):
        assert new[key]==old[key]
    boxes=carton_grid(new['cartons']);before=carton_grid(old['cartons'])
    assert len(boxes)==32 and len([b for b in boxes if b['layer']>=4])==16
    assert np.vstack([corners(b) for b in boxes]).min(0)==pytest.approx([0,-.2075,0])
    assert np.vstack([corners(b) for b in boxes]).max(0)==pytest.approx([.15,.2075,.8])
    for b,a in zip(boxes,before):
        assert b['id']==a['id'] and b['pose']==a['pose'] and b['size_m']==[.15,.1,.1]
    assert boxes[12]['supports']==['carton_r00_l04_c00']
    spec=mechanism_spec(new,'test',{})
    from unloading_sim.eco65.coupled_scene import coupled_conveyor_state
    receiving=coupled_conveyor_state(spec,new['receiver']['initial_height_m'])['receiving']
    for layer in (3,4,6):
        options=process_options(boxes[4*layer],boxes,boxes,spec,receiving)
        assert not any(o['face']=='top' for o in options['options'])
    options=process_options(boxes[28],boxes,boxes,spec,receiving)
    assert any(o['face']=='top' for o in options['options'])


def make_task(monkeypatch,requested):
    def initial(self,*a,**kw):
        self.original_boxes={'lower':{},'upper':{}}
        self.first_target_id='upper';self.deadline=100.;self.started=0.;self.completed_ids=[]
    monkeypatch.setattr(CoupledTask,'__init__',initial)
    monkeypatch.setattr('unloading_sim.eco65.batch_task.perf_counter',lambda:0.)
    return BatchTask(requested_ids=requested)


def test_selected_scope_filters_targets_without_reducing_inventory(monkeypatch):
    task=make_task(monkeypatch,['upper'])
    assert task.completion_goal==SELECTED_CARTONS
    assert task.eligible_next_target({'id':'upper'})
    assert not task.eligible_next_target({'id':'lower'})
    assert set(task.original_boxes)=={'lower','upper'}
    task.completed_ids=['upper']
    monkeypatch.setattr(CoupledTask,'return_next',lambda *a,**kw:pytest.fail('must not unload lower'))
    task.result=lambda **kw:dict(complete=kw['complete'],fingerprint='old')
    monkeypatch.setattr('unloading_sim.eco65.batch_task.validate_cycle',lambda *a:{'status':'PASS'})
    task.snapshot={}
    assert task.return_next()['complete']


@pytest.mark.parametrize('requested',[[],['upper','upper'],['missing'],['lower']])
def test_invalid_scope_rejected(monkeypatch,requested):
    with pytest.raises(ValueError,match='REQUESTED_INVENTORY'):
        make_task(monkeypatch,requested)


def test_unselected_lower_support_must_remain_at_same_pose_and_size():
    from unloading_sim.eco65.coupled_state import check_unselected_cartons
    before={'world':[{'id':'lower','pose':[0,0,.05],'size_m':[.15,.1,.1]}]}
    after=deepcopy(before)
    check_unselected_cartons(before,after,{'lower'})
    after['world'][0]['pose'][2]+=.1
    with pytest.raises(ValueError,match='UNSELECTED_CARTON_CHANGED'):
        check_unselected_cartons(before,after,{'lower'})
    after['world']=[]
    with pytest.raises(ValueError,match='UNSELECTED_CARTON_CHANGED'):
        check_unselected_cartons(before,after,{'lower'})


def test_initial_state_failure_checkpoint_preserves_none_not_fake_q(tmp_path):
    import json
    task=BatchTask.__new__(BatchTask)
    task.progress_path=tmp_path/'native_progress.jsonl'
    task.current_q=None;task.completed_ids=[];task.target={'id':'upper'}
    task.height_m=.331;task.attachment=None;task.cycle_records=[];task.started=0.
    task.result=lambda:{'complete':False,'initial_state':None,'records':[]}
    task.save_checkpoint('BATCH_STOPPED')
    assert json.loads((tmp_path/'batch_progress.json').read_text())['q'] is None
    assert (tmp_path/'latest_plan.json.gz').is_file()


def test_forward_200_keeps_equipment_and_rebuilds_supported_step():
    from unloading_sim.eco65.quarter_prototype import installation_support
    root=Path('configs/workcells')
    old=yaml.safe_load((root/'eco65_lab_prototype_4c8l_fixed_candidate_v2.yaml').read_text())
    new=yaml.safe_load((root/'eco65_lab_prototype_4c8l_forward200_v2.yaml').read_text())
    assert np.subtract(new['installation']['position_m'],old['installation']['position_m'])==pytest.approx([.2,0,0])
    for key in ('chassis','trailer','cartons','external_translation_m'):
        assert new[key]==old[key]
    receiver=deepcopy(new['receiver']);receiver['initial_height_m']=old['receiver']['initial_height_m']
    assert receiver==old['receiver']
    foot,plate=installation_support(new)
    assert foot[0]=='robot_mount_pedestal' and plate[0]=='robot_mount_plate'
    assert foot[1]==pytest.approx([-.295,.0375,.180])
    assert foot[2]==pytest.approx([.140,.140,.060])
    assert plate[1]==pytest.approx([-.2875,.0375,.2175])
    assert plate[2]==pytest.approx([.140,.140,.015])
    assert foot[1][0]+foot[2][0]/2==pytest.approx(-.225)
    assert foot[1][2]+foot[2][2]/2==pytest.approx(plate[1][2]-plate[2][2]/2)
    broken=deepcopy(new);broken['installation'].pop('stepped_pedestal')
    with pytest.raises(ValueError,match='NOT_FULLY_SUPPORTED'):installation_support(broken)
    original=installation_support(old)
    assert len(original)==1 and original[0][2]==pytest.approx([.14,.14,.075])


def test_forward_plate_interference_is_retained_not_hidden():
    from check_eco65_installation_stroke import common_interior,vertices
    from unloading_sim.eco65.quarter_prototype import installation_support
    from unloading_sim.eco65.coupled_scene import coupled_conveyor_state
    config=yaml.safe_load(Path('configs/workcells/eco65_lab_prototype_4c8l_forward200_v2.yaml').read_text())
    spec=mechanism_spec(config,'test',{})
    name,center,size=installation_support(config)[1];pose=np.eye(4);pose[:3,3]=center
    plate=vertices(dict(size=size,pose=pose.tolist()))
    def belt(h):
        return vertices(next(v for v in coupled_conveyor_state(spec,h)['world_objects']
                             if v['id']=='conveyor_transverse_prototype_belt'))
    assert common_interior(plate,belt(.1)) is None
    assert common_interior(plate,belt(.22))['common_inscribed_radius_m']>0
    assert common_interior(plate,belt(.525)) is None
