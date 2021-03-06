"""
Philip Rutter 11/07/18

PRIMAVERA data plotting operation module

Inputs:
- Start dates and end dates for the time series
- A variable to be used for plotting (only tasmax and tasmin currently
available)
- Model names and ensemble members to compare at respective resolutions
- Location. Either at a single point of reference or latitude longitude
boundaries defining an area
- Plot type

Creates an 'SimulationsLoading' class defining all of the above inputs. Uses
constrained loading to restrict timespan and loads in all required data before
concatenating. Output is a list of the cubes to be compared.

The 'SimulationsData' class unifies the simulation's cube data (spatial
dimensions, formatting and location) in order to produce an accurate timeseries
comparison.

'SimulationsPlotting' uses the simulations mean and plot type to visualise data.

Model_input options: ['MOHC.HadGEM3-GC31-LM', 'CMCC.CMCC-CM2-HR4',
                      'EC-Earth-Consortium.EC-Earth3', 'ECMWF.ECMWF-IFS-LR']
Ensemble input options: ['r1i1p1f1', 'r1i2p1f1', 'r1i3p1f1']
Variable input options: ['tasmin', 'tasmax']


"""
from primavera_viewer.simulations_loading import *
from primavera_viewer.simulations_data import *
from primavera_viewer.simulations_plotting import *
import argparse
import sys


def parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-var', '--variable', nargs='+',
                        help='input variable')
    parser.add_argument('-mod', '--models', nargs='+',
                        help='input models to compare')
    parser.add_argument('-ens', '--ensembles', nargs='+',
                        help='input ensemble members to compare')
    parser.add_argument('-stat', '--statistics',
                        help='input statistics for data analysis')
    parser.add_argument('-out', '--output_type',
                        help='type of output required from comparison tool')
    parser.add_argument('-styr', '--start_year',
                        help='input start year constraint', type=int)
    parser.add_argument('-enyr', '--end_year',
                        help='input end year constraint', type=int)
    parser.add_argument('-lat', '--latitude_point',
                        help='input latitude point constraint',
                        type=float)
    parser.add_argument('-lon', '--longitude_point',
                        help='input longitude point constraint',
                        type=float)
    parser.add_argument('-latmin', '--latitude_min_bound',
                        help='input latitude min bound constraint',
                        type=float)
    parser.add_argument('-latmax', '--latitude_max_bound',
                        help='input latitude max bound constraint',
                        type=float)
    parser.add_argument('-lonmin', '--longitude_min_bound',
                        help='input longitude min bound constraint',
                        type=float)
    parser.add_argument('-lonmax', '--longitude_max_bound',
                        help='input longitude max bound constraint',
                        type=float)
    args = parser.parse_args()
    return args


def main(args):
    """
    Run comparison of models/ensembles and plot data
    """

    if args.variable:
        variable = args.variable
    else:
        print('ERROR: Must specify variable input')
        sys.exit()

    if args.models:
        models = args.models
    else:
        print('ERROR: Must specify models')
        sys.exit()

    if args.ensembles:
        ensembles = args.ensembles
    else:
        print('ERROR: Must specify ensemble members')
        sys.exit()

    if args.statistics:
        statistics = args.statistics
    else:
        print('ERROR: Must specify statistics')
        sys.exit()

    if args.output_type:
        output_type = args.output_type
    else:
        print('ERROR: Must specify output_type')
        sys.exit()

    if args.start_year and args.end_year:
        time_constraints = [args.start_year, args.end_year]
    else:
        print('ERROR: No time period specified')
        sys.exit()

    if args.latitude_point and args.latitude_point:
        location_constraints = [args.latitude_point,
                                args.longitude_point]
    elif args.latitude_min_bound and args.latitude_max_bound and \
            args.longitude_min_bound and args.longitude_max_bound:
        location_constraints = [args.latitude_min_bound,
                                args.latitude_max_bound,
                                args.longitude_min_bound,
                                args.longitude_max_bound]
    else:
        print('No location specified. Return global average.')
        location_constraints = [-90.0, 90.0, 0.0, 360.0]

    # Create class containing details of all simulations
    simulations_inputs = SimulationsLoading(variable, models,
                                            ensembles, time_constraints)
    simulations_list = simulations_inputs.load_all_data()

    # Create class for simulation data at requested location
    simulations_data = SimulationsData(simulations_list,
                                       loc=location_constraints,
                                       t_constr=time_constraints)

    # Unify simulation spacial coordinate systems
    simulations_data_unified = simulations_data.simulations_operations()

    simulations_mean = simulations_data_unified.all_simulations_mean()

    # Create class containing data from all simulations, the simulation mean
    # timeseries and the requested plot type
    result = SimulationsPlotting(simulations_data_unified.simulations_list,
                                 simulations_data_unified.location,
                                 simulations_mean, statistics, output_type)

    # Data output as requested
    result.simulations_output()

if __name__ == '__main__':

    args = parse_args()

    # Run the code
    main(args)