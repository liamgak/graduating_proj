import numpy as np

"""
CSV col.: UserID,STime,ETime,SLati,SLongiti,ELati,ELongi
"""
class QueryDatabase():
    database=np.arange(10) #"numpy array Virtual database"
    length_of_cell="length of cell"

    def __init__(self, length_of_cell=10, numpy_mat=""):
        # numpy array: UserID(i4), STime(i4), ETime(i4), SLati, SLongti, ELati, ELongi
        self.database=numpy_mat
        self.length_of_cell=length_of_cell

    def SELECT_row_WHERE_userid(self, UserID):
        """
        TESTING CODE: print(query_obj.SELECT_row_WHERE_id(100))
        :param UserID:
        :return: a row(numpy array) that has information about user.ID=UserID
        """
        row=self.database[UserID]
        return row

    def SELECT_cell_num_WHERE_userid(self, UserID):
        """
        TESTING CODE: print(query_obj.SELECT_cell_num_WHERE_userid(100,10))
        :param UserID:
        :param length_of_cell:
        :return: tuple(Start_cell_number, End_cell_number)
        """
        row=self.SELECT_row_WHERE_userid(UserID)

        s_x = int(row['SLati'] / self.length_of_cell)
        s_y=int(row['SLongiti']/self.length_of_cell)
        e_x = int(row['ELati'] / self.length_of_cell)
        e_y=int(row['ELongi']/self.length_of_cell)

        # return cell index
        return ((s_x, s_y), (e_x, e_y))

    def SELECT_position_WHERE_userid(self, UserID):
        row=self.SELECT_row_WHERE_userid(UserID)

        s_x = row['SLati']
        s_y= row['SLongiti']
        e_x = row['ELati']
        e_y= row['ELongi']

        # return cell index
        return ((s_x, s_y), (e_x, e_y))

    def SELECT_time_WHERE_userid(self, UserID):
        row=self.SELECT_row_WHERE_userid(UserID)

        s_t = row['STime']
        e_t = row['ETime']

        # return tuple
        return (s_t, e_t)

    def SELECT_s_time_WHERE_userid(self, UserID):
        row = self.SELECT_row_WHERE_userid(UserID)
        s_t = row['STime']

        return s_t

    def SELECT_e_time_WHERE_userid(self, UserID):
        row = self.SELECT_row_WHERE_userid(UserID)
        e_t = row['ETime']

        return e_t
