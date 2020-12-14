'''This program is a Linux based voice assistant that currently allows users to change 
   workspaces (If GNOME-Tweaks is installed) and type using their voice.
   It also allows for voice commanded downloading of youtube videos in the active window.
'''

import speech_recognition as sr
import subprocess
import time
from word2number import w2n

# Main command keywords
changeWorkspaceCom = "go"
typeCom = "type"
downloadCom = "download"
mouseClickCom = "click"
browserCom = "browser"
browserPageCom = "page"

# Enables and disables the use of a wake word! 
wakeWordBool = True 
wakeWord = "computer"
terminateWord = "terminate"

def main():
	mic = sr.Recognizer()
	# Microphone calibration duration in seconds.
	calibrationDuration = 5 
	commandWord = ""
	
	with sr.Microphone() as source:
		print("Please wait. Calibrating microphone...") 
		# Listens for calibrationDuration seconds to determine the ambient noise energy level, this helps reduce future parsing errors.   	
		mic.adjust_for_ambient_noise(source, calibrationDuration) 

	while True:
		with sr.Microphone() as source:
			print("Speak!")
			# Value that represents which of the separate words spoken is currently being parsed.
			wordNumber = 0 

			try:
				audio = mic.listen(source)
				# Converting the audio waveform to a string and using that for comparisons instead saves a huge amount of redundant processing.
				audioStr = mic.recognize_sphinx(audio) 

				print("The program thinks you said '" + audioStr + "'") 
				commandList = audioStr.split(' ') 

				if(wakeWordBool == True):
					# Checking of the first word spoken is the wake word.
					if(commandList[0] == wakeWord): 
						wordNumber = 1
						if(len(commandList) < 2):
							print("Insufficient parameters!")
							continue
					else:
						# Goes back to listening if the user does not say the wake word first. (When enabled)
						continue   

			# Terminates the assistant program.
				if(commandList[wordNumber] == terminateWord): 
					break
					
				elif(commandList[wordNumber] == downloadCom):
					SubprocessKeyCall("F6") # Highlights URL to copy for later in all browsers tested.
					time.sleep(1)
					SubprocessKeyCall("Ctrl+c") # Copies active URL data
					subprocess.call(['python3', 'YoutubeDownloader.py']) # Doing a subprocess call because this program requires python2 and the other code segments require python3.
					

			# Navigates between workspaces
				elif(commandList[wordNumber] == changeWorkspaceCom): 
					wordNumber += 1
					if(commandList[wordNumber] == "up"):
						SubprocessKeyCall("super+Page_Up") 
					elif(commandList[wordNumber] == "down"):
						SubprocessKeyCall("super+Page_Down")
					elif(commandList[wordNumber] == "first"):
						SubprocessKeyCall("super+Home")
					elif(commandList[wordNumber] == "last"):
						SubprocessKeyCall("super+end")

			# Typing function  Note: Types only in the active window!
				elif(commandList[wordNumber] == typeCom):
					if(commandList[0] == wakeWord and wakeWordBool == True):
						# Removes the wake word from the statement we want to type.
						del commandList[0] 
					# Removes the "type" command word from the statement we want to type.
					del commandList[0] 
					subprocess.call(["xdotool", "type", "--delay", "40", " ".join(commandList)]) 

				# Sends a single left mouse click
				elif(commandList[wordNumber] == mouseClickCom):
					subprocess.call(["xdotool", "click", "1"])

				elif(commandList[wordNumber] == "copy"):
					SubprocessKeyCall("Ctrl+c")

				elif(commandList[wordNumber] == "paste"):
					SubprocessKeyCall("Ctrl+v")

				# Permits moving forward and backward between visited browser pages. (Window must be active!)
				elif(commandList[wordNumber] == browserCom):
					browser_tab_commands(commandList, wordNumber)

				# Macros many useful browser manipulation hotkeys
				elif(commandList[wordNumber] == browserPageCom):
					browser_page_commands(commandList, wordNumber)				

			except sr.UnknownValueError: 
				print("Could not understand audio")  
			except sr.RequestError as e:  
				print("Sphinx error; {0}".format(e)) 

# Subprocess calling class to help reduce code clutter.
def SubprocessKeyCall(commandKeys):
	subprocess.call(["xdotool", "key", commandKeys])
 
# Controls browser pages.
def browser_page_commands(commandList, wordNumber):
	wordNumber += 1
	if(commandList[wordNumber] == "previous"):
		SubprocessKeyCall("Alt+Left")
	elif(commandList[wordNumber] == "next"):
		SubprocessKeyCall("Alt+Right")

# Manages browser tabs, can open, close, reopen, refresh, and shift through open tabs.
def browser_tab_commands(commandList, wordNumber):
	wordNumber += 1
	if(commandList[wordNumber] == "new"):
		SubprocessKeyCall("Ctrl+t")
	elif(commandList[wordNumber] == "close"):
		SubprocessKeyCall("Ctrl+w")
	elif(commandList[wordNumber] == "recall"):
		SubprocessKeyCall("Ctrl+Shift+t")
	elif(commandList[wordNumber] == "next"):
		SubprocessKeyCall("Ctrl+Tab")
	elif(commandList[wordNumber] == "previous"):
		SubprocessKeyCall("Ctrl+Shift+Tab")
	elif(commandList[wordNumber] == "refresh"):
		SubprocessKeyCall("F5")

main()