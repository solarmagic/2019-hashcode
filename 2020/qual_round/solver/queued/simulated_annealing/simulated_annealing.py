class SimulatedAnnealing:
  def __init__(self, cooling_schedule, acceptance_policy):
    self.cooling_schedule = cooling_schedule
    self.acceptance_policy = acceptance_policy
    self.accepted = 0

  def set_state(self, state):
    self.state = state

  def temperature(self):
    return self.cooling_schedule.temperature()

  def step(self):
    mutation = self.state.random_mutation()
    accept = self.acceptance_policy.accept(self.state,
                                           mutation,
                                           self.cooling_schedule.next())
    if accept:
      self.accepted += 1
      self.state.apply_mutation(mutation)

  def run(self, tries, backup):
    print('Started running simulated annealing...')

    for i in range(1, tries+1):
      self.step()

      if (i % 10 == 0 or i == tries):
        print('tries={}, T={} | accepted={}, score={}'.format(i, self.temperature(), self.accepted, self.state.score()))

      if (i % 100 == 0):
        print('Doing backup...')
        backup()

