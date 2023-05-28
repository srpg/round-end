from cvars import cvar
from events import Event
from messages import TextMsg
from listeners.tick import Delay
from entities.entity import Entity
from filters.entities import EntityIter

can_delay = True

def bomb_amounts():
	return len(EntityIter('func_bomb_target'))

def hostage_amounts():   
	return len(EntityIter('func_hostage_rescue'))

@Event('round_start')
def round_start(args):
	if bomb_amounts() == 0 or hostage_amounts() == 0 or hostage_amounts() == 0 and bomb_amounts() == 0:
		global can_delay
		global mydelay
		ftime = cvar.find_var('mp_freezetime').get_float()
		rtime = cvar.find_var('mp_roundtime').get_float() * 60.0 + ftime + 5.0
		if can_delay:
			mydelay = Delay(float(rtime), endRound)
			print('[Round End]: Timer have been started!')
			can_delay = False
		else:
			try:
				mydelay.cancel()
			except ValueError:
				pass
			print('[Round End]: Old timer have cancelled!!')
			mydelay = Delay(float(rtime), endRound)
			print('[Round End]: Started new timer!')

def endRound():
	global can_delay
	Entity.find_or_create('info_map_parameters').fire_win_condition(9)
	TextMsg('ROUND DRAW').send()
	can_delay = True
	print('[Round End]: Round have been ended!')
