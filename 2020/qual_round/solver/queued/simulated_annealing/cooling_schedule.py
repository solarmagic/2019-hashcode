class CoolingSchedule:
  def temperature(self):
    raise NotImplementedError

  def next(self):
    raise NotImplementedError


class ZeroCoolingSchedule(CoolingSchedule):
  def temperature(self):
    return 0

  def next(self):
    return 0


class ExpCoolingSchedule(CoolingSchedule):
  def __init__(self, T0, rate):
    self.T0 = T0
    self.T = T0
    self.rate = rate

  def temperature(self):
    return self.T

  def next(self):
    self.T *= self.rate
    return self.T


class LinearCoolingSchedule(CoolingSchedule):
  def __init__(self, T0, T1, duration):
    self.T0 = T0
    self.T1 = T1
    self.duration = duration
    self.k = 0

  def temperature(self):
    if self.k > self.duration:
      return self.T1
    else:
      return (self.T0 * (self.duration-self.k) + self.T1 * self.k) / self.duration

  def next(self):
    self.k += 1
    return self.temperature()
