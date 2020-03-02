import numpy as np
import tree_algorithm
import os
import calc_stat_data

class IndexDatabase():
    # Constant
    MIN_LAT=0
    MIN_LON=0
    MAX_LAT=100
    MAX_LON=100

    file_name_csv="" # file having csv extension
    data_matrix="numpy matrix which has full data"
    cell_length=10
    num_of_cell=0   # changed by __index_loc_

    CS = set()
    VH = set()

    # Indexed data
    start_index_info=dict()
    end_index_info=dict()
    depart_inverted_time_table = dict() # first index: cell-ID, second index: time
    arrival_inverted_time_table = dict()

    def __init__(self, file_name, length_of_cell):
        # check whether file has csv extension.
        if file_name.split('.')[1] == "csv" or file_name.split('.')[1] =="txt":
            self.file_name_csv=file_name
            self.data_matrix = self.__spatio_to_numpy()
            self.num_of_cell = int(self.MAX_LAT / length_of_cell)

            index_file_name=self.get_index_file_name()
            path="./index_file/"
            file_list=os.listdir(path)
            if index_file_name in file_list:
                print("[indexor] there is a index file. So, I read that.")
                (self.start_index_info, self.end_index_info)=self.read_index_file() #인덱스 파일이 존재한다면, 인덱스 파일을 읽어 온다.
            else:
                print("[indexor] there is no index file. So, Indexing..")
                (self.start_index_info, self.end_index_info)=self.__index_loc_(length_of_cell)
                print("[indexor] indexing completed")
                print("[indexor] i am writing index files"+index_file_name)
                self.write_index_file() #없으면 index파일을 생성한다.
            CS=set()
            self.cell_length=length_of_cell

    def read_index_file(self):
        departure_file_name=self.get_index_file_name()
        arrival_file_name="a"+departure_file_name[1:]
        path="./index_file/"
        index_info=""
        start_index_array=dict()
        end_index_array=dict()

        with open(path+departure_file_name, "r") as f:
            index_info=f.read().rstrip() #모든 데이터 읽어오기

        #departure 데이터 parsing
        index_info=index_info.split("\n")
        for cell_celldata in index_info:
            tuple_data=cell_celldata.split(")")
            cell_id=eval(tuple_data[0]+")")     #(0.9)와 (0,10)의 크기가 다르다
            if len(tuple_data[1])==0:   #cell에 데이터가 존재하지 않는다면,
                start_index_array[cell_id]=(list(), None)
            else:   #데이터가 존재한다면,
                vertex_data=tuple_data[1].split(",")[1:]    #remove the front ,(comma)
                vertex_data=list(map(int, vertex_data))
                start_index_array[cell_id] = (vertex_data, None)

        index_info=""
        with open(path+arrival_file_name, "r") as f:
            index_info=f.read().rstrip() #모든 데이터 읽어오기

        #arrival 데이터 parsing
        index_info=index_info.split("\n")
        for cell_celldata in index_info:
            tuple_data=cell_celldata.split(")")
            cell_id=eval(tuple_data[0]+")")     #(0.9)와 (0,10)의 크기가 다르다
            if len(tuple_data[1])==0:   #cell에 데이터가 존재하지 않는다면,
                end_index_array[cell_id]=(list(), None)
            else:   #데이터가 존재한다면,
                vertex_data=tuple_data[1].split(",")[1:]    #remove the front ,(comma)
                vertex_data=list(map(int, vertex_data))
                end_index_array[cell_id] = (vertex_data, None)


        return (start_index_array, end_index_array)

    def __spatio_to_numpy(self):
        """
        Generate matrix of spatio.
        :return: 2d matrix which represents spatio dataset
        """
        # UserID(i4), STime(i4), ETime(i4), SLati, SLongti, ELati, ELongi
        types=['i4','i1','i1','double','f8','f8','f8']

        # [structured array(    0,  7,  9, 61.61572103, 40.13141409, 61.61572103, 40.13141409)...]
        mat=np.genfromtxt(self.file_name_csv, dtype=types, delimiter=',', names=True)
        return mat

    def __index_loc_(self, length_of_cell):
        """:return: Tuple of two dictionaries which have _key=coordinate of cell which is component of grid, _value=array of indecies
        """
        if self.file_name_csv != "":
            #raw_mat=self.__spatio_to_numpy()
            num_of_cell=int(self.MAX_LAT/length_of_cell)
            self.num_of_cell=num_of_cell

            start_index_array = dict()
            for cell_x_axis in range(num_of_cell):
                for cell_y_axis in range(num_of_cell):
                    start_index_array[(cell_x_axis,cell_y_axis)]=np.where((\
                        (cell_x_axis <= self.data_matrix["SLati"] / length_of_cell)&\
                        ((cell_x_axis+1) > self.data_matrix["SLati"] / length_of_cell)&\
                        (cell_y_axis <= self.data_matrix["SLongiti"] / length_of_cell)&\
                        ((cell_y_axis+1) > self.data_matrix["SLongiti"] / length_of_cell)\
                        ))

            end_index_array = dict()
            for cell_x_axis in range(num_of_cell):
                for cell_y_axis in range(num_of_cell):
                    end_index_array[(cell_x_axis,cell_y_axis)]=np.where((\
                        (cell_x_axis <= self.data_matrix["ELati"] / length_of_cell)&\
                        ((cell_x_axis+1) > self.data_matrix["ELati"] / length_of_cell)&\
                        (cell_y_axis <= self.data_matrix["ELongi"] / length_of_cell)&\
                        ((cell_y_axis+1) > self.data_matrix["ELongi"] / length_of_cell)\
                        ))
            return (start_index_array, end_index_array)

    def get_index_file_name(self):
        #return departure file name
        num_of_cell=self.num_of_cell
        file_name=self.file_name_csv.split('.')[0]    # 확장자 떼기
        departure_index_file_name="d_index_file_"+str(num_of_cell)+"_"+file_name+".txt"
        return departure_index_file_name

    def write_index_file(self):
        """ read start_index_info=dict(), end_index_info=dict() and write csv that has index
        :return: No return
        """
        #num_of_cell=int(self.MAX_LAT/length_of_cell)
        num_of_cell=self.num_of_cell
        file_name=self.file_name_csv.split('.')[0]    # 확장자 떼기

        index_data=""
        departure_index_file_name="d_index_file_"+str(num_of_cell)+"_"+file_name+".txt"
        arrival_index_file_name = "a_index_file_"+str(num_of_cell)+"_"+file_name+".txt"

        #departure
        for cell in self.start_index_info:
            index_data = index_data + str(cell)
            for a in self.start_index_info[cell][0]:    #self.start_index_info[cell][0]이 vertex 배열이다.
                index_data = index_data + "," + str(a)
            index_data = index_data + "\n"

        with open("./index_file/"+departure_index_file_name, "w") as f:
            f.write(index_data)
        print("[indexor] generating departure index file completed")

        index_data=""   #초기화
        #arrival
        for cell in self.end_index_info:
            index_data = index_data + str(cell)
            for a in self.end_index_info[cell][0]:    #self.start_index_info[cell][0]이 vertex 배열이다.
                index_data = index_data + "," + str(a)
            index_data = index_data + "\n"

        with open("./index_file/"+arrival_index_file_name, "w") as f:
            f.write(index_data)
        print("[indexor] generating arrival index file completed")

    def index_inverted_timetable(self, query_obj):
        self.depart_inverted_time_table=dict()
        self.arrival_inverted_time_table=dict()

        # initializing dictionary by cell_id
        for x_cell in range(0, self.num_of_cell):
            for y_cell in range(0, self.num_of_cell):
                cell_id=(x_cell, y_cell)
                self.depart_inverted_time_table[cell_id]=dict()
                self.arrival_inverted_time_table[cell_id]=dict()
                for i in range(0, 24):
                    self.depart_inverted_time_table[cell_id][i] = list()
                    self.arrival_inverted_time_table[cell_id][i] = list()

        # add time data which will be added to dictionary
        # fill departure_inverted_time_table
        for cell_id in self.depart_inverted_time_table: # traversal all cells
            cell_vertex = self.start_index_info[cell_id][0]
            for vertex in cell_vertex:  #traversal all vertex in a specific cell
                s_time=query_obj.SELECT_s_time_WHERE_userid(vertex)
                self.depart_inverted_time_table[cell_id][s_time].append(vertex)

        # fill arrival_inverted_time_table
        for cell_id in self.arrival_inverted_time_table:
            cell_vertex = self.end_index_info[cell_id][0]
            for vertex in cell_vertex:
                e_time=query_obj.SELECT_e_time_WHERE_userid(vertex)
                self.arrival_inverted_time_table[cell_id][e_time].append(vertex)
        # sum=0
        # for j in range(10):
        #     for k in range(10):
        #         for i in range(24):
        #             sum=sum+len(self.depart_inverted_time_table[(j,k)][i])
        #         print(str(j)+","+str(k)+":"+str(sum))

        #CODE FOR TEST
        # for index in self.depart_inverted_time_table[(8,8)]:
        #     print(index, self.depart_inverted_time_table[(8,8)][index])
        # for index in self.arrival_inverted_time_table[(8,8)]:
        #     print(index, self.arrival_inverted_time_table[(8,8)][index])


    def find_cover_cell(self, UserID, query_obj, learned_dict_start, learned_dict_arrival, threshold):
        # find every cells in which friend are located.
        start_cell_list = set()
        end_cell_list = set()
        max_UserID = self.data_matrix.size
        start_user_cell=query_obj.SELECT_cell_num_WHERE_userid(UserID)[0]
        start_user_position=query_obj.SELECT_position_WHERE_userid(UserID)[0]
        end_user_cell = query_obj.SELECT_cell_num_WHERE_userid(UserID)[1]
        end_user_position = query_obj.SELECT_position_WHERE_userid(UserID)[1]

        SH=tree_algorithm.MinHeap(start_user_cell, start_user_position, self.cell_length)
        EH=tree_algorithm.MinHeap(end_user_cell, end_user_position, self.cell_length)

        # 자기 셀은 삽입 안 하나?? >> 프렌드 셀에 당연 자기가 있을 거라고 생각?
        start_cell_list.add(query_obj.SELECT_cell_num_WHERE_userid(UserID)[0])
        end_cell_list.add(query_obj.SELECT_cell_num_WHERE_userid(UserID)[1])

        drival_bet_distance=calc_stat_data.get_distance(start_user_cell, end_user_cell)

        p_map=dict()
        ep_map=dict()

        #threshold 보다 높은 것들을 다 넣어줘야 한다.
        for a in range(0, 250):
            for b in range(0, 250):
                d=calc_stat_data.get_distance(start_user_cell,(a,b))    #driver와 user 셀 사이의 거리
                if (drival_bet_distance, d) in learned_dict_start:
                    p_map[(a,b)]=learned_dict_start[(drival_bet_distance, d)]
                else:
                    p_map[(a,b)]=calc_stat_data.add_gaussian(0,20,0,d)

        for a in range(0, 250):
            for b in range(0, 250):
               if p_map[(a,b)]>threshold:
                    start_cell_list.add((a,b))

        for a in range(0, 250):
            for b in range(0, 250):
                d=calc_stat_data.get_distance(end_user_cell,(a,b))    #driver와 user 셀 사이의 거리
                if (drival_bet_distance, d) in learned_dict_arrival:
                    ep_map[(a,b)]=learned_dict_arrival[(drival_bet_distance, d)]
                else:
                    ep_map[(a,b)]=calc_stat_data.add_gaussian(0,20,0,d)

        for a in range(0, 250):
            for b in range(0, 250):
                if ep_map[(a,b)]>threshold:
                    end_cell_list.add((a,b))

        print(len(start_cell_list), len(end_cell_list))

        #construct start cell heap
        for cell in start_cell_list:
            SH.insert(cell)
        #construct end cell heap
        for cell in end_cell_list:
            EH.insert(cell)

        return (SH, EH)

    def find_cover_cell_naive(self, UserID, query_obj):
        """
        user가 위치한 cell만 넣게 되는 cover cell module :: 나이브에서만 사용한다.
        :param UserID: ID of USER
        :param query_obj: query_obj
        :return: heaps with cell of user, no cell covering friends
        """
        start_user_cell=query_obj.SELECT_cell_num_WHERE_userid(UserID)[0]
        start_user_position=query_obj.SELECT_position_WHERE_userid(UserID)[0]
        end_user_cell = query_obj.SELECT_cell_num_WHERE_userid(UserID)[1]
        end_user_position = query_obj.SELECT_position_WHERE_userid(UserID)[1]

        # declar heap corresponding to DH, AH
        SH=tree_algorithm.MinHeap(start_user_cell, start_user_position, self.cell_length)
        EH=tree_algorithm.MinHeap(end_user_cell, end_user_position, self.cell_length)

        # SH와 EH에 사용자가 위치한 셀을 삽입한다.
        SH.insert(query_obj.SELECT_cell_num_WHERE_userid(UserID)[0])
        EH.insert(query_obj.SELECT_cell_num_WHERE_userid(UserID)[1])

    def search_cell_data_algo4(self, u, query_obj, cell, user_time, start_flag):
        IO_flag = False

        if start_flag:
            vertex_in_cell=self.start_index_info[cell][0]
        else: #end_flag is true
            vertex_in_cell=self.end_index_info[cell][0]

        for vertex in vertex_in_cell :
            if True:
                IO_flag = True
                self.CS.add(vertex)
                vertex_position = query_obj.SELECT_position_WHERE_userid(vertex)

                # distance constraints
                distance_vertex_position = self.dist(vertex_position[0], vertex_position[
                    1])  # distance between the specific user's position
                mc_vertex = self.VH.moving_cost(vertex_position)

                # time constraints:: Temporal condition
                time_vertex = query_obj.SELECT_time_WHERE_userid(vertex)
                start_time_constraint = user_time[0] >= time_vertex[0]
                end_time_constraint = user_time[1] <= time_vertex[1]

                if mc_vertex < distance_vertex_position and start_time_constraint and end_time_constraint and vertex!=u:  # + time constraints
                    self.VH.insert(vertex)
        return IO_flag

    def search_time_aware_cell_data(self, query_obj, cell, friend_list, user_time, start_flag):
        IO_flag=False
        if start_flag:   # it is from departure heap
            T = self.cell_slot_time(cell, True)    # departure_cell_slot_time
            user_departure_time = user_time[0]
            user_arrival_time = user_time[1]
            while T <= user_departure_time:
                departure_v_set_given_T = self.depart_inverted_time_table[cell][T]
                for vertex in departure_v_set_given_T:
                    IO_flag=True
                    #이미 검사한 vertex인지 확인 후, 친구리스트에 존재하는지 확인하기
                    if vertex not in self.CS:
                        arrival_time_vertex = query_obj.SELECT_time_WHERE_userid(vertex)[1]
                        if (vertex in friend_list) and arrival_time_vertex >= user_arrival_time:       #(not vertex in self.CS) and 를 지웠다.
                            vertex_position = query_obj.SELECT_position_WHERE_userid(vertex)
                            # distance constraints
                            distance_vertex = self.dist(vertex_position[0],
                                                        vertex_position[1])  # distance between the specific user's position
                            mc_vertex = self.VH.moving_cost(vertex_position)
                            if mc_vertex < distance_vertex:
                                # Check set에 넣어주기
                                self.CS.add(vertex)
                    else:
                        self.VH.insert(vertex)
                T=T+1   # decreas time range
            return IO_flag
        else:            # it is from arrival heap
            T = self.cell_slot_time(cell, False)    # arrival_cell_slot_time
            user_departure_time=user_time[0]
            user_arrival_time = user_time[1]
            while T >= user_arrival_time:
                arrival_v_set_given_T = self.arrival_inverted_time_table[cell][T]
                IO_flag = True
                for vertex in arrival_v_set_given_T:
                    if vertex not in self.CS:
                        departure_time_vertex = query_obj.SELECT_time_WHERE_userid(vertex)[0]
                        if (vertex in friend_list) and departure_time_vertex<=user_departure_time:     #(not vertex in self.CS) and를 지웠다.
                            # Check set에 넣어주기
                            vertex_position= query_obj.SELECT_position_WHERE_userid(vertex)
                            distance_vertex = self.dist(vertex_position[0],
                                                        vertex_position[1])  # distance between the specific user's position
                            mc_vertex = self.VH.moving_cost(vertex_position)
                            if mc_vertex < distance_vertex:
                                self.CS.add(vertex)
                    else:
                        self.VH.insert(vertex)
                T=T-1
            return IO_flag

    def cell_slot_time(self, cell, start_flag):
        """
        find cell-timelot that satisfies Definition 12
        :param cell: cell_num
        :param start_flag: is_departure()
        :return: cell-slottime
        """
        if start_flag:  # departure cell-time
            result_time = 0
            inverted_time_table = self.depart_inverted_time_table[cell]

            for time in inverted_time_table:
                vertex_list_given_time = inverted_time_table[time]
                if len(vertex_list_given_time) != 0:
                    break   #return
                result_time = result_time+1
        else:           # arrival cell-time
            result_time = 23
            inverted_time_table = self.arrival_inverted_time_table[cell]
            for time in inverted_time_table:
                vertex_list_given_time = inverted_time_table[23-time]
                if len(vertex_list_given_time) != 0:
                    break   #return
                result_time = result_time - 1
        return result_time


    def dist(self, p1, p2):
        """ this method is from tree_algorithm module
        :param p1: the first point
        :param p2: the second point
        :return: distance(float) value
        """
        square_diff_x=(p1[0]-p2[0])**2
        square_diff_y=(p1[1]-p2[1])**2
        distance=(square_diff_x+square_diff_y)**(float(1)/2)
        return distance

    def is_VH_empty(self):
        if self.VH.is_empty():
            return True
#
# _i=IndexDatabase("Barabasi_60K_SpatioTemporal.csv", 0.4)
# _i=IndexDatabase("Barabasi_70K_SpatioTemporal.csv", 0.4)
# _i=IndexDatabase("Barabasi_80K_SpatioTemporal.csv", 0.4)
# _i=IndexDatabase("Barabasi_90K_SpatioTemporal.csv", 0.4)
# _i=IndexDatabase("Barabasi_100K_SpatioTemporal.csv", 0.4)
# _i=IndexDatabase("Barabasi_300K_SpatioTemporal.csv", 0.4)
# _i=IndexDatabase("Barabasi_600K_SpatioTemporal.csv", 0.4)
# _i=IndexDatabase("Barabasi_900K_SpatioTemporal.csv", 0.4)
#_i.spatio_to_numpy() #no direct
#_i.index_loc_(10)