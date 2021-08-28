from events import Event
from entities.entity import Entity
from listeners.tick import Delay
from messages import HudDestination, TextMsg
from cvars import cvar

can_delay = True

@Event('round_start')
def round_start(args):
	global can_delay
	global mydelay
	ftime = cvar.find_var('mp_freezetime').get_float()
	rtime = cvar.find_var('mp_roundtime').get_float() * 60.0 + ftime + 5.0
	if can_delay:
		mydelay = Delay(float(rtime), endRound)
		print('[Round End]: Timer have been started!')
		can_delay = False
	else:
		mydelay.cancel()
		print('[Round End]: Old timer have cancelled!!')
		mydelay = Delay(float(rtime), endRound)
		print('[Round End]: Started new timer!')

def endRound():
	global can_delay
	Entity.find_or_create('info_map_parameters').fire_win_condition(9)
	TextMsg('ROUND DRAW', HudDestination.CENTER).send()
	can_delay = True
	print('[Round End]: Round have been ended!')
