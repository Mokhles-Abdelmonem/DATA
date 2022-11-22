import json
from collectdata.models import BaseData, SaveData
import pandas as pd 
from io import StringIO


class DataProcess():
    def __init__(self,**kwargs):
        id = kwargs["pk"]
        data_obj = BaseData.objects.get(id=id)
        saved_data = SaveData.objects.filter(data_model=data_obj).order_by("-date")[0]
        data = StringIO(saved_data.saved_data)
        df = pd.read_csv(data,sep=",",index_col=False)
        kwargs["df"] = df
        df_processed = self.process(**kwargs)
        if df_processed.empty:
            self.result = True
        else:
            file_path = str(data_obj.base_file)
            df_processed.to_csv(file_path,index=False)
            data_obj.rows_num , data_obj.cols_num = df_processed.shape
            data_obj.nulls_num = df_processed.isnull().values.sum().sum()
            data_obj.duplicates_num = df_processed.duplicated().any().sum()
            data_obj.save()
            SaveData.objects.create(data_model=data_obj, saved_data=df_processed.to_csv(index=False))
            self.result = "success"

    def process(self,**kwargs):
        pass
    def df_empty(self,**kwargs):
        return self.result
    
class DropColumn(DataProcess):
    def process(self,**kwargs):
        df = kwargs["df"]
        column = kwargs["value1"]
        df_droped = df.drop(columns=[column])
        return df_droped

class DropNaInCol(DataProcess):
    def process(self,**kwargs):
        df = kwargs["df"]
        column = kwargs["value1"]
        df_droped  = df[df[column].notna()]
        return df_droped

class DropNaAll(DataProcess):
    def process(self,**kwargs):
        df = kwargs["df"]
        axis = kwargs["value1"]
        df_droped = df.dropna(axis=int(axis))
        return df_droped

class FillNaAll(DataProcess):
    def process(self,**kwargs):
        df = kwargs["df"]
        fillvalue = kwargs["value1"]
        df_droped = df.fillna(fillvalue)
        return df_droped

class FillNaInCol(DataProcess):
    def process(self,**kwargs):
        df = kwargs["df"]
        column = kwargs["value1"]
        fillvalue = kwargs["value2"]
        df[column] = df[column].fillna(fillvalue)
        return df

class SplitCol(DataProcess):
    def process(self,**kwargs):
        df = kwargs["df"]
        column = kwargs["value1"]
        sep = kwargs["value2"]
        splited_columns = df[column].str.split(sep, expand=True)
        # splited_columns = df.stack().str.split("\t",expand=True).unstack().swaplevel(axis=1)[df.columns]
        df[[f'New Column{index+1}' for index in splited_columns ]] = splited_columns
        return df

class RenameColumn(DataProcess):
    def process(self,**kwargs):
        df = kwargs["df"]
        column = kwargs["value1"]
        new_name = kwargs["value2"]
        df.rename(columns={column:new_name}, inplace=True)
        return df


class UnDo():
    def __init__(self,**kwargs):
        id = kwargs["pk"]
        data_obj = BaseData.objects.get(id=id)
        all_saved_data = SaveData.objects.filter(data_model=data_obj).order_by("-date")
        self.result = False
        if len(all_saved_data) > 1 :
            saved_data = all_saved_data[0]
            saved_data.delete()

            saved_data = SaveData.objects.filter(data_model=data_obj).order_by("-date")[0]
            data = StringIO(saved_data.saved_data)
            df = pd.read_csv(data,sep=",",index_col=False)
            kwargs["df"] = df
            file_path = str(data_obj.base_file)
            df.to_csv(file_path,index=False)
            data_obj.rows_num , data_obj.cols_num = df.shape
            data_obj.nulls_num = df.isnull().values.sum().sum()
            data_obj.duplicates_num = df.duplicated().any().sum()
            data_obj.save()
            self.result = False
        
    def df_empty(self,**kwargs):
        return self.result

class JoinStrCol(DataProcess):
    def process(self,**kwargs):
        df = kwargs["df"]
        column = kwargs["value1"]
        columns = kwargs["valueslist"]
        for col in columns:
            df[column] += df[col]
        return df

class DropDuplicates(DataProcess):
    def process(self,**kwargs):
        df = kwargs["df"]
        df = df.drop_duplicates()
        return df

class RerangeColumn(DataProcess):
    def process(self,**kwargs):
        df = kwargs["df"]
        column = kwargs["value1"]
        the_direction = kwargs["value2"]
        temp_cols = df.columns.tolist()
        index = df.columns.get_loc(column)
        new_cols = self.get_new_cols(temp_cols, index, the_direction)
        df=df[new_cols]
        return df

    def get_new_cols(self, list, index, the_direction):
        if the_direction == "right":
            if index+1 < len(list) :
                list = list[0:index]  + [list[index+1], list[index]] + list[index+2:]
            return list
        if the_direction == "left":
            if index > 0 :
                list = list[0:index-1]  + [list[index],list[index-1]] + list[index+1:]
            return list
        if the_direction == "first":
            return list[index:index+1] + list[0:index] + list[index+1:]
        if the_direction == "last":
            return list[0:index] + list[index+1:] + list[index:index+1]


class SaveEditable(DataProcess):
    def process(self,**kwargs):
        df = kwargs["df"]
        changes = kwargs["value3"]
        changes = json.loads(changes)
        for key, value in changes.items() :
            x , y = key.split(',')
            df.iat[int(x), int(y)] = value
        return df
