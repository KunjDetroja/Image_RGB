from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import UrineStripForm
from .models import UrineStrip
import cv2
import numpy as np

def upload_image(request):
    if request.method == 'POST':
        form = UrineStripForm(request.POST, request.FILES)
        if form.is_valid():
            urine_strip = form.save()
            colors = analyze_image(urine_strip.image.path)
            return JsonResponse({'colors': colors})
    else:
        form = UrineStripForm()
    return render(request, 'upload.html', {'form': form})

def analyze_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    color_list = []
    colors = {'URO': [206, 193, 187],'BIL': [202, 185, 164],'KET': [193, 171, 153],'BLD': [204, 159, 54],'PRO': [191, 172, 130],'NIT': [203, 189, 170],'LEU': [194, 175, 164],'GLU': [128, 173, 163],'SG': [191, 159, 76],'PH': [206, 152, 106]}
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if 0.9 < w/h < 1.1:
            rects.append((x, y, w, h))
    rects = sorted(rects, key=lambda x: x[1])
    coordinate = []
    for i, (x, y, w, h) in enumerate(rects[:10]):
        code = {}
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        code["x1"] = x
        code["y1"] = y
        code["x2"] = x+w
        code["y2"] = y+h
        coordinate.append(code)
    for i in coordinate:
        x1 = i["x1"]
        y1 = i["y1"]
        x2 = i["x2"]
        y2 = i["y2"]
        roi = image[y1:y2, x1:x2]
        average_color_per_row = np.average(roi, axis=0)
        average_color = np.average(average_color_per_row, axis=0)
        average_color = average_color[::-1]
        for i in range(3):
            average_color[i] = int(average_color[i])
        color_list.append(average_color)
    for i, key in enumerate(colors.keys()):
        colors[key] = color_list[i].tolist()
        
    return colors


    # return average_color
