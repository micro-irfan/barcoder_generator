from collections import defaultdict

class Edge:

	def __init__(self, node1, node2):
		self.node1 = node1
		self.node2 = node2

class Graph:
	"""docstring for Edge"""
	def __init__(self): 
		# default dictionary to store graph 
		self.graph = defaultdict(list) 
		self.delete_list = []
		self.save_items = []

	# function to add an edge to graph 
	def addEdge(self,u,v):
		#adds edges in both direction 
		self.graph[u].append(v)
		self.graph[v].append(u)

	def filter_edges(self):
		#print (self.graph['CATGCTGC'])
		#print (self.graph['TGTTCTGC'])
		for k, v in self.graph.items():
			if len(v) >= 2:
				broken_count = 0
				for i in v:
					#check if node in the other node's edge list
					#if True: append to delete list 
					#else: not in the linked to the other node
					#if k in self.graph[i]: 
					#check if in list already
					if len(v) - broken_count <= 1:
						break

					if i in self.delete_list:
						broken_count += 1
						continue

					if len(self.graph[i]) == 1:
						continue

					'''temp_broken_count = 0
					if len(self.graph[i]) > 1:
						for j in self.graph[i]:
							if j in self.delete_list:
								temp_broken_count += 1
						if len(self.graph[i]) - temp_broken_count <= 1:
							broken_count += 1
							continue'''
					
					if not k in self.delete_list:
						self.delete_list.append(k)
						break
			
			if len(v) == 1:
				if len(self.graph[v[0]]) > 1:
					broken_count = 0
					for i in self.graph[v[0]]:
						if i in self.delete_list:
							broken_count += 1
							continue
					if len(v) - broken_count > 1:
						continue
				if not k in self.delete_list or not v in self.delete_list:
					self.delete_list.append(k)


	def print(self):
		print(len(self.delete_list), len(self.save_items) )

	def check_HD_again(self, HD):
		count = 0
		poor_list = []
		for i in range(len(self.save_items)):
			for j in range(i+1, len(self.save_items)):
				h = sum(ch1 != ch2 for ch1, ch2 in zip(self.save_items[i], self.save_items[j]))
				if h <= HD: 
					#count += 1
					print (self.save_items[i],self.save_items[j])
					if self.save_items[j] in poor_list:
						continue
					else:
						poor_list.append(self.save_items[j])
						#break
		print (2, count)

	def write_file(self, barcodes, HD):
		write_file = open(f'saved_barcodes_{HD}.txt', 'w')
		self.save_items = [item for item in barcodes if item not in self.delete_list]
		for i in self.save_items:
			current_index = barcodes.index(i)
			write_file.write(f'{current_index}\t{i}\n')
		write_file.close()

		delete_file = open(f'deleted_barcodes_{HD}.txt', 'w')
		for i in self.delete_list:
			current_index = barcodes.index(i)
			delete_file.write(f'{current_index}\t{i}\n')
		delete_file.close()

graph = Graph()

HD = 3
file = 'file.txt'
barcodes = []
with open(file, 'r') as f:
	for line in f:
		line = line.strip().split('\t')
		barcodes.append(line[1])

#barcodes = sorted(barcodes)

temp_list = []
for i in range(len(barcodes)):
	for j in range(i+1, len(barcodes)):
		h = sum(ch1 != ch2 for ch1, ch2 in zip(barcodes[i], barcodes[j]))
		if h <= HD: 
			graph.addEdge(barcodes[i], barcodes[j])
			temp_list.append(barcodes[i])

temp_list = list(set(temp_list))
print (1, len(temp_list))			#break

graph.filter_edges()

graph.write_file(barcodes, HD)
graph.print()
graph.check_HD_again(HD)

#TGTTCTGC CATGCTGC