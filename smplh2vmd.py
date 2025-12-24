import os
import bpy
import os
from anim import bvh
from anim import amass

def smplh2vmd(input_dir, output_dir):
    files = [os.path.join(input_dir,k) for k in os.listdir(input_dir)]
    bvh_root_dir = os.path.join(output_dir, "for_bvh")
    vmd_root_dir = os.path.join(output_dir, "for_vmd")
    os.makedirs(bvh_root_dir, exist_ok=True)
    os.makedirs(vmd_root_dir, exist_ok=True)
    print(f"bvh_root_dir: {bvh_root_dir}")
    print(f"vmd_root_dir: {vmd_root_dir}")

    for f in files:
        bpy.ops.wm.read_factory_settings(use_empty=True) 
        bpy.ops.preferences.addon_enable(module='mmd_tools') 
        assert len(dir(bpy.ops.mmd_tools)) > 0, "mmd tools not correctly installed" 

        anim = amass.load(
                amass_motion_path=f,
                smplh_path="/Users/tangruiqing/Projects/my_github/SMPLH2VMD/models/smplh_model/model.npz",
        )

        filename = os.path.basename(f)
        print(f"Processing {filename}")

        bvh.save(
            filepath=os.path.join(bvh_root_dir, filename.replace('.npz', '.bvh')),
            anim=anim,
            save_pos=False
        )

        bpy.ops.import_anim.bvh(filepath=os.path.join(bvh_root_dir, filename.replace('.npz', '.bvh')), global_scale=0.0112, use_fps_scale=True, rotate_mode='QUATERNION')

        print("vmd save to", os.path.join(vmd_root_dir, filename.replace('.npz', '.vmd')))

        bpy.ops.mmd_tools.export_vmd(filepath=os.path.join(vmd_root_dir, filename.replace('.npz', '.vmd')), check_existing=True,
                                        filter_glob="*.vmd", scale=12.5, use_pose_mode=True, use_frame_range=False) # 
  
if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--input_smplh_dir", default="/Users/tangruiqing/Projects/my_github/SMPLH2VMD/models/for_vmd")
    parser.add_argument("--output_dir", default="/Users/tangruiqing/Projects/my_github/SMPLH2VMD/models/outputs")
    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    smplh2vmd(args.input_smplh_dir, args.output_dir)
    