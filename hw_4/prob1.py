from random import uniform
from math import sqrt
from time import time 
from dask import delayed
import argparse
import multiprocessing 
from concurrent.futures import ProcessPoolExecutor


#Dart throwing function 
def dart(number_of_darts):
    number_of_darts_in_circle= 0 
    x,y=uniform(0,1), uniform(0,1)
    if sqrt((x-0.5)**2 + (y-0.5)**2) <=0.5:
        number_of_darts_in_circle +=1
    return number_of_darts_in_circle

#Delayed dart throwing function to use with Dask 
@delayed(pure=True)
def dart_delayed(number_of_darts):
    number_of_darts_in_circle= 0 
    for x in range(number_of_darts):
        x,y=uniform(0,1), uniform(0,1)
        if sqrt((x-0.5)**2 + (y-0.5)**2) <=0.5:
            number_of_darts_in_circle +=1
    return number_of_darts_in_circle 

#Delayed addition function to use with dasks
@delayed(pure=True)
def add(x, y, z):
    return x + y + z

#Function for experimenting with simple serial, multiprocessing and dask 
def throw_in_parallel(nthrow):
    print("%d darts" %nthrow)
    ##################
    print('##Multiprocessing##')
    number_of_darts_in_circle = 0
    pools = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    start = time()
    results = pools.map(dart,range(nthrow))
    totaldart = sum(results)
    end=time()
    execution_time=end - start
    pi_approx = 4 *  totaldart / float(nthrow)
    print(f"Finished in {execution_time} sec")
    print("Num darts hit = ",  totaldart)
    print("Pi approx:", pi_approx)
    print("Darts thrown per second:" , nthrow / execution_time)

   ##################
    print('##Simple Serial##')
    number_of_darts_in_circle = 0
    start = time()
    results = []
    for x in range(nthrow):
        results.append(dart(x))
    totaldart = sum(results)
    end= time()
    execution_time= end - start
    pi_approx = 4 *  totaldart / float(nthrow)
    print(f"Finished in {execution_time} sec")
    print("Num darts hit = ", totaldart)
    print("Pi approx:", pi_approx)
    print("Darts thrown per second:" , nthrow / execution_time)

       ##################
    print('##Dask##')
    number_of_darts_in_circle = 0
    start = time()
    
    #Split up manually into three chunks
    values1 = (dart_delayed(int(nthrow/3)))
    values2 = (dart_delayed(int(nthrow/3)))
    values3 = (dart_delayed(nthrow -2*int(nthrow/3)))
    values4 = add(values1,values2,values3)
    results = values4.compute()
    end= time()
    execution_time = end - start
    pi_approx = 4 *  results / float(nthrow)
    print(f"Finished in {execution_time} sec")
    print("Num darts hit = ",results)
    print("Pi approx:", pi_approx)
    print("Darts thrown per second:" , nthrow / execution_time)
    print('\n')

if __name__ == "__main__":
    #Allow user to input number of darts
    parser = argparse.ArgumentParser(description='Sample Application')
    parser.add_argument('-s', action='store', dest='num_throws',
                    help='Store a simple value')
    results = parser.parse_args()
    nthrow = results.num_throws
    nthrow = int(nthrow)

throw_in_parallel(nthrow)
  
