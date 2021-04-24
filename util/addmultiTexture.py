# addmultiTexture.py

from util.myGL_Funcs import *
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr
from PIL import Image

vertex_src = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_color;
layout(location = 2) in vec2 a_texture;

uniform mat4 rotation;

out vec3 v_color;
out vec2 v_texture;

void main()
{
    gl_Position = rotation * vec4(a_position, 1.0);
    v_color = a_color;
    v_texture = a_texture;
    
    //v_texture = 1 - a_texture;                      // Flips the texture vertically and horizontally
    //v_texture = vec2(a_texture.s, 1 - a_texture.t); // Flips the texture vertically
}
"""

fragment_src = """
# version 330

in vec3 v_color;
in vec2 v_texture;
uniform sampler2D tex1;
uniform sampler2D tex2;
uniform float mixValue;

out vec4 out_color;

void main()
{
	vec4 color1 = texture(tex1, vec2(v_texture.s, 1.0 - v_texture.t));
	vec4 color2 = texture(tex2, vec2(v_texture.s, 1.0 - v_texture.t));
    out_color = mix(color1, color2, mixValue);
}
"""
vertices = [-0.5, -0.5,  0,  1.0, 0.0, 0.0,  0.0, 0.0,
             0.5, -0.5,  0,  0.0, 1.0, 0.0,  1.0, 0.0,
             0.5,  0.5,  0,  0.0, 0.0, 1.0,  1.0, 1.0,
            -0.5,  0.5,  0,  1.0, 1.0, 1.0,  0.0, 1.0]

indices = [0,  1,  2,  2,  3,  0]

class RenderSquare:
	def __init__(self,bodybg_path,texture_path,ans_path="ans_render.png"):
		self.mixValue = 0.3
		if not glfw.init():
			raise Exception("glfw can not be initialized!")
		
		# creating the window
		self.window = glfw.create_window(1024, 1024, "OpenGL Window", None, None)
		if not self.window:
			glfw.terminate()
			raise Exception("glfw window can not be created!")
		# set window's position
		glfw.set_window_pos(self.window, 100, 100)
		
		# set the callback function for window resize
		glfw.set_window_size_callback(self.window, self.window_resize)
		# Install a key handler
		glfw.set_key_callback(self.window, self.on_key)
		
		# make the context current
		glfw.make_context_current(self.window)

		self.shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
		glUseProgram(self.shader)
		self.vertices = np.array(vertices, dtype=np.float32)
		self.indices = np.array(indices, dtype=np.uint32)
		# Step2: 创建并绑定VBO 对象 传送数据
		VBO = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, VBO)
		glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
		# Step3: 创建并绑定EBO 对象 传送数据
		EBO = glGenBuffers(1)
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
		glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)
		# Step4: 指定解析方式  并启用顶点属性
		# 顶点位置属性 
		glEnableVertexAttribArray(0)
		glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.vertices.itemsize * 8, ctypes.c_void_p(0))
		# 顶点颜色属性
		glEnableVertexAttribArray(1)
		glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, self.vertices.itemsize * 8, ctypes.c_void_p(12))
		# 顶点纹理属性
		glEnableVertexAttribArray(2)
		glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, self.vertices.itemsize * 8, ctypes.c_void_p(24))
		
		texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, texture)
		self.texid1 = loadTexture(bodybg_path)
		self.texid2 = loadTexture(texture_path)
		self.path = ans_path

	def on_key(self, window, key, scancode, action, mods):
		# 键盘控制, A -混合系数减; S -混合系数增
		if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
			glfw.set_window_should_close(self.window,1)
		elif key ==  glfw.KEY_S and action == glfw.PRESS:
			self.mixValue += 0.05
			print(self.mixValue)
			if (self.mixValue >1.0):
				self.mixValue =1.0
		elif key ==  glfw.KEY_A and action == glfw.PRESS:
			self.mixValue -= 0.05
			if (self.mixValue <0.0):
				self.mixValue =0.0

	# glfw callback functions
	def window_resize(self,window, width, height):
		glViewport(0, 0, width, height)
	
	def save_pict(self):
		viewP = glGetIntegerv(GL_VIEWPORT)
		width=height=int(viewP[2]/2)
		btdata = glReadPixels(256,256,width,height,GL_RGBA,GL_UNSIGNED_BYTE)
		imgdata = []
		for bt in btdata:
			imgdata.append(bt)
		imgdata = np.array(imgdata)
		imgdata = imgdata.reshape(width,height,4)
		imgdata = np.uint8(imgdata)
		# imgdata = np.frombuffer(imgdata)
		img = np.zeros([width,height,4], np.uint8)
		for ind in range(height):
			img[ind,:,:] = imgdata[height-ind-1,:,:]
		img = Image.fromarray(img)
		img.save(self.path)

	def runrender(self):
		# initializing glfw library
		# glClearColor(0, 0.1, 0.1, 1)
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		model = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, 0]))
		
		rotation_loc = glGetUniformLocation(self.shader, "rotation")
		if not glfw.window_should_close(self.window):
			glfw.poll_events()
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
			glClearColor(0, 0, 0, 1)
			#// 启用多个纹理单元 绑定纹理对象
			glActiveTexture(GL_TEXTURE0)
			glBindTexture(GL_TEXTURE_2D, self.texid1)
			glDrawArrays(GL_TRIANGLES, 0, 3)
			glUniform1i(glGetUniformLocation(self.shader, "tex1"), 0) #// 设置纹理单元为0号
			glActiveTexture(GL_TEXTURE1)

			glBindTexture(GL_TEXTURE_2D, 0)
			glBindTexture(GL_TEXTURE_2D, self.texid2)
			glUniform1i(glGetUniformLocation(self.shader, "tex2"), 1) #// 设置纹理单元为1号

			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)

			glUniform1f(glGetUniformLocation(self.shader, "mixValue"), self.mixValue) #// 设置纹理混合参数
			# 绘制第一个矩形
			glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, model)
			glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
			self.save_pict()
			glfw.swap_buffers(self.window)
		glfw.terminate()

if __name__ == '__main__':
	import os
	try:
		os.remove('ans_render.png')
	except:
		pass
	rendersq = RenderSquare('text.png','ans.png')
	rendersq.runrender()


