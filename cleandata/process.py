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
        SaveData.objects.create(data_model=data_obj, saved_data=df_processed.to_csv(index=False))
    def process(self,**kwargs):
        pass
    
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
        if len(all_saved_data) > 1 :
            saved_data = all_saved_data[0]
            saved_data.delete()



class JoinStrCol(DataProcess):
    def process(self,**kwargs):
        df = kwargs["df"]
        column = kwargs["value1"]
        columns = kwargs["valueslist"]
        for col in columns:
            df[column] += df[col]
        return df