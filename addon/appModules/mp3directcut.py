# -*- coding: utf-8 -*-

#mp3directcut.py

import addonHandler
addonHandler.initTranslation()
import appModuleHandler
import globalCommands
import scriptHandler
from oleacc import AccessibleObjectFromWindow, ROLE_SYSTEM_SCROLLBAR
from controlTypes import ROLE_MENUITEM, ROLE_PANE, ROLE_EDITABLETEXT
from datetime import datetime
import time
import os
import api
import gui
import wx
import textInfos
from win32con import GW_HWNDNEXT, GW_CHILD, GW_HWNDPREV
from scriptHandler import getLastScriptRepeatCount
from winUser import getWindow, getForegroundWindow, getControlID, setFocus, mouse_event, MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
from ui import message
import speech

hr, min, sec, hun, th = _('hours'), _('minutes'), _('seconds'), _('hundredths'), _('thousandths')
programName = 'mp3DirectCut'

_addonDir = os.path.join(os.path.dirname(__file__), '..').decode('mbcs')
_curAddon = addonHandler.Addon(_addonDir)
_addonSummary = _curAddon.manifest['summary']

themessages = (
# Translators: Message to inform that no selection has been realized.
	_('No selection'),
	# Translators: Message to inform the user that the playback cursor is at the top of the file.
	_('Beginning of the file.'),
	# Translators: Message to inform the user that the playback cursor is at the end of the file.
	_('End of the file.'),
	# Translators: Message to inform the user that not file is loaded.
	_('Not file is loaded. Please check that you are in a file, open one with Control O, or R to start recording.'),
	# Translators: Message to inform the user that the current command is not available in a recording mode.
	_('This command is not available in a recording mode, it is available only in a reading mode !'),
	# Translators: Message to inform the user that he must close the menu to use this command.
	_('Please close the opened menu to use this command.'),
	# Translators: Message to indicate the position of the selection start marker.
	_('The marker of the beginning of selection B is at'),
	# Translators: Message to indicate the position of the selection end marker.
	_('The marker of the End of selection N is at'),
	# Translators: Message to indicate the level of the vu-meter.
	_('The level of the vu-meter is at'),
	# Translators: Message to indicate the total duration of the current file.
	_('Total time: '),
	# Translators: Message to indicate the duration of the selection.
	_('Duration of selection'),
	# Translators: Message to indicate the actual part.
	_('Actual part'),
	# Translators: Message to inform that no selection was found.
	_('Selection not found.'),
	# Translators: Message to indicate that the information of the current part is not available.
	_('Information specific to the actual part is not available.'),
	# Translators: Message to prompt the user to verify that no selection has been made.
	_('Please check that no selection has been made.'),
	# Translators: Message to prompt the user to verify that it is not in recording mode.
	_('Please chek that you are not in a recording mode.')
)

def timeSplitter(sTime):
	hours = minutes = seconds = hundredths = thousandths = ''
	if ':' in sTime:
		hrs = sTime.split(':')
		if hrs[0] != '00' and hrs[0] != '0':
			hours = '%s %s, ' % (hrs[0], hr)
		if hrs[1].split("'")[0] != '00':
			minutes = hrs[1].split("'")[0]
	else:
		mnts = sTime.split("'")
		if mnts[0] != '00' and mnts[0] != '0':
			minutes = mnts[0]
	if minutes:
		if len(minutes) > 1:
			if minutes[0] == '0':
				minutes = minutes[1]
		minutes = '%s %s, ' % (minutes, min)
	scnds = sTime.split("'")[1].split('.')[0]
	if scnds != '00' and scnds != '0':
		seconds = scnds
	if seconds:
		if len(seconds) > 1:
			if seconds[0] == '0':
				seconds = seconds[1]
		seconds = '%s %s, ' % (seconds, sec)
	hd=sTime.split('.')[1].split()[0]
	if hd != '00' and hd != '000':
		if len(hd) == 3:
			thousandths = '%s %s.' % (hd, th)
		else:
			hundredths = '%s %s.' % (hd, hun)
	timeSplitter = hours + minutes + seconds + hundredths if not thousandths else hours + minutes + seconds + thousandths
	return timeSplitter

