import tree_algorithm

class CPM():
    start_cell = "it is start cell of user"
    end_cell = "it is end cell of user"
    start_expanded_cell_set=set()  #op_cpm에서 셀들을 추가해주고, expand_cell에서 버텍스를 추가한다.
    end_expanded_cell_set=set()    #start와 end를 분리해서 가지고 있어야한다.
    start_op_count=0  #default가 0이다.
    end_op_count=0
    IO_count=0
    cell_size = 0.4

    # condition for cut-off
    start_min_dist_cell = 0
    end_min_dist_cell = 0

    def __init__(self, UserID, query_obj, grid_length, index_table):
        self.user_cell = query_obj.SELECT_cell_num_WHERE_userid(UserID)
        self.user_position = query_obj.SELECT_position_WHERE_userid(UserID)
        self.start_cell = self.user_cell[0]
        self.end_cell = self.user_cell[1]
        self.start_vertex_minheap = tree_algorithm.MinHeap_moving_cost(self.user_position, query_obj)
        self.end_vertex_minheap = tree_algorithm.MinHeap_moving_cost(self.user_position, query_obj)
        self.grid_length = grid_length
        self.index_table = index_table

    def pop(self, start_flag):
        #양수면 정상적으로 return한 상황이고, -1이면 한 번 업데이트해서 vertex가 나오지 않은 경우
        #-2이면 업데이트할 cell이 없는 경우
        if start_flag is True:  #start에서 vertex를 pop하고 싶다면
            if self.start_vertex_minheap.is_empty():
                r = self.expand_cell(start_flag)    #더 이상 추가되는 셀이 없다면 -1을 return한다.
                if r == -1: #더 이상 pop할 cell이 존재하지 않는다.
                    return -2
                if self.start_vertex_minheap.is_empty():
                    return -1   #더 이상 pop할 vertex가 없다면 -1(failure flag)를 return한다.
                return self.start_vertex_minheap.delete()
            else:
                return self.start_vertex_minheap.delete()

        else:   #end에서 vertex를 pop하고 싶다면
            if self.end_vertex_minheap.is_empty():
                r = self.expand_cell(start_flag)
                if r == -1:
                    return -2   #더 이상 pop할 cell이 존재하지 않는다.
                if self.end_vertex_minheap.is_empty():
                    return -1 #더 이상 pop할 vertex가 없다면 -1(failure flag)를 return한다.
                return self.end_vertex_minheap.delete()
            else:
                return self.end_vertex_minheap.delete()

    def expand_cell(self, start_flag):  #여기서 더 이상 pop할 셀이 없다면?? 여기도 처리가 필요하다!
        IO_flag = False

        # cell에 있는 vertex들을 전부 힙에다 삽입한다.
        if start_flag is True:  #start cell updating을 위한 거라면
            update_cell = self.op_cpm_start()   #새로운 셀 추가
            #추가되는 셀이 없다면 -1을 리턴
            if len(update_cell)==0:
                return -1
            self.start_min_dist_cell = self.mindist_user_and_cell(self.user_cell[0], list(update_cell)[0], True)

            for cell in update_cell:
                # self.IO_count = self.IO_count + 1
                for vertex in self.index_table.start_index_info[cell][0]:
                    IO_flag = True
                    self.start_vertex_minheap.insert(vertex)
                if IO_flag == True:
                    self.IO_count = self.IO_count + 1
                    IO_flag = False

                # update start_min_dist_cell
                min_cell_dist=self.mindist_user_and_cell(self.user_cell[0], cell, True)
                if min_cell_dist < self.start_min_dist_cell:
                    self.start_min_dist_cell = min_cell_dist

        else:   #end cell updating을 위한 거라면
            update_cell = self.op_cpm_end()
            # 추가되는 셀이 없다면 -1을 리턴
            if len(update_cell)==0:
                return -1

            self.end_min_dist_cell = self.mindist_user_and_cell(self.user_cell[1], list(update_cell)[0], False)
            for cell in update_cell:
                # self.IO_count = self.IO_count + 1
                for vertex in self.index_table.end_index_info[(cell)][0]:
                    IO_flag = True
                    self.end_vertex_minheap.insert(vertex)
                if IO_flag == True:
                    self.IO_count = self.IO_count + 1
                    IO_flag = False

                # update end_min_dist_cell
                min_cell_dist = self.mindist_user_and_cell(self.user_cell[1], cell, False)
                if min_cell_dist < self.end_min_dist_cell:
                    self.end_min_dist_cell = min_cell_dist

    def op_cpm_start(self):
        #start_cell 집합 채우기
        start_rect_left_x = self.get_max(self.start_cell[0]-1*self.start_op_count)
        start_rect_right_x = self.get_min(self.start_cell[0]+1*self.start_op_count)
        start_rect_below_y = self.get_max(self.start_cell[1]-1*self.start_op_count)
        start_rect_on_y = self.get_min(self.start_cell[1]+1*self.start_op_count)
        new_start_cell =set()
        # print(start_rect_left_x, start_rect_right_x, start_rect_below_y, start_rect_on_y) # for test

        for x in range(start_rect_left_x, start_rect_right_x+1):
            for y in range(start_rect_below_y, start_rect_on_y+1):
                new_start_cell.add((x,y))

        tmp=new_start_cell.difference(self.start_expanded_cell_set)  #새로 추가된 cell들의 집합
        #IO COUNT 새어주기
        self.start_expanded_cell_set = new_start_cell    #처리된 셀들의 집합 업데이트
        self.start_op_count = self.start_op_count+1

        return tmp  #새로 확장해야하는 것을 return한다.

    def op_cpm_end(self):
        #end_cell 집합 채우기
        end_rect_left_x = self.get_max(self.end_cell[0] - 1 * self.end_op_count)
        end_rect_right_x = self.get_min(self.end_cell[0] + 1 * self.end_op_count)
        end_rect_below_y = self.get_max(self.end_cell[1] - 1 * self.end_op_count)
        end_rect_on_y = self.get_min(self.end_cell[1] + 1 * self.end_op_count)
        new_end_cell = set()

        for x in range(end_rect_left_x, end_rect_right_x+1):
            for y in range(end_rect_below_y, end_rect_on_y+1):
                new_end_cell.add((x,y))

        tmp = new_end_cell.difference(self.end_expanded_cell_set)  # 새로 추가된 cell들의 집합
        self.end_expanded_cell_set = new_end_cell  # 처리된 셀들의 집합 업데이트
        self.end_op_count = self.end_op_count + 1

        return tmp  #새로 확장해야 하는 것을 return 한다.

    def get_max(self, a):
        # a가 음수이면 0을 리턴하는 메소드
        if a>=0:
            return a
        return 0

    def get_min(self, b):
        # b가 max를 넘어가면 max를 리턴하는 메소드
        if b <= self.grid_length-1:
            return b
        return int(self.grid_length-1)

    def mindist_user_and_cell(self, user_cell, cell_R, start_flag):
        """
        :param cell_X: ((x1,y1)), self.user_cell : ((x1,y1))
        :return:  minDist: dg(p^d_u, c)-ordered
        """
        equal_x=user_cell[0]==cell_R[0] # were they in same y axis?
        equal_y=user_cell[1]==cell_R[1] # were they in same x axis?
        is_right=user_cell[0]<cell_R[0] # were they in the right direction of user? else is in left direction!
        is_upper=user_cell[1]<cell_R[1] # were they in the right direction of user? else is in below direction!

        if start_flag:
            user_position = self.user_position[0]
        else:
            user_position = self.user_position[1]

        if equal_x:
            if equal_y:
                min_dist=0  # it is in same cell with user
            elif is_upper:
                min_dist=(cell_R[1]*self.cell_size)-user_position[1]
            else:   #is_below
                min_dist=user_position[1]-((cell_R[1]+1)*self.cell_size)
        elif equal_y:
            if is_right:
                min_dist=(cell_R[0]*self.cell_size)-user_position[0]
                #print(cell_R, min_dist)
            else:   #is_left
                min_dist=user_position[0]-((cell_R[0]+1)*self.cell_size)
                #print(cell_R, min_dist)
        elif is_right:
            if is_upper:
                min_dist=self.dist(user_position, (cell_R[0]*self.cell_size, cell_R[1]*self.cell_size))
            else:
                min_dist=self.dist(user_position,(cell_R[0]*self.cell_size,(cell_R[1]+1)*self.cell_size))
        else:   #is_left
            if is_upper:
                min_dist=self.dist(user_position, ((cell_R[0]+1)*self.cell_size, cell_R[1]*self.cell_size))
            else:
                min_dist=self.dist(user_position, ((cell_R[0]+1)*self.cell_size, (cell_R[1]+1)*self.cell_size))
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