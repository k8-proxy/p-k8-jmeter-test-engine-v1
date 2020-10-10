# JMeter Resource estimation

## The fastest servers you have = the fastest clients you must have

- It is impossible to say something like "this hardware will able to simulate that much virtual users" as the maximum load you can produce from hardware strongly depends on the nature of your test.

## So what can we do ?

Actually it depends on what your test is doing, number of Samplers, number of PreProcessors, PostProcessors, Assertions, request and response size, etc.

### TEST IT !

- Make sure that all the recommendations from JMeter Performance and Tuning Tips are applied
Start with i.e. 100 concurrent users and mention how much CPU and RAM are used.

- Increase concurrency to 200, measure CPU/RAM once more
Continue increasing concurrency till resource consumption reaches ~80% of total CPU or RAM, whatever comes the first.

### Remember the golden tips:

- GUI mode is for Script creation and debugging, not for load testing

- If the method teardownTest is not overridden by a subclass of AbstractJavaSamplerClient, its teardownTest method will not be called. This reduces JMeter memory requirements. This will not have any impact on existing Test plans.

- Graph Results MUST NOT BE USED during load test as it consumes a lot of resources (memory and CPU). Use it only for either functional testing or during Test Plan debugging and Validation.

- View Results Tree MUST NOT BE USED during load test as it consumes a lot of resources (memory and CPU). Use it only for either functional testing or during Test Plan debugging and Validation.

- Compare Assertion must not be used during load test as it consumes a lot of resources (memory and CPU). Use it only for either functional testing or during Test Plan debugging and Validation.

## Some suggestions on reducing resource usage.

- Use CLI mode: jmeter -n -t test.jmx -l test.jtl
- Use as few Listeners as possible; if using the -l flag as above they can all be deleted or disabled.
- Don't use "View Results Tree" or "View Results in Table" listeners during the load test, use them - - only during scripting phase to debug your scripts.
- Rather than using lots of similar samplers, use the same sampler in a loop, and use variables (CSV - Data Set) to vary the sample. [The Include Controller does not help here, as it adds all the test - - elements in the file to the test plan.]
- Don't use functional mode
- Use CSV output rather than XML
- Only save the data that you need
- Use as few Assertions as possible
- Use the most performing scripting language (see JSR223 section)

## What we want in GW-traffic-generator?
- 100k concurent users (threads)
- 100 threads per pod
- 1k pods

### The basic resource estimation based on local tests
- for basic resource estimation you must count on these parameters:
```
testDurationInHour: ex: 0.2 hour
numberOfThreads: ex: 100000 Thread(s)
numberOfThreadsPerPod: ex: 100 Thread(s)
memoryPerThreadInMB: ex: 0.5 MB
memoryPerPodInMB: ex: 200 MB
cpuPerThread: ex: 0.1 Core(s)
cpuPerPod: ex: 1 Core(s)
diskUsagePerPodInGB: ex: 2 GB
numberOfPodsNeeded: ex: 1000 Pod(s)
cpuPerWorker: ex: 50 Core(s)
memoryPerWorkerInGB: ex: 15 GB
pricePerWorkerInHourInUSD: ex: $0.5
pricePerDiskInGBInUSD: ex: $0.1
```
[CPU]

Load testing and jmeter in nature is a cpu sensitive job. Basically 1 cpu core per threads needed but we count on context switching. so we can assign single cpu core to multiple threads.

see: (https://stackoverflow.com/questions/34689709/java-threads-and-number-of-cores#:~:text=Lets%20say%20you%20started%2030,running%20at%20the%20same%20time)

- to calculate the resource needed you can simply open ```Jmeter-resource-estemination.js```, change the default values in variables (Params section) and run the js file: ```node Jmeter-resource-estemination.js```

The result should look like this:
```
########### params ##########
testDurationInHour: 0.2 Hour(s)
numberOfThreads: 100000 Thread(s)
numberOfThreadsPerPod: 100 Thread(s)
memoryPerThreadInMB: 0.5 MB
memoryPerPodInMB: 200 MB
cpuPerThread: 0.1 Core(s)
cpuPerPod: 1 Core(s)
diskUsagePerPodInGB: 2 GB
numberOfPodsNeeded: 1000 Pod(s)
cpuPerWorker: 50 Core(s)
memoryPerWorkerInGB: 15 GB
pricePerWorkerInHourInUSD: $0.5
pricePerDiskInGBInUSD: $0.1

########### all resources needed ##########
allMemoryNeededInGB: 250 GB
allCPUCoresNeeded: 11000 Core(s)
allDiskNeededInGB: 2000 TB

########### workers needed ##########
numberOfWorkersByMemory: 16.666666666666668 Workers
numberOfWorkersByCpu: 220 Workers
numberOfWorkersNeeded: 220 Workers
diskPerWorkerInGB: 10 GB

########### workers needed ##########
workersPricePerHour: $110
diskPrice: $200
clusterPrice for 0.2 hour(s): $222
```
















[resources]:
- https://jmeter.apache.org/usermanual/component_reference.html#samplers
- https://jmeter.apache.org/usermanual/component_reference.html#Graph_Results
- https://sqa.stackexchange.com/questions/15178/-what-is-recommended-hardware-infrastructure-for-running-heavy-jmeter-load-tests
- https://jmeter.apache.org/usermanual/component_reference.html#postprocessors
- https://jmeter.apache.org/usermanual/best-practices.html
- https://www.blazemeter.com/blog/9-easy-solutions-jmeter-load-test-%E2%80%9Cout-memory%E2%80%9D-failure
- https://jmeter.apache.org/usermanual/best-practices.html#lean_mean
- https://www.blazemeter.com/blog/how-monitor-your-server-health-performance-during-jmeter-load-test
- https://jmeter.apache.org/usermanual/boss.html
- https://stackoverflow.com/questions/34689709/java-threads-and-number-of-cores#:~:text=Lets%20say%20you%20started%2030,running%20at%20the%20same%20time.
- http://tutorials.jenkov.com/java-concurrency/index.html
- https://www.tutorialspoint.com/what-is-context-switching-in-operating-system
