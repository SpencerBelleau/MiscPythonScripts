list = []
n = int(input("Enter an array size: "))
for i in range(n):
	list.append(i+1)
##This is really funny because if I was a cheater I'd just show this number at the end
while True:
	x = int(input("Enter a number to remove: "))
	if x in list:
		list.remove(x)
		break
	else:
		print("Error, number not in list")
##The actual meat of the algorithm
left = 0
middle = 0 ##Just a placeholder in case python would wreck the memory management without it
right = len(list) - 1
##Step counter
steps = 0
while(abs(left - right) > 1):
	print("----------------------------------------")
	print("left index = " + str(left) + ", right index = " + str(right))
	print("left val = " + str(list[left]) + ", right val = " + str(list[right]))
	##Compute the middle
	middle = int((right + left)/2)
	##Get the diffs
	diffLeft = list[middle] - list[left]
	diffRight = list[right] - list[middle]
	print("middle index = " + str(middle))
	print("dL = " + str(diffLeft) + ", dR = " + str(diffRight))
	##Shift the bounds of out search range
	if(diffLeft >= diffRight):
		right = middle
	else:
		left = middle
	steps = steps + 1
##Final step would normally not print, so here it is
print("----------------------------------------")
print("left index = " + str(left) + ", right index = " + str(right))
print("left val = " + str(list[left]) + ", right val = " + str(list[right]))
print("middle index = " + str(middle))
print("dL = " + str(diffLeft) + ", dR = " + str(diffRight))
print("-------------Solution Found-------------")
print("Missing Number is " + str(list[left] + 1))
print("Algorithm took " + str(steps) + " steps to finish.")