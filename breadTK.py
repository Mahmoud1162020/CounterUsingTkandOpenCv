import time
from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk
import numpy as np
import os
import cv2
from tracker import *
import cloud4rpi

# import absl
global variables


tracker = EuclideanDistTracker()
flag = 1

root = Tk()
root.geometry("800x600")
root.configure(bg="black")
root.title("SamaSoft")
root.iconbitmap(r'C:\Users\User\Desktop\samasoftIcon.ico')
f1 = LabelFrame(root, bg="white")
f1.pack()
L1 = Label(f1,bg="white",height=240,width=600)
L1.pack()
frame2 = Frame()
frame2.pack(fill=X)


f2 = LabelFrame(root, bg="white")
f2.pack()
L2 = Label(f1, bg="white", height=300, width=600)
L2.pack()
img = Image.open(r"C:\Users\User\Desktop\samasoftLogo.jpg")
resizedImage = img.resize((200, 205), Image.ANTIALIAS)
my_image = ImageTk.PhotoImage(resizedImage)


v = 0
#Calibration window
def print_value(val):
    print(val)
    global blur
    val=int(val)
    if val == 0:
        blur = 1
    else:
        blur = (val + ((-1) ** (val + 1) - 1) / 2)
    return blur



def updateCounter(cnt):

    Label(root, text =f"العدد: {cnt}",bg="white").place(x=10,y=140,width=80)

def contactUs():
    contactWindow=Toplevel()
    contactWindow.geometry("400x400")
    contactWindow.iconbitmap(r'C:\Users\User\Desktop\samasoftIcon.ico')

    logo_label=Label(contactWindow,image=my_image).pack(pady=10)
    email_label=Label(contactWindow,text="E-mail: mahmoudalsaffar322@gmail.com").pack()
    phone_label=Label(contactWindow,text="Phone No. : 00905346822270").pack()
    addrss_label=Label(contactWindow,text="Turkey , Gaziantep").pack()



setOpen=0
def zeroAcount():
    global starting
    global id
    global cntofpcs
    cntofpcs=0
    starting=True
    id=0
def CalibWindow():
    global setOpen
    print("======", setOpen)

    def on_closing():
        global setOpen
        setOpen=0

        if messagebox.askokcancel("خروج","الخروج من نافذة المعايرة؟"):

            top.destroy()


    if setOpen !=1:
        top = Toplevel()
        top.geometry("800x600")
        top.iconbitmap(r'C:\Users\User\Desktop\samasoftIcon.ico')
        setOpen=top.winfo_exists()
        circle_radius_label = Label(top, text="قطر الدائرة").place(x=40, y=13)
        sensitivity_label = Label(top, text="الحساسية").place(x=40, y=53)
        distancebtcrcl_label = Label(top, text="المسافة بين \nالمراكز").place(x=40, y=93)
        prm1_label = Label(top, text="معامل \nالتشبع1").place(x=40, y=133)
        prm2_label = Label(top, text="معامل \nالتشبع2").place(x=40, y=173)
        dst_label = Label(top, text="مسافة العد").place(x=40, y=213)
        blur_filter_label = Label(top, text="الشفافية").place(x=40, y=253)
        frspd_label = Label(top, text="السرعة").place(x=40, y=303)
        my_label = Button(top, image=my_image, command=contactUs)
        my_label.place(x=300, y=380)

        circle_radius_scale = Scale(top, width=15, orient=HORIZONTAL, command=radius)
        circle_radius_scale.set(rad)
        circle_radius_scale.pack(fill=X, padx=100)

        sensitivityScale = Scale(top, width=15, orient=HORIZONTAL, from_=0, to=1000, command=thresh_callback)
        sensitivityScale.set(threshold * 100)
        sensitivityScale.pack(fill=X, padx=100)
        distancebtcrcl_scale = Scale(top, width=15, orient=HORIZONTAL, from_=0, to=600, command=distancebtcrcl)
        distancebtcrcl_scale.set(disbtcrcls)
        distancebtcrcl_scale.pack(fill=X, padx=100)
        prm1_scale = Scale(top, width=15, orient=HORIZONTAL, from_=0, to=150, command=params)
        prm1_scale.set(param1)
        prm1_scale.pack(fill=X, padx=100)
        prm2_scale = Scale(top, width=15, orient=HORIZONTAL, from_=0, to=150, command=param)
        prm2_scale.set(param2)
        prm2_scale.pack(fill=X, padx=100)
        dst_scale = Scale(top, width=15, orient=HORIZONTAL, from_=0, to=100, command=distance)
        dst_scale.set(vpdist)
        dst_scale.pack(fill=X, padx=100)
        blur_filter_scale = Scale(top, width=15, orient=HORIZONTAL, from_=0, to=100, command=blurF)
        blur_filter_scale.set(blur)
        blur_filter_scale.pack(fill=X, padx=100)
        frspd_scale = Scale(top, width=15, orient=HORIZONTAL, from_=0, to=1000, command=frspeed)
        frspd_scale.set(fspeed)
        frspd_scale.pack(fill=X, padx=100)
        saveButton = Button(top, text="حفظ الاعدادات",
                            command=lambda: saveonfile(threshold, vpdist, disbtcrcls, param1, param2, rad, fspeed,
                                                       blur)).place(x=40, y=400, width=80)
        loaddefaultButton = Button(top, text="اعادة ضبط", command=loaddefault).place(x=140, y=400, width=80)
        top.protocol("WM_DELETE_WINDOW",on_closing)












