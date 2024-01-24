import arcpy

arcpy.env.workspace = r"C:\Users\gis-t10\Documents\ArcGIS\Projects\buildings\buildings.gdb"
fc = "building"

district_counts = {}
building_counts = {}
district_populations = {}
max_building_population = 0
buildings_with_most_population = []

with arcpy.da.SearchCursor(fc, ["DistrictName", "population", "Name", "floor"]) as cursor:
    for row in cursor:
        district = row[0]
        population = row[1]
        building = row[2]
        floor = row[3]

        district_counts[district] = district_counts.get(district, 0) + 1
        building_counts[building] = building_counts.get(building, 0) + 1
        district_populations[district] = district_populations.get(district, 0) + population

        if population > max_building_population:
            max_building_population = population
            buildings_with_most_population = [f"{building} ({population} population)"]
        elif population == max_building_population:
            buildings_with_most_population.append(f"{building} ({population} population)")

districts_with_largest_population = []
max_population = max(district_populations.values())

for district, population in district_populations.items():
    if population == max_population:
        districts_with_largest_population.append(f"{district} ({population})")

district_with_most_buildings = max(district_counts, key=district_counts.get)
buildings_with_most_floors = []
max_floors = 0
building_floors = {}

with arcpy.da.SearchCursor(fc, ["Name", "floor"]) as cursor:
    for row in cursor:
        building = row[0]
        floor = row[1]
        building_counts[building] = building_counts.get(building, 0) + 1
        building_floors[building] = max(building_floors.get(building, 0), floor)
        max_floors = max(max_floors, floor)

for building, floors in building_floors.items():
    if floors == max_floors:
        buildings_with_most_floors.append(f"{building} ({floors} floors)")

print("Districts with largest population:", ", ".join(districts_with_largest_population))
print("District with largest number of buildings:", district_with_most_buildings, "(", district_counts[district_with_most_buildings], "buildings)")
print("Buildings with most number of floors:", ", ".join(buildings_with_most_floors))
print("Buildings with most population:", ", ".join(buildings_with_most_population))
