class Sample:
	
	def __init__(self, r):
		self.r = r
	
	def get_sample(self):
		min_range = (int)(len(self.r) / 2) - 500
		max_range = (int)(len(self.r) / 2) + 500
		sample = self.r[min_range:max_range]
		sample = [float(i) for i in sample] #sample instead of r
		return sample
