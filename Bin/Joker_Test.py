#!/bin/python
# encoding: utf-8
'''
	Version  1.0
	Date	 2014/08/30
'''
import serial
import os
import Tkinter
import commands
import thread

import time
import tkMessageBox
import telnetlib



def mkdir():
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

def get_time():
	return str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

def get_jtag_id():
	jtag_id = commands.getoutput('lsusb')
	if 'JTAG' in jtag_id:
		Label_Jtag['text'] = 'JTAG '
		Label_Jtag['bg']='yellow'
		top.update()
		return str(commands.getoutput('lsusb')).split('JTAG ARM-USB-TINY-H  Serial: ')[1][0:7]
	else:
		Text_dataline.insert('end','Please check the connection of JTAG\n')
		Text_dataline.update()
		Text_dataline.see('end')
		
		Label_Jtag['text'] = 'No JTAG '
		Label_Jtag['bg']='red'
		top.update()
		return ' '
			



#=========================================Find serials and change the layout============================================
def find_usbserial():
	global usb_serialA,usb_serialB
	global done_flag
	done_flag = 0
	usb_serialA = ''
	usb_serialB = ''
	while True:
		usb_serials = commands.getoutput('ls /dev/tty.usbserial*')
		time.sleep(2)


		if 'No such file' in usb_serials and usb_serialA != '':
			usb_serialA = ''
			usb_serialB = ''
			Label_PORTA['text'] = 'PORTA'
			Label_PORTA_over = Tkinter.Label(top,width=200,height=3)
		    	Label_PORTA_over.pack()
		    	Label_PORTA_over.place(x=17,y=60)
			
			Label_PORTB['text'] = 'PORTB'
			Label_PORTA_over = Tkinter.Label(top,width=200,height=3)
		    	Label_PORTA_over.pack()
		    	Label_PORTA_over.place(x=17,y=170)

			Label_Jtag_over = Tkinter.Label(top,width=200,height=3)
		    	Label_Jtag_over.pack()
		    	Label_Jtag_over.place(x=17,y=280)
			
			Text_dataline.insert('end','=====================================================\n')
			Text_dataline.update()
			Text_dataline.see('end')
			f.write('\n')

			ISN.delete(0,14)
			done_flag = 0

		elif 'No such file' in usb_serials:
			if done_flag == 0:
				done_flag = save_barcode(done_flag)
			
		else:
			if done_flag == 0:
				done_flag = save_barcode(done_flag)
			usb_serialA_tmp = usb_serials.split('\n')[0]
			usb_serialB_tmp = usb_serials.split('\n')[1]
			if usb_serialA_tmp != usb_serialA:
				usb_serialA = usb_serialA_tmp

				Label_PORTA['text'] = 'PORTA: '+usb_serialA
				top.update()

				Text_dataline.insert('end',get_time()+':'+'Find PORTA:'+usb_serialA+'\n')
				Text_dataline.update()
				Text_dataline.see('end')

				button_PORTA = Button(top,'Start/开始','blue',serial_write_A)
    				button_PORTA.pack()
    				button_PORTA.place(x=17,y=60)

			if usb_serialB_tmp != usb_serialB:
				usb_serialB = usb_serialB_tmp

				Label_PORTB['text'] = 'PORTB: '+usb_serialB
				top.update()

				Text_dataline.insert('end',get_time()+':'+'Find PORTB:'+usb_serialB+'\n')
				Text_dataline.update()
				Text_dataline.see('end')


#====================================Send cmd===========================================================
def serial_write_A():
	global joker_port_A
	joker_port_A = serial.Serial(usb_serialA,115200)

#	time.sleep(0.5)
	joker_port_A.write('diag-kl15-passthru l**+\n')
	Text_dataline.insert('end',get_time()+':'+'Send command: diag-kl15-passthru l**+\n')
	Text_dataline.update()
	Text_dataline.see('end')

	time.sleep(1)
	joker_port_A.write('diag-kl15-passthru l**-\n')
	Text_dataline.insert('end',get_time()+':'+'Send command: diag-kl15-passthru l**-\n')
	Text_dataline.update()
	Text_dataline.see('end')

	time.sleep(0.8)
	joker_port_A.close()
	pass_fail(0)

