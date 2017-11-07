from gurobipy import *

class VRPsolve():
    def __init__(self,dist,demand,capacity,sites,clients,siteNames):
        self.dist = dist
        self.demand = demand
        self.capacity = capacity
        self.sites = sites
        self.clients = clients
        self.siteNames = siteNames
    def run(self):    
        dist = self.dist
        demand = self.demand
        capacity = self.capacity
        sites = self.sites
        clients = self.clients
        siteNames = self.siteNames
        model = Model('Diesel Fuel Delivery')
        x = {}
        arcs = []
        routes = {}
        for i in sites:
            for j in sites:
                x[i,j] = model.addVar(vtype=GRB.BINARY,name="routes")
                
                arcs.append((i,j))

        u = {}
        quant = {}
        us = []
        for i in clients:
            u[i] = model.addVar(lb=demand[i], ub=capacity)
            us.append(i)
            quant[i] = demand[i]

        model.update()

        model.setObjective(quicksum(dist[i][j]*x[i,j] for i in sites for j in sites if i != j),GRB.MINIMIZE)

        thesum = 0
        for j in clients:
            model.addConstr(quicksum( x[i,j] for i in sites if i != j ) == 1)
            
        for i in clients:
            model.addConstr(quicksum( x[i,j] for j in sites if i != j ) == 1)

        for i in clients:
            model.addConstr(u[i] <= capacity + (demand[i] - capacity)*x[0,i])
##            model.addConstr(u[i] == capacity + (demand[i] - capacity)*x[0,i])

        for i in clients:
            for j in clients:
                if i != j:
                    model.addConstr(u[i] - u[j] + capacity*x[i,j] <= capacity - quant[j])

        model.setParam('OutputFlag',False)
        model.optimize()
        # Print Solution
        if model.status == GRB.Status.OPTIMAL:
            solution = model.getAttr('x')
            arcsol = []
            for i in range(0,len(solution),1):
                if solution[i] == 1:
        ##            print arcs[i] , " : ", solution[i]
                    arcsol.append(arcs[i])

        TheRoute = arcsol
        FirstRoutes = {}
        for arc in TheRoute:
            if arc[0] == 0:
                depot = arc[0]
                firstdest = arc[1]
                FirstRoutes[(depot,firstdest)]= []

        for firstarc in FirstRoutes.keys():
            for arc in TheRoute:
                if arc not in FirstRoutes[firstarc]:
                    if arc[0] == firstarc[1]:
                        FirstRoutes[firstarc].append(arc)
                        

        for firstarc in FirstRoutes.keys():
            for arc in TheRoute:
                if arc not in FirstRoutes[firstarc]:
                    next_arc = FirstRoutes[firstarc][-1][1]
                    if arc[0] == next_arc and arc[0] != 0:
                        FirstRoutes[firstarc].append(arc)

        for firstarc in FirstRoutes.keys():
            for arc in TheRoute:
                if arc not in FirstRoutes[firstarc]:
                    next_arc = FirstRoutes[firstarc][-1][1]
                    if arc[0] == next_arc and arc[0] != 0:
                        FirstRoutes[firstarc].append(arc)
        count = 1
        for firstarc in FirstRoutes:
            print "------------"
            print "Bus " + str(count) + " Route"
            print "------------"
            count +=1
            total_picked_up = 0
            distance_traveled = dist[firstarc[0]][firstarc[1]]
            routelist = FirstRoutes[firstarc]
            print siteNames[firstarc[0]],
            for arc in routelist:
                distance_traveled += dist[arc[0]][arc[1]]
                total_picked_up += demand[arc[0]]
                print " -> " + siteNames[arc[0]],
            print " -> " + siteNames[0]
            print "Number Picked Up: " + str(total_picked_up)
            print "Distance Traveled: " + str(distance_traveled)
if __name__ == "__main__":
    siteNames = ["Reno", "South Lake Tahoe", "Carson City", "Garnerville",
                  "Fernerly", "Tahoe City", "Incline Village", "Truckee"]
    sites = range(len(siteNames))
    clients = sites[1:]
    print "THE LENGTH OF CLIENTS: " + str(len(clients))
    demand = [ 0,1000, 1200, 1600, 1400, 1200, 1000, 1700]
    demandsum = 0
    for i in demand:
        demandsum += i
    print "THE DEMAND SUM IS: " + str(demandsum)
    dist = [[0, 59.3, 31.6, 47.8, 34.2, 47.1, 36.1, 31.9],
            [62.2, 0, 27.9, 21.0, 77.5, 30.0, 27.1, 44.7],
            [32.2, 27.7, 0, 16.2, 50.0, 39.4, 24.9, 42.6],
            [50.7, 21.0, 16.4, 0, 66.1, 49.7, 35.2, 52.9],
            [34.4, 77.4, 49.6, 65.9, 0, 80.8, 67.1, 65.5],
            [46.9, 30.1, 39.6, 49.7, 80.5, 0, 14.4, 15.0],
            [36.9, 27.1, 25.2, 35.2, 67.1, 14.4, 0, 17.6],
            [31.9, 44.7, 62.8, 52.8, 65.6, 15.0, 17.6, 0]]


    capacity = 5000 
    #execute the function
    vrpsolve = VRPsolve(dist,demand,capacity).run()
