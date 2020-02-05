from reportlab.pdfgen import canvas
from reportlab.platypus import Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
import PIL.Image
import PIL.ExifTags
import os
import re
import time


class ImgToPdf():
    def img_search(self, mypath, filenames):
        for lists in os.listdir(mypath):
            path = os.path.join(mypath, lists)
            if os.path.isfile(path):
                expression = r'[\w]+\.(jpg|png|jpeg)$'
                if re.search(expression, path, re.IGNORECASE):
                    filenames.append(path)
            elif os.path.isdir(path):
                self.img_search(path, filenames)

    def img_search1(self, mypath, filenames):
        for lists in os.listdir(mypath):
            path = os.path.join(mypath, lists)
            if os.path.isfile(path):
                a = path.split('.')
                if a[-1] in ['jpg', 'png', 'JPEG']:
                    filenames.append(path)
            elif os.path.isdir(path):
                self.img_search1(path, filenames)

    def rotate_img_to_proper(self, image):
        global orientation
        try:
            # image = Image.open(filename)
            if hasattr(image, '_getexif'):  # only present in JPEGs
                for orientation in PIL.ExifTags.TAGS.keys():
                    if PIL.ExifTags.TAGS[orientation] == 'Orientation':
                        break
                e = image._getexif()  # returns None if no EXIF data
                if e is not None:
                    #log.info('EXIF data found: %r', e)
                    exif = dict(e.items())
                    orientation = exif[orientation]
                    # print('found, ',orientation)

                    if orientation == 3:
                        image = image.transpose(Image.ROTATE_180)
                    elif orientation == 6:
                        image = image.transpose(Image.ROTATE_270)
                    elif orientation == 8:
                        image = image.rotate(90, expand=True)
        except:
            pass
        return image

    def pmain(self, src_folder, title):
        output_file_name = '文件库//'+str(title)+'.pdf'

        imgDoc = canvas.Canvas(output_file_name)
        # 修改PDF文件方向：-默认纵向，改direction为其他则是横向
        direction = '|'
        if direction == '-':
            imgDoc.setPageSize(landscape(A4))
            document_width, document_height = landscape(A4)
        else:
            imgDoc.setPageSize(A4)
            document_width, document_height = A4
        if src_folder is None:
            mypath = input('Input the image folder please:')
        else:
            mypath = src_folder
        filenames = []
        start = time.clock()
        self.img_search(mypath, filenames)
        end = time.clock()
        print('find file cost time: ', end-start,
              'find files: ', len(filenames))

        for image in filenames:
            try:
                image_file = PIL.Image.open(image)
                image_file = self.rotate_img_to_proper(image_file)

                image_width, image_height = image_file.size
                # print('img size:', image_file.size)
                if not(image_width > 0 and image_height > 0):
                    raise Exception
                image_aspect = image_height/float(image_width)
                # Determins the demensions of the image in the overview
                print_width = document_width
                print_height = document_width*image_aspect
                imgDoc.drawImage(ImageReader(image_file), document_width-print_width,
                                 document_height-print_height, width=print_width,
                                 height=print_height, preserveAspectRatio=True)
                # inform the reportlab we want a new page
                imgDoc.showPage()
            except Exception as e:
                print('error:', e, image)
        imgDoc.save()
        print('Done')


if __name__ == '__main__':
    pass
