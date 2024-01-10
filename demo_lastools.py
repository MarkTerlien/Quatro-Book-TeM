import os
import sys
import json
import requests

# LASTools aansturen vanuit Python: https://lastools.github.io/download/

# Converteer van LAZ naar LAS:
# C:\Software\LAStools\bin\laszip.exe –i C:\temp\C_44DZ1.LAZ 

# Ophalen kaartbladen als JSON:
ahn_json = "c:/temp/AHN.json"
url  = 'https://service.pdok.nl/rws/ahn/atom/downloads/dtm_05m/kaartbladindex.json'
r = requests.get(url)
if r.status_code ==  200 :
    print('Request succesvol')
    json_object = json.dumps(r.json(), indent=4)
    with open(ahn_json, "w") as outfile:
        outfile.write(json_object)
else :
    print('Request niet succesvol. Foutcode: ' + str(r.status_code))

# Parse JSON
features = r.json()["features"]
for feature in features:
    download_url = feature["properties"]["url"]
    if feature["properties"]["name"] == 'M_02DZ1.tif':
        print('Downloading ' + download_url)
        my_ahnfile = requests.get(download_url)
        output_file = 'c:/temp/' + feature["properties"]["name"]
        open(output_file, 'wb').write(my_ahnfile.content)
        print('Downloading to file ' + output_file  + 'completed')

# Instructions to download file: https://realpython.com/python-download-file-from-url/

# Download AHN: https://esrinl-content.maps.arcgis.com/apps/Embed/index.html?appid=a3dfa5a818174aa787392e461c80f781

# File names
lasfile = 'C:/temp/C_44DZ1.las'
txtfile = 'C:/temp/C_44DZ1_info.txt'

# Write info of las file to txt file
las_command = 'C:/Software/LAStools/bin/lasinfo -i ' + lasfile + ' -o ' + txtfile
print(las_command)
os.system(las_command)

# Print info files
txtfile = open(txtfile)
for line in txtfile:
    print(line)
txtfile.close()

# Clip uit LAS file
las_command = 'C:/Software/LAStools/bin/las2las -i ' + lasfile + ' -o C:/temp/C_44DZ1_clip.las -keep_xy 110500 400200 110800 400400'
print(las_command)
os.system(las_command)

# Open LAS viewer
las_command = 'C:/Software/LAStools/bin/lasview -i C:/temp/C_44DZ1_clip.las'
print(las_command)
os.system(las_command)

#las2iso -i lidar.laz -o contours.shp -last_only -clean 100

print('End')
