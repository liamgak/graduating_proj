import parse_dataset_file
import tree_algorithm
import time

class MakeFriendList():
    #user_ID=123 #integer
    #hop=123 #integer   ###REMOVED

    def __init__(self, friends_list):
        #self.user_ID=user_ID
        self.friends_list_inmemory = friends_list

    def get_n_hop_friend_list(self, user_ID, hop):
        """ this method is used as a baseline method
        :param user_ID: user identifier
        :return: a set of friends
        """
        start_time1=time.time()
        trv_obj=tree_algorithm.AlgorithmForTree(self.friends_list_inmemory)
        result=trv_obj.bf_travelsal_friend(user_ID, hop)
        time_cost=time.time()-start_time1
        return (result.difference({user_ID}), time_cost)

    def friend_list_with_SCF(self, user_ID, hop):
        start_time2 = time.time()
        # Initializing phase
        expanding_vertex = set()   # 확장되어야 할 vertex 집합
        tmp=list()
        result=set()
        # controling hop
        current_hop = 0 #이미 if 분기로 hop control되고 있음.
        expanding_vertex.add(user_ID)   # input vertex 부터 확장

        if hop>=2:
            V_one_hop = self.friends_list_inmemory.one_parse_row_friends(user_ID)  # list of one-hop-friends
            F_two_hop = self.friends_list_inmemory.two_parse_row_friends(user_ID)  # list of exac-two-hop-friends
            tmp = V_one_hop + F_two_hop  # 2 hop general friend set
            result = set(tmp)
            expanding_vertex = F_two_hop
            current_hop = current_hop + 2

        while current_hop < hop:
            if current_hop + 1 < hop:
                for vertex in expanding_vertex:
                    V_one_hop = self.friends_list_inmemory.one_parse_row_friends(vertex)  # list of one-hop-friends
                    tmp.extend(V_one_hop)
                    #친구 set에 2 hop general friend set에 추가해주기
                tmp=set(tmp)
                result = result.union(tmp)
                expanding_vertex = tmp
                tmp=list()
                current_hop=current_hop+1
            else:   # the last trial, generating social counting filter SCF를 만드는 phase이다.
                tmp=list()
                for vertex in expanding_vertex:
                    V_one_hop = self.friends_list_inmemory.one_parse_row_friends(vertex)  # list of one-hop-friends
                    tmp.extend(V_one_hop)
                    #친구 set에 2 hop general friend set에 추가해주기
                result = result.union(tmp)
                current_hop=current_hop+1

        time_cost = time.time() - start_time2
        return (result.difference({user_ID}), time_cost)     #foot_print_set 을 반환해준다.

# ### CODE FOR TEST
# parse_friend_data_obj = parse_dataset_file.ParseDatasetFile("Barabasi_60K_lvOneFri.csv", "Barabasi_60K_lvTwoFri.csv")
# _m=MakeFriendList(parse_friend_data_obj)
# print("parsing obj")
# # phase 1
# time2=0
# time1=0
# result1=[]
# result2=[]
# k=1
#
# for k in range(1,10):
#     (result1, tmp_time2)=_m.friend_list_with_SCF(k, 3)
#     time2=time2+tmp_time2
#     # # phase 2
#     (result2, tmp_time1)=_m.get_n_hop_friend_list(k, 3)
#     time1 = time1 + tmp_time1
#
# ## TEST RESULT
# print("vertex : "+str(k))
# print("scf"+str(result1))
# print("naive"+str(result2))
# print(result1.difference(result2))
# print(result2.difference(result1))
# print("scf:" + str(time2))
# print("naive:" + str(time1))
# print("end")