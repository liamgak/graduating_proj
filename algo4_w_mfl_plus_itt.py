import make_friend_list
import index_dataset
import query_npdata
import tree_algorithm
import compute_group_algo4
import parse_dataset_file
import time
import random
import print_format

def query_processing_algo4(u, l, m, cell_u_position_info, query_obj, friend_obj):
    """
    Algorithm 4 :: Query processing using two-level friend list
    :param u: userID
    :param l: an acceptable social boundary
    :param m: the number of seats of a vehicle
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
    best_cost=10000

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
    compute_group_obj = compute_group_algo4.ComputeGroup_algo4(m, friend_obj, p, query_obj)
    optimal_group=set()

    start_time = time.time()
    # Line 4
    user_friend_list=friend_obj.friend_list_with_SCF(u, l)[0] #이거 return 값 업데이트 되었다.

    # Line 5
    if m<=len(user_friend_list.union({u})):
        # print("length of user list: "+str(len(user_friend_list)))

        # Line 6 : 친구들이 커버하고 있는 셀 찾기. >> overhead
        DH, AH = cell_u_position_info.find_cover_cell(u, user_friend_list, query_obj)   # return (SH, EH)

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
            #print(DH.mindist_user_and_cell(cd) , AH.mindist_user_and_cell(ca))
            IO_flag = cell_u_position_info.search_time_aware_cell_data(query_obj, cd, user_friend_list, t, True)
            if IO_flag:
                IO_count=IO_count+1

            # Line 13
            #cell_u_position_info.search_cell_data_algo4(query_obj, ca, user_friend_list, u, t, False) # it is from end cell
            IO_flag = cell_u_position_info.search_time_aware_cell_data(query_obj, ca, user_friend_list, t, False)
            if IO_flag:
                IO_count=IO_count+1

            # Line 14
            while not cell_u_position_info.is_VH_empty():
                # Line 15
                selected_vertex=cell_u_position_info.VH.delete()
                # Line 16
                selected_vertex_position = query_obj.SELECT_position_WHERE_userid(selected_vertex)
                selected_vertex_mc = cell_u_position_info.VH.moving_cost(selected_vertex_position)

                #candidate 갱신이 여기서 이루어져야 한다.
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
                    computed_group=compute_group_obj.find_min_mc_group_with_MFL(selected_vertex, candidate_list, l, m)

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
                        # candiCost 갱신
                        # copied_heap = copy.deepcopy(candidate_list)
                        # top_m_minus_1.clear()
                        # for count in range(m-2):
                        #     best_vertex = copied_heap.delete()
                        #     top_m_minus_1.append(best_vertex)
                        # candidate_cost = compute_group_obj.group_moving_cost(set(top_m_minus_1))
    result_time=time.time()-start_time
    print(candidate_cost)
    print(best_cost)
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
        version_name="ITT_Param_"
        separated_file_name = test_file.split("_")
        prefix = separated_file_name[0] + "_" + separated_file_name[1]
        version_name = version_name + prefix + "_"
        cell_number=int(100/cell_length)
        post_fix=str(cell_number)+"x"+str(cell_number)
        file_name=version_name+post_fix+".txt"
    else:
        version_name="ITT_"
        separated_file_name = test_file.split("_")
        prefix = separated_file_name[0] + "_" + separated_file_name[1]
        version_name = version_name + prefix + "_"
        cell_number=int(100/cell_length)
        post_fix=str(cell_number)+"x"+str(cell_number)
        file_name=version_name+post_fix+".txt"
    return file_name

def main(c, cell_u_position_info, query_obj, _m):
    """ simulate query processing using two-level friend list
    :return: result set
    """
    # Defining Object
    cell_length=0.4  # parameters of object
    #
    # # index by position
    # cell_u_position_info=index_dataset.IndexDatabase(c[0], cell_length)    # Indexing obj
    # print("[simulator] user data obectj uploaded")
    #
    # # query object
    # query_obj=query_npdata.QueryDatabase(cell_length, cell_u_position_info.data_matrix)     # Query obj
    # print("[simulator] query object uploaded")
    #
    # # generate inverted_time_table
    # cell_u_position_info.index_inverted_timetable(query_obj)
    # print("[simulator] inverted time table uploaded")
    #
    # # upload friends data into main memory
    # parse_friend_data_obj = parse_dataset_file.ParseDatasetFile(c[1], c[2])
    # _m = make_friend_list.MakeFriendList(parse_friend_data_obj)
    # print("[simulator] friendship object uploaded")

    print_format.executor(c, cell_length, cell_u_position_info, query_obj, _m, 4)



if __name__=="__main__":
    main()