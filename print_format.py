import naive_simulator
import query_simulator_main
import algo4_w_makefriend
import algo4_w_mfl_plus_itt
import p1_query_simulator_main

def get_name_pro_file(c):
    version_name = "proposed_probability"
    return version_name+(c[0].split(".")[0])

def executor(c, cell_length, cell_u_position_info, query_obj, pid):
    """
    :param c: file name
    :param cell_length:
    :param cell_u_position_info:
    :param query_obj:
    :param pid:
    :return:
    """

    grid_length=100/cell_length # FOR NAIVE
    # query
    # 결과 파일 초기화
    path = "./query_result/"

    if pid==1:
        file_name = naive_simulator.get_result_file_name(cell_length, c[0], False)
    elif pid==2:
        file_name = query_simulator_main.get_result_file_name(cell_length, c[0], False)
    elif pid==3:
        file_name = algo4_w_makefriend.get_result_file_name(cell_length, c[0], False)
    else:
        file_name = algo4_w_mfl_plus_itt.get_result_file_name(cell_length, c[0], False)

    with open(path + file_name, "w") as f:
        f.write("")

    if pid==1:
        param_file_name = naive_simulator.get_result_file_name(cell_length, c[0], True)
    elif pid==2:
        param_file_name = query_simulator_main.get_result_file_name(cell_length, c[0], True)
    elif pid==3:
        param_file_name = algo4_w_makefriend.get_result_file_name(cell_length, c[0], True)
    else:
        param_file_name = algo4_w_mfl_plus_itt.get_result_file_name(cell_length, c[0], True)

    with open(path + param_file_name, "w") as f:
        f.write("")

    valid_result_count=0
    a=""
    a = a + c[0] + "\n"
    b=""
    total_time=0
    count=0
    IO_count =0

    # fix query range
    first_queater = len(cell_u_position_info.data_matrix) // 4
    second_queater = first_queater*2
    third_queater = first_queater*3

    # 돌려야 할 vertex id 리스트

    learned_dict_start=dict()
    learned_dict_arrival=dict()

    with open(get_name_pro_file(c)+"posterior_arrive_add_norm_all.txt", "r") as f:
        learning_result=f.read()
        learning_result=learning_result.split("\n")
        for l in learning_result[:-1]:
            suba=l.split(" -> ")
            learned_dict_start[eval(suba[0])]=float(suba[1])


    with open(get_name_pro_file(c)+"posterior_start_add_norm_all.txt", "r") as f:
        learning_result=f.read()
        learning_result=learning_result.split("\n")
        for l in learning_result[:-1]:
            suba=l.split(" -> ")
            learned_dict_arrival[eval(suba[0])]=float(suba[1])

    if not c[3]:
        #실제 데이터
        for m in range(4, 5):
            for i in range(0, len(cell_u_position_info.data_matrix)):
                if i>=1001:
                    if pid==1:
                        print("NAIVE query "+str(m) + " seats, " + str(i) + " th query start!")
                        result=naive_simulator.query_processing_algo4(i, m, cell_u_position_info, query_obj, grid_length) #1로 쿼리하면 왜 m=2결과로 나오노!
                    elif pid==2:
                        print("query processing "+str(m) + " seats, " + str(i) + " th query start!")
                        result = p1_query_simulator_main.query_processing_algo4(i, m, cell_u_position_info, query_obj, learned_dict_start, learned_dict_arrival)  # 1로 쿼리하면 왜 m=2결과로 나오노!
                    elif pid==3:
                        result = algo4_w_makefriend.query_processing_algo4(i, m, cell_u_position_info, query_obj)
                    else: #pid==4
                        result = algo4_w_mfl_plus_itt.query_processing_algo4(i, m, cell_u_position_info, query_obj)

                    total_time = total_time + result[1]
                    IO_count = IO_count + result[2]

                    if len(result[0])==m:
                        #print("vertex : "+str(i))
                        print(str(i)+"th vertex, "+"there is result :"+str(result[0]))
                        a=a+"vertex : "+str(i)+" there is result :"+str(result[0])+"\n"
                        a=a+"time : "+str(result[1])+", IO count :  "+str(result[2])+"\n"
                        valid_result_count+=1
                    else:
                        print(str(i) + "th vertex, " + "there is no result.")
                        a = a + str(i) + "th query ended, but result not founded\n"
                        a = a + "time : " + str(result[1]) + ", IO count :  " + str(result[2]) + "\n"
                    count=count+1
            b = b +"===========PARAMETERS===========\n"
            b = b +"m: "+str(m)+"\n"
            b = b +"time: "+str(total_time/count)+"\n"
            b = b +"cell: "+str(IO_count/count)+"\n"
            b = b +"matching: "+str(valid_result_count)+"/"+str(count)+"\n"
            b = b + "===========\\PARAMETERS\\===========\n"
            a = a + b
            total_time=0
            count=0
            IO_count = 0
            valid_result_count = 0
            with open(path + file_name, "a") as f:
                f.write(a)
            with open(path + param_file_name, "a") as f:
                f.write(b)
            a=""
            b=""

    else:
        # 합성 데이터
        for m in range(4, 5):
            for i in range(0, 2):
                if i<=3000 and i>=1001: #or (i>= first_queater and i<first_queater+5) or (i>= second_queater and i<second_queater+5) or (i>= third_queater and i<third_queater+5):
                    if pid==1:
                        result=naive_simulator.query_processing_algo4(i, m, cell_u_position_info, query_obj, grid_length) #1로 쿼리하면 왜 m=2결과로 나오노!
                    elif pid==2:
                        result = query_simulator_main.query_processing_algo4(i, m, cell_u_position_info, query_obj)  # 1로 쿼리하면 왜 m=2결과로 나오노!
                    elif pid==3:
                        result = algo4_w_makefriend.query_processing_algo4(i, m, cell_u_position_info, query_obj)
                    else: #pid==4
                        result = algo4_w_mfl_plus_itt.query_processing_algo4(i, m, cell_u_position_info, query_obj)

                    total_time = total_time + result[1]
                    IO_count = IO_count + result[2]

                    if len(result[0])==m:
                        #print("vertex : "+str(i))
                        print(str(i)+"th vertex, "+"there is result :"+str(result[0]))
                        a=a+"vertex : "+str(i)+" there is result :"+str(result[0])+"\n"
                        a=a+"time : "+str(result[1])+", IO count :  "+str(result[2])+"\n"
                        valid_result_count+=1
                    else:
                        print(str(i) + "th vertex, " + "there is no result.")
                        a = a + str(i) + "th query ended, but result not founded\n"
                        a = a + "time : " + str(result[1]) + ", IO count :  " + str(result[2]) + "\n"
                    count=count+1
            b = b +"===========PARAMETERS===========\n"
            b = b +"m: "+str(m)+"\n"
            b = b +"time: "+str(total_time/count)+"\n"
            b = b +"cell: "+str(IO_count/count)+"\n"
            b = b +"matching: "+str(valid_result_count)+"/"+str(count)+"\n"
            b = b + "===========\\PARAMETERS\\===========\n"
            a = a + b
            total_time=0
            count=0
            IO_count = 0
            valid_result_count = 0
            with open(path + file_name, "a") as f:
                f.write(a)
            with open(path + param_file_name, "a") as f:
                f.write(b)
            a=""
            b=""