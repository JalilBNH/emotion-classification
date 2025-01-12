from utils import clean_dataset, clean_instructions_file, correct_dataset, read_instuction_file, load_dataset


dataset_path = './Data/Kinect'
instruction_file_path = './Data/instructions.txt'

# Try this first 
#clean_instructions_file('./Data/BestImages.txt', instruction_file_path)
#instructions = read_instuction_file(instruction_file_path)

#correct_dataset(dataset_path)
#clean_dataset(dataset_path, instructions)

# After try this
print('ca arrive')
img_rgb, img_depth, targets = load_dataset(dataset_path)
print(img_rgb.shape)
print(img_depth.shape)
print(targets.shape)