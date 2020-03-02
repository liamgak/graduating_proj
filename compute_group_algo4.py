import copy

class ComputeGroup_algo4():
    def __init__(self, members, user_position, query_obj):
        self.members=members
        self.user_position=user_position
        self.query_obj=query_obj

    def find_min_mc_group(self, new_vertex, candidate_list, m):
        """ Finding new group which has minimum moving-cost and include new vertex
        :param new_vertex: candidate_vertex
        :param candidate_list: candidate_list:: mc minheap
        :return: A new group which has minimum moving-cost and include new vertex
        """
        possible_group=list()
        best_group = set()
        best_score =10000
        len_of_CL=len(candidate_list.heap)

        #copied_candidate_list를 깊은 복사한다.
        copied_candidate_list=copy.deepcopy(candidate_list)
        ascending_list = list()

        # MC에 대한 오름차순 리스트 만들기
        while not copied_candidate_list.is_empty():
            ascending_list.append(copied_candidate_list.delete())

        if len_of_CL+1>= self.members:
            # 가능한 그룹 모두 추출
            possible_group = self.rec_combination(new_vertex, ascending_list, {new_vertex}, m)

        # 가능한 한 그룹에서 가장 좋은 그룹을 best_group으로 한다.
        for group in possible_group:
            cur_group_mc = self.group_moving_cost(group)
            if best_score > cur_group_mc:
                best_group = group
                best_score = cur_group_mc

        # Checked list new_vertex를 추가한다.
        candidate_list.insert(new_vertex)
        return best_group

    def find_min_mc_group_with_MFL(self, new_vertex, candidate_list, m):
        """ Finding new group which has minimum moving-cost and include new vertex
        :param new_vertex: candidate_vertex
        :param candidate_list: candidate_list:: mc minheap
        :return: A new group which has minimum moving-cost and include new vertex
        """
        possible_group=list()
        best_group = set()
        best_score =10000
        len_of_CL=len(candidate_list.heap)

        #copied_candidate_list를 깊은 복사한다.
        copied_candidate_list=copy.deepcopy(candidate_list)
        ascending_list = list()

        # MC에 대한 오름차순 리스트 만들기
        while not copied_candidate_list.is_empty():
            ascending_list.append(copied_candidate_list.delete())

        if len_of_CL+1>= self.members:
            # 가능한 그룹 모두 추출
            possible_group = self.rec_combination(new_vertex, ascending_list, {new_vertex}, m)

        # 가능한 한 그룹에서 가장 좋은 그룹을 best_group으로 한다.
        for group in possible_group:
            cur_group_mc = self.group_moving_cost(group)
            if best_score > cur_group_mc:
                best_group = group
                best_score = cur_group_mc

        # Checked list new_vertex를 추가한다.
        candidate_list.insert(new_vertex)
        return best_group

    def rec_combination(self, new_vertex, rest_vertex_list, current_set, m):
        tmp_result = list()
        tmp_rest_list = list()
        if len(current_set) == m-1:
            return [current_set]

        for rest_vertex in rest_vertex_list:
            # if rest_vertex in tmp:    //아마 친구 검사하는 파트?
                tmp_rest_list.append(rest_vertex)

        for index, vertex in enumerate(tmp_rest_list):
            for result_ in self.rec_combination(vertex, tmp_rest_list[index + 1:], current_set.union({vertex}),m):
                tmp_result.append(result_)
        return tmp_result

    def find_max_mc_vertex(self, group):
        maximum_cost=0
        optimal_vertex=-1
        for vertex in group:
            vertex_position=self.query_obj.SELECT_position_WHERE_userid(vertex)
            mc=self.moving_cost(vertex_position)
            if maximum_cost<=mc:
                maximum_cost=mc
                optimal_vertex=vertex
        return optimal_vertex

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

    def depart_aspect_cost(self, vertex):
        vertex_position = self.query_obj.SELECT_position_WHERE_userid(vertex)
        dist=self.dist(vertex_position[0], self.user_position[0])
        return dist

    def arrival_aspect_cost(self, vertex):
        vertex_position = self.query_obj.SELECT_position_WHERE_userid(vertex)
        dist=self.dist(vertex_position[1], self.user_position[1])
        return dist

    def group_moving_cost(self, group):
        sum_dist=0
        for vertex in group:
            vertex_position = self.query_obj.SELECT_position_WHERE_userid(vertex)
            sum_dist=sum_dist+self.moving_cost(vertex_position)
        return sum_dist