import heapq

candidate_heap = []


def add_candidate(candidate):

    # Store negative score for max heap behaviour
    heapq.heappush(candidate_heap, (-candidate["score"], candidate))


def get_ranked_candidates():

    sorted_candidates = sorted(candidate_heap)

    ranked_list = []

    for score, candidate in sorted_candidates:

        candidate_copy = candidate.copy()

        # restore positive score
        candidate_copy["score"] = -score

        ranked_list.append(candidate_copy)

    return ranked_list