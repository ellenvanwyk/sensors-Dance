function [timestamp, accMag, lpfAccMagBucket] = runLowPassFilter(filename, lpf, bucketInt, startTime, endTime)

    WM = csvread(filename);

    timestamp = WM(:,1);
    accX = WM(:,2);
    accY = WM(:,3);
    accZ = WM(:,4);

    accMag = sqrt( accX.^2 + accY.^2 + accZ.^2 );
    
    accMagBucket = bucketData( bucketInt, timestamp, accMag);

    coeffHz = ones(1, lpf)/lpf;

    lpfAccMagBucketFull = filter(coeffHz, 1, accMagBucket);
    
    lpfAccMagBucket = lpfAccMagBucketFull(round(startTime/bucketInt) : round(endTime/bucketInt));
    
    
    
end
