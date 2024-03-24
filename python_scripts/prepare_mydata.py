import numpy as np
import sys
import os
from os.path import join as pjoin
from pathlib import Path
from glob import glob
from typing import Any, Dict, List, Optional

def readlines(filename, ignore_chara = '#'):
    """Read all the lines in a text file and return as a list
    """
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    lines = [l for l in lines if not l.startswith(ignore_chara)]
    return lines

def write_to_file(txt_fn, files_list):
    with open(txt_fn, 'w') as fw:
        for l in files_list:
            fw.write(l + "\n")
    print("Done! Saved {} names to {}".format(len(files_list), txt_fn))

def prepare_data(img_list_txtfile, dst_dir):
    img_names = readlines(img_list_txtfile)
    img_root = img_names[0]
    os.makedirs(dst_dir, exist_ok=True)
    for idx, img_name in enumerate(img_names[1:]):
        exten = img_name.split(".")[-1]
        src_img = pjoin(img_root, img_name)
        dst_img = pjoin(dst_dir, f"{idx:04d}.{exten}")
        if not os.path.exists(dst_img):
            # copy image
            os.system(f"ln -s {src_img} {dst_img}")
            #os.system(f"cp {src_img} {dst_img}")
            #print(f"ln -s {src_img} {dst_img}")

def run_main(data_root = "./WheatstoneData_nocc/test_team", dst_dir = "./data/WheatstoneData_nocc"):
    #  '0912-1/2023-09-12-10-33-17'
    img_paths = glob(pjoin(data_root, '*/*/'))
    #img_paths = ['/nfs/STG/SemanticDenseMapping/data/WheatstoneData_nocc/test_team/0912-1/2023-09-12-10-41-17']
    
    src_dst_folders = {
        'left_rectified': "image_0", 
        'right_rectified': "image_1",
        'raft_stereo_pseudo_gt': "depth_0",
        }
    
    for cur_path in img_paths:
            
        img_names = sorted(
            glob(pjoin(cur_path, "left_rectified/*.png")),
            # */left_rectified/294_560943060599_10000000.png, vs */left_rectified/1939_583841230182_10000000.png
            # to compare "294" vs "1939";
            key = lambda x : int(os.path.basename(x).split('_')[0])
            ) 
        
        img_names_for_timeStamps = []
        img_names_maps = []
 
        for idx, img_name in enumerate(img_names):
            #img_base_name = os.path.basename(img_name)
            #img_dir_name = os.path.dirname(img_name)
            exten = "." + img_name.split(".")[-1]

            for src_fold, dst_fold in src_dst_folders.items():
                if idx == 0:
                    print (f"mapping {src_fold} to {dst_fold}")

                if src_fold in ['left_rectified', 'right_rectified']:
                    src_img = img_name.replace("left_rectified", src_fold)
                    scan = os.path.dirname(src_img[len(data_root):]).replace(src_fold, dst_fold)
                elif src_fold == 'raft_stereo_pseudo_gt':
                    src_img = img_name.replace("left_rectified", src_fold).replace(exten, "_l_nocc.pfm" )
                    exten = "_l_nocc.pfm"
                    scan = os.path.dirname(src_img[len(data_root):]).replace(src_fold, dst_fold)
                
                if idx == 0:
                    print ("scan = ", scan)

                tmp_dst_dir = pjoin(dst_dir, scan)
                os.makedirs(tmp_dst_dir, exist_ok=True)
                dst_img = pjoin(tmp_dst_dir,  f"{idx:04d}{exten}")
                
                if src_fold == 'left_rectified':
                    img_names_for_timeStamps.append(f"{idx:04d}")
                    img_names_maps.append(f"{idx:04d}, {os.path.basename(src_img)}")
                
                if not os.path.exists(dst_img):
                    # copy image
                    os.system(f"ln -s {src_img} {dst_img}")
                    #os.system(f"cp {src_img} {dst_img}")
                    #print(f"ln -s {src_img} {dst_img}")

        # save as */times.txt and nampes_times.txt
        write_to_file(txt_fn= pjoin(tmp_dst_dir, '../times.txt'), 
                        files_list= img_names_for_timeStamps)
        write_to_file(txt_fn= pjoin(tmp_dst_dir, '../names_map.txt'), 
                        files_list= img_names_maps
                        )
        #sys.exit()
                
                
                
            



    

"""
How to run this file:
- cd ~/this-colmap-proj/
- python3 -m wheatstone_exam
"""
if __name__ == "__main__":

    if 0:
        src_data_root = Path("/media/changjiang/disk1/innopeak/data/WheatstoneData/processed/test_team/0912-2/2023-09-12-15-42-56") 
        src_data_root = Path("/media/changjiang/disk1/innopeak/data/WheatstoneData/processed/test_team/0912-2/2023-09-12-15-42-56") 
        proj_root = Path("/home/changjiang/code/github-code-study-oppo/ORB_SLAM3/") 
        prepare_data(
            ## left images
            #img_list_txtfile= src_data_root / 'left_img_list.txt',
            #dst_dir = proj_root / 'data/wheatstone/2023-09-12-15-42-56/image_0'
            
            ## right images
            #img_list_txtfile= src_data_root / 'right_img_list.txt',
            #dst_dir = proj_root / 'data/wheatstone/2023-09-12-15-42-56/image_1' 
            
            # depth maps
            img_list_txtfile= src_data_root / 'left_depth_list.txt',
            dst_dir = proj_root / 'data/wheatstone/2023-09-12-15-42-56/depth_0' 
            )
        sys.exit()
    
    if 0:
        pose_file = './results/wheatstone/2023-09-12-15-42-56/CameraTrajectory.txt'
        poses = np.loadtxt(pose_file, comments='#').astype(np.float32)
        img_paths = glob('data/wheatstone/2023-09-12-15-42-56/image_0/*.png')
        assert len(img_paths) == poses.shape[0], f"Requires #image {len(img_paths)} == #pose {poses.shape[0]}"
        pose_dst_dir = pjoin(os.path.dirname(pose_file), 'pose_me')
        os.makedirs(pose_dst_dir, exist_ok=True)
        for i in range(poses.shape[0]):
            pose_txtfile = pjoin(pose_dst_dir, f"{i:04d}_left.txt") 
            pose_cam2world44 = np.eye(4, dtype=np.float32)
            pose_cam2world44[:3,:4] = poses[i].reshape(3,4)
            np.savetxt(pose_txtfile, pose_cam2world44)
            #sys.exit()
    
    if 1:
        run_main(
            data_root = "/nfs/STG/SemanticDenseMapping/data/WheatstoneData_nocc/test_team/", 
            dst_dir = "./data/WheatstoneData_nocc/"
            )