import math
import cv2
import numpy as np
import time
start_time = time.time()
def main():
    img = cv2.imread('test_img.bmp') 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 7, 255, cv2.THRESH_BINARY) 
    
    contours, hierarchy = cv2.findContours( 
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        cv2.drawContours(img, [contour], 0, (0, 0, 255), 1)

    cnt = contours[4] # 0 for blin.jpg

    """Рисуем окружность вокруг полученного контура"""
    
    (x_axis_raw,y_axis_raw), radius_raw = cv2.minEnclosingCircle(cnt)
    center = (int(x_axis_raw),int(y_axis_raw))

    """Определяем самое короткое расстояние от центра до контура, что будет точкой отсечения сегмента круга"""

    dist_to_contour = cv2.pointPolygonTest(cnt, center, measureDist=True)
    radius = int(radius_raw)

    """Считаем хорду сегмента (длина искомого среза) по формуле через диаметр (2 радиуса) и
    высоту сегмента H (разница между радиусом и расстоянием от центра до контура)"""

    H = radius - abs(dist_to_contour)
    value_for_alpha = 1 - (H/radius)
    alpha = math.acos(value_for_alpha)
    chord = 2*radius * math.sin(alpha)

    length_contour = cv2.arcLength(cnt,closed=True)
    percent = chord*100/length_contour

    # hull = cv2.convexHull(cnt,returnPoints = False)
    # defects = cv2.convexityDefects(cnt,hull)

    # for i in range(defects.shape[0]):
    #     s,e,f,d = defects[i,0]
    #     start = tuple(cnt[s][0])
    #     end = tuple(cnt[e][0])
    #     far = tuple(cnt[f][0])
    #     cv2.line(img,start,end,[0,255,0],2)
    #     cv2.circle(img,far,5,[0,0,255],-1)

    print("Длина среза:", round(chord, 2), "Процент длины среза от периметра:", round(percent, 2))

    cv2.circle(img,center, 1,(0,255,0),2)
    cv2.circle(img,center,radius,(0,255,0),2)

    cv2.imshow('Хорда сегмента', img)

    cv2.waitKey(0) 
    cv2.destroyAllWindows() 


if __name__ == "__main__":
    main()
    print(f"Время выполнения: {round((time.time() - start_time), 5)}")
