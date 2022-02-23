hw_4 README
Margaret Doyle 


# In your README file, explain the behavior you measure and illustrate in the plot: 


The execution time for the simple serial method approaches a scale on the order of about ~8 seconds when number of darts ~ 1e7. This is twice as slow as the ~ 4 second time scale achieved by both dask and multiprocessing methods when run for the same number of darts. This is despite the fact that when number of darts was small and ~10, the execution time for both of the parallel tasks occurred on a time scale roughly two orders of magnitude slower relative to the serial method. The advantage of the parallel computing over the simple serial method is visible around 1e4 darts. 

On this log-log plot, the serial execution time appears to be nearly linear for nearly all n, indicating that a power relationship exists between any number of darts thrown and execution time. This linear behavior on the log-log plot only resolves itself for the parallel methods after number_darts ~ 1e4. Before this point, the execution time for both multiprocessing and dask appears somewhat flat - overhead time is likely accounting for a majority of it.

The simulation rate achieved for all three methods appears somewhat logarithmic and appears to to plateau between 1e6 and 1e7 darts/second. Both dask and multiprocessing converge to rates higher than the simple serial method despite the fact that they started at rates at least 2 orders of magnitude slower. 


```python

```
