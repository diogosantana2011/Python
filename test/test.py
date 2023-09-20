def gameType_filter_values(filter_values):
    for filter in filter_values:
        print(f'//li[@data-option-value="{filter}"]')
        
values = ['Live Game', 'Lottery Game', 'Other Game Type']       
gameType_filter_values(values)