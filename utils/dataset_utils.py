import os 
import shutil
import numpy as np
from matplotlib import pyplot as plt

def correct_dataset(dataset_path, remove_useless=True):
    for subject in os.listdir(dataset_path):
        patterns = [
            f"{subject}_color_0.png",
            f"{subject}_color_1.png",
            f"{subject}_depth_image_0.png",
            f"{subject}_depth_image_1.png",
            f"{subject}_ir_image_0.png",
            f"{subject}_ir_image_1.png",
            f"{subject}_points_0.ply",
            f"{subject}_points_1.ply",
            f"{subject}_smooth_depth_color_image_0.png",
            f"{subject}_smooth_depth_color_image_1.png",
            f"{subject}_transformed_point_0.ply",
            f"{subject}_transformed_point_1.ply"
        ]
        for emotion in os.listdir(os.path.join(dataset_path, subject)):
            img_path = os.path.join(dataset_path, subject, emotion)
            
            
            if os.path.exists(os.path.join(img_path, '00')):
                os.rmdir(os.path.join(img_path, '00'))
                
            for i, file in enumerate(os.listdir(os.path.join(img_path))):
                if file != patterns[i]:
                    os.rename(os.path.join(img_path, file), os.path.join(img_path, patterns[i]))
            
            if remove_useless:
                for i in range(2):
                    if os.path.exists(os.path.join(img_path, f'{subject}_ir_image_{i}.png')):
                        os.remove(os.path.join(img_path, f'{subject}_ir_image_{i}.png'))
                    if os.path.exists(os.path.join(img_path, f'{subject}_smooth_depth_color_image_{i}.png')):
                        os.remove(os.path.join(img_path, f'{subject}_smooth_depth_color_image_{i}.png'))
                    if os.path.exists(os.path.join(img_path, f'{subject}_points_{i}.ply')):
                        os.remove(os.path.join(img_path, f'{subject}_points_{i}.ply'))
                    if os.path.exists(os.path.join(img_path, f'{subject}_transformed_point_{i}.ply')):
                        os.remove(os.path.join(img_path, f'{subject}_transformed_point_{i}.ply'))
                    
            os.makedirs(os.path.join(img_path, '00'), exist_ok=True)
            

def clean_instructions_file(instructions_path, instructions_out_path):
    
    with open(instructions_path, 'r') as f:
        content = f.read()  
    with open(instructions_out_path, 'w') as f:
        f.write(content.lower())
    


def read_instuction_file(dataset_instructions_path):
    
        
        
            
    translate = {
        'anger': 'Colere',
        'disgust': 'Degout',
        'happiness': 'Joie',
        'neutrality': 'Neutre', 
        'fear': 'Peur', 
        'surprise': 'Surprise',
        'sadness': 'Tristesse',
        'no emotion' : 0
    }
    
    instructions = []
    with open(dataset_instructions_path, 'r') as f:
        for row in f:
            cols = [col.strip() for col in row.split(';')]
            subject, emotion, image, folder = cols
            instructions.append({
                'subject': 'K' + str(int(subject[2:])).zfill(3),
                'emotion': translate.get(emotion, 0),
                'image': image,
                'folder': translate.get(folder, 1)
            })
    return instructions



def clean_dataset(dataset_path, instructions):
    for row in instructions:
        sub_path = os.path.join(dataset_path, row['subject'])

        if row['emotion'] == 0:
            for emotion in os.listdir(sub_path):
                path = os.path.join(sub_path, emotion)
                for img in os.listdir(path)[1:]:
                    for i in range(2):
                        color_path = row['subject'] + '_color_' + str(i) + '.png'
                        depth_path = row['subject'] + '_depth_image_' + str(i) + '.png'
                        if os.path.exists(os.path.join(path, color_path)):
                            shutil.move(os.path.join(path, color_path), os.path.join(path,'00',color_path))
                        if os.path.exists(os.path.join(path, depth_path)):
                            shutil.move(os.path.join(path, depth_path), os.path.join(path,'00',depth_path))

        
        else :
            
            path = os.path.join(sub_path, row['emotion'])
            color_path = row['subject'] + '_color_' + str(int(row['image'])-1) + '.png'
            depth_path = row['subject'] + '_depth_image_' + str(int(row['image'])-1) + '.png'
            
            if row['folder'] == 0:
                if os.path.exists(os.path.join(path, color_path)):
                    os.remove(os.path.join(path, color_path))
                if os.path.exists(os.path.join(path, depth_path)):
                    os.remove(os.path.join(path, depth_path))
            
            if row['folder'] == 1:
                if os.path.exists(os.path.join(path, color_path)):
                    shutil.move(os.path.join(path, color_path), os.path.join(path,'00',color_path))
                if os.path.exists(os.path.join(path, depth_path)):
                    shutil.move(os.path.join(path, depth_path), os.path.join(path,'00',depth_path))
            
            else:
                new_color_path = row['subject'] + '_color_' + str(int(row['image'])-1) + f'_{row['emotion']}_moved.png'
                new_depth_path = row['subject'] + '_depth_image_' + str(int(row['image'])-1) + f'_{row['emotion']}_moved.png'
                if os.path.exists(os.path.join(path, color_path)):
                    shutil.move(os.path.join(path, color_path), os.path.join(sub_path, row['folder'], new_color_path))
                if os.path.exists(os.path.join(path, depth_path)):
                    shutil.move(os.path.join(path, depth_path), os.path.join(sub_path, row['folder'], new_depth_path))


def count_images(dataset_path):
    nb_img = 0
    for subject in os.listdir(dataset_path):
        for emotion in os.listdir(os.path.join(dataset_path, subject)):
            for img_name in os.listdir(os.path.join(dataset_path, subject, emotion))[1:]:
                if 'color' in img_name:
                    nb_img += 1 
    return nb_img


def load_dataset(dataset_path):
    nb_img = count_images(dataset_path)
    
    img_rgb = np.empty(shape=(nb_img, 1080, 1920, 3), dtype=np.float32)
    img_depth = np.empty(shape=(nb_img, 288, 320, 3), dtype=np.float32)
    targets = []

    i = 0
    j = 0
    for subject in os.listdir(dataset_path):
        for emotion in os.listdir(os.path.join(dataset_path, subject)):
            for img_name in os.listdir(os.path.join(dataset_path, subject, emotion))[1:]:
                img = np.array(plt.imread(os.path.join(dataset_path, subject, emotion, img_name)))
                if 'color' in img_name:
                    img_rgb[i] = img
                    i += 1
                    targets.append(emotion) 
                if 'depth' in img_name:
                    img_depth[j] = img
                    j += 1
    
    return img_rgb, img_depth, np.array(targets)