import os
import sys
import shutil
from PIL import Image
import face_recognition

sys.setrecursionlimit(1000000)

os.chdir(os.path.dirname(os.path.realpath(__file__)))

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

bad_face_path = str(input("Path to BAD face (jpg): "))
if os.path.exists(bad_face_path) == False:
	print("BAD face file not found. Closing...")
	input()
	exit()
elif bad_face_path.split(".")[-1] != "jpg" and bad_face_path.split(".")[-1] != "jpeg":
	print("BAD face file exists, but is not a 'jpg' or 'jpeg'. Closing...")
	input()
	exit()

image = face_recognition.load_image_file(bad_face_path)

try:
    image_face_encoding = face_recognition.face_encodings(image)[0]
except IndexError:
    print("No face detected. Closing...")
    input()
    exit()

known_faces = [
    image_face_encoding
]

try:
	os.mkdir(os.path.join(desktop, "BAD"))
except:
	pass

try:
	os.mkdir(os.path.join(desktop, "GOOD"))
except:
	pass

def analyze(face):
	try:
		picture = face_recognition.load_image_file(face)
		picture_face_encoding = face_recognition.face_encodings(picture)[0]
		results = face_recognition.compare_faces(known_faces, picture_face_encoding)
		for i in results:
			if i:
				return True
		return False
	except:
		return False

def enum(folder):
	os.chdir(folder)
	for FILE in os.listdir():
		if FILE.split(".")[-1] == "jpg" or FILE.split(".")[-1] == "jpeg":
			if analyze(FILE):
				shutil.copy(FILE, os.path.join(desktop, os.path.join("BAD", FILE.split("\\")[-1])))
				print(FILE, "is BAD!")
			else:
				shutil.copy(FILE, os.path.join(desktop, os.path.join("GOOD", FILE.split("\\")[-1])))
				print(FILE, "is GOOD!")

enum(str(input("Path to images folder: ")))
