from sumolib.route import mapTrace as mt
import os
import xml.etree.ElementTree as ET
import re

# location of the folder containing gpx files (real-world vehivles' trace information)
gpx_folder = r"C:\Users\18611\Desktop\gps_traces\traces"
# location of the traffic network's file
net_file = r'C:\Users\18611\Desktop\school\worlds\myMap_net\sumo.net.xml'
# location that the output file is to be saved
loc_file = r'C:\Users\18611\Desktop\gps_traces\locations.txt'

# extract vehicle trace information from XML files and save them into array
def readGPX(file_dir):
    lines = []
    files = os.listdir(file_dir)
    for file in files:
        if file.endswith('.gpx'):
            tree = ET.parse(os.path.join(file_dir, file))
            root = tree.getroot()
            ns = re.findall('\{.+?}', root.tag)[0]
            for elm in root.iter(ns + 'trk'):
                line_name = elm.find(ns + 'name').text
                if elm.find(ns + 'trkseg'):
                    line = []
                    for spot in elm.find(ns + 'trkseg').findall(ns + 'trkpt'):
                        lat, lon = float(spot.attrib['lat']), float(spot.attrib['lon'])
                        lat = -110028.089888 * lat + 3441819.00787
                        lon = 98995.8405109 * lon - 11951055.7025
                        line.append((lat, lon))
                    lines.append(line)
                    bounds = root.find(ns + 'metadata').find(ns + 'bounds').attrib
                    print(f"{line_name} added, {len(line)} locations.\ngps boundaries: {bounds}\n")
    return lines

# save the information into file
def writelocation(file, locations):
    with open(file, 'w') as f:
        for i, track in enumerate(locations):
            line = f'car {i+1}:'
            for j, loc in enumerate(track):
                line += f'{loc[0]},{loc[1]} '
            f.write(line + '\n')
        f.close()


tracks = readGPX(gpx_folder)
writelocation(loc_file, tracks)
