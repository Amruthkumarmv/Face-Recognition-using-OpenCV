import cv2
from simple_facerec import SimpleFacerec
import datetime
import math
import csv

nameStatus = {}
nameLastUpdate = {}
enteringTime = {}

unknowncount = 0
now = datetime.datetime.now()

logfilename = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '_logs.csv'
print(logfilename)
logfile = open(logfilename,'a')
writer = csv.writer(logfile)
# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")


# Load Camera
cap = cv2.VideoCapture(0)

i=0

while True:
    ret, frame = cap.read()
    currentTime = datetime.datetime.now()
    # Detect Faces
    face_locations, face_names = sfr.detect_known_faces(frame)
    
    

    for face_loc, name in zip(face_locations, face_names):
        
        if not name in nameStatus:
            logfile = open(logfilename,'a')
            
            INcache = (name+' has entered at ' )
            i=i+1
            tp = (i,INcache,(str(currentTime.hour) + ':' + str(currentTime.minute) + ':' + str(currentTime.second)))
            writer.writerow(tp)
            # logfile.write(name+' has entered at - ' + str(currentTime.hour) + ':' + str(currentTime.minute) + ':' + str(currentTime.second) + '\n')
            print(name+' has entered')
            nameStatus[name]='IN'
            nameLastUpdate[name]=currentTime
            enteringTime[name]=currentTime
        else:
            lastUpdateTime = nameLastUpdate[name]
            difference = currentTime - lastUpdateTime
            if difference.seconds < 10:
                print('last_update_time_too_close : not changing status')   
            else:
                if nameStatus[name] == 'IN':
                    timein = currentTime - enteringTime[name]
                    minutesIn = math.floor(timein.seconds /60)
                    secondsIn = timein.seconds %60
                    i=i+1
                    INcache = (name+' has left at - ')
                    tp = (i,INcache,(str(currentTime.hour) + ':' + str(currentTime.minute) + ':' + str(currentTime.second)),('Duration - ' + str(minutesIn) + ' mins ' + str(secondsIn)))
                    writer.writerow(tp)
                    # INcache = ('...........Duration - ' + str(minutesIn) + ' mins ' + str(secondsIn) + 'secs \n')
                    # tp = (i,INcache)
                    # writer.writerow(tp)
                    
                    
                    # logfile.write(name+' has left at - ' + str(currentTime.hour) + ':' + str(currentTime.minute) + ':' + str(currentTime.second)+'\n')
                    # logfile.write('...........Duration - ' + str(minutesIn) + ' mins ' + str(secondsIn) + 'secs \n' )
                    print(name+' has left.')
                    nameStatus[name] = 'OUT'
                else:
                    
                    INcache = (name+' has entered at - ')
                    i=i+1
                    tp = (i,INcache,(str(currentTime.hour) + ':' + str(currentTime.minute) + ':' + str(currentTime.second)))
                    writer.writerow(tp)
                   
                   
                    # logfile.write(name+' has entered at - ' + str(currentTime.hour) + ':' + str(currentTime.minute) + ':' + str(currentTime.second) + '\n')
                    print(name+' has entered.')
                    nameStatus[name]='IN'
                    enteringTime[name]=currentTime
            
            nameLastUpdate[name] = currentTime



        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()