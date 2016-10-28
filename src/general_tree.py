# A General tree in Python using lists.
# Tested for sample inputs


class Node(object):							#Class is Created for Node
	def __init__(self,data):				#Constructor defines the data members
		self.data = data
		self.children = []

	def add_child(self,obj):				#Adds new Child
		self.children.append(obj)

print("Enter root node :")
root_node = raw_input().strip()

n = Node(root_node)							#Calls to the Constructor

node_list = []								#An Empty list

print("Number of childs in it :")

N = int(raw_input().strip())

for j in range (0, N):
	temp = raw_input()
	node_list.append(temp)

r = Node(root_node)

for k in range(0,N):
	temp1 = Node(node_list[k])
	r.add_child(temp1)

for i in r.children:
	print i.data,"->",
