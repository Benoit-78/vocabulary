"""
    Author: Benoît Delorme
    Creation date: 22nd July 2023
    Main purpose: analyse execution time and memory usage.
"""

import cProfile
import pstats
import csv

import interro


if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.enable()
    interro.main()
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    with open('logs\profile_stats.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Function', 'ncalls', 'tottime', 'percall', 'cumtime', 'percall'])
        stats.stream = csvfile
        stats.print_stats()