def serial_write_B():
	global joker_port_B
	joker_port_B = serial.Serial(usb_serialB,115200)
	joker_port_B.write('topaz\n')
	time.sleep(0.5)

	joker_port_B.write('l**+\n')
	Text_dataline.insert('end',get_time()+':'+'Send command: l**+\n')
	Text_dataline.update()
	Text_dataline.see('end')
	time.sleep(0.5)

	joker_port_B.write('l**-\n')
	time.sleep(0.2)
	joker_port_B.write('r\n')
	Text_dataline.insert('end',get_time()+':'+'Send command: l**-\n')
	Text_dataline.update()
	Text_dataline.see('end')
	time.sleep(0.5)

	joker_port_B.close()
	pass_fail(1)

#=========================================Choose PASS or FAIL============================================
def pass_fail(port):
	if port == 0:
		button_PORTA = Button(top,'PASS','green',info_save_AP)
 	  	button_PORTA.pack()
    		button_PORTA.place(x=170,y=60)

		button_PORTA = Button(top,'FAIL','red',info_save_AF)
    		button_PORTA.pack()
    		button_PORTA.place(x=320,y=60)
	if port == 1:
		button_PORTB = Button(top,'PASS','green',info_save_BP)
    		button_PORTB.pack()
    		button_PORTB.place(x=170,y=170)

		button_PORTB = Button(top,'FAIL','red',info_save_BF)
    		button_PORTB.pack()
    		button_PORTB.place(x=320,y=170)

def info_save_AP():
#	print '0'
	f.write('PASS'+' ')
	Text_dataline.insert('end',get_time()+':'+usb_serialA+' PASS\n')
	Text_dataline.update()
	Text_dataline.see('end')
	
	Label_PORTA_over = Tkinter.Label(top,width=200,height=3)
    	Label_PORTA_over.pack()
    	Label_PORTA_over.place(x=17,y=60)

	button_PORTB = Button(top,'Start/开始','blue',serial_write_B)
    	button_PORTB.pack()
   	button_PORTB.place(x=17,y=170)
	joker_port_A.close()
	
def info_save_AF():
#	print '1'	
	f.write('FAIL'+' ')
	Text_dataline.insert('end',get_time()+':'+usb_serialA+' FAIL\n')
	Text_dataline.update()
	Text_dataline.see('end')

	Label_PORTA_over = Tkinter.Label(top,width=200,height=3)
    	Label_PORTA_over.pack()
    	Label_PORTA_over.place(x=17,y=60)

	button_PORTB = Button(top,'Start/开始','blue',serial_write_B)
    	button_PORTB.pack()
   	button_PORTB.place(x=17,y=170)
	joker_port_A.close()

def info_save_BP():
#	print '2'	
	f.write('PASS'+' ')
	Text_dataline.insert('end',get_time()+':'+usb_serialB+' PASS\n')
	Text_dataline.update()
	Text_dataline.see('end')

	Label_PORTA_over = Tkinter.Label(top,width=200,height=3)
    	Label_PORTA_over.pack()
    	Label_PORTA_over.place(x=17,y=170)
	joker_port_B.close()

	button_Jtag = Button(top,'Start/开始','blue',Jtag_test)
    	button_Jtag.pack()
   	button_Jtag.place(x=17,y=280)


def info_save_BF():
#	print '3'	
	f.write('FAIL'+' ')
	Text_dataline.insert('end',get_time()+':'+usb_serialB+' FAIL\n')
	Text_dataline.update()
	Text_dataline.see('end')

	Label_PORTA_over = Tkinter.Label(top,width=200,height=3)
    	Label_PORTA_over.pack()
    	Label_PORTA_over.place(x=17,y=170)
	joker_port_B.close()

	button_Jtag = Button(top,'Start/开始','blue',Jtag_test)
    	button_Jtag.pack()
   	button_Jtag.place(x=17,y=280)

def Jtag_test():
	global happy_flag,jtag
	jtag=get_jtag_id()+'?A'
	if jtag != ' ?A':
	
		os.system('export scriptsFolder=`dirname /Users/pe/Desktop/Joker8/Bin/Resources/openocd-t2.cfg`')
	
		thread.start_new_thread(Openocd,())
		time.sleep(3)
	
		telnet = telnetlib.Telnet('127.0.0.1',4460)
		time.sleep(2)
		telnet.write('shutdown\n')
		time.sleep(0.5)

		if 'k24.cpu tap/device found' in result:
			Text_dataline.insert('end',get_time()+': Jtag PASS\n')
			Text_dataline.update()
			Text_dataline.see('end')
			f.write('PASS'+'\n')
			Label_Jtag_over = Tkinter.Label(top,width=200,height=3)
			Label_Jtag_over.pack()
			Label_Jtag_over.place(x=17,y=280)

			Label_result = Tkinter.Label(top,text='PASS',font='Helvetica -12 bold',width=25,height=2,bg='green')
    			Label_result.pack()
    			Label_result.place(x=150,y=280)

		else:
			Text_dataline.insert('end',get_time()+': Jtag FAIL\n')
			Text_dataline.update()
			Text_dataline.see('end')
			f.write('FAIL'+'\n')

			Label_Jtag_over = Tkinter.Label(top,width=200,height=3)
			Label_Jtag_over.pack()
			Label_Jtag_over.place(x=17,y=280)
	
			Label_result = Tkinter.Label(top,text='FAIL',font='Helvetica -12 bold',width=25,height=2,bg='red')
    			Label_result.pack()
    			Label_result.place(x=150,y=280)
	else:
		pass


