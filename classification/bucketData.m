function [ bucketedData ] = bucketData( bucketInterval, timestamps, values)

    numBuckets = ceil(max(timestamps) / bucketInterval);
    numElementsPerBucket = zeros(numBuckets, 1);
    bucketedData = zeros(numBuckets, 1);

    for idx = 1:numel(timestamps)
        timestamp = timestamps(idx);
        value = values(idx);

        bucketIndex = floor(timestamp / bucketInterval)+1;
        if bucketIndex <= numel(bucketedData)
            numElementsPerBucket(bucketIndex) = numElementsPerBucket(bucketIndex) + 1;
            bucketedData(bucketIndex) = value;
        end
        
    end
    
    lastBucketValue = 0.0;
    for idx = 1:numel(numElementsPerBucket)
        if numElementsPerBucket(idx) == 0
            disp('Missing data in bucket! Filling in with last known bucket value.');
            bucketedData(idx) = lastBucketValue;
        else
            lastBucketValue = bucketedData(idx);
        end
    end

end