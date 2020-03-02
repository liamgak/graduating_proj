import parse_dataset_file
import query_npdata
import copy
from heapq import heappush, heappop, heapify

class AlgorithmForTree():
    def __init__(self, friends_list_inmemory):
        self.friends_list_inmemory = friends_list_inmemory

    def bf_travelsal_friend(self, userID, hop):
        """
        클래스명, 메소드명 바꿔야 함
        :param userID:
        :param hop:
        :return: A set of friends list of n-hop
        """
        #init
        one_hop_list= copy.copy(self.friends_list_inmemory.one_parse_row_friends(userID)) # list of Integer
        result_list = set(one_hop_list) #cumulative
        next_hop_list=[]

        #traverse
        if hop > 1 :
            for i in range(hop-1):
                # jump into next hop
                while len(one_hop_list)!=0:
                    # insert the vertecies of one hop
                    x=one_hop_list.pop(0)
                    y=copy.copy(self.friends_list_inmemory.one_parse_row_friends(x))
                    next_hop_list.extend(y)     # expaned friends list
                next_hop_list=set(next_hop_list)    # 한번에 전부 추가한 다음 중복을 제거하는 과정
                #one_hop_list = next_hop_list.difference(result_list)# 수정전
                result_list=result_list.union(next_hop_list)
                one_hop_list = list(next_hop_list) #수정전
                next_hop_list=[]
        return result_list

class MinHeap():
    """
    Min Priority Queue: https://smlee729.github.io/python/data%20structure/2015/03/04/1-heap.html
    """
    heap=[]

    query_obj=query_npdata.QueryDatabase()
    query_obj="query_npdata instance"
    user_cell="querying user"
    user_position = "position of querying user"
    cell_size="cell size"

    def __init__(self, user_cell, user_position, cell_size):
        self.heap = [None]
        self.heap_size=0
        #self.user_cell=self.query_obj.SELECT_cell_num_WHERE_userid(UserID)
        self.user_cell = user_cell
        self.user_position= user_position
        self.cell_size=cell_size

    def insert(self, cell):
        self.heap.append(cell)
        i=len(self.heap)-1
        while i>1:
            parent=i//2
            if self.metric_for_cell_dist(self.heap[parent], cell):
                self.heap[i],self.heap[parent]=self.heap[parent],self.heap[i]
                i=parent
            else:
                break

    def delete(self):
        # removing phase
        i=len(self.heap)-1
        self.heap[1], self.heap[i] = self.heap[i], self.heap[1]
        return_value = self.heap[i]
        self.heap.pop(i)

        # heapifying pase
        self.min_heapify(1)
        return return_value

    def min_heapify(self, i):
        left=i*2
        right=i*2+1
        smallest=i
        if left<=len(self.heap)-1 and self.metric_for_cell_dist(self.heap[smallest], self.heap[left]):
            smallest=left
        if right<=len(self.heap)-1 and self.metric_for_cell_dist(self.heap[smallest], self.heap[right]):
            smallest=right
        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self.min_heapify(smallest)

    def is_empty(self):
        if len(self.heap)==1:
            return True
        return False

    def metric_for_cell_dist(self, cell_A, cell_B):
        """
        cell_<index>=((x1,y1))
        :return: if cell_A is closer to User,then return true. else, return false.
        """
        #measure the distance between user_cell and each cell
        dist_A = self.mindist_user_and_cell(cell_A)
        dist_B = self.mindist_user_and_cell(cell_B)
        if dist_A>=dist_B:
            return True
        else:
            return False

    def mindist_user_and_cell(self, cell_R):
        """
        :param cell_X: ((x1,y1)), self.user_cell : ((x1,y1))
        :return:  minDist: dg(p^d_u, c)-ordered
        """
        equal_x=self.user_cell[0]==cell_R[0] # were they in same y axis?
        equal_y=self.user_cell[1]==cell_R[1] # were they in same x axis?
        is_right=self.user_cell[0]<cell_R[0] # were they in the right direction of user? else is in left direction!
        is_upper=self.user_cell[1]<cell_R[1] # were they in the right direction of user? else is in below direction!
        if equal_x:
            if equal_y:
                min_dist=0  # it is in same cell with user
            elif is_upper:
                min_dist=(cell_R[1]*self.cell_size)-self.user_position[1]
            else:   #is_below
                min_dist=self.user_position[1]-((cell_R[1]+1)*self.cell_size)
                #print(cell_R, min_dist)
        elif equal_y:
            if is_right:
                min_dist=(cell_R[0]*self.cell_size)-self.user_position[0]
                #print(cell_R, min_dist)
            else:   #is_left
                min_dist=self.user_position[0]-((cell_R[0]+1)*self.cell_size)
                #print(cell_R, min_dist)
        elif is_right:
            if is_upper:
                min_dist=self.dist(self.user_position, (cell_R[0]*self.cell_size, cell_R[1]*self.cell_size))
            else:
                min_dist=self.dist(self.user_position,(cell_R[0]*self.cell_size,(cell_R[1]+1)*self.cell_size))
        else:   #is_left
            if is_upper:
                min_dist=self.dist(self.user_position, ((cell_R[0]+1)*self.cell_size, cell_R[1]*self.cell_size))
            else:
                min_dist=self.dist(self.user_position, ((cell_R[0]+1)*self.cell_size, (cell_R[1]+1)*self.cell_size))
        return min_dist

    def dist(self, p1, p2):
        """
        :param p1: the first point
        :param p2: the second point
        :return:
        """
        square_diff_x=(p1[0]-p2[0])**2
        square_diff_y=(p1[1]-p2[1])**2
        distance=(square_diff_x+square_diff_y)**(float(1)/2)
        return distance

