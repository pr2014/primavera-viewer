"""
Philip Rutter 10/07/18
Module for handling cube list statistics
"""

import iris
import nearestknownpoint as nkp
import singlecubestats as scs


def locate_point_cubes(point, cubes):
    """
    Purpose: find nearest known point in each coordinate system for each model/ensemble and subset cubes at that point
    :param point: latitude and longitude point
    :param cubes: iris.cube.CubeList
    :return: list of cubes at the requested point
    """
    all_cubes_list = iris.cube.CubeList([])
    for cube in cubes:
        cube = nkp.PointLocation(point, cube)
        cube = cube.find_point()
        all_cubes_list.append(cube)
    return all_cubes_list

def locate_area_cubes(area_bounds, cubes):
    """
    Purpose: find nearest known point in each coordinate system for each model/ensemble within latitude and longitude
    bounds and produce a zonal mean for each cube.
    :param point: latitude and longitude point
    :param cubes: iris.cube.CubeList
    :return: list of cubes averaged over the requested area
    """
    all_cubes_list = iris.cube.CubeList([])
    for cube in cubes:
        cube = nkp.AreaLocation(area_bounds, cube)
        cube = cube.find_area()
        all_cubes_list.append(cube)
    return all_cubes_list

def all_experiments_mean(cubes):
    """
    Purpose: Calculates the multi-model/multi-ensemble mean for each time point for a given variable.
    :param cubes: iris.cube.CubeList
    :return: single cube containing multi-model/ensemble mean
    Note: All calendars are converted to a 360 day calendar by this script. Gregorian and 365 day calendars keep
    31/01 and 31/03 to balance 28/02. All other 31st days and leap days are removed.
    """
    all_cubes_list = iris.cube.CubeList([])
    for cube in cubes:
        cube = scs.change_cube_format(cube)
        all_cubes_list.append(cube)
    cubes = all_cubes_list
    merged_cube = cubes.merge_cube()
    experiments_mean = merged_cube.collapsed('experiment_label', iris.analysis.MEAN)

    return experiments_mean
