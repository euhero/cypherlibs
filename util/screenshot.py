from mss import mss

def GetScreenShot(outputname='screenshot.png'):
	with mss() as sct:
		sct.shot(mon=1,output=outputname)
