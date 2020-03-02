import make_friend_list
import index_dataset
import query_npdata
import pseudo_pcm
import compute_group_algo4
import parse_dataset_file
import tree_algorithm
import time
import print_format

def query_processing_algo4(u, m, cell_u_position_info, query_obj, grid_length):
    """
    Algorithm 4 :: Query processing using two-level friend list
    :param u: userID
    :param m: the number of seats of a vehicle
    :param cell_u_position_info: client information
    :param query_obj: query system(DB system)
    :param grid_length: grid length(only for v.naive)
    :return:
    """
    #count IO
    IO_count=0
    best_cost = 100000
    #저번 epoch 흔적 지우기
    cell_u_position_info.VH = set()
    cell_u_position_info.CS = set()


    #candidate cost 추출을 위한 변수
    group_generating_flag = False
    top_m_minus_1 = list()
    top_m_minus_1_mc = list()
    threshold_cost = 10000
    threshold = 0
    first_vertex = True
    candidate_cost = 0

    p = query_obj.SELECT_position_WHERE_userid(u)
    t = query_obj.SELECT_time_WHERE_userid(u)
    cell_u_position_info.VH=tree_algorithm.MinHeap_moving_cost(p, query_obj)

    # CPM 객체 생성
    cpm=pseudo_pcm.CPM(u, query_obj, grid_length, cell_u_position_info)
    best_group = set()

    # DECLARE SET
    departure_set = set()
    arrival_set = set()
    intermediate_set = tree_algorithm.MinHeap_moving_cost(p, query_obj)

    # 그룹을 생성하는 객체 생성
    compute_group_obj = compute_group_algo4.ComputeGroup_algo4(m, p, query_obj)

    #start
    start_time = time.time()

    if True: #originally this statement is for the number of friend inspection
        while True: #not DH.is_empty() and not AH.is_empty():
            # CPM으로 vertex하나씩 꺼내는 코드
            start_vertex = cpm.pop(True)
            while start_vertex == -1 or start_vertex == u:  #-1이 return되면 계속해서 탐색해야하고, user와 같은 vertex는 무시한다.
                start_vertex = cpm.pop(True)

            end_vertex = cpm.pop(False)
            while end_vertex == -1 or end_vertex == u:   #위와 같은 이유이다.
                end_vertex = cpm.pop(False)

            if start_vertex == -2  and end_vertex == -2: # 한 쪽에서라도 더 이상 탐색할 cell이 없다면, break한다
                break

            #line 8-9 : step of filtering veretx
            if group_generating_flag:
                if best_cost - candidate_cost < cpm.start_min_dist_cell + cpm.end_min_dist_cell:
                    break

            # getting start-info phase
            start_vertex_position = query_obj.SELECT_position_WHERE_userid(start_vertex)
            mc_start_vertex = cpm.start_vertex_minheap.moving_cost(start_vertex_position)
            start_vertex_time = query_obj.SELECT_time_WHERE_userid(start_vertex)
            dist_vertex_position = cpm.start_vertex_minheap.dist(start_vertex_position[0], start_vertex_position[1])

            if (mc_start_vertex < dist_vertex_position) and check_time_condition(t, start_vertex_time):
                departure_set.add(start_vertex)

            # getting end-info phase
            end_vertex_position = query_obj.SELECT_position_WHERE_userid(end_vertex)
            mc_end_vertex = cpm.start_vertex_minheap.moving_cost(end_vertex_position)
            end_vertex_time = query_obj.SELECT_time_WHERE_userid(end_vertex)
            dist_vertex_position = cpm.start_vertex_minheap.dist(end_vertex_position[0], end_vertex_position[1])

            if (mc_end_vertex<dist_vertex_position)\
                and check_time_condition(t, end_vertex_time):
                arrival_set.add(end_vertex)

            # line 12- : 그룹 검사하기
            added_vertex_set=set()
            added_vertex_set.add(start_vertex)
            added_vertex_set.add(end_vertex)

            for vertex in added_vertex_set:
                selected_vertex_position = query_obj.SELECT_position_WHERE_userid(vertex)
                selected_vertex_mc = cell_u_position_info.VH.moving_cost(selected_vertex_position)
                if m!=2:
                    if len(top_m_minus_1) < m - 2:
                        top_m_minus_1.append(vertex)
                        top_m_minus_1_mc.append(selected_vertex_mc)

                        if first_vertex:
                            first_vertex = False
                            threshold = vertex
                            threshold_cost = selected_vertex_mc

                        if threshold_cost < selected_vertex_mc:
                            threshold = vertex
                            threshold_cost = selected_vertex_mc

                    else:  # m-1이 되면!
                        if threshold_cost > selected_vertex_mc:
                            top_m_minus_1.remove(threshold)
                            top_m_minus_1_mc.remove(threshold_cost)
                            top_m_minus_1.append(vertex)
                            top_m_minus_1_mc.append(selected_vertex_mc)
                            candidate_cost = compute_group_obj.group_moving_cost(set(top_m_minus_1))

                            # threshold를 정하는 반복문
                            max = top_m_minus_1_mc[0]
                            max_index = 0
                            for index, mc in enumerate(top_m_minus_1_mc):
                                if max < mc:
                                    max = mc
                                    max_index = index

                            threshold_cost = top_m_minus_1_mc[max_index]
                            threshold = top_m_minus_1[max_index]

                if (vertex in departure_set) or (vertex in arrival_set):
                    if vertex not in intermediate_set.heap:  #intermediate_set에 새로운 vetex가 추가 된다면 그룹을 만들어야한다.
                        computed_group = compute_group_obj.find_min_mc_group(vertex, intermediate_set, m)  #메소드 안 쪽에서 vertex를 intermediate set에 추가해준다.
                        if len(computed_group)+1 >= m:
                            current_cost = compute_group_obj.group_moving_cost(computed_group)

                            if current_cost < best_cost:
                                best_group = computed_group
                                best_cost = compute_group_obj.group_moving_cost(best_group)
                                group_generating_flag = True

    print(best_cost, candidate_cost)
    result_time = time.time() - start_time
    IO_count=cpm.IO_count
    return (best_group.union({u}), result_time, IO_count)

