#Importing Librarires necessary for the program to run.
import picamera2
import face_rec_module as frm
import face_recognition as face
import numpy as np
import libcamera
import multiprocessing
import cv2
import time
import os


#Raspbery Pi camera Confgurations
picam2 = picamera2.Picamera2()
preview_config = picam2.create_preview_configuration(main={"format": 'RGB888', "size": (320, 240)},                                             
                                                    lores={"format": 'YUV420', "size": (320, 240)},
                                                    transform=libcamera.Transform(hflip=1))
                                                    


#Path of directories
known_face_dir = "/home/bounty/main/database/known_face_dir"
known_face_encodings_dir = "/home/bounty/main/database/known_face_encodings"

#Global Variables
known_face_encodings = []
known_face_names = []
img_array = np.empty((240, 320, 3), dtype=np.uint8)
counter = 0

#Functions



#_____MAIN-PROGRAM______#

if __name__ == "__main__":
    print("Starting>>>...")
    print("Creating/Loading faces.....")
    
    #Generating and Loading saved encodings
    known_face_names, known_face_encodings = frm.generate_face_encodings_with_checking(known_face_dir, known_face_encodings_dir)
    print("Names: ", known_face_names)

    print("\nStarting camera...\n")
    picam2.start()
    time.sleep(10)
    while True:
        start = time.time()
        img_array = picam2.capture_array("main")
        cv2.imshow('Preview', img_array.copy())
        cv2.waitKey(1)

        #if counter%15 == 0:
        face_locations = face.face_locations(cv2.coloermg_array)
        print("Found {} faces in image.".format(len(face_locations)))
        face_encodings = face.face_encodings(img_array, face_locations)

        try:
            for i in range(len(face_encodings)):
                match = face.compare_faces(known_face_encodings, face_encodings[i])

                if match[0]:
                        print("Found...{}".format(known_face_names[i]))
        except:
            pass
            
        end = time.time()
        print("Time Taken: ", end-start)




    
    


'''
if __name__=='__main__':
    start = time.time()
    p0 = multiprocessing.Process(target=face.load_image_file, args=(known_face_dir+"/spandan.jpg",))
    p1 = multiprocessing.Process(target=face.load_image_file, args=(known_face_dir+"/swikar.jpg",))
    p2 = multiprocessing.Process(target=face.load_image_file, args=(known_face_dir+"/shounak.jpg",))
    
    im1 = p0.start()
    im2 = p1.start()
    im3 = p2.start()

    p0.join()
    p1.join()
    p2.join()
    print(time.time()-start)

    p0 = multiprocessing.Process(target=face.face_encodings, args=(im1,))
    p1 = multiprocessing.Process(target=face.face_encodings, args=(im2,))
    p2 = multiprocessing.Process(target=face.face_encodings, args=(im3,))
    start = time.time()

    #names, face_encodings = frm.generate_face_encodings_from_dir(known_face_dir)

    for i in range(len(names)):
        p = 'p' + str(i)
        globals()[p] = multiprocessing.Process(target=frm.save_binary_file, args=(face_encodings[i], known_face_encodings, names[i])) 
        #print("Succes")
    print(names)
    
    
    print(p0.start())
    print(p1.start())
    print(p2.start())
    p0.join()
    p1.join()
    p2.join()
    #print(frm.read_binary_file(known_face_encodings+'/'))
    print(time.time()-start)
    '''