def stateOfRecording():
	if partOrSelection() <3:
		return 3
	if partOrSelection() == 5:
		return 1
	if partOrSelection() == 3:
		return 2
	if partOrSelection() == 6:
		return 7
	if partOrSelection() == 8:
		return 8
	return 4

def sayMessage(msg, space = None, marker = None):
	import config
	if space:
		if config.conf['mp3DCReport']['space']:
			message (msg)
	elif marker:
		if config.conf['mp3DCReport']['marker']:
			message (msg)
	else:
		if config.conf['mp3DCReport']['other']:
			message(msg)

def isRead():
	sActual= actualDuration()
	time.sleep(0.2)
	if actualDuration() != sActual:
		return True
	return False

def isMenu():
	role = api.getFocusObject().role
	if role == ROLE_MENUITEM:
		return True
	return False

def readOrRecord():
	hWnd = getWindow(getWindow(getForegroundWindow(), GW_CHILD), GW_CHILD)
	return hWnd

def isStarting():
	hWnd = readOrRecord()
	if not hWnd: return False
	o = AccessibleObjectFromWindow(hWnd, -4)
	sStarting = o.accValue(0)
	if sStarting == ' ':
		return True
	return False

def vuMeterHandle():
	focus = api.getFocusObject()
	if focus.appModule.productVersion in ['2.2.1.0', '2.2.2.0']:
		try:
			hWnd = focus.firstChild.firstChild.firstChild.next.next.next.next.next.windowHandle
		except:
			hWnd = None
		return hWnd
	try:
		hWnd = getWindow(getWindow(getForegroundWindow(), GW_CHILD), GW_CHILD)
	except:
		return None
	for i in range(9):
		hWnd = getWindow(hWnd, GW_HWNDNEXT)
	return hWnd

def isRecording():
	hWnd = vuMeterHandle()
	if not hWnd: return False
	o = AccessibleObjectFromWindow(hWnd, -4)
	sLevel = o.accValue(0)
	if sLevel != '' and partOrSelection() > 2:
		return True
	return False

def partOrSelection():
	hWnd = readOrRecord()
	if hWnd:
		hWnd = getWindow(hWnd, GW_HWNDNEXT)
		if hWnd and getControlID(hWnd) == 160:
			o = AccessibleObjectFromWindow(hWnd, -4)
			text = o.accValue(0)
			if not text.isspace() and not text == None:
				text = text.split('   ')
				text=text[-1].split()
				word=text[0]
				if ':' in word:
					return 2
				else:
					if text[1][:1] == '(':
						return 1
					if text[1][:1] == "'":
						return 3
					return 4
			hWnd = getWindow(hWnd, GW_HWNDPREV)
			if hWnd:
				o = AccessibleObjectFromWindow(hWnd, -4)
				text = o.accValue(0)
				if text != '' and not text.isspace():
					return 5
				return 6
		return 7
	return 8

def part(flag=None):
	if partOrSelection() == 1:
		hWnd = getWindow(readOrRecord(), GW_HWNDNEXT)
		o = AccessibleObjectFromWindow(hWnd, -4)
		text = o.accValue(0)
		text = text.split('(')
		text = text[1]
		text = text.split(')')
		text = text[0]
		text = text.replace('/', ' %s ' % _('of'))
		return '%s %s' % (themessages[11], text) if not flag else '%s %s' % (_('Part'), text)

def selectionDuration():
	if partOrSelection() == 2:
		hWnd = getWindow(readOrRecord(), GW_HWNDNEXT)
		o = AccessibleObjectFromWindow(hWnd, -4)
		text = o.accValue(0)
		selectionDuration = text.split('(')
		selectionDuration = selectionDuration[1]
		selectionDuration = selectionDuration[:-1]
		return timeSplitter(selectionDuration)

def beginSelection():
	if partOrSelection() == 2:
		hWnd = getWindow(readOrRecord(), GW_HWNDNEXT)
		o = AccessibleObjectFromWindow(hWnd, -4)
		text = o.accValue(0)
		beginSelection = text.split(' - ')
		beginSelection = beginSelection[0]
		beginSelection = beginSelection.split()[1]
		return timeSplitter(beginSelection)

