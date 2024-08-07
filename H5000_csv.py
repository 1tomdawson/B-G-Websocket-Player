import asyncio
import websockets
import json
import csv
from datetime import datetime  
import os

# Define the ID names as a dictionary
idNames = {
    0: "ModesMessage",
    1: "Altitude",
    3: "PositionError",
    4: "Hdop",
    5: "Vdop",
    6: "Tdop",
    7: "Pdop",
    8: "GeoidalSeperation",
    9: "Cog",
    10: "PositionQuality",
    11: "PositionIntegrity",
    12: "SatsInView",
    13: "WaasStatus",
    14: "Bearing",
    15: "BearingWaypointWaypoint",
    17: "CourseToSteer",
    18: "CrossTrack",
    19: "VelocityMadeGood",
    20: "Destination",
    21: "DistanceToTurn",
    22: "DistanceToDest",
    23: "TimeToTurn",
    24: "TimeToDest",
    25: "EtaAtTurn",
    26: "EtaAtDest",
    27: "TotalDistance",
    28: "SteerArrow",
    29: "Odometer",
    30: "TripDistance",
    31: "TripTime",
    32: "Date",
    33: "Time",
    34: "UtcDate",
    35: "UtcTime",
    36: "LocalTimeOffset",
    37: "Heading",
    38: "Voltage",
    39: "CurrentSet",
    40: "CurrentDrift",
    41: "SpeedSog",
    42: "SpeedWater",
    43: "SpeedPitot",
    44: "SpeedTripAvg",
    45: "SpeedTripMax",
    46: "SpeedWindApp",
    47: "SpeedWindTrue",
    48: "TempWater",
    49: "TempOutside",
    50: "TempInside",
    51: "TempEngineRoom",
    52: "TempMainCabin",
    53: "TempLiveWell",
    54: "TempBaitWell",
    55: "TempRefrigeration",
    56: "TempHeatingSystem",
    57: "TempDewPoint",
    58: "TempWindChillApp",
    59: "TempWindChillTheoretic",
    60: "TempHeatIndex",
    61: "TempFreezer",
    62: "EngineTemp",
    63: "EngineAirTemp",
    64: "EngineOilTemp",
    65: "TempBattery",
    66: "PressureAtmospheric",
    67: "EngineBoostPres",
    68: "EngineOilPres",
    69: "EngineWaterPres",
    70: "EngineFuelPres",
    71: "EngineManifoldPres",
    72: "PressureSteam",
    73: "PressureComprAir",
    74: "PressureHydraulic",
    77: "Depth",
    78: "WaterDistance",
    79: "EngineRpm",
    80: "EngineTrim",
    81: "EngineAlternatorPotential",
    82: "EngineFuelRate",
    83: "EnginePercentLoad",
    84: "EnginePercentTorque",
    85: "SuzukiAlarmLevLo",
    86: "SuzukiAlarmLevHigh",
    87: "TankFuelLevel",
    88: "FluidLevelFreshWater",
    89: "FluidLevelGrayWater",
    90: "FluidLevelLiveWell",
    91: "FluidLevelOil",
    92: "FluidLevelBlackWater",
    93: "TankFuelRemaining",
    94: "FluidVolumeFreshWater",
    95: "FluidVolumeGrayWater",
    96: "FluidVolumeLiveWell",
    97: "FluidVolumeOil",
    98: "FluidVolumeBlackWater",
    99: "GenFluidVolume",
    105: "GenTankCapacity",
    106: "TankFuelCapacity",
    107: "TankCapacityFreshWater",
    108: "TankCapacityGrayWater",
    109: "TankCapacityLiveWell",
    110: "TankCapacityOil",
    111: "TankCapacityBlackWater",
    112: "TankFuelUsed",
    113: "EngineFuelUsed",
    114: "EngineFuelUsedTrip",
    115: "EngineFuelUsedSeasonal",
    116: "EngineFuelKValue",
    117: "BatteryPotential",
    118: "BatteryCurrent",
    119: "TrimTab",
    121: "RateOfTurn",
    122: "AttitudeYaw",
    123: "AttitudePitch",
    124: "AttitudeRoll",
    125: "MagneticVariation",
    126: "Deviation",
    127: "FuelEconomyWtr",
    128: "FuelEconomyGps",
    130: "FuelRangeWtr",
    131: "FuelRangeGps",
    132: "EngineHoursUsed",
    133: "EngineType",
    134: "VesselFuelRate",
    135: "VesselFuelEconomyWtr",
    136: "VesselFuelEconomyGps",
    137: "VesselFuelRemaining",
    138: "VesselFuelRangeWtr",
    139: "VesselFuelRangeGps",
    140: "WindAppAngle",
    141: "WindTrueAngle",
    142: "WindTrueDirection",
    143: "HumidityInside",
    144: "HumidityOutside",
    145: "SetHumidity",
    146: "RudderAngle",
    147: "TransGear",
    148: "TransOilPressure",
    149: "TransOilTemp",
    150: "CmdRudderAngle",
    151: "RudderLimit",
    152: "OffHeadingLim",
    153: "RadiusOfTurnOrder",
    154: "RateOfTurnOrder",
    155: "OffTrackLim",
    156: "LoggingTimeRemaining",
    157: "PositionFixType",
    158: "EngineDiscreteStatus",
    159: "TransmissionDiscreteStatus",
    160: "GpsBestOfFourSnr",
    161: "GenFluidLevel",
    162: "GenPressure",
    163: "GenTemperature",
    164: "InternalVoltage",
    165: "DepthOffset",
    166: "StructureDepth",
    167: "LoranPosition",
    168: "VesselStatus",
    169: "BatteryDcType",
    170: "BatteryStateOfCharge",
    171: "BatteryStateOfHealth",
    172: "BatteryTimeRemaining",
    173: "BatteryRippleVoltage",
    174: "Ac1Acceptability",
    175: "Ac2Acceptability",
    176: "Ac3Acceptability",
    177: "Ac1Voltage",
    178: "Ac2Voltage",
    179: "Ac3Voltage",
    180: "Ac1Current",
    181: "Ac2Current",
    182: "Ac3Current",
    183: "Ac1Frequency",
    184: "Ac2Frequency",
    185: "Ac3Frequency",
    186: "Ac1BreakerSize",
    187: "Ac2BreakerSize",
    188: "Ac3BreakerSize",
    189: "Ac1RealPower",
    190: "Ac2RealPower",
    191: "Ac3RealPower",
    192: "Ac1ReactivePower",
    193: "Ac2ReactivePower",
    194: "Ac3ReactivePower",
    195: "Ac1PowerFactor",
    196: "Ac2PowerFactor",
    197: "Ac3PowerFactor",
    198: "SwitchState",
    199: "SwitchCurrent",
    200: "SwitchFault",
    201: "SwitchDimLevel",
    202: "PreviousCmdHeading",
    203: "CmdWindAngle",
    204: "CmdBearingOffset",
    205: "CmdBearing",
    206: "CmdDepthContour",
    207: "CmdCourseChange"
}

