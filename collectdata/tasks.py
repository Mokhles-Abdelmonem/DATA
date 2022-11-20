from celery import shared_task
import subprocess
import pandas as pd
from .models import BaseData , SaveData


@shared_task
def refine_task(obj_id):
    data_obj = BaseData.objects.get(id=obj_id)
    file_path = str(data_obj.base_file)
    full_file_name = file_path.split('/')[-1]
    file_name_parts = full_file_name.split('.')
    file_name = file_name_parts[0]
    extention = file_name_parts[1]
    if extention in ['xlsx', 'xls','ods'] :
        df = pd.read_excel(f'mydocs/{full_file_name}')

    else:
        sep_dict = {'csv':',','tsv':'\t'}
        sep = sep_dict.get(extention)
        try:
            df = pd.read_csv(f'mydocs/{full_file_name}', sep=sep)
        except:
            cmd1 = f'openrefine-client_0-3-10_windows.exe --create mydocs/{full_file_name} --encoding=UTF-8'
            cmd2 = f'openrefine-client_0-3-10_windows.exe --export --output=mydocs/refined_{file_name}.csv "{file_name}"'
            result1 = subprocess.call(cmd1, shell=True)
            result2 = subprocess.call(cmd2, shell=True)
            df = pd.read_csv(f'mydocs/refined_{file_name}.csv',sep=",")
            

    data_obj.rows_num , data_obj.cols_num = df.shape
    data_obj.nulls_num = df.isnull().values.sum().sum()
    data_obj.duplicates_num = df.duplicated().any().sum()
    data_obj.save()
    SaveData.objects.create(data_model=data_obj, saved_data=df.to_csv(index=False))
    return 'task finished successfully'