def endSelection():
	if partOrSelection() == 2:
		hWnd = getWindow(readOrRecord(), GW_HWNDNEXT)
		o = AccessibleObjectFromWindow(hWnd, -4)
		text = o.accValue(0)
		endSelection = text.split(' - ')
		endSelection = endSelection[1]
		endSelection = endSelection.split(' ')
		endSelection = endSelection[0]
		return timeSplitter(endSelection)

def actualDuration():
	hWnd = readOrRecord()
	if not hWnd: return 2
	o = AccessibleObjectFromWindow(hWnd, -4)
	sActual = o.accValue(0)
	if sActual and not sActual.isspace() and '   ' in sActual:
		sActual = sActual.split(': ')
		sActual = sActual[2].split()
		sActual=sActual[0]
		sActual = timeSplitter(sActual)
	else:
		sActual = 1
	return sActual

def actualDurationPercentage():
	hWnd = readOrRecord()
	o = AccessibleObjectFromWindow(hWnd, -4)
	sActual = o.accValue(0)
	if sActual.index('('):
		sActual = sActual.split('(')
		sActual = sActual[1]
		sActual = sActual[:-1]
	return sActual

def totalTime():
	if stateOfRecording() == 3:
		hWnd = readOrRecord()
		o = AccessibleObjectFromWindow(hWnd, -4)
		sTime = o.accValue(0)
		sTime = sTime.split(': ')
		sTime = sTime[1]
		sTotal = timeSplitter(sTime)
		return sTotal

def timeRemaining():
	hWnd = readOrRecord()
	o = AccessibleObjectFromWindow(hWnd, -4)
	sActual = o.accValue(0)
	if sActual != '' and not sActual.isspace() and '   ' in sActual:
		sActual = sActual.split(': ')
		sActual = sActual[2].split()
		sActual=sActual[0]
	else:
		sActual = 1
	sTotal = o.accValue(0)
	sTotal = sTotal.split(': ')
	sTotal = sTotal[1]
	sTotal = sTotal.split('   ')[0]
	if sTotal == sActual:
		return _('No time remaining !')
	hORm = len(sTotal.split('.')[1])
	fmt = "%H:%M'%S.%f"
	if not ':' in sActual:
		sActual = '0:%s' % sActual
	if not ':' in sTotal:
		sTotal = '0:%s' % sTotal
	result = datetime.strptime(sTotal, fmt) - datetime.strptime(sActual, fmt)
	result = str(result).decode('utf-8')
	result = result.replace(':', "'")
	result = result.replace("'", ':', 1)
	result = result[:-4] if hORm == 2 else result[:-3]
	return timeSplitter(result)

