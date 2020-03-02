import algo4_w_mfl_plus_itt
import algo4_w_makefriend
import query_simulator_main
import naive_simulator
import index_dataset
import query_npdata
import parse_dataset_file

if __name__=="__main__":
    a = ["Barabasi_100K_SpatioTemporal.csv", "Barabasi_100K_LvOneFri.csv", "Barabasi_100K_LvTwoFri.csv", False]
    b = ["Barabasi_300K_SpatioTemporal.csv", "Barabasi_300K_LvOneFri.csv", "Barabasi_300K_LvTwoFri.csv", True]
    c = ["Barabasi_200K_SpatioTemporal.csv", "Barabasi_200K_LvOneFri.csv", "Barabasi_200K_LvTwoFri.csv", True]
    d = ["Barabasi_60K_SpatioTemporal.csv", "Barabasi_60K_LvOneFri.csv", "Barabasi_60K_LvTwoFri.csv", False]
    e = ["Barabasi_70K_SpatioTemporal.csv", "Barabasi_70K_LvOneFri.csv", "Barabasi_70K_LvTwoFri.csv", False]
    f = ["Barabasi_80K_SpatioTemporal.csv", "Barabasi_80K_LvOneFri.csv", "Barabasi_80K_LvTwoFri.csv", False]
    h = ["Barabasi_90K_SpatioTemporal.csv", "Barabasi_90K_LvOneFri.csv", "Barabasi_90K_LvTwoFri.csv", False]
    i = ["munged_GowallaEurope_SpatioTemporal.csv", "GowallaEurope_LvOneFri.csv", "GowallaEurope_LvTwoFri.csv", False]
    j = ["munged_BrightkiteAmerica_SpatioTemporal.csv", "BrightkiteAmerica_LvOneFri.csv", "BrightkiteAmerica_LvTwoFri.csv", False]
    k = ["munged_BrightkiteEurope_SpatioTemporal.csv", "BrightkiteEurope_LvOneFri.csv", "BrightkiteEurope_LvTwoFri.csv", False]
    l = ["munged_GowallaAmerica_SpatioTemporal.csv", "GowallaAmerica_LvOneFri.csv", "GowallaAmerica_LvTwoFri.csv", False]
    q = [k, i, j, l]   #합성데이터, 실제데이터 순, d, e, f, h, a, c, b,

    for per_test in q:
        cell_length = 0.4

        #Intro
        print("[simulator] Hi program is starting to run v.2019 KCS")

        # index by position
        cell_u_position_info = index_dataset.IndexDatabase(per_test[0], cell_length)  # Indexing obj
        print("[simulator] user data object uploaded")

        # query object
        query_obj = query_npdata.QueryDatabase(cell_length, cell_u_position_info.data_matrix)  # Query obj
        print("[simulator] query object uploaded")

        #naive version 정상작동 확인 완료
        # print("[simulator] v.naive start")
        # naive_simulator.main(per_test, cell_u_position_info, query_obj)
        # #
        # one by one version
        print("[simulator] v.algo4 start")
        query_simulator_main.main(per_test, cell_u_position_info, query_obj)