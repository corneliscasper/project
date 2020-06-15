from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_id_actuator(id):
        sql = "SELECT DATE_FORMAT(datum,'%d-%m-%Y') as Datum ,count(Actuatorid) as AantalDranken from Historie where ActuatorId= %s group by DATE_FORMAT(datum,'%d-%m-%Y')"
        params=[id]
        return Database.get_rows(sql,params)

    @staticmethod
    def create_new_row(datum,waarde,status,sensorId,ActuatorId):
        
        sql = "insert into project1.Historie(Datum,Waarde,Status,actuatorid,sensorid) VALUES(%s,%s,%s,%s,%s)"
        params=[datum,waarde,status,sensorId,ActuatorId]
        print(sql)
        #params=[datum,status_US,status,actuatorId,sensorId]
        return Database.execute_sql(sql,params)
    