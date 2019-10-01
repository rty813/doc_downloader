import os
import string
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait
import sys
from tqdm import trange


def file_name(file_dir, suffix=".jpg"):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == suffix:
                L.append(os.path.join(root, file))
    L = sorted(L, key=lambda x: int(x.split('\\')[-1].split('/')[-1][:-4]))
    return L


def conpdf(f_pdf, filedir, suffix=".jpg", scale=False):
    fileList = file_name(filedir, suffix)
    img = Image.open(fileList[0])
    if scale and img.size[0] < img.size[1]:
        # (w, h) = (940, 529)
        (w, h) = (848, 1168)
    else:
        (w, h) = img.size

    c = canvas.Canvas(f_pdf, pagesize=(w, h))

    for i in trange(len(fileList)):
        f = fileList[i]
        (xsize, ysize) = Image.open(f).size

        ratx = xsize / w
        raty = ysize / h
        ratxy = xsize / (1.0 * ysize)
        if ratx > 1:
            ratx = 0.99
        if raty > 1:
            raty = 0.99
        rat = ratx
        if ratx < raty:
            rat = raty
        widthx = w * rat
        widthy = h * rat
        widthx = widthy * ratxy
        posx = (w - widthx) / 2
        if posx < 0:
            posx = 0

        posy = (h - widthy) / 2
        if posy < 0:
            posy = 0

        c.drawImage(f, posx, posy, widthx, widthy)
        c.showPage()
    c.save()
    print("转码完毕")


if __name__ == "__main__":
    conpdf('output.pdf', 'temp', '.png')
