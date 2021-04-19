import win32console
import win32gui

def Hide():
	win = win32console.GetConsoleWindow()
	win32gui.ShowWindow(win, 0)