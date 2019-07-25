import cv2

take_every = 30

cap = cv2.VideoCapture('Biscuit_Video.mp4')
ret, current_frame = cap.read()
previous_frame = current_frame

#def frame_val(frame):
#	for x in 

count = 1
while(cap.isOpened()):
    current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)    

    frame_diff = cv2.absdiff(current_frame_gray,previous_frame_gray)

    cv2.imshow('frame diff ',frame_diff)
    sum = frame_diff.sum()
    if sum > 5000000:
    	previous_frame = current_frame.copy()
    	count+=1
    	if not count%take_every:
    		name = "./Images/frame%d.jpg"%(count//take_every)
    		cv2.imwrite(name, previous_frame)
    	
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    
    ret, current_frame = cap.read()

cap.release()
cv2.destroyAllWindows()