import pandas as pd
import numpy as np
df_links = pd.read_csv("links.csv")

import networkx as nx
import matplotlib.pyplot as plt

class Network20():
    def __init__(self):
        self.G = nx.Graph()
        self.NUM = None
        self.node_no = None
        self.node_name = None
        
    def set_points(self,df_links):
        self.NUM = len(df_links.index)
        for i in range(1,self.NUM+1):
            self.node_no = df_links.columns[i].strip("Node")
            self.G.add_node(str(self.node_no))
    
    def set_edges(self,df_links):
        for i in range(self.NUM):
            for j in range(self.NUM):
                self.node_name = "Node"+str(j)
                if df_links[self.node_name].iloc[i]==1:
                    self.G.add_edge(str(i),str(j))
        return self.G
    
    def drawing(self):
        nx.draw_networkx(self.G,node_color="k",edge_color="k",font_color="w")
        plt.show()
      
ne20 = Network20()
ne20.set_points(df_links)
G = ne20.set_edges(df_links)

class KuchikomiSim():
    def __init__(self):
        self.percent_percolation = 0.1
        self.T_NUM = 36
        self.NUM = None
        self.list_active = None
        self.list_timeSeries = []
        self.list_color = []
        self.rand_val = None
        self.NUM = 0
        self.list_active = None
    
    def set_NUM(self,df_links):
        self.NUM = len(df_links.index)
        self.list_active = np.zeros(self.NUM)
        self.list_active[0] = 1
        
    def determine_link(self):
        self.rand_val = np.random.rand()
        if self.rand_val<=self.percent_percolation:
            return 1
        else:
            return 0
    
    def simulate_percolation(self,df_links):
        for i in range(self.NUM):
            if self.list_active[i]==1:
                for j in range(self.NUM):
                    node_name = "Node" + str(j)
                    if df_links[node_name].iloc[i]==1:
                        if KuchikomiSim.determine_link(self)==1:
                            self.list_active[j] = 1
    
    def make_timeSeries(self,df_links):
        for i in range(self.T_NUM):
            self.list_active = KuchikomiSim.simulate_percolation(self,df_links)
            self.list_timeSeries.append(self.list_active.copy())
            
    def active_node_coloring(self,t):
        for i in range(len(self.list_timeSeries[t])):
            if self.list_timeSeries[t][i]==1:
                self.list_color.append("r")
            else:
                self.list_color.append("k")
                
    def drawing(self,t,G):
        nx.draw_networkx(G,font_color="w",node_color=KuchikomiSim.active_node_coloring(self,t))
        plt.show()

t = [0,11,35]
KS = KuchikomiSim()
KS.set_NUM(df_links)
KS.simulate_percolation(df_links)
KS.make_timeSeries(df_links)
for i in range(len(t)):
    KS.active_node_coloring(t[i])
    KS.drawing(t[i],G)
