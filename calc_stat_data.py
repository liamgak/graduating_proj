import numpy as np
import math


def get_distance(cell_driver, cell_customer): #cell[0] : lat, cell[1] : long
    joint_dist = min(abs(cell_customer[0] - cell_driver[0]), abs(cell_customer[1] - cell_driver[1]))
    union_dist = max(abs(cell_customer[0] - cell_driver[0]), abs(cell_customer[1] - cell_driver[1]))
    m_dist = round((joint_dist * math.sqrt(2)) + (union_dist - joint_dist))
    return m_dist


def get_prob_prior(result, val, i):  # val = distance, i=0 -> predict(len), i=1 -> class(dst)
    total_cnt = 0
    prob_cnt = 0

    for c in result.values():
        total_cnt += c
    for key in result.keys():
        if key[i] == val:
            prob_cnt += result[key]

    try:
        return prob_cnt / total_cnt
    except:
        return 0


def get_prob_for_likelihood(result, vlen, dst):
    total_cnt = 0
    prob_cnt = 0
    p_prior = get_prob_prior(result, dst, 1)

    for c in result.values():
        total_cnt += c

    for key in result.keys():
        if key == (vlen, dst):
            prob_cnt += result[key]
            break

    try:
        return prob_cnt / total_cnt / p_prior
    except:
        return 0


def get_posterior(result, vlen, dst): #(dist|vlen)
    try:
        return get_prob_for_likelihood(result, vlen, dst) * get_prob_prior(result, dst, 1) / get_prob_prior(result,
                                                                                          vlen, 0)
    except:
        return 0


def add_gaussian(mean, sigma, org_prob, dist):  # mean = 0, dist difference 0 -> probability maximization
    g = 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(- (dist - mean) ** 2 / (2 * sigma ** 2))
    return g + org_prob


def get_posterior_list(result):
    posterior_list = dict()
    for key in result.keys():
        posterior_list[key] = get_posterior(result, key[0], key[1])
    return posterior_list


def add_post_gauss(post_list):
    weighted_posterior_list = dict()
    for key in post_list.keys():
        weighted_posterior_list[key] = add_gaussian(0, 20, post_list[key], key[1])
    return weighted_posterior_list
