hw_4 README
Margaret Doyle 


# In your README file, explain the behavior you measure and illustrate in the plot: 


The execution time for the simple serial method approaches a time scale on the order of about ~8 seconds when number of darts ~ 1e7. This is twice as slow as the ~ 4 second time scale achieved by both dask and multiprocessing method at the same number of darts. This is despite the fact that the execution time for both parallel tasks began on a time scale roughly two orders of magntude slower relative to the serial method when number of darts is small and ~ 10. 

On this log-log plot, the serial execution time appears nearly linear, whilt the dask and multiprocessing execution time looks slightly more exponential. The rate for all three methods looks somewhat logaraithmic.

