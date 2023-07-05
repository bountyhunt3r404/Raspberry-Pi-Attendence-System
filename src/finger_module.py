import time
import serial
import adafruit_fingerprint


uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)


def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""
    print("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching...")
    if finger.finger_fast_search() != adafruit_fingerprint.OK:
        return False
    return True

def enroll_finger(location):
    """Take a 2 finger images and template it, then store in 'location'"""
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Place finger on sensor...", end="", flush=True)
        else:
            print("Place same finger again...", end="", flush=True)
        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="", flush=True)
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Image converted")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not find fingerprint features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Could not find fingerprint features")
            else:
                print("Other error")
            return False
        time.sleep(1)
    if finger.create_model() != adafruit_fingerprint.OK:
        print("Unable to combine fingerprints")
        return False
    if finger.store_model(location) != adafruit_fingerprint.OK:
        print("Unable to store fingerprint template")
        return False
    return True

while True:
    if enroll_finger(1):
        print("Finger enrolled successfully!")
        break
    else:
        print("Failed to enroll fingerprint!")

def verify_finger():
    """Get a finger print image, template it, and see if it matches!"""
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    if finger.finger_fast_search() != adafruit_fingerprint.OK:
        return False
    return True

while True:
    if verify_finger():
        print("Finger verified!")
        break
    else:
        print("Failed to verify fingerprint!")

