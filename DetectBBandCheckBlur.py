import cv2
net = cv2.dnn.readNet("./models/ClasifyandDetectIDCard/detectbb.weights",
                      "./models/ClasifyandDetectIDCard/detectbb.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
CONFIDENCE_THRESHOLD = 0.2
NMS_THRESHOLD = 0.4
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(255, 255), scale=1/255)
def detectBB(frame):
    classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    (h, w, d) = frame.shape
    crop_img=[]
    for (classid, score, box) in zip(classes, scores, boxes):
        if box[1]+box[3]<h-75:
            x3=box[1]+box[3]+75
        else:
            x3=h
        if box[1]>75:
            x1=box[1]-75
        else:
            x1=0
        if box[0]+box[2]<w-75:
            x2=box[0]+box[2]+75
        else:
            x2=w
        if box[0]>75:
            x0=box[0]-75
        else:
            x0=0
        crop_img.append([frame[x1:x3, x0:x2],classid])
    return crop_img
def detect_blur_fft(image, size=60, thresh=10, vis=False):
    canny = cv2.Canny(image, 50,250)
    mean=cv2.mean(canny)[0]
    return (mean, mean <= thresh)
