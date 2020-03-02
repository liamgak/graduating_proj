import make_friend_list

class ComputeGroup():
    seats=123 # integer
    social_boundary=123 # integer
    cumulative_friend_list=dict()
    make_friend_list="make_friend obj"
    exist_group=list()
    query_obj="query obj"

    def __init__(self, m, l, make_friend_list_obj, query_obj):
        self.seats=m
        self.social_boundary=l
        self.cumulative_friend_list=dict()
        self.make_friend_list=make_friend_list_obj
        self.query_obj=query_obj

    def compute_group(self, candidate_list, new_vertex):
        """
        :param candidate_list: candidate_list=tree_algorithm.MinHeap_moving_cost(p, query_obj)
        :param new_vertex: newly found vertex
        :return:
        """
        intermidiate_set=set()
        candidate_list.insert(new_vertex)
        candidate_list_size=len(candidate_list.heap)

        # FOR TEST
        # new_vertex_friends=make_friend_list.MakeFriendList(new_vertex, self.social_boundary)
        print("seats: "+str(self.seats))
        print("size: "+str(candidate_list_size-1))

        if candidate_list_size-1>= self.seats:  #candidate list include "None" element
            # Finding group
            #self.exist_group.append({new_vertex})
            new_group = self.find_min_group(new_vertex, candidate_list)
            print(new_group)
        else:
            # No action
            #self.exist_group.append({new_vertex})
            new_group = self.find_min_group(new_vertex, candidate_list)
            print(new_group)
            return

    def find_min_group(self, new_vertex, candidate_list):
        """ Finding group algorithm built on the logical binomial tree.
        :return: if there is no group, return false. else, return a group which has minimum moving cost.
        """
        #우리는 added_group_list에서 3개가 나왔다면 거기서 찾으면 된다.
        added_group_list, minimum_group = self.expand_binomial_tree_and_find_minimum(self.exist_group, candidate_list, new_vertex)
        #merge phase
        self.exist_group=self.merge_two_group(self.exist_group, added_group_list)
        print(self.exist_group)

    def expand_binomial_tree_and_find_minimum(self, group_list, candidate_list, new_vertex):
        """
        :param group_list: copied group list
        :param new_vertex:
        :return: no return
        """
        copied_list=group_list.copy()
        copied_list.append({new_vertex})

        len_group_list=len(copied_list)
        new_group_list=[]
        minimum_cost=1000
        minimum_group=set()

        for index in range(len_group_list):
            not_checked_group=copied_list[index].union({new_vertex})
            if self.check_group_is_friend(not_checked_group):
                if len(not_checked_group)==3:
                    moving_cost_of_group=self.sum_of_moving_cost(not_checked_group, candidate_list)
                    if minimum_cost>=moving_cost_of_group:
                        minimum_cost=moving_cost_of_group
                        minimum_group=not_checked_group
                        print("minimum_group:::")
                        print(minimum_group)
                else:
                    new_group_list.append(not_checked_group)  #social bound 속성을 만족시키는 그룹을 저장한다. 크기가 내림차순으로 저장되야 한다. 길이가 2 혹은 1인 그룹만 넘어간다.
        return new_group_list, minimum_group

    def sum_of_moving_cost(self, group, candidate_list):
        sum_mc=0
        for vertex in group:
            vertex_position=self.query_obj.SELECT_position_WHERE_userid(vertex)
            mc=candidate_list.moving_cost(vertex_position)
            sum_mc=sum_mc+mc
        return sum_mc

    def merge_two_group(self, first_group_list, second_group_list):
        merged_group_list=[]
        first_group_separated_index=0
        second_group_separated_index=0

        for i in first_group_list:
            if len(i)==1:
                break
            first_group_separated_index = first_group_separated_index+1

        for i in second_group_list:
            if len(i)==1:
                break
            second_group_separated_index = second_group_separated_index+1

        #merge
        merged_group_list = first_group_list[:first_group_separated_index] + second_group_list[:second_group_separated_index]
        merged_group_list = merged_group_list + first_group_list[first_group_separated_index:] + second_group_list[second_group_separated_index:]

        return merged_group_list

    def check_group_is_friend(self, group):
        """ if all elements are in friendship with each other, return true. else, false.
        :return: if all elements are in friendship with each other, return true. else, false.
        """
        return True