import time
import serial
import sqlite3
import adafruit_fingerprint


uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

# Connect to the database (creates a new file if it doesn't exist)
conn = sqlite3.connect('fingerprint.db')
c = conn.cursor()

# Create the table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS fingerprints (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
''')


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


def enroll_finger_in_dir(location=str):
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


def verify_finger():
    """Get a finger print image, template it, and see if it matches!"""
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    if finger.finger_fast_search() != adafruit_fingerprint.OK:
        return False
    return True


# Enroll a new fingerprint and add its information to the database
def save_finger_in_database(location, name):
    # Enroll the fingerprint (code from previous example)
    # ...
    # If enrollment was successful, add the information to the database
    c.execute('INSERT INTO fingerprints VALUES (?, ?)', (location, name))
    conn.commit()


def search_finger_in_database(location):
    """Search for a fingerprint in the database and return the name if found"""
    # Verify the fingerprint (code from previous example)
    # ...
    # If verification was successful, search the database for the fingerprint ID
    c.execute('SELECT name, unique_id FROM fingerprints WHERE id = ?', (location,))
    result = c.fetchone()
    if result:
        name = result
        return name
    else:
        return None