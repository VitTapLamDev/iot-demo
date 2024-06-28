from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

import json
import pymysql.cursors
import os 

from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Create your views here.
@csrf_exempt
def index(request):
    return render(request, "web/index.html")

@require_http_methods(["POST"])
@csrf_exempt
def sensor_data(request):
    if request.method == "POST":
        fire_alarm = False
        body_content = json.loads(request.body)
        
        temperature = body_content["temperature"]
        humidity    = body_content["humidity"]
        lux         = body_content["lux"]
        
        print(f"temperature: {temperature}")
        print(f"humidity: {humidity}")
        print(f"lux: {lux}")
        
        if (temperature >= 60 and humidity <= 20) or (lux >= 1200):
            fire_alarm = True
        connection = pymysql.connect(
            host=os.getenv('DATABASE_HOST'),
            user=os.getenv('DATABASE_USERNAME'),
            password=os.getenv('DATABASE_PASSWORD'),
            database=os.getenv('DATABASE_NAME'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        print(connection)
        with connection:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `sensor_data` (`temperature`, `humidity`, `lux`, `fire_alram`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (temperature, humidity, lux, fire_alarm))
            connection.commit()
            
        return JsonResponse({"text": "Succesfully send data !!!"})
    else:
        return JsonResponse({"text": "Method not allowed !!!"})

@csrf_exempt
def data_sensor(request):
    return render(request, "web/data_sensor.html")
    
@csrf_exempt
def data(request):
    if request.method == "GET":
        connection = pymysql.connect(
            host=os.getenv('DATABASE_HOST'),
            user=os.getenv('DATABASE_USERNAME'),
            password=os.getenv('DATABASE_PASSWORD'),
            database=os.getenv('DATABASE_NAME'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        print(connection)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `sensor_data`"
                cursor.execute(sql)
                results = cursor.fetchall()
                results = [{k: v.isoformat() if isinstance(v, datetime) else v for k, v in d.items()} for d in results]
                return JsonResponse(results, safe=False)    
        
