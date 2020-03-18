#Artificial Intelligence Assignment 2



#Code Author - Nischal Badarinath Kashyap
#computer Science Department
#Dated - Febrauary 22nd 2020
#North Carolina State University

import math
import sys

class map:
	def __init__(self,di,cost,source,dest,cities,consi,minpath,glo):
		self.di = di
		self.cost = cost
		self.source = source
		self.dest = dest
		self.cities = cities
		self.consi = consi
		self.minpath = minpath
		self.pcost = 0
		self.globaldict = {}
		self.previous_city = {}
		self.costtillnow = {}
		self.compath = {}
		self.glo = glo
		self.cycle = []
		self.maxical = 0

class astar(map):
	def __init__(self, di, cost, source, dest, cities,consi,minpath,glo):
		map.__init__(self, di, cost, source, dest, cities,consi,minpath,glo)

	def ast(self,a,b,prev,calc):
		if a not in self.consi:
			self.consi.append(a)
			#Number of cities expanded
		
		if a==self.dest:
			print("")
			print("A* Search")
			print("-------------------")
			print("Destination reached")
			print("-------------------")
			print("")
			print("Cost is ",b)
			print("")
			print("Cities expanded = ",len(self.consi))
			print("")
			print("The Path to be taken is ")
			print("")
			print(self.compath[self.dest])
			print("")
			print("Maximum successor queue = ",calc)
			print("")
		else:
			for i in self.di[a]: 
				if i!=prev:
					self.compath[i] = self.compath[a]+"->"+i
					self.costtillnow[self.source+i]=roads[i+a]+b
					cost1 = roads[i+a]+heuristic(i,self.dest,int(self.glo))+b
					self.globaldict[i] = cost1
					self.previous_city[i] = a
			sorted_x = sorted(self.globaldict.items(), key=lambda kv: kv[1])
			del self.globaldict[sorted_x[0][0]]

			if calc>len(sorted_x):
				valuepassed = calc
				#valuepassed is a variable used to check the maximum queue that could be achieved in the A* search in one search.
			else:
				valuepassed = len(sorted_x)
			astar.ast(self,sorted_x[0][0],self.costtillnow[self.source+sorted_x[0][0]],self.previous_city[sorted_x[0][0]],valuepassed)

	def run(self):
		for i in self.di[self.source]:
			
			self.compath[i] = self.source + "->" + i
			#self.compath stores the path taken by the search algorithm until the node i. Here key is i while value is the path to i from source.
			
			self.costtillnow[self.source+i] = roads[i+self.source]
			#self.costtillnow stores the path cost of the search algorithm until the node i from the sourcenode. Eg : bostonraleigh : x, seattleraleigh : y
			
			cost1 = roads[i+self.source]+heuristic(i,self.dest,int(self.glo))
			#cost1 provides us with the total cost, f(n)
			
			self.globaldict[i] = cost1
			#self.globaldict is the open list from which the minimum node will be extracted and further on which the A* would be performed.
			
			self.previous_city[i] = self.source
			#self.previous_city stores the previous node to a particular node x.
		
		sorted_x = sorted(self.globaldict.items(), key=lambda kv: kv[1])
		del self.globaldict[sorted_x[0][0]]
		#we need to delete the node after considering it for A*.
		
		astar.ast(self,sorted_x[0][0],roads[sorted_x[0][0]+self.source],self.previous_city[sorted_x[0][0]],len(sorted_x))

