/*********** Params ************/

// General
const numberOfThreads = 100000;
const numberOfThreadsPerPod = 100;
const testDurationInHour = 0.2;

// Memory
const memoryPerThreadInMB = 0.5;
const memoryPerPodInMB = 200;

// CPU
const cpuPerThread = 0.1;
const cpuPerPod = 1;

// Disk
const diskUsagePerPodInGB = 2;

// K8s Workers Size
const cpuPerWorker = 50;
const memoryPerWorkerInGB = 15;
const pricePerWorkerInHourInUSD = 0.5; 
const pricePerDiskInGBInUSD = 0.1; 

/*********** Formula ************/

const numberOfPodsNeeded = numberOfThreads / numberOfThreadsPerPod;

const allMemoryNeededInGB = 
    (
        (numberOfThreads * memoryPerThreadInMB) + 
        (numberOfPodsNeeded * memoryPerPodInMB)
    ) / 1000

const allCPUCoresNeeded = 
    (numberOfThreads * cpuPerThread) + 
    (numberOfPodsNeeded * cpuPerPod)

const allDiskNeededInGB = numberOfPodsNeeded * diskUsagePerPodInGB;

const numberOfWorkersByMemory = allMemoryNeededInGB / memoryPerWorkerInGB;
const numberOfWorkersByCpu = allCPUCoresNeeded / cpuPerWorker;
const numberOfWorkersNeeded = Math.ceil(numberOfWorkersByCpu > numberOfWorkersByMemory ? numberOfWorkersByCpu : numberOfWorkersByMemory);
const diskPerWorkerInGB = Math.ceil(allDiskNeededInGB / numberOfWorkersNeeded);
const workersPricePerHour = pricePerWorkerInHourInUSD * numberOfWorkersNeeded;
const diskPrice = pricePerDiskInGBInUSD * allDiskNeededInGB;
const clusterPrice = (testDurationInHour * workersPricePerHour) + diskPrice;

/*********** Report ************/

console.log('########### params ##########')

console.log(`testDurationInHour: ${testDurationInHour} Hour(s)`)
console.log(`numberOfThreads: ${numberOfThreads} Thread(s)`)
console.log(`numberOfThreadsPerPod: ${numberOfThreadsPerPod} Thread(s)`)
console.log(`memoryPerThreadInMB: ${memoryPerThreadInMB} MB`)
console.log(`memoryPerPodInMB: ${memoryPerPodInMB} MB`)
console.log(`cpuPerThread: ${cpuPerThread} Core(s)`)
console.log(`cpuPerPod: ${cpuPerPod} Core(s)`)
console.log(`diskUsagePerPodInGB: ${diskUsagePerPodInGB} GB`)
console.log(`numberOfPodsNeeded: ${numberOfPodsNeeded} Pod(s)`)
console.log(`cpuPerWorker: ${cpuPerWorker} Core(s)`)
console.log(`memoryPerWorkerInGB: ${memoryPerWorkerInGB} GB`)
console.log(`pricePerWorkerInHourInUSD: $${pricePerWorkerInHourInUSD}`)
console.log(`pricePerDiskInGBInUSD: $${pricePerDiskInGBInUSD}`)

console.log('\n########### all resources needed ##########')

console.log(`allMemoryNeededInGB: ${allMemoryNeededInGB} GB`)
console.log(`allCPUCoresNeeded: ${allCPUCoresNeeded} Core(s)`)
console.log(`allDiskNeededInGB: ${allDiskNeededInGB} TB`)

console.log('\n########### workers needed ##########')

console.log(`numberOfWorkersByMemory: ${numberOfWorkersByMemory} Workers`)
console.log(`numberOfWorkersByCpu: ${numberOfWorkersByCpu} Workers`)
console.log(`numberOfWorkersNeeded: ${numberOfWorkersNeeded} Workers`)
console.log(`diskPerWorkerInGB: ${diskPerWorkerInGB} GB`)

console.log('\n########### workers needed ##########')

console.log(`workersPricePerHour: $${workersPricePerHour}`)
console.log(`diskPrice: $${diskPrice}`)
console.log(`clusterPrice for ${testDurationInHour} hour(s): $${clusterPrice}`)
