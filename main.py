import numpy as np
import random
import itertools
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
class Point:
    id_count = 0
    def __init__(self, x, y, z):

        self.id=Point.id_count
        self.x = x
        self.y = y
        self.z = z
        self.conflict={}
        Point.id_count += 1

    def __str__(self):
        return f"(id:{self.id}({self.x},{self.y},{self.z}))"
class Edge:
    id_count = 0
    def __init__(self, p0, p1):
        self.id = f'{p0}{p1}'
        self.p0 = p0
        self.p1 = p1
        self.facets={}
        Edge.id_count += 1

    def __str__(self):
        return f"(id:{self.id}({self.p0},{self.p1}) facets:{self.facets})"

class Facet:
    id_count =0
    def __init__(self, p0, p1, p2,edges_dict):#need to check maybe to order p0 p1 p2 clockwise!
        self.id=Facet.id_count
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.alive=True
        Facet.id_count+=1

        if not edges_dict.__contains__(f'{p0}{p1}') and not edges_dict.__contains__(f'{p1}{p0}'):
            edges_dict[f'{p0}{p1}']=Edge(p0,p1)
            e1=f'{p0}{p1}'
        elif edges_dict.__contains__(f'{p0}{p1}'):
            e1=f'{p0}{p1}'
        elif edges_dict.__contains__(f'{p1}{p0}'):
            e1=f'{p1}{p0}'


        if not edges_dict.__contains__(f'{p0}{p2}') and not edges_dict.__contains__(f'{p2}{p0}'):
            edges_dict[f'{p0}{p2}']=Edge(p0,p2)
            e2=f'{p0}{p2}'
        elif edges_dict.__contains__(f'{p0}{p2}'):
            e2=f'{p0}{p2}'
        elif edges_dict.__contains__(f'{p2}{p0}'):
            e2=f'{p2}{p0}'


        if not edges_dict.__contains__(f'{p1}{p2}') and not edges_dict.__contains__(f'{p2}{p1}'):
            edges_dict[f'{p1}{p2}']=Edge(p1,p2)
            e3=f'{p1}{p2}'
        elif edges_dict.__contains__(f'{p1}{p2}'):
            e3=f'{p1}{p2}'
        elif edges_dict.__contains__(f'{p2}{p1}'):
            e3=f'{p2}{p1}'

        self.edges=[e1,e2,e3]
        for e in self.edges:
            edges_dict[e].facets[self.id]=self.id
        self.conflict={}
        self.neighbors={}
    def destroy(self,edges_dict,points_dict):
        #self.alive=False
        # for e in self.edges:
        #     edges_dict[e].facets.pop(self.id)
        for p in self.conflict:
           points_dict[p].conflict.pop(self.id)

    def __str__(self):
        return f"(id:{self.id}({self.p0},{self.p1},{self.p2}))"
def plot(edges_dict,points_dict):
    plt.axes(projection='3d')

    for e in edges_dict:
        p1=edges_dict[e].p0
        p2=edges_dict[e].p1

        x = [p1.x, p2.x]
        y = [p1.y, p2.y]
        z = [p1.z, p2.z]

        plt.plot(x, y, z, 'r', linewidth=2)

    for p in points_dict:
        x=points_dict[p].x
        y=points_dict[p].y
        z=points_dict[p].z
        xx=[x,x+0.1]
        yy=[y,y+0.1]
        zz=[z,z+0.1]

        plt.plot(xx, yy, zz, 'b', linewidth=3)




    plt.title('Polygon')
    plt.show()
def points_equal(p1,p2):
    if p1.x!=p2.x:
        return False
    if p1.y != p2.y:
        return False
    if p1.z != p2.z:
        return False
    return True

def read_points(file):
    points=[]
    with open(file, 'r') as f:
        n = int(f.readline())
        #reading the points
        for i in range(n):
            x,y,z=f.readline().split()
            p=Point(int(x),int(y), int(z))
            points.append(p)
    return points

def findsubsets(s, n):
    return list(itertools.combinations(s, n))

def generate_unique_random_list(n): #return a random order of the points
    #n=len(points)
    #new_order={}
    permutation=random.sample(range(n), n)
    # for i in range(n):
    #     new_order[i]=points[permutation[i]]
    return permutation

def fix_face(face):#the vertices of each face should be listed in clockwise order when viewed from outside
    v=[face.p0.id,face.p1.id,face.p2.id]

    idx_first=v.index(min(v))
    return [v[idx_first],v[(idx_first+1)%3],v[(idx_first+2)%3]]

def fix_output(facets):
    fixed_facets=[]
    for face in facets:
        fixed_facets.append(fix_face(face))
    return sorted(fixed_facets)
