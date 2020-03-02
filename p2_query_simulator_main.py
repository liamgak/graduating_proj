import make_friend_list
import index_dataset
import query_npdata
import tree_algorithm
import compute_group_algo4
import parse_dataset_file
import time
import print_format
import copy

def query_processing_algo4(u, m, cell_u_position_info, query_obj):
    """
    Algorithm 4 :: Query processing using two-level friend list
    :param u: userID
    :param m: the number of seats of a vehicle
    :param cell_u_position_info: client information
    :param query_obj: query system(DB system)
    :return:
    """
    #IO_count
    IO_count=0

    #저번 epoch 흔적 지우기
    cell_u_position_info.VH = set()
    cell_u_position_info.CS = set()

    p = query_obj.SELECT_position_WHERE_userid(u)
    t = query_obj.SELECT_time_WHERE_userid(u)

    # Line 3
    best_cost=100000

    # new exit condition
    group_generating_flag=False
    top_m_minus_1 = list()
    top_m_minus_1_mc = list()
    threshold_cost = 10000
    threshold = 0
    first_vertex = True
    candidate_cost = 0

    # defining necessary minheap
    cell_u_position_info.VH=tree_algorithm.MinHeap_moving_cost(p, query_obj)
    candidate_list=tree_algorithm.MinHeap_moving_cost(p, query_obj)

    # computing group obj
    # group 연산에 대한 메소드를 가진 오브젝트
    compute_group_obj = compute_group_algo4.ComputeGroup_algo4(m, p, query_obj)
    optimal_group=set()

    #셀들 전부 다 넣고 시작
    DH, AH = cell_u_position_info.find_cover_cell(u, query_obj)  # return (SH, EH)
    print("[simulator] complete to make cell heap")
    start_time = time.time()

    # Line 5
    if True: #originally this statement is for the number of friend inspection
        # Line 6 : 친구들이 커버하고 있는 셀 찾기. 여기를 고쳐야한다. 1. 모든 셀 다 넣어버리던가
        # Line 7
        while not DH.is_empty() or not AH.is_empty():
            # Line 8
            if not DH.is_empty():
                cd=DH.delete()
            # Line 9
            if not AH.is_empty():
                ca=AH.delete()

            # Line 10
            if group_generating_flag:
                if best_cost - candidate_cost < DH.mindist_user_and_cell(cd) + AH.mindist_user_and_cell(ca):    #>>overhead
                    # Line 11
                    break

            IO_flag = cell_u_position_info.search_cell_data_algo4(u, query_obj, cd, t, True) # it is from start cell
            if IO_flag:
                IO_count=IO_count+1

            # Line 13
            IO_flag = cell_u_position_info.search_cell_data_algo4(u, query_obj, ca, t, False) # it is from end cell
            if IO_flag:
                IO_count=IO_count+1

            # Line 14
            while not cell_u_position_info.is_VH_empty():
                # Line 15
                selected_vertex=cell_u_position_info.VH.delete()
                # Line 16
                selected_vertex_position = query_obj.SELECT_position_WHERE_userid(selected_vertex)
                selected_vertex_mc = cell_u_position_info.VH.moving_cost(selected_vertex_position)

                if m!=2:
                    if len(top_m_minus_1)<m-2:
                        top_m_minus_1.append(selected_vertex)
                        top_m_minus_1_mc.append(selected_vertex_mc)

                        if first_vertex:
                            first_vertex = False
                            threshold = selected_vertex
                            threshold_cost = selected_vertex_mc

                        if threshold_cost < selected_vertex_mc:
                            threshold = selected_vertex
                            threshold_cost = selected_vertex_mc

                    else:   #m-1이 되면!
                        if threshold_cost > selected_vertex_mc:
                            top_m_minus_1.remove(threshold)
                            top_m_minus_1_mc.remove(threshold_cost)
                            top_m_minus_1.append(selected_vertex)
                            top_m_minus_1_mc.append(selected_vertex_mc)
                            candidate_cost = compute_group_obj.group_moving_cost(set(top_m_minus_1))

                            #threshold를 정하는 반복문
                            max = top_m_minus_1_mc[0]
                            max_index = 0
                            for index, mc in enumerate(top_m_minus_1_mc):
                                if max < mc:
                                    max = mc
                                    max_index = index

                            threshold_cost = top_m_minus_1_mc[max_index]
                            threshold = top_m_minus_1[max_index]

                if group_generating_flag:
                    if best_cost - candidate_cost < selected_vertex_mc:
                        # Line 17
                        break

                # Line 18
                if selected_vertex not in candidate_list.heap:
                    computed_group=compute_group_obj.find_min_mc_group(selected_vertex, candidate_list, m)

                # Line 19
                if len(computed_group)+1 >= m:  #user도 포함해서 계산해야한다.
                    group_moving_cost = compute_group_obj.group_moving_cost(computed_group)
                    if best_cost > group_moving_cost:
                        # Line 24
                        optimal_group=computed_group.copy()
                        # Line 25
                        best_cost=group_moving_cost
                        # Line 26
                        group_generating_flag = True

    result_time=time.time()-start_time
    print(candidate_cost, best_cost)
    return (optimal_group.union({u}), result_time, IO_count)

def print_vertex_result(vertex, query_obj, compute_group_obj):
    _p = query_obj.SELECT_position_WHERE_userid(vertex)
    print("====================================")
    print("1. vertex: " + str(vertex)+","+str(query_obj.SELECT_cell_num_WHERE_userid(vertex)))
    print("2. user position: " + str(query_obj.SELECT_position_WHERE_userid(vertex)))
    print("3. Time: " + str(query_obj.SELECT_time_WHERE_userid(vertex)))
    print("4. MC: " + str(compute_group_obj.moving_cost(_p)))
    print("5. dist: " + str(compute_group_obj.dist(_p[0], _p[1])))

def get_result_file_name(cell_length, test_file, param_setting):
    if param_setting==True:
        version_name="NCF_Param_"
        separated_file_name=test_file.split("_")
        prefix=separated_file_name[0]+"_"+separated_file_name[1]
        version_name = version_name + prefix + "_"
        cell_number=int(100/cell_length)
        post_fix=str(cell_number)+"x"+str(cell_number)
        file_name=version_name+post_fix+".txt"
    else:
        version_name="NCF_"
        separated_file_name = test_file.split("_")
        prefix = separated_file_name[0] + "_" + separated_file_name[1]
        version_name = version_name + prefix + "_"
        cell_number=int(100/cell_length)
        post_fix=str(cell_number)+"x"+str(cell_number)
        file_name=version_name+post_fix+".txt"
    return file_name

def main(c, cell_u_position_info, query_obj):
    """ simulate query processing using two-level friend list
    :return: result set
    """
    # Defining Object
    cell_length=0.4  # parameters of object

    #결과 파일 초기화
    path="./query_result/"
    file_name=get_result_file_name(cell_length, c[0],False)
    with open(path + file_name, "w") as f:
        f.write("")

    param_file_name=get_result_file_name(cell_length, c[0], True)
    with open(path + param_file_name, "w") as f:
        f.write("")

    print_format.executor(c, cell_length, cell_u_position_info, query_obj, 2)

if __name__=="__main__":
    main()