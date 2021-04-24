from PIL import Image

def convertcolour(source_path,ans_path):
    img = Image.open(source_path)#读取系统的内照片
    width = img.size[0]#长度
    height = img.size[1]#宽度
    for i in range(0,width):
        for j in range(0,height):
            data = (img.getpixel((i,j)))
            if (data[0]==0 and data[1]==0 and data[2]==0)==False:
                img.putpixel((i,j),(255,255,255,255))

    img = img.convert("RGB")
    img.save(ans_path)
