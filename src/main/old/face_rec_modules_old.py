import face_recognition
import numpy as np
import os

def generate_face_encoding(path_to_dir=str):
    """Function to create face encodings,
    Takes path of the image directory as an input and returns a dictionary containing img name with its corresponding ndArrays"""
    face_encodings_dict = {}
    images_with_path_list = []

    #Getting .jpg images from the input directory
    for root, dirs, files in os.walk(path_to_dir):
         for file in files:
            if file.endswith('.jpg'):
                #print(root+'/'+str(file))
                images_with_path_list.append(root+'/'+str(file))
    #print(images_with_path_list)

    #Generating face encodings and storing them in a list
    for imgpath in images_with_path_list:
        temp_face = face_recognition.load_image_file(imgpath)
        temp_face_encoding = face_recognition.face_encodings(temp_face)[0]
        face_encodings_dict[imgpath.replace(path_to_dir+'/', '')] = temp_face_encoding
        #print("Temp\n", temp_face_encoding)  
    #print(face_encodings)

    return face_encodings_dict


def save_face_encodings(face_encodings=dict, path_to_dir=str):
    """Function to store the arrays locally on the machine in the form of binary files
        Takes two inputs 1. Dictionary 2. Path to directory as str"""
    
    for img_file_name in face_encodings:
        np.save(os.path.join(path_to_dir, img_file_name), face_encodings[img_file_name])


def check_face_encodings_in_files(face_encoding=np.ndarray, path_to_dir=str):
    """Function to check an existing face encodings stored in binary files.
        Takes path to directory and an array to compare against, to return a boolean value and the matching array"""

    file_check = False
    output_array = np.ndarray

    for root, dirs, files in os.walk(path_to_dir):
         for file in files:
            if file.endswith('.npy'):
                #print(root+'/'+str(file))
                arry_bin = np.load(os.path.join(path_to_dir, file))

                if (face_encoding == arry_bin).all():
                    file_check=True
                    output_array = arry_bin
                    
    
    return file_check, output_array