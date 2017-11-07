siteNames = ["Reno", "South Lake Tahoe", "Carson City", "Garnerville",
             "Fernerly", "Tahoe City", "Incline Village","bus stop 1","bus stop 2","bus stop 3","Truckee"]

depot_list = ["Reno","South Lake Tahoe", "Carson City", "Garnerville"]

depot_capacity = {}

depot_index = []
node_index = []

for j in siteNames:
    if j in depot_list:
        depot_index.append(siteNames.index(j))
    else:
        node_index.append(siteNames.index(j))



print len(node_index)/len(depot_index)
print node_index
print depot_index

for i in range(0,len(depot_index),1):
    print depot_index[i]
    depot_capacity[depot_index[i]] = len(node_index)/len(depot_index)

remainder = len(node_index)%len(depot_index)

if len(node_index)%len(depot_index) != 0:
    for i in range(0,remainder,1):
        depot_capacity[i] += 1
print depot_capacity

##counter = 0
##for depot in depot_index:
##    if len(node_index)/len(depot_index) % 2 == 0:
##        model.addConstr(quicksum( x[depot,node] for node in node_index) <= len(node_index)/len(depot_index))
##    else:
##        if counter == 0:
##            model.addConstr(quicksum( x[depot,node] for node in node_index) <= len(node_index)/len(depot_index)+1)
##        else:
##            model.addConstr(quicksum( x[depot,node] for node in node_index) <= int(len(node_index)/len(depot_index)))
##        counter+=1
