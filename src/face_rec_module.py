import face_recognition
import numpy as np
import os


#Functions
def generate_face_encodings_from_dir(dir=str):
    """Function to generate and extract name(s) form the given directory and return the 
        names and encodings in the form of lists."""
    face_encodings=[]
    face_names=[]

    for filename in os.listdir(dir):
        #print(filename)
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image = face_recognition.load_image_file(os.path.join(dir, filename))
            encoding = face_recognition.face_encodings(image)[0]
            face_encodings.append(encoding)
            face_names.append(os.path.splitext(filename)[0])
    
    return face_names, face_encodings

def generate_face_encoding(path_to_image):
    """This Function takes the img path as argument and returns the list of ndarray of the face"""
    img_ndarray = face_recognition.load_image_file(path_to_image)
    data = face_recognition.face_encodings(img_ndarray)[0]

    return data

def read_binary_file(file_path):
    """Function for loading binary file from the given path and return the it
        in the form of list"""

    data = []

    if file_path.endswith('.npy'):
        data = np.load(file_path)
    elif file_path.endswith('.npz'):
        with np.load(file_path) as data:
            data = [data[key] for key in data]
    return data

def save_binary_file(data, directory, filename, file_format='.npy'):
    """This function takes four arguments: data, directory, filename, and file_format. 
        The data argument is the data to be stored in the binary file. The directory argument is the path to the directory where the binary file
        should be saved. The filename argument is the name of the binary file. The file_format argument specifies the format of the binary file and can be either 'npy' or 'npz'"""
    file_path = os.path.join(directory, filename)
    #Debugging for path and file(s), name
    #print(file_path)
    #print(file_path+file_format)
 
    if not os.path.exists(file_path+file_format):
        if file_format == '.npy':
            np.save(file_path, data)
            print("Success")
        elif file_format == '.npz':
            np.savez(file_path, data)

def generate_face_encodings_with_checking(known_face_dir, check_encoding_dir):
    """This function takes two arguments: encoding_dir and check_dir. The encoding_dir argument is the path to the directory where the images for generating face encodings are located. 
    The check_dir argument is the path to the directory where the generated encodings should be saved and checked."""
    encodings = []
    filenames = []
    for img_file in os.listdir(known_face_dir):
        img_path = os.path.join(known_face_dir, img_file)
        encoding_path = os.path.join(check_encoding_dir, os.path.splitext(img_file)[0] + '.npy')
        if os.path.exists(encoding_path):
            face_encoding = np.load(encoding_path)
        else:
            image = face_recognition.load_image_file(img_path)
            face_encodings = face_recognition.face_encodings(image)
            #removing saving functionality
            if face_encodings:
                face_encoding = face_encodings[0]
            #    np.save(encoding_path, face_encoding)
        encodings.append(face_encoding)
        filenames.append(img_file)
    return filenames, encodings