def check_time_condition(time1, time2):
    # time is (start_time, end_time). time 1 is user's time
    if time2[0] <= time1[0] and time1[1] <=time2[1]:
        return True
    return False

def get_result_file_name(cell_length, test_file, param_setting):
    if param_setting==True:
        version_name="Naive_Param_"
        separated_file_name=test_file.split("_")
        prefix=separated_file_name[0]+"_"+separated_file_name[1]
        version_name = version_name + prefix + "_"
        cell_number=int(100/cell_length)
        post_fix=str(cell_number)+"x"+str(cell_number)
        file_name=version_name+post_fix+".txt"
    else:
        version_name="Naive_"
        separated_file_name=test_file.split("_")
        prefix=separated_file_name[0]+"_"+separated_file_name[1]
        version_name = version_name + prefix + "_"
        cell_number=int(100/cell_length)
        post_fix=str(cell_number)+"x"+str(cell_number)
        file_name=version_name+post_fix+".txt"
    return file_name

def print_vertex_result(vertex, query_obj, compute_group_obj):
    _p = query_obj.SELECT_position_WHERE_userid(vertex)
    print("====================================")
    print("1. vertex: " + str(vertex)+","+str(query_obj.SELECT_cell_num_WHERE_userid(vertex)))
    print("2. user position: " + str(query_obj.SELECT_position_WHERE_userid(vertex)))
    print("3. Time: " + str(query_obj.SELECT_time_WHERE_userid(vertex)))
    print("4. MC: " + str(compute_group_obj.moving_cost(_p)))
    print("5. dist: " + str(compute_group_obj.dist(_p[0], _p[1])))

def main(c, cell_u_position_info, query_obj):
    """ simulate query processing using two-level friend list
    :return: result set
    """
    # Defining Object
    cell_length=0.4  # parameters of object

    print_format.executor(c, cell_length, cell_u_position_info, query_obj, 1)

if __name__=="__main__":
    main()