import sys
import cv2
from datetime import datetime

font = cv2.FONT_HERSHEY_PLAIN
line = cv2.LINE_AA

def gstreamer_pipeline(capture_width=1920, capture_height=1080, display_width=640, display_height=480, framerate=60,
                       flip_method=0):
  return ('nvarguscamerasrc ! '
          'video/x-raw(memory:NVMM), '
          'width=(int)%d, height=(int)%d, '
          'format=(string)NV12, framerate=(fraction)%d/1 ! '
          'nvvidconv flip-method=%d ! '
          'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
          'videoconvert ! '
          'video/x-raw, format=(string)BGR ! appsink' % (
          capture_width, capture_height, framerate, flip_method, display_width, display_height))

cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

# Check if camera opened successfully
if not cap.isOpened():
  print("Unable to read camera")
  cap.release()
  sys.exit('Failed to open camera!')

frame_width = int(cap.get(3))
print('frame width: ', frame_width)
frame_height = int(cap.get(4))
print('frame height: ', frame_height)

record_flag = False
save_flag = False



while(True):

  ret, frame = cap.read() 

  if ret: 
    
    if record_flag:
      shown_frame = frame.copy()
      shown_text = 'RECORDING' #{:.1f}'.format(fps)
      help_text = 'to stop and save the video, Press "S"' 
      help_text_con = 'afterwards, you can press "R" again to start recording another video'
      cv2.putText(shown_frame, shown_text, (50, int(frame_height - 50)), font, 2.0, (0, 0, 255), 4, line)
      cv2.putText(shown_frame, help_text, (10, 20), font, 1.0, (0, 0, 0), 4, line)
      cv2.putText(shown_frame, help_text, (11, 20), font, 1.0, (255, 255, 255), 1, line)
      cv2.putText(shown_frame, help_text_con, (10, 40), font, 1.0, (0, 0, 0), 4, line)
      cv2.putText(shown_frame, help_text_con, (11, 40), font, 1.0, (255, 255, 255), 1, line)
      out.write(frame)
      # print('capturing')
      cv2.imshow('frame', shown_frame)
    else:
      shown_frame = frame.copy()
      help_text = 'Press "R" to start recording a video'
      help_text_end = 'to close the program, Press "Esc"' 
      cv2.putText(shown_frame, help_text, (10, 20), font, 1.0, (0, 0, 0), 4, line)
      cv2.putText(shown_frame, help_text, (11, 20), font, 1.0, (255, 255, 255), 1, line)
      cv2.putText(shown_frame, help_text_end, (10, 40), font, 1.0, (0, 0, 0), 4, line)
      cv2.putText(shown_frame, help_text_end, (11, 40), font, 1.0, (255, 255, 255), 1, line)      
      cv2.imshow('frame', shown_frame)
      
   
  else:
    print("Unable to read camera")
    break 
   # Press Esc to stop recording
  key = cv2.waitKey(1)
  if key == 27:
    out.release()
    cv2.destroyAllWindows() 
    cap.release()
    break
  
  elif key == ord('r'):
    if not record_flag:
      now = datetime.now()
      datepart = now.strftime("%d-%m-%Y_%H-%M-%S")
      output_name = 'capture-' + datepart + '.mp4'
      out = cv2.VideoWriter(output_name, cv2.VideoWriter_fourcc(*'MP4V'), 20, (frame_width,frame_height))
      record_flag = True
      save_flag = False
    else:
      continue

  elif key == ord('s'):
    if record_flag:
      save_flag = True
      record_flag = False
    else: 
      continue

  else:
    continue
  
  if save_flag:
    out.release()
    record_flag = False
    save_flag = False
    shown_frame = frame.copy()
    shown_text = 'SAVING... Please wait!'
    cv2.putText(shown_frame, shown_text, (50, int(frame_height - 50)), font, 2.0, (0, 128, 255), 4, line)
    cv2.imshow('frame', shown_frame)
    cv2.waitKey(2000)

out.release()
cv2.destroyAllWindows() 
cap.release()