class MinHeap_moving_cost():
    """
    Min Priority Queue: https://smlee729.github.io/python/data%20structure/2015/03/04/1-heap.html
    """
    heap=[]

    query_obj=query_npdata.QueryDatabase()
    query_obj="query_npdata instance"
    user_position = "position of querying user"

    def __init__(self, user_position, query_obj):
        self.heap = [None]
        self.heap_size=0
        self.user_position= user_position
        self.query_obj=query_obj

    def insert(self, vertex):
        self.heap.append(vertex)
        i=len(self.heap)-1
        while i>1:
            parent=i//2
            if self.metric_for_moving_cost(self.heap[parent], vertex):
                self.heap[i],self.heap[parent]=self.heap[parent],self.heap[i]
                i=parent
            else:
                break

    def delete(self):
        # removing phase
        i=len(self.heap)-1
        self.heap[1], self.heap[i] = self.heap[i], self.heap[1]
        return_value = self.heap[i]
        self.heap.pop(i)

        # heapifying pase
        self.min_heapify(1)
        return return_value

    def min_heapify(self, i):
        left=i*2
        right=i*2+1
        smallest=i
        if left<=len(self.heap)-1 and self.metric_for_moving_cost(self.heap[smallest], self.heap[left]):
            smallest=left
        if right<=len(self.heap)-1 and self.metric_for_moving_cost(self.heap[smallest], self.heap[right]):
            smallest=right
        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self.min_heapify(smallest)

    def metric_for_moving_cost(self, vertex1, vertex2):
        vertex1_position = self.query_obj.SELECT_position_WHERE_userid(vertex1)
        vertex2_position = self.query_obj.SELECT_position_WHERE_userid(vertex2)
        mc_vertex1=self.moving_cost(vertex1_position)
        mc_vertex2=self.moving_cost(vertex2_position)

        if mc_vertex1>mc_vertex2:
            return True
        return False

    def moving_cost(self, vertex_position):
        # CODE FOR TEST
        # print("1"+str(user_position))
        # print("2"+str(vertex_position))
        mc_1=self.dist(self.user_position[0], vertex_position[0])
        mc_2=self.dist(self.user_position[1], vertex_position[1])
        mc=mc_1+mc_2
        return mc

    def dist(self, p1, p2):
        """ this method is from tree_algorithm module
        :param p1: the first point
        :param p2: the second point
        :return:
        """
        square_diff_x=(p1[0]-p2[0])**2
        square_diff_y=(p1[1]-p2[1])**2
        distance=(square_diff_x+square_diff_y)**(float(1)/2)
        return distance

    def is_empty(self):
        if len(self.heap)==1:
            return True
        return False


# CODE FOR tesing travelsnig freind
#_a=AlgorithmForTree()
#_a.bf_travelsal_friend(200,2)

# CODE FOR