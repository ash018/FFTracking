from django.db import models
from django.db import connection, connections
import json
from datetime import datetime
from sqlserver_ado.fields import LegacyDateTimeField
import urllib3
import urllib.request

class CurrentMSRLocation(models.Model):
    Userid = models.CharField(max_length=50, db_column='Userid',  primary_key=True)
    Level1Name = models.CharField(max_length=50, db_column='Level1Name')
    UpazilaCode = models.CharField(max_length=50, db_column='UpazilaCode')
    UpazilaName = models.CharField(max_length=50, db_column='UpazilaName')
    Time = models.DateTimeField()
    Latitude = models.FloatField(db_column='Latitude')
    Longitude = models.FloatField(db_column='Longitude')

    class Meta:
        managed = False
        db_table = 'vwmmCurrentMSRLocation'


class PlaceLocation(models.Model):
    Userid = models.CharField(max_length=50, db_column='Userid',  primary_key=True)
    PlaceType = models.CharField(max_length=50, db_column='Level1Name')
    Latitude = models.FloatField(db_column='Latitude')
    Longitude = models.FloatField(db_column='Longitude')
    Time = models.DateTimeField()


    class Meta:
        managed = False
        db_table = 'vwmmPlaceLocation'

class MSRMovement(models.Model):
    ID = models.CharField(max_length=50, db_column='ID',  primary_key=True)
    Latitude = models.FloatField(db_column='Latitude')
    Longitude = models.FloatField(db_column='Longitude')
    Userid = models.CharField(max_length=50, db_column='Userid')
    ServerTime = models.DateTimeField()
    #UpazilaCode = models.CharField(max_length=50, db_column='UpazilaCode')
    #UpazilaName = models.CharField(max_length=50, db_column='UpazilaName')
    #Level1Name = models.CharField(max_length=50, db_column='Level1Name')

    class Meta:
        managed = False
        db_table = 'vwmmMSRmovement'


def GetCurrentMSRLocation():
    cur = connections['MotorDashboard'].cursor()
    cur.execute("SELECT *  FROM  vwmmCurrentMSRLocation")
    result = dictfetchall(cur)
    cur.close()
    return result

def GetPlaceLocation():
    cur = connections['MotorDashboard'].cursor()
    cur.execute("""SELECT [PlaceId]
                          ,[PlaceType]
                          --,[PlaceName]
                          --,[PlaceAddress]
                          ,[Latitude]
                          ,[Longitude]
                          ,PLACE.[EntryBy] as UserId
                          ,[Level1Name]
                          ,[EntryDate]
                          ,[TypeName] 
                          ,COVER.Coverage1
                          ,COVER.Coverage2
                          ,COVER.Coverage3
                    FROM  vwmmPlaceLocation PLACE
                    LEFT JOIN [dbo].[MSRCoverage] COVER ON PLACE.Entryby = COVER.UserId
                    WHERE PlaceId NOT IN (269, 410, 414)""")
    result = dictfetchall(cur)
    cur.close()
    return result

def GetBoundedPlaceLocationData(latUpper, latBottom, lngUpper, lngBottom):
    cur = connections['MotorDashboard'].cursor()
    cur.execute("""SELECT [PlaceId]
                      ,[PlaceType]
                      ,[PlaceName]
                      --,[PlaceAddress]
                      ,[Latitude]
                      ,[Longitude]
                      ,PLACE.[EntryBy] as UserId
                      ,[Level1Name]
                      ,[EntryDate]
                      ,[TypeName] 
                      ,COVER.Coverage1
                      ,COVER.Coverage2
                      ,COVER.Coverage3
                FROM  vwmmPlaceLocation PLACE
                LEFT JOIN [dbo].[MSRCoverage] COVER ON PLACE.Entryby = COVER.UserId
                WHERE PlaceId NOT IN (269, 410, 414)
                and Latitude <= """ + str(latUpper) + " and Latitude >= "  + str(latBottom) + " and Longitude <= " + str(lngUpper) + " and Longitude >= " + str(lngBottom))
    result = dictfetchall(cur)
    cur.close()
    return result


def GetInitialMSRPosition():
    cur = connections['MotorDashboard'].cursor()
    cur.execute("""SELECT  DISTINCT T1.ID,
                        T1.[UserId]
                        ,[Level1Name]
                        ,[Latitude] as Latitude
                        ,[Longitude] as Longitude
                        ,ServerTime AS MaxUpdateTime
                FROM ( 
                        SELECT [UserId], MAX(ID) as ID,  MAX([ServerTime]) as MaxUpdateTime
                        FROM [dbo].[vwmmMSRmovement] 
						WHERE CAST( [ServerTime] as DATE) = CAST(GETDATE() as DATE)
                        GROUP BY [UserId]
                ) as T1 
                INNER JOIN [dbo].[vwmmMSRmovement] as T2 ON T1.UserId = T2.UserId AND T1.MaxUpdateTime = T2.ServerTime AND T1.ID = T2.ID
				WHERE CAST(MaxUpdateTime as DATE) = CAST(GETDATE() as DATE)
                order by T1.[UserId] """)
    result = dictfetchall(cur)
    cur.close()
    return result

def GetInitialPharmaFFPosition():
    cur = connections['DCR'].cursor()
    cur.execute("""SELECT  DISTINCT T1.ID,
                        T1.[UserId]
                        ,[Level1Name]
                        ,[Latitude] as Latitude
                        ,[Longitude] as Longitude
                        ,ServerTime AS MaxUpdateTime
                FROM ( 
                        SELECT [UserId], MAX(ID) as ID,  MAX([ServerTime]) as MaxUpdateTime
                        FROM [dbo].ViewFFMovement 
						WHERE CAST( [ServerTime] as DATE) = CAST(GETDATE() as DATE)
                        GROUP BY [UserId]
                ) as T1 
                INNER JOIN [dbo].ViewFFMovement as T2 ON T1.UserId = T2.UserId AND T1.MaxUpdateTime = T2.ServerTime AND T1.ID = T2.ID
				WHERE CAST(MaxUpdateTime as DATE) = CAST(GETDATE() as DATE)
                order by T1.[UserId] """)
    result = dictfetchall(cur)
    cur.close()
    return result


def dictfetchall(cur):
    dataset = cur.fetchall()
    columns = [col[0] for col in cur.description]
    return [
        dict(zip(columns, row))
        for row in dataset
        ]
