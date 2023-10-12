rus_raw = """январь
февраль
март
апрель
май
июнь
июль
август
сентябрь
октябрь
ноябрь
декабрь"""

eng_raw = """January
February
March
April
May
June
July
August
September
October
November
December"""

rus_list = rus_raw.split('\n')
eng_list = eng_raw.split('\n')

res_dict = {rus_list[i]: eng_list[i] for i in range(len(rus_list))}

print(res_dict)