class depth(map):
	def __init__(self, di, cost, source, dest, cities,consi,minpath,glo):
		map.__init__(self, di, cost, source, dest, cities,consi,minpath,glo)
	def dfs(self,s,prev):
		if s not in self.cities:
			self.cities.append(s)
		#To find all the cities that have been touched in this search process

		mainpath = ""
		minipath = 25000000
		maxidepth = -1
		depthval = 0
		if s == self.dest:
			return [s,0,0]
		#returns distance as 0
		
		if len(self.di[s])==1:
			return 25000000
		#if this is a leaf node and is not the destination

		for i in self.di[s]:
			if i not in self.consi:
				self.consi.append(i)
			#self.consi is used to check for cycles.

				k = depth.dfs(self,i,s)
				self.consi = self.consi[0:len(self.consi) - 1]
				if k!=25000000:
					depthval = k[2]+1
					if depthval>maxidepth:
						maxidepth = depthval
						#since we need the maximum depth, we store the search tree that has the maximum depth/path in its search process.
					
					value = self.cost[s+i]+k[1]
					if value<minipath:
						minipath = self.cost[s+i]+k[1]
						mainpath = s + ' -> ' + k[0]
					#to compare and store the tree path that has the lowest cost after the destination is successsfully reached.
			
			if i in self.consi and i!=prev and len(self.di[s])==1:
				return 25000000
		
		return [mainpath,minipath,depthval]

	def run(self):
		maxidepth = -1
		for i in self.di[self.source]:
			self.consi.append(i)
			k = depth.dfs(self,i,self.source)
			if k!=25000000:
				if maxidepth<(k[2]+1):
					maxidepth = k[2]+1
				val = k[1]+self.cost[self.source+i]
				pathdet = self.source + ' -> ' + k[0]
				
				if val<self.minpath:
					oldpath = pathdet
					self.minpath = val
			
			self.consi = [self.source]
		print("")
		print("Depth First Search")
		print("")
		print("-------------------")
		print("Destination reached")
		print("-------------------")
		print("The total from ",source," to ",destination," is ",self.minpath)
		print("")
		print("The route to be taken is ")
		print("")
		print(oldpath)
		print("")
		print("Cities expanded = ",len(self.cities))
		print("")
		print("Maximum Successor Queue length is ",maxidepth)
		print("")
		
		return len(self.cities)

