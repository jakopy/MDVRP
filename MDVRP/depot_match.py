from gurobipy import *

class depot_matcher():
    def __init__(self,siteNames,depot_list,dist):
        self.siteNames=siteNames
        self.depot_list = depot_list
        self.dist = dist
    def run(self,match_type,depot_capacity):
        siteNames = self.siteNames
        depot_list = self.depot_list
        dist = self.dist
        depot_index = []
        node_index = []

        #index through site names and build the depot and node indexes        
        for j in siteNames:
            if j in depot_list:
                depot_index.append(siteNames.index(j))
            else:
                node_index.append(siteNames.index(j))

        #name the model
        model = Model('Depot Matcher')

        #initiate x, depot distance matrix and set of all arcs
        x={}
        depot_dist = {}
        arcs = []
        
        #build the depot distance matrix and the decision variable (x)
        for depot in depot_index:
            depot_dist[depot]={}
            for node in node_index:
                x[depot,node] = model.addVar(vtype=GRB.BINARY,name="match_arcs")
                depot_dist[depot][node]=dist[depot][node]
                arcs.append([depot,node])

        #Set The Model Objective
        model.setObjective(quicksum(depot_dist[i][j]*x[i,j] for i in depot_index for j in node_index),GRB.MINIMIZE)

        #Constraint "All nodes must be serviced by a depot"
        for node in node_index:
            model.addConstr(quicksum( x[depot,node] for depot in depot_index) == 1)

        #Depot Match Types (if needed)
        #require nodes be split evenly among depots
        if match_type == "split_even":
            #initiate depot capacity
            depot_capacity = {}
            
            #build depot capacity
            for i in range(0,len(depot_index),1):
                depot_capacity[depot_index[i]] = len(node_index)/len(depot_index)

            #build depot capacity continued
            remainder = len(node_index)%len(depot_index)
            if len(node_index)%len(depot_index) != 0:
                for i in range(0,remainder,1):
                    depot_capacity[i] += 1

            #add the constraint
            for depot in depot_index:
                model.addConstr(quicksum( x[depot,node] for node in node_index) <= depot_capacity[depot])

        #require a capacity specified
        if match_type == "cs":
            for depot in depot_index:
                model.addConstr(quicksum( x[depot,node] for node in node_index) <= depot_capacity[depot])

        #Tell Gurobi to Optimize the Model
        model.setParam('OutputFlag',False)
        model.optimize()

        #Return The Solution (Depots Matched List)
        depots_matched = {}
        if model.status == GRB.Status.OPTIMAL:
            solution = model.getAttr('x')
            for i in range(0,len(solution),1):
                if solution[i] == 1:
                    if arcs[i][0] not in depots_matched.keys():
                        depots_matched[arcs[i][0]]=[arcs[i][1]]
                    else:
                        depots_matched[arcs[i][0]].append(arcs[i][1])
                        
        return depots_matched

if __name__ == "__main__":
    siteNames = ["Reno", "South Lake Tahoe", "Carson City", "Garnerville",
                  "Fernerly", "Tahoe City", "Incline Village", "Truckee"]
    sites = range(len(siteNames))
    clients = sites[1:]
    demand = [ 0,1000, 1200, 1600, 1400, 1200, 1000, 1700]
    demandsum = 0
    for i in demand:
        demandsum += i
            #"Reno", "South Lake Tahoe", "Carson City", "Garnerville", "Fernerly", "Tahoe City", "Incline Village", "Truckee"
    dist = [[0,       59.3,               31.6,         47.8,          34.2,       47.1,          36.1,              31.9], #Reno
            [62.2,    0,                  27.9,         21.0,          77.5,       30.0,          27.1,              44.7], #South Lake Tahoe
            [32.2, 27.7, 0, 16.2, 50.0, 39.4, 24.9, 42.6], #Carson City
            [50.7, 21.0, 16.4, 0, 66.1, 49.7, 35.2, 52.9], #Garnerville
            [34.4, 77.4, 49.6, 65.9, 0, 80.8, 67.1, 65.5], #Fernerly
            [46.9, 30.1, 39.6, 49.7, 80.5, 0, 14.4, 15.0], #Tahoe City
            [36.9, 27.1, 25.2, 35.2, 67.1, 14.4, 0, 17.6], #Incline Village
            [31.9, 44.7, 62.8, 52.8, 65.6, 15.0, 17.6, 0]] #Truckee

    capacity = 5000
    depot_list = ["Reno","South Lake Tahoe"]
    match_type = "split_even"
    depot_capacity = None
    
    #execute the function
    depots_matched = depot_matcher(siteNames,depot_list,dist).run(match_type,depot_capacity)
    print depots_matched
