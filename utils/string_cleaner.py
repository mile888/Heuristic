def trim(q):

    word_list = q.lower().replace("hai", "").split()
    if len(q) > 0:
        phrase = " ".join(word_list[1:]) if word_list[0] in [",", ";"] else " ".join(word_list[:])
        return phrase
    else:
        return " ".join(word_list)