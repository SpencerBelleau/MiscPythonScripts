def colorTupleFromValue(val, base):
	if(val > (pow(base, 3) - 1)):
		raise Exception("Cannot represent number " + str(val) + " as a 3 digit integer of base " + str(base))
		#You screwed it up
	color = [0, 0, 0]
	
	hundreds = (val - (val%pow(base, 2)))/pow(base, 2)
	color[2] = int(hundreds)
	val -= hundreds * pow(base, 2)
	
	tens = (val - (val%base))/base
	color[1] = int(tens)
	val -= tens * base
	
	color[0] = int(val)
	
	return tuple(color)
try:
	print(colorTupleFromValue(44, 6))
except Exception as e:
	print(e)