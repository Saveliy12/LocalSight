from sqlite_req import main

'''
1. Делать все не перебором, а по каждому sight_id из sorted_sights_id делать запрос к SIGHTS по id
'''
# main('DELETE FROM Reactions WHERE ...')

def most_popular_sights():
    rcts = main(f"SELECT userid, messageid, flag FROM Reactions")
    sights = main(f'SELECT id, area, year, season, month, description, feedback, mark, tags, src FROM Sights')
    sights_id = set() # список всех id (из таблицы SIGHTS) мест

    for rct_id in rcts:
        sights_id.add(rct_id[1])

    def count_repeats(sights_id):
        repeat_sights = {}
        for sight_id in sights_id:
            like = 0
            dis = 0
            flags = main(f'SELECT flag FROM Reactions WHERE `messageid` = {sight_id}')
            for flag in flags:
                if flag[0] == 1:
                    like = like + 1
                elif flag[0] == 0:
                    dis = dis + 1
                else:
                    print('Error: count_repeats')
            count_reactions = like - dis
            repeat_sights.update({sight_id: count_reactions})
        return repeat_sights

    repeat_sights = count_repeats(sights_id) # словарь ключ - id (из таблицы SIGHTS), ключ - сколько раз повторяется в таблице
    sorted_sights_dict = dict(sorted(repeat_sights.items(), key=lambda item: item[1], reverse=True)) # отсортированный по значениям repeat_sights
    sorted_sights_id = [] # отсортированные по "популярности" id (из таблицы SIGHTS) мест 
    sorted_rcts = [] # отсортированный по "популярности" список мест (из таблицы SIGHTS)
    # формируем список id, отсортированных по значению словаря sorted_sights_dict
    for sight_id in sorted_sights_dict:
        sorted_sights_id.append(sight_id)

    # формируем список мест по популярности (из всех мест) по популярности (по id) из массива sorted_sights_id
    for sight_id in sorted_sights_id:
        for sight in sights:
            if sight_id == sight[0]:
                sorted_rcts.append(sight)

    return sorted_rcts