from PIL import Image
import numpy as np
import os

def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    return size / 1024

def get_outfile(infile, outfile):
    if outfile:
        return outfile
    dir, suffix = os.path.splitext(infile)
    outfile = '{}-out{}'.format(dir, suffix)
    return outfile

def compress_image(infile, outfile='t3.jpg', mb=20, step=10, quality=80):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    o_size = get_size(infile)
    print(o_size)
    if o_size <= mb:
        return infile
    outfile = get_outfile(infile, outfile)
    while o_size > mb:
        im = Image.open(infile)
        im.save(outfile, quality=quality)
        if quality - step < 0:
            break
        quality -= step
        o_size = get_size(outfile)
        print(o_size)
    return outfile, get_size(outfile)

def resize_image(infile, pic_size=20):
    """修改图片尺寸
    :param infile: 图片源文件
    :param outfile: 重设尺寸文件保存地址
    :param x_s: 设置的宽度
    :return:
    """
    im = Image.open(infile)
    #y_s = int(y * x_s / x)
    x_s=y_s=int(pic_size)
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    return out

def create_image():
    img = np.zeros([512,512,4],np.uint8)
    img[:,:,0:3]+=255
    img[:,:,3]+=255
    # 改变不透明度
    imgdata = Image.fromarray(img)
    # img0.save('t4.png')
    # markImg = Image.new('RGBA',(120,120),'white')
    return imgdata

def paste_image(bgimg,textimg,outfile,pos=(220,80)):
    bgimg.paste(textimg,pos)
    bgimg.save(outfile)

testdata=20
if __name__ == '__main__':
    # compress_image(r'lena.png')
    textimg = resize_image('texture.png',80)
    bgimg = create_image()
    paste_image(bgimg, textimg,'ans.png')
