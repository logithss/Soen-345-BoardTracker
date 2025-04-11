import numpy as np
import cv2
import win32api, win32con

global pointerPos
global rawUnitPos
global controlMouse
controlMouse = False

global matrix
pts1=np.float32([[0,0],[1,0],[1,1],[0,1]]) 
pts2=np.float32([[184, 90],[393, 60],[395, 295],[191, 301]])
matrix=cv2.getPerspectiveTransform(pts2, pts1)

cap = cv2.VideoCapture(1)

def getPointerPosition():
    global pointerPos
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask1 = cv2.inRange(hsv, (170, 128, 128), (180, 255, 255)) # pinkish red
    mask2 = cv2.inRange(hsv, (  0, 128, 128), ( 10, 255, 255)) # yellowish red

    maskFinal = mask1+mask2

    # set my output img to zero everywhere except my mask
    output_img = frame.copy()

    ret,thresh1 = cv2.threshold(gray,240,255,cv2.THRESH_BINARY)
    ret,thresh2 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
    ret,thresh3 = cv2.threshold(gray,127,255,cv2.THRESH_TRUNC)
    ret,thresh4 = cv2.threshold(gray,240,255,cv2.THRESH_TOZERO)
    ret,thresh5 = cv2.threshold(gray,127,255,cv2.THRESH_TOZERO_INV)
    
    kernel = np.ones((3,3),np.uint8)
    dilated = cv2.dilate(thresh4, kernel, iterations=1)

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (0,255,0),1)

    if len(contours) > 0:
        contourLength = cv2.arcLength(contours[0], True)
        if contourLength < 35:
            pointerPos = (int(contours[0][0][0][0]), int(contours[0][0][0][1]))
            pointerCoordinateText = str(pointerPos[0]) + ", " + str(pointerPos[1])
            cv2.putText(frame, pointerCoordinateText, (200,40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1,)
            cv2.putText(frame, str(contourLength), (200,80), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1,)
        else:
           pointerPos = None
    else:
        pointerPos = None

    # Display the resulting frame
    #if cv2.countNonZero(dilated) == 0:
    #    cv2.rectangle(frame,(0,0),(200,200),(0,255,0),3)
    cv2.imshow('frame',frame)
    cv2.imshow('gray',gray)
    cv2.imshow('hsv',hsv)
    cv2.imshow('maskFinal',maskFinal)
    cv2.imshow('thresh1',thresh1)
    cv2.imshow('thresh4',dilated)

def performPointerMapping():
    global pointerPos
    global rawUnitPos
    p=pointerPos
    px = (matrix[0][0]*p[0] + matrix[0][1]*p[1] + matrix[0][2]) / ((matrix[2][0]*p[0] + matrix[2][1]*p[1] + matrix[2][2]))
    py = (matrix[1][0]*p[0] + matrix[1][1]*p[1] + matrix[1][2]) / ((matrix[2][0]*p[0] + matrix[2][1]*p[1] + matrix[2][2]))
    rawUnitPos = (max(0, min(px, 1)), max(0, min(py, 1)))
    p_after = (int(px*800), int(py*400))
    perspResult = np.zeros((400,800,3), np.uint8)
    cv2.putText(perspResult, str(rawUnitPos[0]) + ", " + str(rawUnitPos[1]), (200,40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1,)
    #cv2.putText(perspResult, str(random.random()), (200,20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1,)
    cv2.circle(perspResult,p_after, 5, (0,0,255), 5)
    if controlMouse:
        cv2.circle(perspResult,(10, 10), 5, (0,255,0), 5)
    else:
        cv2.circle(perspResult,(10, 10), 5, (0,0,170), 5)
    cv2.imshow('perspResult',perspResult)

def handleMousePosition():
    global controlMouse
    global rawUnitPos
    if controlMouse:
        win32api.SetCursorPos((int(1920+rawUnitPos[0]*800), int(rawUnitPos[1]*600)))
while(True):
    if cv2.waitKey(1) & 0xFF == ord('r'):
        print(str(pointerPos[0]) + ", " + str(pointerPos[1]))
    if cv2.waitKey(1) & 0xFF == ord('1'):
        controlMouse = True
    if cv2.waitKey(1) & 0xFF == ord('2'):
        controlMouse = False
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    getPointerPosition()
    if pointerPos != None:
        performPointerMapping()
        handleMousePosition()
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()