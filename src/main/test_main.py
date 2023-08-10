import picamera2
import libcamera
import os

import face_recognition as face
import numpy as np

#Directory Paths
database = "/home/bounty/main/database"
image_db = "/home/bounty/main/database/images"
face_db = "/home/bounty/main/database/face_bins"



def list_content_0f_dir(path):
    dirs = []
    filenames = []
    if os.path.exists(path):
        dirs = os.listdir(path)
        
        print(dirs)

def generate_and_save_face_encodings(img_db_path, face_db_path):
    if os.path.exists(img_db_path):
        #Checking and Storing images in the img db
        for  dirpath, dirnames, filenames in os.walk(img_db_path):

            #Printing teh data in os.walk
            #print(dirpath, dirnames, filenames)

            #Checking for sub-directoires in face_bin
            if dirnames != None:
                #Checking if the sub directory exits, if not then create one!!
                for dirname in dirnames:
                    if os.path.exists(os.path.join(face_db, dirname)) != True:
                        print(dirname, ", does not exists...")
                        print(">> Creating directory,", dirname)
                        os.mkdir(os.path.join(face_db, dirname))
                        print(">> Done" , end="\n\n")

                    else:
                        pass
            
            #

            if filenames != None:
                print("Checking for new images")
                for filename in filenames:
                    #Checking for img files
                    if filename.endswith(('.jpg', '.png', '.jpeg')):

                        #Debugging for path and boolean values
                        #Uncomment the lines below for printing path and if the path does exists
                        #print(os.path.join(face_db_path, filename.split('_')[0], os.path.splitext(filename)[0] + ".npy"), end=":  ")
                        #print(os.path.exists(os.path.join(face_db_path, filename.split('_')[0], os.path.splitext(filename)[0] + ".npy")))


                        if os.path.exists(os.path.join(face_db_path, filename.split('_')[0], os.path.splitext(filename)[0] + ".npy")) == False:
                            print("Found new img: ", filename)
                            print(">> Starting generation....")
                            print(">> Loading image..")
                            img = face.load_image_file(os.path.join(dirpath, filename))
                            print(">> Done")
                            print(">> Generating FACE ENCODING for: ", filename)
                            face_location = face.face_locations(img)
                            face_encoding = face.face_encodings(img, face_location)
                            #print(face_encoding)
                            print(">> Done")
                            print(">> Saving encoding....")
                            #print(os.path.join(face_db+filename.remove('.jpg'), os.path.splitext(filename)[0]))
                            np.save(os.path.join(face_db_path, filename.split('_')[0], os.path.splitext(filename)[0]), face_encoding)
                            print(">> Done")
                        
                        else:
                            print("No new image file found")
    else:
        print("The path does not exits!!")                    

def load_face_encodings(face_db_path: str):
    """Takes input as path to load the data from and returns a dictionary containing the name and list of face encodings"""
    data = {}

    if os.path.exists(face_db_path):
        for  dirpath, dirnames, filenames in os.walk(face_db_path):
            #print(dirpath, dirnames, filenames)

            if dirnames != None:
                for dirname in dirnames:
                    data.update({dirname: []})

            if filenames != None:
                print("Loading face encodings...")
                face_encodings = []
                for filename in filenames:
                    face_encoding = np.load(os.path.join(dirpath, filename))
                    #print(face_encoding)
                    face_encodings.append(face_encoding)
                #print(face_encodings)
                #print(dirpath.rsplit('/', 1)[-1])
                data.update({dirpath.rsplit('/', 1)[-1]: face_encodings})
        #print(data)

            

                        


        




if __name__ == "__main__":
    print("Starting>>>>.....")
    print("Creating/Loading faces......")
    generate_and_save_face_encodings(image_db, face_db)
    #list_content_0f_dir(face_db)
    load_face_encodings(face_db)