import lcd_config
import time
import numpy as np

LCD_1IN44 = 1
LCD_1IN8 = 0
if LCD_1IN44 == 1:
	LCD_WIDTH  = 128  #LCD width
	LCD_HEIGHT = 128 #LCD height
	LCD_X = 2
	LCD_Y = 1
if LCD_1IN8 == 1:
	LCD_WIDTH  = 160
	LCD_HEIGHT = 128
	LCD_X = 1
	LCD_Y = 2

LCD_X_MAXPIXEL = 132  #LCD width maximum memory 
LCD_Y_MAXPIXEL = 162  #LCD height maximum memory

#scanning method
L2R_U2D = 1
L2R_D2U = 2
R2L_U2D = 3
R2L_D2U = 4
U2D_L2R = 5
U2D_R2L = 6
D2U_L2R = 7
D2U_R2L = 8
SCAN_DIR_DFT = U2D_R2L


class LCD(lcd_config.RaspberryPi):

	width = LCD_WIDTH
	height = LCD_HEIGHT
	LCD_Scan_Dir = SCAN_DIR_DFT
	LCD_X_Adjust = LCD_X
	LCD_Y_Adjust = LCD_Y

	"""    Hardware reset     """
	def  LCD_Reset(self):
		self.digital_write(self.GPIO_RST_PIN,True)
		time.sleep(0.01)
		self.digital_write(self.GPIO_RST_PIN,False)
		time.sleep(0.01)
		self.digital_write(self.GPIO_RST_PIN,True)
		time.sleep(0.01)

	"""    Write register address and data     """
	def  LCD_WriteReg(self, Reg):
		self.digital_write(self.GPIO_DC_PIN, False)
		self.spi_writebyte([Reg])

	def LCD_WriteData_8bit(self, Data):
		self.digital_write(self.GPIO_DC_PIN, True)
		self.spi_writebyte([Data])

	def LCD_WriteData_NLen16Bit(self, Data, DataLen):
		self.digital_write(self.GPIO_DC_PIN, True)
		for i in range(0, DataLen):
			self.spi_writebyte([Data >> 8])
			self.spi_writebyte([Data & 0xff])
		
	"""    Common register initialization    """
	def LCD_InitReg(self):
		#ST7735R Frame Rate
		self.LCD_WriteReg(0xB1)
		self.LCD_WriteData_8bit(0x01)
		self.LCD_WriteData_8bit(0x2C)
		self.LCD_WriteData_8bit(0x2D)

		self.LCD_WriteReg(0xB2)
		self.LCD_WriteData_8bit(0x01)
		self.LCD_WriteData_8bit(0x2C)
		self.LCD_WriteData_8bit(0x2D)

		self.LCD_WriteReg(0xB3)
		self.LCD_WriteData_8bit(0x01)
		self.LCD_WriteData_8bit(0x2C)
		self.LCD_WriteData_8bit(0x2D)
		self.LCD_WriteData_8bit(0x01)
		self.LCD_WriteData_8bit(0x2C)
		self.LCD_WriteData_8bit(0x2D)
		
		#Column inversion 
		self.LCD_WriteReg(0xB4)
		self.LCD_WriteData_8bit(0x07)
		
		#ST7735R Power Sequence
		self.LCD_WriteReg(0xC0)
		self.LCD_WriteData_8bit(0xA2)
		self.LCD_WriteData_8bit(0x02)
		self.LCD_WriteData_8bit(0x84)
		self.LCD_WriteReg(0xC1)
		self.LCD_WriteData_8bit(0xC5)

		self.LCD_WriteReg(0xC2)
		self.LCD_WriteData_8bit(0x0A)
		self.LCD_WriteData_8bit(0x00)

		self.LCD_WriteReg(0xC3)
		self.LCD_WriteData_8bit(0x8A)
		self.LCD_WriteData_8bit(0x2A)
		self.LCD_WriteReg(0xC4)
		self.LCD_WriteData_8bit(0x8A)
		self.LCD_WriteData_8bit(0xEE)
		
		self.LCD_WriteReg(0xC5)#VCOM 
		self.LCD_WriteData_8bit(0x0E)
		
		#ST7735R Gamma Sequence
		self.LCD_WriteReg(0xe0)
		self.LCD_WriteData_8bit(0x0f)
		self.LCD_WriteData_8bit(0x1a)
		self.LCD_WriteData_8bit(0x0f)
		self.LCD_WriteData_8bit(0x18)
		self.LCD_WriteData_8bit(0x2f)
		self.LCD_WriteData_8bit(0x28)
		self.LCD_WriteData_8bit(0x20)
		self.LCD_WriteData_8bit(0x22)
		self.LCD_WriteData_8bit(0x1f)
		self.LCD_WriteData_8bit(0x1b)
		self.LCD_WriteData_8bit(0x23)
		self.LCD_WriteData_8bit(0x37)
		self.LCD_WriteData_8bit(0x00)
		self.LCD_WriteData_8bit(0x07)
		self.LCD_WriteData_8bit(0x02)
		self.LCD_WriteData_8bit(0x10)

		self.LCD_WriteReg(0xe1)
		self.LCD_WriteData_8bit(0x0f)
		self.LCD_WriteData_8bit(0x1b)
		self.LCD_WriteData_8bit(0x0f)
		self.LCD_WriteData_8bit(0x17)
		self.LCD_WriteData_8bit(0x33)
		self.LCD_WriteData_8bit(0x2c)
		self.LCD_WriteData_8bit(0x29)
		self.LCD_WriteData_8bit(0x2e)
		self.LCD_WriteData_8bit(0x30)
		self.LCD_WriteData_8bit(0x30)
		self.LCD_WriteData_8bit(0x39)
		self.LCD_WriteData_8bit(0x3f)
		self.LCD_WriteData_8bit(0x00)
		self.LCD_WriteData_8bit(0x07)
		self.LCD_WriteData_8bit(0x03)
		self.LCD_WriteData_8bit(0x10) 
		
		#Enable test command
		self.LCD_WriteReg(0xF0)
		self.LCD_WriteData_8bit(0x01)
		
		#Disable ram power save mode
		self.LCD_WriteReg(0xF6)
		self.LCD_WriteData_8bit(0x00)
		
		#65k mode
		self.LCD_WriteReg(0x3A)
		self.LCD_WriteData_8bit(0x05)

	#********************************************************************************
	#function:	Set the display scan and color transfer modes
	#parameter: 
	#		Scan_dir   :   Scan direction
	#		Colorchose :   RGB or GBR color format
	#********************************************************************************
	def LCD_SetGramScanWay(self, Scan_dir):
		#Get the screen scan direction
		self.LCD_Scan_Dir = Scan_dir
		
		#Get GRAM and LCD width and height
		if (Scan_dir == L2R_U2D) or (Scan_dir == L2R_D2U) or (Scan_dir == R2L_U2D) or (Scan_dir == R2L_D2U) :
			self.width	= LCD_HEIGHT 
			self.height 	= LCD_WIDTH 
			if Scan_dir == L2R_U2D:
				MemoryAccessReg_Data = 0X00 | 0x00
			elif Scan_dir == L2R_D2U:
				MemoryAccessReg_Data = 0X00 | 0x80
			elif Scan_dir == R2L_U2D:
				MemoryAccessReg_Data = 0x40 | 0x00
			else:		#R2L_D2U:
				MemoryAccessReg_Data = 0x40 | 0x80
		else:
			self.width	= LCD_WIDTH 
			self.height 	= LCD_HEIGHT 
			if Scan_dir == U2D_L2R:
				MemoryAccessReg_Data = 0X00 | 0x00 | 0x20
			elif Scan_dir == U2D_R2L:
				MemoryAccessReg_Data = 0X00 | 0x40 | 0x20
			elif Scan_dir == D2U_L2R:
				MemoryAccessReg_Data = 0x80 | 0x00 | 0x20
			else:		#R2L_D2U
				MemoryAccessReg_Data = 0x40 | 0x80 | 0x20
		
		#please set (MemoryAccessReg_Data & 0x10) != 1
		if (MemoryAccessReg_Data & 0x10) != 1:
			self.LCD_X_Adjust = LCD_Y
			self.LCD_Y_Adjust = LCD_X
		else:
			self.LCD_X_Adjust = LCD_X
			self.LCD_Y_Adjust = LCD_Y
		
		# Set the read / write scan direction of the frame memory
		self.LCD_WriteReg(0x36)		#MX, MY, RGB mode 
		if LCD_1IN44 == 1:
			self.LCD_WriteData_8bit( MemoryAccessReg_Data | 0x08)	#0x08 set RGB
		else:
			self.LCD_WriteData_8bit( MemoryAccessReg_Data & 0xf7)	#RGB color filter panel

	#/********************************************************************************
	#function:	
	#			initialization
	#********************************************************************************/
	def LCD_Init(self, Lcd_ScanDir):
		if (self.module_init() != 0):
			return -1
		
		#Turn on the backlight
		self.bl_DutyCycle(100)
		
		#Hardware reset
		self.LCD_Reset()
		
		#Set the initialization register
		self.LCD_InitReg()
		
		#Set the display scan and color transfer modes	
		self.LCD_SetGramScanWay(Lcd_ScanDir)
		self.delay_ms(200)
		
		#sleep out
		self.LCD_WriteReg(0x11)
		self.delay_ms(120)
		
		#Turn on the LCD display
		self.LCD_WriteReg(0x29)
		
	#/********************************************************************************
	#function:	Sets the start position and size of the display area
	#parameter: 
	#	Xstart 	:   X direction Start coordinates
	#	Ystart  :   Y direction Start coordinates
	#	Xend    :   X direction end coordinates
	#	Yend    :   Y direction end coordinates
	#********************************************************************************/
	def LCD_SetWindows(self, Xstart, Ystart, Xend, Yend):
		#set the X coordinates
		self.LCD_WriteReg(0x2A)
		self.LCD_WriteData_8bit(0x00)
		self.LCD_WriteData_8bit((Xstart & 0xff) + self.LCD_X_Adjust)
		self.LCD_WriteData_8bit(0x00)
		self.LCD_WriteData_8bit(((Xend - 1) & 0xff) + self.LCD_X_Adjust)

		#set the Y coordinates
		self.LCD_WriteReg (0x2B)
		self.LCD_WriteData_8bit(0x00)
		self.LCD_WriteData_8bit((Ystart & 0xff) + self.LCD_Y_Adjust)
		self.LCD_WriteData_8bit(0x00)
		self.LCD_WriteData_8bit(((Yend - 1) & 0xff )+ self.LCD_Y_Adjust)

		self.LCD_WriteReg(0x2C)

	def LCD_Clear(self):
		#hello
		_buffer = [0xff]*(self.width * self.height * 2)
		self.LCD_SetWindows(0, 0, self.width, self.height)
		self.digital_write(self.GPIO_DC_PIN, True)
		for i in range(0,len(_buffer),4096):
			self.spi_writebyte(_buffer[i:i+4096])

	def LCD_ShowImage(self,Image,Xstart,Ystart):
		if (Image == None):
			return
		imwidth, imheight = Image.size
		if imwidth != self.width or imheight != self.height:
			raise ValueError('Image must be same dimensions as display \
				({0}x{1}).' .format(self.width, self.height))
		img = np.asarray(Image)
		pix = np.zeros((self.width,self.height,2), dtype = np.uint8)
		pix[...,[0]] = np.add(np.bitwise_and(img[...,[0]],0xF8),np.right_shift(img[...,[1]],5))
		pix[...,[1]] = np.add(np.bitwise_and(np.left_shift(img[...,[1]],3),0xE0),np.right_shift(img[...,[2]],3))
		pix = pix.flatten().tolist()
		self.LCD_SetWindows(0, 0, self.width , self.height)
		self.digital_write(self.GPIO_DC_PIN, True)
		for i in range(0,len(pix),4096):
			self.spi_writebyte(pix[i:i+4096])
