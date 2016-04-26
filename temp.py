numbers_float=[]
with open('antenna_pattern.txt') as f:
	for line in f:
		numbers_float.append(map(float, line.split()))