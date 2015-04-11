from boxlift_api import BoxLift, Command
from collections import defaultdict

class Elevator(object):
	speed = None
	direction = None

	def __init__(self, id, floor, max_floor):
		self.id = id
		self.direction = 1
		self.speed = 1
		self.buttons_pressed = []
		self.floor = floor
		self.max_floor = max_floor
		self.assigned_requests = []

	def update_elevator(self):
			self.floor += (self.direction * self.speed)

	def go_up(self):
		self.direction = 1

	def go_down(self):
		self.direction = -1

	def stop(self):
		self.speed = 0

	def move(self):
		self.speed = 1

	def chose_own_command(self):
		if self.floor == 0:
			self.go_up()
			self.move()

		elif self.floor == self.max_floor:
			self.go_down()
			self.move()

		elif self.floor == self.max_floor / 2:
			self.stop()

	def fulfill_requests(self):
		if self.assigned_requests or self.buttons_pressed:
			requested_floors = [
				request['floor'] for request in self.assigned_requests
			]

			for floor in self.buttons_pressed:
				requested_floors.append(floor)

			if self.floor in requested_floors:
				self.stop()

				for request in self.assigned_requests:
					if request['floor'] == self.floor:

						self.direction = request['direction']
						self.assigned_requests.remove(request)
						break

			else:
				if requested_floors[0] < self.floor:
					self.go_down()
				else:
					self.go_up()

				self.move()

		else:
			self.chose_own_command()

	def get_command(self):
		return Command(
			id=self.id,
			direction=self.direction,
			speed=self.speed)

	def get_assigned(self, request):
		if request in self.assigned_requests:
			return True

		if not self.assigned_requests and not self.buttons_pressed:
			self.assigned_requests.append(request)
			return True

		if self.direction == request['direction']:
			if self.direction == 1 and self.floor <= request['floor']:
				self.assigned_requests.append(request)
				return True

			elif self.direction == -1 and self.floor >= request['floor']:
				self.assigned_requests.append(request)
				return True

		return False

def decide_on_commands(state, elevators):
	print('########################')
	commands = []

	already_assigned_requests = []

	for elevator in elevators:
		already_assigned_requests.extend(elevator.assigned_requests)

	for request in state['requests']:
		if request in already_assigned_requests:
			continue

		# find the closest elevator
		elevator_by_gaps = defaultdict(list)

		for elevator in elevators:
			gap = abs(request['floor'] - elevator.floor)
			elevator_by_gaps[gap].append(elevator)

		assigned = False
		for gap in sorted(elevator_by_gaps.keys()):
			if assigned:
				break

			for elevator in elevator_by_gaps[gap]:
				if assigned:
					break

				assigned = elevator.get_assigned(request)

				if assigned:
					print('elevator ', elevator.id, elevator.floor, 'got assigned', request)

	for elevator in elevators:
		elevator.fulfill_requests()
		commands.append(elevator.get_command())
		elevator.update_elevator()

	return commands





REG_ID = "11650"
PYCON2015_EVENT_NAME = "pycon2015"

def run_simulation(name):

	lift_api = BoxLift(bot_name='dumbelevator', plan=name, email='sleongkoan@gmail.com',
	    registration_id=REG_ID, event_name=PYCON2015_EVENT_NAME, sandbox_mode=True)

	state = lift_api.send_commands()

	elevators = [
		Elevator(
			id=elevator['id'],
			floor=elevator['floor'],
			max_floor=state['floors']
		)

		for elevator in state['elevators']
	]

	# setup building with elevators from returned state
	while state['status'] != 'finished':

	    commands = decide_on_commands(state, elevators)
	    state = lift_api.send_commands(commands)


run_simulation('training_1')
# run_simulation('training_2')
# run_simulation('training_3')
# run_simulation('ch_rnd_500_1')
# run_simulation('ch_rnd_500_2')
# run_simulation('ch_rnd_500_3')
# run_simulation('ch_clu_500_1')
# run_simulation('ch_clu_500_2')
# run_simulation('ch_clu_500_3')
# run_simulation('ch_rea_1000_1')
# run_simulation('ch_rea_1000_2')
# run_simulation('ch_rea_1000_3')
