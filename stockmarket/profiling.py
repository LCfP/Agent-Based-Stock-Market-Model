import pstats

stats = pstats.Stats("profiling_results")
stats.sort_stats("tottime")

stats.print_stats(10)