def define_order(p1,p2,p3,points_till_now_dict):
    points=[p1,p2,p3]
    d=None
    for p in points_till_now_dict:
        if not points_equal(p1,points_till_now_dict[p]) and not points_equal(p2,points_till_now_dict[p]) and not points_equal(p3,points_till_now_dict[p]):
            d=points_till_now_dict[p]
            break
    combinations=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,1,0],[2,0,1]]
    c=[]
    for comb in combinations:
        cc=comb
        p1_temp=points[comb[0]]
        p2_temp=points[comb[1]]
        p3_temp=points[comb[2]]
        m = [[1, 1, 1, 1], [p1_temp.x, p2_temp.x, p3_temp.x, d.x], [p1_temp.y, p2_temp.y, p3_temp.y, d.y], [p1_temp.z, p2_temp.z, p3_temp.z, d.z]]
        det=np.linalg.det(m)
        if det>0:
            c=comb
            break
    print('hi')
    return points[c[0]],points[c[1]],points[c[2]]


def clockwise(p1,p2,p3,d):
    m=[[1, 1, 1, 1], [p1.x, p2.x, p3.x, d.x], [p1.y, p2.y, p3.y, d.y], [p1.z, p2.z, p3.z, d.z]]
    det=np.linalg.det(m)
    if det==0:
        print('det ===========0')
    if det<0:
        return -1 # clockwise
    else:
        return 1 #counter clockwise


def convex_hull(file):
    points = read_points(file)
    Q = list(range(len(points)))#generate_unique_random_list(len(points)) #ids of points not yet inserted
    facets_dict = {}
    points_dict = {}
    edges_dict = {}
    points_till_now_dict={}
    for i in range(len(points)):
        points_dict[points[i].id]=points[i]

    q0 = points_dict[Q.pop()]
    q1 = points_dict[Q.pop()]
    q2 = points_dict[Q.pop()]
    q3 = points_dict[Q.pop()]
    points_till_now_dict[q0.id]=q0
    points_till_now_dict[q1.id]=q1
    points_till_now_dict[q2.id]=q2
    points_till_now_dict[q3.id]=q3

    s={q0,q1,q2,q3}
    subsets_of_3=findsubsets(s,3)
    for sub in subsets_of_3:
        p1,p2,p3=define_order(sub[0],sub[1],sub[2],points_till_now_dict)
        facet=Facet(p1,p2,p3,edges_dict)
        facets_dict[facet.id]=facet

    while len(Q)>0:
        new_point=points_dict[Q.pop()]
        points_till_now_dict[new_point.id]=new_point
        for f in facets_dict:
            temp_facet=facets_dict[f]
            if clockwise(temp_facet.p0,temp_facet.p1,temp_facet.p2,new_point)==-1:
                temp_facet.conflict[new_point.id]=True
                new_point.conflict[temp_facet.id]=True
        if len(new_point.conflict)>0:
            horizon_edges=[]
            destroy={}
            for face in new_point.conflict:
                for e in facets_dict[face].edges:
                    wing=[]
                    if e=='(id:45(32,9,292))(id:36(240,45,36))':
                        print('debug')
                    for facet_in_wing in edges_dict[e].facets:
                        wing.append(facet_in_wing)
                    f1=facets_dict[wing[0]]
                    f2=facets_dict[wing[1]]
                    c1=clockwise(f1.p0,f1.p1,f1.p2,new_point)
                    c2=clockwise(f2.p0,f2.p1,f2.p2,new_point)
                    if c1!=c2:
                        if not horizon_edges.__contains__(e):
                            horizon_edges.append(e)
                        destroy[face]=True
            if new_point.id == 35: #debug
                print('h')
                plot(edges_dict, points_till_now_dict)
            #plot(edges_dict, points_till_now_dict)
            #destroy2=destroy
            for f in destroy:
                for e in facets_dict[f].edges:

                    if not horizon_edges.__contains__(e):
                        if edges_dict.__contains__(e):
                            edges_dict.pop(e)
                    else:
                        edges_dict[e].facets.pop(f)
                    if new_point.id == 35:
                        print('h')
                        plot(edges_dict, points_till_now_dict)

                facets_dict[f].destroy(edges_dict, points_dict)
                facets_dict.pop(f)
            for e in horizon_edges:
                e_temp=edges_dict[e]
                p1, p2, p3 = define_order(e_temp.p0,e_temp.p1,new_point, points_till_now_dict)
                new_facet=Facet(p1,p2,p3,edges_dict)
                facets_dict[new_facet.id]=new_facet
        plot(edges_dict, points_till_now_dict)
        print(new_point)

    final_facets=[]
    for f in facets_dict:
        final_facets.append(facets_dict[f])
    fixed_output=fix_output(final_facets)
    return fixed_output














if __name__ == '__main__':
    file='sampleinput.txt'
    # points=read_points('sampleinput.txt')
    # facets=[[3,4,5],[8,7,6],[4,2,5],[2,3,4]]
    # print(facets.pop())
    # print(facets)
    # p=Point(1,1,1)
    # p1=Point(2,2,2)
    # p2=Point(3,3,3)
    # p3=Point(4,4,4)
    # d=Point(5,5,5)


    # p.conflict.append(f)
    # print(f)
    # #p.conflict[0].p0=d
    # print(f2)
    #convex_hull(file)
    # e={}
    # f=Facet(p1,p2,p3,e)
    # f2 = Facet(p1, p2, d, e)
    # print()



    out=convex_hull(file)
    # print(out)






