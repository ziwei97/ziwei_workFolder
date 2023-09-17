'''
change the excel file below, and run "python biopsy_burnDegree.py", 
will generate the "burnDegree_colorcode.csv" under the same folder of your biopsy excel file
'''


import pandas as pd

columns = ['Accession#', 'Location#', 'SubjectID', 'StudyID', 'BiopsyID', 'Location', 'R.L', 'Site', 'Other', 
'PERCENT >50%', 'Viable Papillary Dermis', 'Reticular Dermis', 'DEGENERATION OF RETICULAR DERMIS COLLAGEN',
'Total # of Necrotic & Viable', 'Total # of Necrotic Only', 'DEGREE OF THROMBOSIS']

colorMap = {
    '1st Degree Burn': '[44 160 44]',
    'Superficial 2nd Degree Burn':'[31 119 180]',
    'Deep 2nd Degree Burn':'[255 127 14]',
    '3rd Degree Burn': '[214 39 40]',
    'skip': 'None',
    'Wrong': 'None'
}

def decision_tree_B(pn, drdc, dt):
    '''
    pn: "Total # of Necrotic Only / Total # of Necrotic & Viable"
    drdc:'DEGENERATION OF RETICULAR DERMIS COLLAGEN'
    dt: 'DEGREE OF THROMBOSIS'
    
    '''
    if pn or drdc or dt:
        if pn >= 0.5 or drdc >= 3 or dt >= 3:
            return '3rd Degree Burn'
        else:
            return 'Deep 2nd Degree Burn'
    else:
        return 'Superficial 2nd Degree Burn'

if __name__ == '__main__':
    # change the excel file path here!
    excel_file_path = '/Users/ziweishi/Downloads/BurnStudyReporting-20230-08-03.xlsx'
    df = pd.read_excel(excel_file_path, sheet_name="DV HH")


    new_df = pd.DataFrame(df.values[2:, ], columns = columns)
    burn_degree = []
    color = []
    for i in range(len(new_df)):
        
        tno = str(new_df['Total # of Necrotic & Viable'][i])
        tna = str(new_df['Total # of Necrotic & Viable'][i])
        drdc_n = str(new_df['DEGENERATION OF RETICULAR DERMIS COLLAGEN'][i]).split('+')[0]
        dt_n = str(new_df['DEGREE OF THROMBOSIS'][i]).split('+')[0]
            
        if tno.isnumeric() and tna.isnumeric():
            if new_df['Total # of Necrotic & Viable'][i] != 0:
                pn = new_df['Total # of Necrotic Only'][i] / new_df['Total # of Necrotic & Viable'][i]
            else:
                pn = 0 
        else:
            pn = 'NA'
        
        if drdc_n.isnumeric():
            drdc = float(str(new_df['DEGENERATION OF RETICULAR DERMIS COLLAGEN'][i]).split('+')[0])
        else:
            drdc = new_df['DEGENERATION OF RETICULAR DERMIS COLLAGEN'][i]
        if dt_n.isnumeric():
            dt = float(str(new_df['DEGREE OF THROMBOSIS'][i]).split('+')[0])
        else:
            dt = new_df['DEGREE OF THROMBOSIS'][i]
        import numbers
        if isinstance(drdc,  numbers.Number) and isinstance(dt,  numbers.Number) and isinstance(pn, numbers.Number):
            
            res = decision_tree_B(pn, drdc, dt)
        else:
            res = 'Wrong'
        burn_degree.append(res)
        color.append(colorMap[res])

    new_df['RGB_colorcode'] = color
    new_df['burn_degree'] = burn_degree

    save_path = excel_file_path.replace('.xlsx',  ' BurnDegree and colorcode.csv')
    new_df.to_csv(save_path, index=False)
    print('Done!')



    