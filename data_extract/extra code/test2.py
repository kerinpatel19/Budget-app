import data_sorter

sorter = data_sorter.line_extract()

file_path = '/Users/kerinpatel/Desktop/20240123-statements-1859--2.pdf'

return_list = sorter.extract_lines(file_path)


for x in return_list:
    print(x)