import asyncio
import websockets
import json
import csv
from datetime import datetime  # Correct import for datetime class
import os

# Define the ID names as a dictionary (not repeated here for brevity)

# Extract fieldnames from idNames
fieldnames = list(idNames.values()) + ["UtcDate", "UtcTime"]

# Function to write data to CSV
def write_to_csv(data):
    # Define the CSV file name
    filename = 'websocket_data.csv'
    
    # Check if the file exists to write headers only once
    file_exists = os.path.isfile(filename)
    
    # Open the CSV file in append mode
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write headers only if file does not exist
        if not file_exists:
            writer.writeheader()
            
        # Create a row dictionary from the data
        row = {}
        for item in data:
            id = item["id"]
            if id in idNames:
                row[idNames[id]] = item.get("val", None)

        # Add UtcDate and UtcTime to the row
        row["UtcDate"] = datetime.utcnow().strftime('%Y-%m-%d')
        row["UtcTime"] = datetime.utcnow().strftime('%H:%M:%S')

        # Write the row to the CSV file
        writer.writerow(row)

# Consumer handler to process messages
async def consumer_handler(websocket):
    async for message in websocket:
        if message:  # Ensure message is not empty
            try:
                data = json.loads(message)
                if "Data" in data:
                    write_to_csv(data["Data"])  # Directly process the data
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
            except KeyError as e:
                print(f"Key error: {e}")

# Main function to connect to the WebSocket server and start listening
async def main():
    url = "ws://0.0.0.0:2053"  # Replace with your WebSocket server URL

    async with websockets.connect(url) as websocket:
        await consumer_handler(websocket)

if __name__ == "__main__":
    asyncio.run(main())