class rbfs(map):
	def __init__(self, di, cost, source, dest, cities,consi,minpath,glo):
		map.__init__(self, di, cost, source, dest, cities,consi,minpath,glo)

	def rbf(self,a,b,nextbest,nextbestcity,prev,calc):

		if len(self.di[a])==1 and a!=self.dest:
			return [2000000000,nextbestcity]
		
		if a not in self.consi:
			self.consi.append(a)
		
		if a in self.cycle:
			return [2000000000,nextbestcity]
		#if cycle encountered

		self.cycle.append(a)
		
		if a==nextbestcity:
			return [2000000000,nextbestcity]

		nextbestvar = True
		level = {}
		flag = 0
		least = 10000000000
		nextbestlocal = nextbest
		nextbestlocalcity = nextbestcity
		
		if a==self.dest:
			print("")
			print("Recursive Best First Search")
			print("")
			print("-------------------")
			print("Destination reached")
			print("-------------------")
			print("")
			print("The total route cost is ",b)
			print("")
			print("Cities expanded = ",len(self.consi))
			print("")
			print("The path to be taken is ")
			print("")
			print(self.compath[self.dest])
			print("")
			print("Maximum successor queue = ",self.maxical)
			print("")
		else:
			for i in self.di[a]:
				if i!=prev and i!=nextbestcity:
					self.compath[i] = self.compath[a]+"->"+i\
					#self.compath stores the path taken by the search algorithm until the node i. Here key is i while value is the path to i from source.
					
					self.costtillnow[self.source+i]=roads[i+a]+b
					#self.costtillnow stores the path cost of the search algorithm until the node i from the sourcenode. Eg : bostonraleigh : x, seattleraleigh : y
					
					cost1 = roads[i+a]+heuristic(i,self.dest,int(self.glo))+b
					#cost1 provides us with the total cost, f(n)
					
					level[i] = cost1
					#Stores the heuristic cost of all nodes at every level in tree expansion.
					
					self.previous_city[i] = a
					#self.previous_city stores the previous node to a particular node x.

			if len(level)==0:
				self.cycle = self.cycle[0:len(self.cycle)-1]
				#if this is a leaf node
				
				return [200000000,nextbestcity]
			while nextbestvar == True:
				nextbest = nextbestlocal
				nextbestcity = nextbestlocalcity
				level_sorted = sorted(level.items(), key=lambda kv: kv[1])
				#find the least cost element
				
				if level_sorted[0][1]<=nextbest:
					if len(level_sorted)>1 and level_sorted[1][1]<=nextbest:
						#if the 2nd least is lower than the previous best then make nextbest as 2nd least
						nextbest = level_sorted[1][1]
						nextbestcity = level_sorted[1][0]
					retval = rbfs.rbf(self,level_sorted[0][0],self.costtillnow[self.source+level_sorted[0][0]],nextbest,nextbestcity,a,calc+len(level_sorted))
					#recursively call rbfs
					
					if self.maxical<calc:
						self.maxical = calc
						#stores the maximum queue achieved value
					
					if retval is None:
						return None
					level[level_sorted[0][0]] = retval[0]
					#update the current node traversed with the value of least cost of child nodes

					if retval[1] not in level:
						#check whether the next best is not in the current level
						
						level_sorted = sorted(level.items(), key=lambda kv: kv[1])
						#resort the values again since it was updated. Check if the current resorted values have a node with lower cost. If yes send the value as next best to root nodes
						#If no then send the value received from the child node.
						
						if level_sorted[0][1]<retval[0]:
							self.cycle = self.cycle[0:len(self.cycle)-1]
							return [level_sorted[0][1],nextbestcity]
						else:
							self.cycle = self.cycle[0:len(self.cycle)-1]
							return [retval[0],nextbestcity]

					#else continue to traverse the while loop again with the next best node.
				else:
					self.cycle = self.cycle[0:len(self.cycle)-1]
					#if least cost of current level is less than the previous best, then backtrack with the current least value
					
					return [level_sorted[0][1],nextbestcity]


	def run(self):
		globaldict = {}
		for i in self.di[self.source]:
			self.compath[i] = self.source + "->" + i
			self.costtillnow[self.source+i] = roads[i+self.source]
			cost1 = roads[i+self.source]+heuristic(i,self.dest,int(self.glo))
			globaldict[i] = cost1
			self.previous_city[i] = self.source
		
		while True:
			sorted_x = sorted(globaldict.items(), key=lambda kv: kv[1])
			nextbestcity = sorted_x[1][0]
			self.cycle = [self.source]
			retval = rbfs.rbf(self,sorted_x[0][0],roads[sorted_x[0][0]+self.source],sorted_x[1][1],nextbestcity,self.source,len(sorted_x))
			
			if retval is None:
				print("Search Ends")
				return
			globaldict[sorted_x[0][0]] = retval[0]
			
def addpath(a,b,n):
	if a in adj:
		adj[a].append(b)
	else:
		adj[a]=[b]

	if b in adj:
		adj[b].append(a)
	else:
		adj[b]=[a]

	x = a+b
	y = b+a

	roads[x]=n
	roads[y]=n

def city(a,b,c):
	heur[str(a)] = [b,c]

def heuristic(a,b,glo):
	if glo==0:
		Lat1 = heur[a][0]
		Lat2 = heur[b][0]
		Long1 = heur[a][1]
		Long2 = heur[b][1]
		a = math.sqrt((69.5 * (Lat1 - Lat2))**2 + (69.5 * math.cos((Lat1 + Lat2)/360 * 3.1415) * (Long1 - Long2))**2)
		return a
	
	elif glo==1:
		Lat1 = heur[a][0]
		Lat2 = heur[b][0]
		Long1 = heur[a][1]
		Long2 = heur[b][1]
		

		if Lat1<0:
			Lat1 = abs(Lat1)
		if Lat2<0:
			Lat2 = abs(Lat2)

		if Lat1>Lat2:
			x = Lat1-Lat2
		else:
			x = Lat2-Lat1

		if Long1<0:
			Long1 = abs(Long1)
		if Long2<0:
			Long2 = abs(Long2)
		if Long1>Long2:
			y = Long1-Long2
		else:
			y = Long2-Long1

		return x+y

	else:
		print("Wrong Input")

