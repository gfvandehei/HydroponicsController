# REDIS Key design

## For system sensor data
### Keys
System:`systemid`:sensor:`sensortype`:`sensor id`

## Values
### DHT
```json
{
    "temperature": "float",
    "humidity": "float"
}    
```