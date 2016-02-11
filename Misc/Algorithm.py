#Returns the sum of a set
def sum(list):
	if (list == []):
		return 0
	sum = 0
	for element in list:
		sum += element
	return sum
#Set input here
#set = [4,14,15,16,17]
set = []
inp = 0
while inp != -1:
	inp = int(input("Enter set element (-1 to end input): "))
	#Ugly Hack
	if inp != -1:
		set.append(inp)
#Check to make sure the sum is even
if(sum(set)%2 != 0):
	print ("Set sum is not even, exiting")
	exit()
print (set)
total = sum(set)
print ("Set total is " + str(total))
#Get the target set sum
target = total/2
print ("Target set size is " + str(int(target)))
#Sort the set in ascending order
set.sort(reverse=True)
set1, set2 = [], []
#Used for searching the base set
offset = 0
#Add elements to the first subset, starting with the largest, until we reach the target
while sum(set1) < target:
	#If we've gone through the whole thing without finding an appropriate number, exit
	if (offset > len(set) - 1):
		print ("No possible way to evenly split sets, exiting")
		exit()
	#If we're on a suitable number, i.e. number is less than or equal to the difference between current set size and target set size
	if(set[0 + offset] <= (target - sum(set1))):
		#add that number to the first subset
		set1.append(set[0 + offset])
		set.pop(0 + offset)
	#If we're not
	else:
		#Look at the next number
		offset += 1
#Second subset is equal to the remaining elements from the first set
set2 = set
#Show the world how smart we are
print ("First Set is " + str(set1) + ", sum is " + str(sum(set1)) + "\nSecond Set is " + str(set2) + ", sum is " + str(sum(set2)))
target = input()