def Openocd():
	global result
	
	result = commands.getoutput('/Users/pe/Desktop/Joker8/Bin/Resources/launchopenocd.sh /var/tmp/joker8 /Users/pe/Desktop/Joker8/Bin/Resources/openocd-0.7.0 /Users/pe/Desktop/Joker8/Bin/Resources/openocd-t2.cfg 2 ft2232_serial\ '+jtag+' telnet_port\ 4460 tcl_port\ 6640 gdb_port\ 3340')

def Telnet():
	pass


#=============================================Layout=============================================

def save_barcode(done_flag):
	while True:
		if (len(ISN.get()) == 14) and (done_flag == 0):		
			f.write(str(ISN.get()[3:14])+' ')
			done_flag = 1
#			print str(ISN.get()[3:14])
			return done_flag
		

def Button(top,text_info,color,do_what):
    	return Tkinter.Button(top,text=text_info,bg=color,command=do_what,width=10,height=2)

def layout():
	
	global top,Label_PORTA,Label_PORTB,Text_dataline,f,ISN,path,Label_Jtag
	path="/Users/pe/Joker8/"

	mkdir()
	f = file(path+str(time.strftime('%Y-%m-%d',time.localtime(time.time())))+'.csv', "a")	
	f.close()
	f = file(path+str(time.strftime('%Y-%m-%d',time.localtime(time.time())))+'.csv', "r")
	if 'Barcode' not in f.readline():
		f.close()
		f = file(path+str(time.strftime('%Y-%m-%d',time.localtime(time.time())))+'.csv', "a")
		f.write('Barcode'+' '+'PORTA'+' '+'PORTB'+' '+'Jtag'+'\n')
	else:
		f.close()
		f = file(path+str(time.strftime('%Y-%m-%d',time.localtime(time.time())))+'.csv', "a")
		f.write(get_time()+'\n')
	top = Tkinter.Tk()
    	top.title('Joker8 Test')
    	top.geometry('460x800+0+0')

   	Label_PORTA = Tkinter.Label(top,text='PORTA',font='Helvetica -12 bold',width=70,height=2,bg='yellow')
    	Label_PORTA.pack()
    	Label_PORTA.place(x=13,y=20)

    	Label_PORTB = Tkinter.Label(top,text='PORTB',font='Helvetica -12 bold',width=70,height=2,bg='yellow')
    	Label_PORTB.pack()
    	Label_PORTB.place(x=13,y=130)

    	Label_Jtag = Tkinter.Label(top,text='JTAG',font='Helvetica -12 bold',width=70,height=2,bg='yellow')
    	Label_Jtag.pack()
    	Label_Jtag.place(x=13,y=240)
    
    	Label_dataline = Tkinter.Label(top,text='LOG:',font='Helvetica -12 bold',width=70,height=2,bg='yellow')
    	Label_dataline.pack()
    	Label_dataline.place(x=13,y=430)

	Label_ISN = Tkinter.Label(top,text='ISN:',font='Helvetica -12 bold',width=70,height=2,bg='yellow')
	Label_ISN.pack()
	Label_ISN.place(x=13,y=350)

	e_ISN = Tkinter.StringVar()
	ISN = Tkinter.Entry(top,textvariable = e_ISN,width=44)
	e_ISN.set('')
	ISN.pack()
	ISN.place(x=43,y=390)

    	Text_dataline = Tkinter.Text(top,width=63,height=22)
    	Text_dataline.pack()
    	Text_dataline.place(x=5,y=460)
    	Text_dataline.bind("<KeyPress>", lambda e : "break")
	
	thread.start_new_thread(find_usbserial,())
    	top.mainloop()
#================================================================================================

if __name__=='__main__':
	layout()
