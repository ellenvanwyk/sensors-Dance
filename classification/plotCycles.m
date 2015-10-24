
lpf =7;

secondsStartWalk = 5;
secondsEndWalk = 35;
secondsStartDance = 5;
secondsEndDance = 35;

bucketInt = 1/30;

[timestampWalk, accMagWalk, lpfAccMagBucketWalk] = runLowPassFilter...
    ('data/walking10_17_2015 06_41_13.csv', lpf, bucketInt, secondsStartWalk,secondsEndWalk);
bucketTimestampWalk = (1: length(lpfAccMagBucketWalk))'/30;
figure
line(bucketTimestampWalk,lpfAccMagBucketWalk, 'Color',[1,0.4,0.6]);

hold on

[timestampDance, accMagDance, lpfAccMagBucketDance] = runLowPassFilter...
    ('data/salsapartner10_17_2015 03_46_48.csv', lpf, bucketInt, secondsStartDance, secondsEndDance);
bucketTimestampDance = (1: length(lpfAccMagBucketDance))'/30;
line(bucketTimestampDance,lpfAccMagBucketDance, 'Color', [.2,.3,1]);
legend('walking', 'salsa')
xlabel('seconds');
ylabel('acceleration amplitude');
hold off


[frequenciesWalk, freqDomainWalk] = periodogram((lpfAccMagBucketWalk - mean(lpfAccMagBucketWalk)), hamming(length(lpfAccMagBucketWalk)), [], 1/bucketInt);
[frequenciesDance, freqDomainDance] = periodogram((lpfAccMagBucketDance - mean(lpfAccMagBucketDance)), hamming(length(lpfAccMagBucketWalk)), [], 1/bucketInt);

figure


plot (freqDomainWalk, frequenciesWalk, 'Color',[1,0.4,0.6]);
hold on
plot (freqDomainDance,frequenciesDance,'Color', [.2,.3,1] );
legend('walking', 'salsa')
xlabel('cycles/second');
ylabel('power/frequency');




