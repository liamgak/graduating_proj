class ParseDatasetFile():
    file_name="" #file_path
    file_name_csv=""
    __file_one_hop_friend="GowallaAmerica_LvOneFri.csv"
    __file_two_hop_friend="GowallaAmerica_LvTwoFri.csv"
    exac_two_hop_friends_list=dict()
    one_hop_friends_list=dict()

    def __init__(self, file_one_hop_friend="BrightkiteEurope_LvOneFri.csv", file_two_hop_friend="BrightkiteEurope_LvTwoFri.csv"):
        #self.file_name=file_name
        self.__file_one_hop_friend = file_one_hop_friend
        self.__file_two_hop_friend = file_two_hop_friend
        self.one_hop_friends_list = self.upload_friends_file(self.__file_one_hop_friend)
        self.exac_two_hop_friends_list = self.upload_friends_file(self.__file_two_hop_friend)

    def get_one_hop_filename(self):
        return self.__file_one_hop_friend

    def get_two_hop_filename(self):
        return self.__file_two_hop_friend

    def get_num_user(self):
        return len(self.one_hop_friends_list)

    def txt_to_csv(self, file_name):
        ### 수정이 필요한 함수
        with open(file_name, 'r') as dataset_txt:
            S=dataset_txt.read()
            S=S.replace('	', ',')
            D=file_name.split('.')[0] #filename without extension

            file_name_csv=D
            # CAUTION: if csv file is opend by excel, you will see float has the smaller precision.
            with open(D+'.csv','w') as dataset_csv:
                dataset_csv.write(S)

    def upload_friends_file(self, file_name):
        """ dict() which has the entire information about friends, storting <user_id: user_friend_list>
        """
        result_dict = dict()

        with open(file_name, 'r') as frineds_file:
            S=frineds_file.read()
            print(S.split('\n')[0])
            S=S.split('\n')[1:] # remove header
            for row in S:   # traversing each row in csv
                if row is '':   # ignoring the last \n, if that is exist
                    continue
                str_to_list=row.split(',')
                user_id = str_to_list[0]    # parsing userid
                freind_list_size= str_to_list[1]    # size of list
                user_friend_list = str_to_list[2:] # parsing friends list of specific userid
                user_friend_list = list(map(int, user_friend_list)) # converting str to int
                result_dict[int(user_id)]=user_friend_list  # storting <user_id: user_friend_list>
        return result_dict

    def one_parse_row_friends(self, userID):
        """input is the specific UserID
        :return: List of user's friends (List(int) built-in python)
        """
        return self.one_hop_friends_list[userID]

    def two_parse_row_friends(self, userID):
        return self.exac_two_hop_friends_list[userID]


#CODE FOR TEST
# _pfs=ParseDatasetFile()
# _pfs.file_name="BrightkiteEurope_LvTwoFri.txt"
# # _pfs.txt_to_csv("Barabasi_200K_LvOneFri.txt")
# # _pfs.txt_to_csv("Barabasi_70K_LvOneFri.txt")
# # _pfs.txt_to_csv("Barabasi_80K_SpatioTemporal.txt")
# # _pfs.txt_to_csv("Barabasi_90K_SpatioTemporal.txt")
# _pfs.txt_to_csv("Barabasi_200K_SpatioTemporal.txt")
# _pfs.txt_to_csv("Barabasi_300K_SpatioTemporal.txt")
# _pfs.txt_to_csv("Barabasi_600K_LvOneFri.txt")
# _pfs.txt_to_csv("Barabasi_900K_LvOneFri.txt")
#
# _pfs.txt_to_csv("Barabasi_60K_LvTwoFri.txt")
# _pfs.txt_to_csv("Barabasi_70K_LvTwoFri.txt")
# _pfs.txt_to_csv("Barabasi_80K_LvTwoFri.txt")
# _pfs.txt_to_csv("Barabasi_90K_LvTwoFri.txt")
# _pfs.txt_to_csv("Barabasi_100K_LvTwoFri.txt")
# _pfs.txt_to_csv("Barabasi_300K_LvTwoFri.txt")
# _pfs.txt_to_csv("Barabasi_600K_LvTwoFri.txt")
# _pfs.txt_to_csv("Barabasi_900K_LvTwoFri.txt")
#다 하면 INDEX OBJ로 가서 전부다 객체 생성 해버리기. >> index파일 만들어진다.

# start_time = time.time()
#print(_pfs.two_parse_row_friends(30))
# print("A--- %s seconds ---" % (time.time() - start_time))
#parse_friend_data_obj = ParseDatasetFile()

#_pws=ParseDatasetFile('GowallaAmerica_LvTwoFri.txt')
#_p.txt_to_csv()
#_pfs.txt_to_csv()
#_pws.txt_to_csv()