adj = {}
roads = {}
heur = {}
addpath('albanyNY', 'montreal', 226)
addpath('albanyNY', 'boston', 166)
addpath('albanyNY', 'rochester', 148)
addpath('albanyGA', 'tallahassee', 120)
addpath('albanyGA', 'macon', 106)
addpath('albuquerque', 'elPaso', 267) 
addpath('albuquerque', 'santaFe', 61)
addpath('atlanta', 'macon', 82)
addpath('atlanta', 'chattanooga', 117)
addpath('augusta', 'charlotte', 161) 
addpath('augusta', 'savannah', 131)
addpath('austin', 'houston', 186) 
addpath('austin', 'sanAntonio', 79)
addpath('bakersfield', 'losAngeles', 112)  
addpath('bakersfield', 'fresno', 107)
addpath('baltimore', 'philadelphia', 102)  
addpath('baltimore', 'washington', 45)
addpath('batonRouge', 'lafayette', 50)  
addpath('batonRouge', 'newOrleans', 80)
addpath('beaumont', 'houston', 69)
addpath('beaumont', 'lafayette', 122)
addpath('boise', 'saltLakeCity', 349) 
addpath('boise', 'portland', 428)
addpath('boston', 'providence', 51)
addpath('buffalo', 'toronto', 105) 
addpath('buffalo', 'rochester', 64)  
addpath('buffalo', 'cleveland', 191)
addpath('calgary', 'vancouver', 605)  
addpath('calgary', 'winnipeg', 829)
addpath('charlotte', 'greensboro', 91)
addpath('chattanooga', 'nashville', 129)
addpath('chicago', 'milwaukee', 90)  
addpath('chicago', 'midland', 279)
addpath('cincinnati', 'indianapolis', 110)  
addpath('cincinnati', 'dayton', 56)
addpath('cleveland', 'pittsburgh', 157)  
addpath('cleveland', 'columbus', 142)
addpath('coloradoSprings', 'denver', 70)  
addpath('coloradoSprings', 'santaFe', 316)
addpath('columbus', 'dayton', 72)
addpath('dallas', 'denver', 792)  
addpath('dallas', 'mexia', 83)
addpath('daytonaBeach', 'jacksonville', 92)  
addpath('daytonaBeach', 'orlando', 54)
addpath('denver', 'wichita', 523)
addpath('denver', 'grandJunction', 246)
addpath('desMoines', 'omaha', 135)  
addpath('desMoines', 'minneapolis', 246)
addpath('elPaso', 'sanAntonio', 580)
addpath('elPaso', 'tucson', 320)
addpath('eugene', 'salem', 63) 
addpath('eugene', 'medford', 165)
addpath('europe', 'philadelphia', 3939)
addpath('ftWorth', 'oklahomaCity', 209)
addpath('fresno', 'modesto', 109)
addpath('grandJunction', 'provo', 220)
addpath('greenBay', 'minneapolis', 304) 
addpath('greenBay', 'milwaukee', 117)
addpath('greensboro', 'raleigh', 74)
addpath('houston', 'mexia', 165)
addpath('indianapolis', 'stLouis', 246)
addpath('jacksonville', 'savannah', 140)  
addpath('jacksonville', 'lakeCity', 113)
addpath('japan', 'pointReyes', 5131)
addpath('japan', 'sanLuisObispo', 5451)
addpath('kansasCity', 'tulsa', 249)
addpath('kansasCity', 'stLouis', 256) 
addpath('kansasCity', 'wichita', 190)
addpath('keyWest', 'tampa', 446)
addpath('lakeCity', 'tampa', 169)  
addpath('lakeCity', 'tallahassee', 104)
addpath('laredo', 'sanAntonio', 154)
addpath('laredo', 'mexico', 741)
addpath('lasVegas', 'losAngeles', 275)  
addpath('lasVegas', 'saltLakeCity', 486)
addpath('lincoln', 'wichita', 277)  
addpath('lincoln', 'omaha', 58)
addpath('littleRock', 'memphis', 137) 
addpath('littleRock', 'tulsa', 276)
addpath('losAngeles', 'sanDiego', 124)  
addpath('losAngeles', 'sanLuisObispo', 182)
addpath('medford', 'redding', 150)
addpath('memphis', 'nashville', 210)
addpath('miami', 'westPalmBeach', 67)
addpath('midland', 'toledo', 82)
addpath('minneapolis', 'winnipeg', 463)
addpath('modesto', 'stockton', 29)
addpath('montreal', 'ottawa', 132)
addpath('newHaven', 'providence', 110) 
addpath('newHaven', 'stamford', 92)
addpath('newOrleans', 'pensacola', 268)
addpath('newYork', 'philadelphia', 101)
addpath('norfolk', 'richmond', 92)
addpath('norfolk', 'raleigh', 174)
addpath('oakland', 'sanFrancisco', 8) 
addpath('oakland', 'sanJose', 42)
addpath('oklahomaCity', 'tulsa', 105)
addpath('orlando', 'westPalmBeach', 168) 
addpath('orlando', 'tampa', 84)
addpath('ottawa', 'toronto', 269)
addpath('pensacola', 'tallahassee', 120)
addpath('philadelphia', 'pittsburgh', 319) 
addpath('philadelphia', 'newYork', 101)
addpath('philadelphia', 'uk1', 3548)
addpath('philadelphia', 'uk2', 3548)
addpath('phoenix', 'tucson', 117)  
addpath('phoenix', 'yuma', 178)
addpath('pointReyes', 'redding', 215)  
addpath('pointReyes', 'sacramento', 115)
addpath('portland', 'seattle', 174)
addpath('portland', 'salem', 47)
addpath('reno', 'saltLakeCity', 520)
addpath('reno', 'sacramento', 133)
addpath('richmond', 'washington', 105)
addpath('sacramento', 'sanFrancisco', 95)  
addpath('sacramento', 'stockton', 51)
addpath('salinas', 'sanJose', 31)
addpath('salinas', 'sanLuisObispo', 137)
addpath('sanDiego', 'yuma', 172)
addpath('saultSteMarie', 'thunderBay', 442)  
addpath('saultSteMarie', 'toronto', 436)
addpath('seattle', 'vancouver', 115)
addpath('thunderBay', 'winnipeg', 440)

