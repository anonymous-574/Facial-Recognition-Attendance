import os ,ctypes, sys , cv2 , math , face_recognition , numpy as np

#ctypes.windll.user32.MessageBoxW(0, "Your text", "Your title", 1)

##  Styles:
##  0 : OK
##  1 : OK | Cancel
##  2 : Abort | Retry | Ignore
##  3 : Yes | No | Cancel
##  4 : Yes | No
##  5 : Retry | Cancel 
##  6 : Cancel | Try Again | Continue


def face_confidence (face_distance , face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance)/(range*2)

    if face_distance > face_match_threshold:
        raise str(round(linear_val*100,2))+ "%"
    else:
        value = (linear_val+ ((1.0-linear_val)*math.pow((linear_val-0.5)*2,0.2)))*100
        return str(round(value,2))+"%"


class face_Recog:
    #encoding is basically converting the image to a matrix to use it easier
    #we actually compare the encodings of image from webcam and premade image
    face_location=[]
    face_encoding=[]
    face_names=[]
    known_face_encoding=[]
    known_face_names=[]
    found=[]
    process_current_frame=True

    def __init__(self):
        self.encode_faces()

    # MAKE THE DIRECTORY FIRST
    def encode_faces(self):
        for image in os.listdir("D:/code/python_code/me/face_test/face"):
            face_image = face_recognition.load_image_file(f"D:/code/python_code/me/face_test/face/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encoding.append(face_encoding)
            self.known_face_names.append(image)
            self.found.append(False)

    def run_recognition(self):
        user_video=cv2.VideoCapture(0)

        if not user_video.isOpened():
            sys.exit("WHERE IS YO WEBCAM")

        while True:
            success , frame = user_video.read()

            if self.process_current_frame:
                small_frame = cv2.resize(frame , (0,0),fx=0.25,fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame,cv2.COLOR_BGR2RGB)

                self.face_location= face_recognition.face_locations(rgb_small_frame)
                self.face_encoding= face_recognition.face_encodings(rgb_small_frame, self.face_location)

                self.face_names=[]
                for face in self.face_encoding:
                    match = face_recognition.compare_faces(self.known_face_encoding,face)
                    name = "Unknown"
                    confidence="Unknown"

                    face_dist = face_recognition.face_distance(self.known_face_encoding,face)
                    best_match_idx = np.argmin(face_dist)

                    if match[best_match_idx]:
                        name=self.known_face_names[best_match_idx]
                        confidence=face_confidence(face_dist[best_match_idx])
                        self.found[best_match_idx]=True

                    self.face_names.append(f"{name} {confidence}")

            self.process_current_frame=not self.process_current_frame

            for (top,right,bottom,left) ,name in zip (self.face_location , self.face_names):
                #cvt to orig
                top*=4
                right*=4
                bottom*=4
                left*=4

                cv2.rectangle(frame, (left,top), (right,bottom),(0,0,255),2)
                cv2.rectangle(frame, (left,bottom-35), (right,bottom),(0,0,255),-1)
                cv2.putText(frame,name,(left+6,bottom-6),cv2.FONT_HERSHEY_DUPLEX,0.8,(255,255,255),1)
                
            cv2.imshow("Face Recognition",frame)

            if cv2.waitKey(1) ==ord('q'):
                break
            
        user_video.release()
        cv2.destroyAllWindows()

    def final_result(self):
        absent_names=[]
        for i in range(len(os.listdir("D:/code/python_code/me/face_test/face"))):
            if self.found[i]==False:
                absent_names.append(self.known_face_names[i])

        ctypes.windll.user32.MessageBoxW(0, f"{absent_names}", "ABSENTEE LIST", 1)







def main():
    face = face_Recog()
    face.run_recognition()
    face.final_result()

if __name__ =="__main__":
    main()