class AppModule(appModuleHandler.AppModule):
	scriptCategory = _addonSummary

	def script_checkRecording(self, gesture):
		gesture.send()
		if api.getFocusObject().role != ROLE_PANE:
			return 
		if stateOfRecording() == 1:
			# Translators: Message to inform the user that the recording is ready.
			sayMessage (_('The recording is ready ! It remains only to press spacebar for begin the recording. This same spacebar  will stop the recording !'))
		elif stateOfRecording() == 2:
			# Translators: Message to inform the user that a recording is in progress.
			sayMessage (_('A recording is in progress, please press spacebar for stop it and start a new one.'))
		else:
			# Translators: Message to inform the user that the recording is not ready.
			sayMessage (_('The recording is not ready !'))

	def script_begin(self, gesture):
		gesture.send()
		role = api.getFocusObject().role
		if isMenu() == True:
			return
		if role == ROLE_EDITABLETEXT:
			api.processPendingEvents()
			scriptHandler.executeScript(globalCommands.commands.script_review_currentCharacter, None)
			return
		if actualDuration() in [1, 2]:
			return
		if role != ROLE_PANE and not 'total' in api.getFocusObject().displayText:
			return
		if stateOfRecording() < 3:
			return
		if isStarting():
			sayMessage(themessages[3])
			return
		if not isRead():
			sayMessage (themessages[1])

	def script_end(self, gesture):
		gesture.send()
		role = api.getFocusObject().role
		if isMenu() == True:
			return
		if role == ROLE_EDITABLETEXT:
			api.processPendingEvents()
			scriptHandler.executeScript(globalCommands.commands.script_review_currentCharacter, None)
			return
		if actualDuration() in [1, 2]:
			return
		if stateOfRecording() < 3:
			return 
		if role != ROLE_PANE and not 'total' in api.getFocusObject().displayText:
			return
		if isStarting():
			sayMessage(themessages[3])
			return
		text = themessages[2]
		total = totalTime()
		if not isRead():
			sayMessage(text)
			time.sleep(0.3)
			sayMessage(total)

	def script_space(self, gesture):
		gesture.send()
		if isMenu() == True:
			return 
		if api.getFocusObject().role != ROLE_PANE:
			return
		if isStarting():
			sayMessage(themessages[3], space = True)
			return
		if isRecording ():
			return
		if stateOfRecording() > 5:
			return
		if isRead():
			return 
		sActual = actualDuration()
		if sActual in [1, 2]:
			return
		if not sActual:
			sayMessage(themessages[1], space = True)
			return
		sActual = sActual + ' ' + actualDurationPercentage()
		sayMessage(sActual, space = True)

	def script_left(self, gesture):
		gesture.send()
		role = api.getFocusObject().role
		if isMenu() == True:
			return 
		if role == ROLE_EDITABLETEXT:
			api.processPendingEvents()
			scriptHandler.executeScript(globalCommands.commands.script_review_currentCharacter, None)
			return
		if isStarting():
			sayMessage(themessages[3])
			return
		if stateOfRecording() > 4:
			return 
		if api.getFocusObject().role != ROLE_PANE:
			return
		if stateOfRecording() == 3:
			sActual = actualDuration()
			if not sActual:
				sActual = themessages[1]
			else:
				sActual = sActual + ' ' + actualDurationPercentage()
			if not isRead():
				sayMessage(sActual)

	def script_right(self, gesture):
		gesture.send()
		role = api.getFocusObject().role
		if isMenu() == True:
			return 
		if role == ROLE_EDITABLETEXT:
			api.processPendingEvents()
			scriptHandler.executeScript(globalCommands.commands.script_review_currentCharacter, None)
			return
		if isStarting():
			sayMessage(themessages[3])
			return
		if stateOfRecording() > 4:
			return
		if api.getFocusObject().role != ROLE_PANE:
			return 
		if stateOfRecording() == 3:
			sActual = actualDuration()
			if sActual == totalTime():
				sActual = themessages[2]
			else:
				sActual = sActual + ' ' + actualDurationPercentage()
			if not isRead():
				sayMessage(sActual)

	def script_nextSplittingPoint(self, gesture):
		gesture.send()
		role = api.getFocusObject().role
		if isMenu() == True:
			return 
		if role == ROLE_EDITABLETEXT:
			api.processPendingEvents()
			scriptHandler.executeScript(globalCommands.commands.script_review_currentWord, None)
			return
		if isStarting():
			sayMessage(themessages[3])
			return
		if stateOfRecording() > 4:
			return
		if api.getFocusObject().role != ROLE_PANE:
			return 
		if stateOfRecording() == 3:
			sActual = actualDuration()
			if sActual == totalTime():
				sActual = themessages[2]
			else:
				sActual = sActual + ' ' + actualDurationPercentage() if partOrSelection() == 2 else sActual + ' ' + part(flag=True)
			if not isRead():
				sayMessage(sActual)

	def script_previousSplittingPoint(self, gesture):
		gesture.send()
		role = api.getFocusObject().role
		if isMenu() == True:
			return 
		if role == ROLE_EDITABLETEXT:
			api.processPendingEvents()
			scriptHandler.executeScript(globalCommands.commands.script_review_currentWord, None)
			return
		if isStarting():
			sayMessage(themessages[3])
			return
		if stateOfRecording() > 4:
			return
		if api.getFocusObject().role != ROLE_PANE:
			return 
		if stateOfRecording() == 3:
			sActual = actualDuration()
			if not sActual:
				sActual = themessages[1]
			else:
				sActual = sActual + ' ' + actualDurationPercentage() if partOrSelection() == 2 else sActual + ' ' + part(flag=True)
			if not isRead():
				sayMessage(sActual)

	def script_moveSingleFrameForward(self, gesture):
		gesture.send()
		role = api.getFocusObject().role
		if isMenu() == True:
			return 
		if isStarting():
			sayMessage(themessages[3])
			return
		if stateOfRecording() > 4:
			return
		if api.getFocusObject().role != ROLE_PANE:
			return 
		if stateOfRecording() == 3:
			sActual = actualDuration()
			if sActual == totalTime():
				sActual = themessages[2]
			else:
				sActual = sActual + ' ' + actualDurationPercentage()
			if not isRead():
				sayMessage(sActual)

	def script_moveSingleFrameBackwards(self, gesture):
		gesture.send()
		role = api.getFocusObject().role
		if isMenu() == True:
			return 
		if isStarting():
			sayMessage(themessages[3])
			return
		if stateOfRecording() > 4:
			return
		if api.getFocusObject().role != ROLE_PANE:
			return 
		if stateOfRecording() == 3:
			sActual = actualDuration()
			if not sActual:
				sActual = themessages[1]
			else:
				sActual = sActual + ' ' + actualDurationPercentage()
			if not isRead():
				sayMessage(sActual)

	def script_pageUp(self, gesture):
		gesture.send()
		if isMenu() == True:
			return 
		if isStarting():
			sayMessage(themessages[3])
			return
		if stateOfRecording() > 4:
			return 
		if api.getFocusObject().role != ROLE_PANE:
			return
		sActual = actualDuration()
		if not sActual:
			sActual = themessages[1]
		else:
			sActual = sActual + ' ' + actualDurationPercentage()
		if not isRead():
			sayMessage(sActual)

	def script_pageDown(self, gesture):
		gesture.send()
		if isMenu() == True:
			return 
		if isStarting():
			sayMessage(themessages[3])
			return
		if stateOfRecording() > 4:
			return 
		if api.getFocusObject().role != ROLE_PANE:
			return
		sActual = actualDuration()
		if actualDurationPercentage() == '100%' and actualDuration() == totalTime():
			sActual = themessages[2]
		else:
			sActual = sActual + ' ' + actualDurationPercentage()
		if not isRead():
			sayMessage(sActual)

	def script_up(self, gesture):
		gesture.send()
		role = api.getFocusObject().role
		if isMenu() == True:
			return
		if isRecording():
			return
		if stateOfRecording() in [4, 8] and role == ROLE_EDITABLETEXT:
			scriptHandler.executeScript(globalCommands.commands.script_review_currentLine, None)
			return
		if stateOfRecording() == 8 and role != ROLE_EDITABLETEXT:
			curObject = api.getFocusObject()
			curObjectName = curObject.name
			curObjectValue = curObject.value
			curObjectRole = curObject.role
			if curObjectName == u'-90 dB' or curObjectRole & ROLE_SYSTEM_SCROLLBAR:
				sayMessage(curObjectValue)
				return
		if isStarting():
			sayMessage(themessages[3])
			return
		if stateOfRecording() == 3:
			if partOrSelection() == 2:
				if not isRead():
					sActual = actualDuration()
					if not sActual:
						sActual = themessages[1]
					if sActual == totalTime():
						sActual = '%s %s' % (sActual, themessages[2])
					sayMessage (themessages[6] + ' : ' + sActual + ' ' + actualDurationPercentage())
			else:
				if not isRead():
					sActual = actualDuration()
					if not sActual:
						sayMessage('%s, %s' % (themessages[0], themessages[1]))
						return
					if sActual == totalTime():
						sActual = '%s %s' % (sActual, themessages[2])
					# Translators: Message to indicate the elapsed time.
					sayMessage ('%s, %s %s %s' % (themessages[0], _('Elapsed time: '), sActual, actualDurationPercentage()))

	def script_down(self, gesture):
		gesture.send()
		role = api.getFocusObject().role
		if isMenu() == True:
			return
		if isRecording():
			return
		if stateOfRecording() in [4, 8] and role == ROLE_EDITABLETEXT:
			scriptHandler.executeScript(globalCommands.commands.script_review_currentLine, None)
			return
		if stateOfRecording() == 8 and role != ROLE_EDITABLETEXT:
			curObject = api.getFocusObject()
			curObjectName = curObject.name
			curObjectValue = curObject.value
			curObjectRole = curObject.role
			if curObjectName == u'-90 dB' or curObjectRole & ROLE_SYSTEM_SCROLLBAR:
				sayMessage(curObjectValue)
				return
		if isStarting():
			sayMessage(themessages[3])
			return
		if stateOfRecording() == 3:
			if partOrSelection() == 2:
				if not isRead():
					sActual = actualDuration()
					if not sActual:
						sActual = themessages[1]
					if sActual == totalTime():
						sActual = '%s %s' % (sActual, themessages[2])
					sayMessage (themessages[7] + ' : ' + sActual + ' ' + actualDurationPercentage())
			else:
				if not isRead():
					sActual = actualDuration()
					if not sActual:
						sayMessage('%s, %s' % (themessages[0], themessages[1]))
						return
					if sActual == totalTime():
						sActual = '%s %s' % (sActual, themessages[2])
					# Translators: Message  to indicate the elapsed time.
					sayMessage ('%s, %s %s %s' % (themessages[0], _('Elapsed time: '), sActual, actualDurationPercentage()))

	def script_elapsedTime(self, gesture):
		if isMenu() == True:
			message(themessages[5])
			return 
		if stateOfRecording() > 5:
			if stateOfRecording() == 7:
				message(themessages[3])
				return
		if isRecording():
			message(themessages[4])
			return
		if stateOfRecording() == 3:
			if not actualDuration():
				text = themessages[1]
			elif actualDuration() == totalTime():
				text = '%s %s %s %s' % (_('Elapsed time: '), actualDuration(), themessages[2], actualDurationPercentage())
			else:
				# Translators: Message to indicate the elapsed time.
				text = '%s %s %s' % (_('Elapsed time: '), actualDuration(), actualDurationPercentage())
			repeat = getLastScriptRepeatCount()
			if repeat == 0:
				message(text)
			elif repeat == 1:
				message('%s %s' % (themessages[9], totalTime()))

	script_elapsedTime.__doc__ = _('Gives the duration from the beginning of the file to the current position of the playback cursor. If pressed twice, gives the total duration.')

	def script_timeRemaining(self, gesture):
		if isMenu() == True:
			message(themessages[5])
			return 
		if stateOfRecording() > 5:
			if stateOfRecording() == 7:
				message(themessages[3])
				return
		if isRecording():
			message(themessages[4])
			return
		if stateOfRecording() == 3:
			# Translators: Message to indicate the remaining time.
			message('%s %s' % (_('Remaining time: '), timeRemaining()))

	script_timeRemaining.__doc__ = _('Gives the time remaining from the current position of the playback cursor to the end of the file.')

	def script_vuMeter(self, gesture):
		gesture.send()
		h=api.getFocusObject().windowHandle
		hWnd = vuMeterHandle()
		if not hWnd:
			# Translators: Message to indicate that the vu-meter is not available.
			sayMessage(_('The vu-meter is not available. Please verify if a recording is in progress, and that the checkbox enable the margin button is checked in the options of %s.') % programName)
			return
		repeat = getLastScriptRepeatCount()
		o = AccessibleObjectFromWindow(hWnd, -4)
		sLevel = o.accValue(0)
		if sLevel:
			if repeat == 0:
				sayMessage(themessages[8] + ' : ' + sLevel)
			elif repeat == 1:
				setFocus(hWnd)
				mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, None, None)
				mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, None, None)
				# Translators: Message to confirm that the level of the vu-meter has been reset.
				sayMessage(_('The level of the vu-meter has been reset !'))
				setFocus(h)
		else:
			sayMessage(_('The vu-meter is not available. Please verify if a recording is in progress, and that the checkbox enable the margin button is checked in the options of %s.') % programName)

	script_vuMeter.__doc__ = _('Used to determine the current level of the vu-meter, during recording, double pressure reset it.')

	def script_bPosition(self, gesture):
		gesture.send()
		if isMenu() == True:
			return 
		if stateOfRecording() != 3 and stateOfRecording() != 4:
			return 
		if api.getFocusObject().role != ROLE_PANE:
			return 
		if not isRead():
			# Translators: Message to confirm the placement of the selection start marker.
			sayMessage(_("It's OK, your marker of the beginning of selection B has been posed."), marker = True)

	def script_nPosition(self, gesture):
		gesture.send()
		if isMenu() == True:
			return 
		if stateOfRecording() != 3 and stateOfRecording() != 4:
			return 
		if api.getFocusObject().role != ROLE_PANE:
			return 
		if not isRead():
			# Translators: Message to confirm the placement of the selection end marker.
			sayMessage(_("It's OK, your marker of the end of selection N has been posed."), marker = True)

	def script_stop(self, gesture):
		gesture.send()
		if isMenu() == True:
			return 
		if stateOfRecording() > 4:
			return
		if api.getFocusObject().role != ROLE_PANE:
			return 
		sActual = actualDuration()
		sActual = sActual + ' ' + actualDurationPercentage()
		sayMessage(sActual)

	def script_beginningOfSelection(self, gesture):
		repeat = getLastScriptRepeatCount()
		beginSelection = beginSelection()
		if not beginSelection:
			beginSelection = themessages[1]
		if partOrSelection() == 2:
			if repeat == 0:
				sayMessage(themessages[6] + ' : ' + beginSelection)
			elif repeat == 1:
				sayMessage(themessages[10] + ' : ' + selectionDuration())
		else:
			sayMessage(themessages[12])

	script_beginningOfSelection.__doc__ = _('Used to indicate the position of the marker of the beginning of selection B. Double pressure lets give you the duration of the selection.')

	def script_endOfSelection(self, gesture):
		repeat = getLastScriptRepeatCount()
		beginSelection = beginSelection()
		if not beginSelection:
			beginSelection = themessages[1]
		if partOrSelection() == 2:
			if repeat == 0:
				sayMessage(themessages[7] + ' : ' + endSelection())
			elif repeat == 1:
				sayMessage(themessages[6] + ' : ' + beginSelection)
				sayMessage(themessages[7] + ' : ' + endSelection())
				sayMessage(themessages[10] + ' : ' + selectionDuration())
		else:
			sayMessage(themessages[12])

	script_endOfSelection.__doc__ = _('Used to indicate the position of the marker of the end of selection N. Double pressure gives recapitulatif positions B and N, and the duration of the selection.')

	def script_actualPart(self, gesture):
		if partOrSelection() == 1:
			message(part())
		elif stateOfRecording() > 5:
			if stateOfRecording() != 7:
				return
			message(themessages[3])
		elif isRecording():
			message(themessages[13] + ' ' + themessages[15])
		elif partOrSelection() == 2:
			message(themessages[13] + ' ' + themessages[14])
		else:
			message(themessages[13])

	script_actualPart.__doc__ = _('Give the reference of the actual part and the total number of parts in the current file.')

	def script_open_help(self, gesture):
		os.startfile(addonHandler.getCodeAddon().getDocFilePath())

	script_open_help.__doc__=_('Lets open the help of the current add-on.')

	__gestures = {
		'kb:r': 'checkRecording',
		'kb:home': 'begin',
		'kb:end': 'end',
		'kb:control+shift+d': 'elapsedTime',
		'kb:control+shift+r': 'timeRemaining',
		'kb:space': 'space',
		'kb:leftArrow': 'left',
		'kb:rightArrow': 'right',
		'kb:control+leftArrow':'previousSplittingPoint',
		'kb:control+rightArrow':'nextSplittingPoint',
		'kb:shift+leftArrow':'moveSingleFrameBackwards',
		'kb:shift+rightArrow':'moveSingleFrameForward',
		'kb:pageUp': 'pageUp',
		'kb:pageDown': 'pageDown',
		'kb:upArrow': 'up',
		'kb:downArrow': 'down',
		'kb:control+shift+space': 'vuMeter',
		'kb:b': 'bPosition',
		'kb:n': 'nPosition',
		'kb:s': 'stop',
		'kb:control+shift+b': 'beginningOfSelection',
		'kb:control+shift+n': 'endOfSelection',
		'kb:control+shift+p': 'actualPart',
		'kb:NVDA+H': 'open_help'
	}
