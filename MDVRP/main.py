from gurobi_vrp import *
from gurobipy import *

###########
# THE DATA
###########
siteNames = ["Reno", "South Lake Tahoe", "Carson City", "Garnerville",
              "Fernerly", "Tahoe City", "Incline Village", "Truckee"]

depot_list = ["Reno","South Lake Tahoe"]#,"South Lake Tahoe"]

capacity = 5000 

demand = [ 0,0, 1200, 1600, 1400, 1200, 1000, 1700]

dist = [[0, 59.3, 31.6, 47.8, 34.2, 47.1, 36.1, 31.9],   #RENO
        [62.2, 0, 27.9, 21.0, 77.5, 30.0, 27.1, 44.7],   #South Lake Tahoe
        [32.2, 27.7, 0, 16.2, 50.0, 39.4, 24.9, 42.6],   #Carson
        [50.7, 21.0, 16.4, 0, 66.1, 49.7, 35.2, 52.9],   #Garnerville
        [34.4, 77.4, 49.6, 65.9, 0, 80.8, 67.1, 65.5],   #Fenerly
        [46.9, 30.1, 39.6, 49.7, 80.5, 0, 14.4, 15.0],   #Tahoe City
        [36.9, 27.1, 25.2, 35.2, 67.1, 14.4, 0, 17.6],   #Incline Village
        [31.9, 44.7, 62.8, 52.8, 65.6, 15.0, 17.6, 0]]   #Truckee

depot_capacity = {"Reno":1,"South Lake Tahoe":5}
dc = {}
for i in depot_capacity:
    dc[siteNames.index(i)] = depot_capacity[i]

#optimally split nodes on depots evenly
##match_type = "split even"
##depot_capacity_list = None

#optimally split nodes on depots with a capacity specified
match_type = "cs"
depot_capacity_list = dc

#optimally split on nodes closest to depot
match_type = ""
depot_capacity_list = None

##############
# SOLVE MDVRP
##############

#Depot Match Algo
from depot_match import depot_matcher
depots_matched = depot_matcher(siteNames,depot_list,dist).run(match_type,depot_capacity_list)

print depots_matched

#Solve Sub VRP Problems
solution_list = []
sub_prob_count = 0
for depot in depots_matched:
    depot
    nodes = depots_matched[depot]
    sub_prob = [depot] + nodes
    sub_dist = []
    sub_siteNames = []
    sub_demand = []
    counter = -1
    for i in sub_prob:
        sub_dist.append([])
        sub_siteNames.append(siteNames[i])
        sub_demand.append(demand[i])
        counter +=1
        for j in sub_prob:
            sub_dist[counter].append(dist[i][j])
    sub_sites = range(len(sub_siteNames))
    sub_clients = sub_sites[1:]

##    print sub_prob
##    print sub_siteNames
##    print sub_demand
##    print sub_sites
##    print sub_clients
##    print sub_dist
##    print "------------------"


#execute the function
    sub_prob_count+=1
    print "================================================"
    print "THE VRP SOLUTION FOR DEPOT NAME: " + siteNames[depot]
    print "================================================"
    VRPsolve(sub_dist,sub_demand,capacity,sub_sites,sub_clients,sub_siteNames).run()
    print "\n"
