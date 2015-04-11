from boxlift_api import BoxLift, Command

elevators_dict = {}

def decide_on_commands(state):
	commands = []

	already_treated_elevators = []

	for elevator in state['elevators']:
		if elevator['buttons_pressed']:
			if elevator['floor'] in elevator['buttons_pressed']:
				commands.append(
					Command(
						id=elevator['id'], 
						direction=elevators_dict.get(str(elevator['id']), 1),
						speed=0
					)
				)
				already_treated_elevators.append(str(elevator['id']))
				elevators_dict[str(elevator['id'])] = 0

			else:
				if elevator['buttons_pressed']:
					if elevator['buttons_pressed'][0] < elevator["floor"]:
						commands.append(
							Command(
								id=elevator['id'], 
								direction=-1,
								speed=1
							)
						)
						already_treated_elevators.append(str(elevator['id']))
						elevators_dict[str(elevator['id'])] = -1
					else:
						commands.append(
							Command(
								id=elevator['id'], 
								direction=1,
								speed=1
							)
						)
						already_treated_elevators.append(str(elevator['id']))
						elevators_dict[str(elevator['id'])] = 1


	for request in state['requests']:
		closest_id = None
		closest_gap = 9000
		direction = 0
		for elevator in state['elevators']:
			if str(elevator['id']) in already_treated_elevators:
				continue

			# find closest elevator
			if closest_id is None or (abs(elevator['floor']) - request['floor'] < closest_gap):
				closest_id = elevator['id']
				closest_gap = abs(elevator['floor']) - request['floor']
				if closest_gap:
					break

		if closest_id is None:
			continue

		if closest_gap == 0:
			commands.append(
				Command(
					id=closest_id,
					direction=request['direction'],
					speed=0)
			)
			elevators_dict[str(elevator['id'])] = 0
		else:
			if elevator['floor'] > request['floor']:
				direction = -1
			else:
				direction = 1

			commands.append(
				Command(
					id=closest_id,
					direction=direction,
					speed=1))

			elevators_dict[str(elevator['id'])] = direction

		already_treated_elevators.append(str(closest_id))

	if len(already_treated_elevators) < len(commands):
		
		for elevator in state['elevators']:
			if str(elevator['id']) in already_treated_elevators:
				continue

			if elevator['floor'] < state['floors']/2:
				commands.append(
					Command(
						id=elevator['id'], 
						direction=1, 
						speed=1
					)
				)
				elevators_dict[str(elevator['id'])] = 1
				already_treated_elevators.append(str(elevator['id']))

			elif elevator['floor'] == state['floors']/2:
				commands.append(
					Command(
						id=elevator['id'], 
						direction=-1, 
						speed=0
					)
				)
				elevators_dict[str(elevator['id'])] = 0
				already_treated_elevators.append(str(elevator['id']))
			else:
				commands.append(
					Command(
						id=elevator['id'], 
						direction=-1, 
						speed=1
					)
				)
				elevators_dict[str(elevator['id'])] = -1
				already_treated_elevators.append(str(elevator['id']))

	return commands





REG_ID = "11650"
PYCON2015_EVENT_NAME = "pycon2015"

def run_simulation(name):

	lift_api = BoxLift(bot_name='dumbelevator', plan=name, email='sleongkoan@gmail.com',
	    registration_id=REG_ID, event_name=PYCON2015_EVENT_NAME)

	state = lift_api.send_commands()

	elevators_dict = {str(elevator['id']): 1 for elevator in state['elevators']}

	# setup building with elevators from returned state
	while state['status'] != 'finished':

	    commands = decide_on_commands(state)
	    state = lift_api.send_commands(commands)

run_simulation('training_1')
run_simulation('training_2')
run_simulation('training_3')
run_simulation('ch_rnd_500_1')
run_simulation('ch_rnd_500_2')
run_simulation('ch_rnd_500_3')
run_simulation('ch_clu_500_1')
run_simulation('ch_clu_500_2')
run_simulation('ch_clu_500_3')
run_simulation('ch_rea_1000_1')
run_simulation('ch_rea_1000_2')
run_simulation('ch_rea_1000_3')
