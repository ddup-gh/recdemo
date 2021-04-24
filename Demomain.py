import os
from util.picUtil import *
from util.addmultiTexture import RenderSquare
from util.removebg import rembg
from util.convertcor import convertcolour

PATH_URL = 'static/upload/'
BodyBg = PATH_URL+'_bodybg.png'
Texture = PATH_URL+'_texture.png'
Renderpath = PATH_URL+'ans_render.png'
Maskpath0 = PATH_URL+'mask_.png'
Maskpath = PATH_URL+'ans_render_mask.png'

class RunModel():
	def __init__(self,kw,kh,ks,bgpath,textpath):
		self.kw = kw
		self.kh = kh
		self.ks = ks
		self.bgpath = PATH_URL+bgpath
		self.textpath = PATH_URL+textpath

	def prepare(self):
		try:
			os.remove(BodyBg)
			os.remove(Texture)
			os.remove(Renderpath)
			os.remove(Maskpath)
			os.remove(Maskpath0)
		except:
			pass
		bgimg = resize_image(self.bgpath, 512)
		bgimg.save(BodyBg)
		textbg = create_image()
		textimg = resize_image(self.textpath, 80*self.ks)
		pos=(int(512*self.kw),int(512*self.kh))
		paste_image(textbg, textimg, Texture, pos)

	def render(self):
		rendersq = RenderSquare(BodyBg,Texture,Renderpath)
		rendersq.runrender()

	def getmask(self):
		rembg(Renderpath, Maskpath0)
		out = resize_image(Maskpath0,512)
		out.save(Maskpath0)
		convertcolour(Maskpath0, Maskpath)


	def pifuparm(self):
		NETG_PATH='./PIFu/checkpoints/net_G'
		NETC_PATH='./PIFu/checkpoints/net_C'
		TEST_PATH='./static/upload'
		# command
		os.system("python ./PIFU/apps/eval.py --test_folder_path %s --load_netG_checkpoint_path %s --load_netC_checkpoint_path %s" % (TEST_PATH,NETG_PATH,NETC_PATH))

	def main(self):
		self.prepare()
		self.render()
		self.getmask()
		self.pifuparm()

if __name__ == '__main__':
	modelobj = RunModel(0.43,0.2,1,'text.png','text1.png')
	# modelobj.main()
	modelobj.pifuparm()