calibrationButton=Button(root,text="معايرة",command=CalibWindow).place(x=10,y=100,width=80)
zeroButton=Button(root,text="تصفير العداد",command=zeroAcount).place(x=10,y=160,width=80)

developed_by_label=Button(text="Developed by",command=contactUs).place(x=10,y=360,width=80)


def on_closing():
    if messagebox.askokcancel("خروج", "هل تريد الخروج من البرنامج؟"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
cap = cv2.VideoCapture(0)

numberofpeices = 0
disbtcrcls = 95
param1 = 58
param2 = 27
rad = 54
fspeed = 212
blur = 25
count1 = 0
starting = True

total = 0

rflag = 1
# if the dictionary file dosent exiist
if not os.path.isfile('my_file.npy'):
    f = open("my_file.npy", "w+")

filesize = os.path.getsize("my_file.npy")

if filesize == 0:
    with open('my_file.npy', 'w') as f:
        dictionary = {'disbtcrcls': disbtcrcls, 'param1': param1, 'param2': param2, 'rad': rad, 'fspeed': fspeed,
                      'blur': blur}
        np.save('my_file.npy', dictionary)

# file_in = open("mmm.txt", "r")

if not os.path.isfile('mmm.txt'):
    f = open("mmm.txt", "w+")

xx = []

filesize = os.path.getsize("mmm.txt")

print(filesize)

if filesize == 0:
    with open('mmm.txt', 'w') as f:
        f.write(str(19) + '\n' + str(58))
        f.close()

file_in = open('mmm.txt', 'r')

print(file_in)

for yy in file_in.read():

    if yy.isdigit():
        xx.append(float(yy))

        print(xx, len(xx))
        file_in.close()

vpdist = int(xx[-2] * 10 + xx[-1])

threshold = xx[0] + xx[1] * 0.1 + xx[2] * 0.01
read_dictionary = np.load('my_file.npy', allow_pickle='TRUE').item()
disbtcrcls = (read_dictionary['disbtcrcls'])
param1 = (read_dictionary['param1'])
param2 = (read_dictionary['param2'])
rad = (read_dictionary['rad'])
fspeed = (read_dictionary['fspeed'])
blur = (read_dictionary['blur'])
print(param1)


def frspeed(val):
    global fspeed
    val=int(val)
    fspeed = val
    return fspeed


def thresh_callback(val):
    global threshold
    val=int(val)

    threshold = (val / 100) + 0.001

    with open('mmm.txt', 'w') as f:
        f.write(str(threshold) + '\n' + str(vpdist))

    return threshold


def distancebtcrcl(val):
    global disbtcrcls
    val=int(val)
    disbtcrcls = val + 0.01
    return disbtcrcls


def distance(val):
    global vpdist
    val=int(val)
    vpdist = val

    with open('mmm.txt', 'w') as f:
        f.write(str(threshold) + '\n' + str(vpdist))

    return vpdist


def saveonfile(threshold, vpdist, disbtcrcls, param1, param2, rad, fspeed, blur):
    with open('mmm.txt', 'w') as f:
        f.write(str(threshold) + '\n' + str(vpdist))
    dictionary = {'disbtcrcls': disbtcrcls, 'param1': param1, 'param2': param2, 'rad': rad, 'fspeed': fspeed,
                  'blur': blur}
    np.save('my_file.npy', dictionary)


def loaddefault():


    # text = sg.popup_get_text('Title', 'Please input password')
    # if text == "2021b":
    os.remove("mmm.txt")
    os.remove('my_file.npy')
    cap.release()
    cv2.destroyAllWindows()


def blurF(val):
    global blur
    val=int(val)
    if val == 0:
        blur = 1
    else:
        blur = (val + ((-1) ** (val + 1) - 1) / 2)

    return blur


def radius(val):
    global rad
    val=int(val)
    rad = val
    return rad


def param(val):
    global param2
    val=int(val)
    param2 = val + 0.001
    return param2


def params(val):
    global param1
    val=int(val)
    param1 = val + 0.001
    return param1


def NumOfPcs(count):
    cv2.putText(output, f'numberofP={count}', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (170, 10, 100), 2,

                cv2.LINE_AA)
    return count

packages_time = 0
i=0

while True:

    ret2, frame = cap.read()

    # x1, y1, _ = frame.shape

    s = 150  # y1 / 25  # 25

    e = 310  # y1 - 40

    s1 = 50  # x1 / 1.5  # 2

    e1 = 590  # x1 - 40

    # calibration = frame.copy()
    output = frame.copy()
    # image = frame[10:600, 200:500]

    image = frame[int(s):int(e), int(s1):int(e1)]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, int(blur))  # cv2.bilateralFilter(gray,10,50,50)  Must be Odd number

    # detect circles in the image                                 ##\/##very important

    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, threshold, disbtcrcls, param1=param1, param2=param2,
                               minRadius=(rad - 10), maxRadius=rad)

    # the  6th parameter is important for accuracy the more the better>>

    # the 3d parameter for accuracy and the 4d for D.b.C

    # ensure at least some circles were found

    detections = []

    cnt = 0

    if circles is not None:

        cnt = (circles.shape[1])

        # convert the (x, y) coordinates and radius of the circles to integers

        circles = np.round(circles[0, :]).astype("int")

        # print(len(circles))

        # loop over the (x, y) coordinates and radius of the circles

        for (x, y, r) in circles:
            detections.append([x, y, r])

        print("detections")

        print(detections)

        circle_id = tracker.update(detections,vpdist)

        for cir_id in circle_id:
            x, y, r, id = cir_id
            id = id + 1

            cv2.putText(output, str(id), (x + int(s1), y + int(s) - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

            cv2.circle(output, (x + int(s1), y + int(s)), r, (0, 255, 0), 4)

            center = cv2.circle(output, (x + int(s1), y + int(s)), 2, (0, 0, 255), 3)

            # global numberofpeices

            # numberofpeices = numberofpeices + cnt

            # draw the circle in the output image, then draw a rectangle

            # corresponding to the center of the circle

            # cv2.circle(output, (x, y), r, (0, 255, 0), 4)

        # cv2.putText(output, f'numberofP={total}', (70, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,  cv2.LINE_AA)
        # reg=cnt
        # cnt=cnt+reg

        cv2.putText(output, f'number={cnt}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    #    NumOfPcs(cnt)

    # show the output image
    if starting == True:
        id = 0
        starting = False
    cntofpcs = NumOfPcs(id)
    updateCounter(cntofpcs)


    max_thresh = 999

    # packages_time += 1
    # if packages_time == 300:
    #     readings = {'number of pieces': cntofpcs}
    #     device.publish_data(readings)
    #     packages_time = 0

    # cv2.createTrackbar('Canny thresh:', 'output', thresh, max_thresh, thresh_callback)

    # thresh_callback(thresh)



   # add save and reset buttons ------here

    crtflag=0
    img = ImageTk.PhotoImage(Image.fromarray(output))
    img2 = ImageTk.PhotoImage(Image.fromarray(blurred))
    L2['image'] = img2
    L1['image'] = img

    root.update()