city("albanyGA",        31.58,  84.17)
city("albanyNY",        42.66,  73.78)
city("albuquerque",     35.11, 106.61)
city("atlanta",         33.76,  84.40)
city("augusta",         33.43,  82.02)
city("austin",          30.30,  97.75)
city("bakersfield",     35.36, 119.03)
city("baltimore",       39.31,  76.62)
city("batonRouge",      30.46,  91.14)
city("beaumont",        30.08,  94.13)
city("boise",           43.61, 116.24)
city("boston",          42.32,  71.09)
city("buffalo",         42.90,  78.85)
city("calgary",         51.00, 114.00)
city("charlotte",       35.21,  80.83)
city("chattanooga",     35.05,  85.27)
city("chicago",         41.84,  87.68)
city("cincinnati",      39.14,  84.50)
city("cleveland",       41.48,  81.67)
city("coloradoSprings", 38.86, 104.79)
city("columbus",        39.99,  82.99)
city("dallas",          32.80,  96.79)
city("dayton",          39.76,  84.20)
city("daytonaBeach",    29.21,  81.04)
city("denver",          39.73, 104.97)
city("desMoines",       41.59,  93.62)
city("elPaso",          31.79, 106.42)
city("eugene",          44.06, 123.11)
city("europe",          48.87,  -2.33)
city("ftWorth",         32.74,  97.33)
city("fresno",          36.78, 119.79)
city("grandJunction",   39.08, 108.56)
city("greenBay",        44.51,  88.02)
city("greensboro",      36.08,  79.82)
city("houston",         29.76,  95.38)
city("indianapolis",    39.79,  86.15)
city("jacksonville",    30.32,  81.66)
city("japan",           35.68, 220.23)
city("kansasCity",      39.08,  94.56)
city("keyWest",         24.56,  81.78)
city("lafayette",       30.21,  92.03)
city("lakeCity",        30.19,  82.64)
city("laredo",          27.52,  99.49)
city("lasVegas",        36.19, 115.22)
city("lincoln",         40.81,  96.68)
city("littleRock",      34.74,  92.33)
city("losAngeles",      34.03, 118.17)
city("macon",           32.83,  83.65)
city("medford",         42.33, 122.86)
city("memphis",         35.12,  89.97)
city("mexia",           31.68,  96.48)
city("mexico",          19.40,  99.12)
city("miami",           25.79,  80.22)
city("midland",         43.62,  84.23)
city("milwaukee",       43.05,  87.96)
city("minneapolis",     44.96,  93.27)
city("modesto",         37.66, 120.99)
city("montreal",        45.50,  73.67)
city("nashville",       36.15,  86.76)
city("newHaven",        41.31,  72.92)
city("newOrleans",      29.97,  90.06)
city("newYork",         40.70,  73.92)
city("norfolk",         36.89,  76.26)
city("oakland",         37.80, 122.23)
city("oklahomaCity",    35.48,  97.53)
city("omaha",           41.26,  96.01)
city("orlando",         28.53,  81.38)
city("ottawa",          45.42,  75.69)
city("pensacola",       30.44,  87.21)
city("philadelphia",    40.72,  76.12)
city("phoenix",         33.53, 112.08)
city("pittsburgh",      40.40,  79.84)
city("pointReyes",      38.07, 122.81)
city("portland",        45.52, 122.64)
city("providence",      41.80,  71.36)
city("provo",           40.24, 111.66)
city("raleigh",         35.82,  78.64)
city("redding",         40.58, 122.37)
city("reno",            39.53, 119.82)
city("richmond",        37.54,  77.46)
city("rochester",       43.17,  77.61)
city("sacramento",      38.56, 121.47)
city("salem",           44.93, 123.03)
city("salinas",         36.68, 121.64)
city("saltLakeCity",    40.75, 111.89)
city("sanAntonio",      29.45,  98.51)
city("sanDiego",        32.78, 117.15)
city("sanFrancisco",    37.76, 122.44)
city("sanJose",         37.30, 121.87)
city("sanLuisObispo",   35.27, 120.66)
city("santaFe",         35.67, 105.96)
city("saultSteMarie",   46.49,  84.35)
city("savannah",        32.05,  81.10)
city("seattle",         47.63, 122.33)
city("stLouis",         38.63,  90.24)
city("stamford",        41.07,  73.54)
city("stockton",        37.98, 121.30)
city("tallahassee",     30.45,  84.27)
city("tampa",           27.97,  82.46)
city("thunderBay",      48.38,  89.25)
city("toledo",          41.67,  83.58)
city("toronto",         43.65,  79.38)
city("tucson",          32.21, 110.92)
city("tulsa",           36.13,  95.94)
city("uk1",             51.30,   0.00)
city("uk2",             51.30,   0.00)
city("vancouver",       49.25, 123.10)
city("washington",      38.91,  77.01)
city("westPalmBeach",   26.71,  80.05)
city("wichita",         37.69,  97.34)
city("winnipeg",        49.90,  97.13)
city("yuma",            32.69, 114.62)

source = sys.argv[3]
destination = sys.argv[4]

if source not in adj:
		print(source,"is an Invalid Source")
if destination not in adj:
		print(destination,"is an Invalid Destination")

if sys.argv[1]=="dfs":
	if source in adj and destination in adj:
		obj = depth(adj,roads,source,destination,[source],[source],100000000,0)
		obj.run()

if sys.argv[1]=="A*":
	if source in adj and destination in adj:
		glo = sys.argv[2]
		obj = astar(adj,roads,source,destination,[source],[source],10000000000,glo)
		obj.run()

if sys.argv[1]=="rbfs":
	if source in adj and destination in adj:
		glo = sys.argv[2]
		obj = rbfs(adj,roads,source,destination,[source],[source],10000000000,glo)
		obj.run()