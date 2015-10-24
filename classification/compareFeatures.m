

data = {'data/walking10_17_2015 06_41_13.csv','data/walking10_17_2015 09_08_36.csv',...
    'data/walking10_17_2015 11_10_29-1.csv','data/walkingIncircles10_17_2015 04_03_11.csv','data/walkingSidewalk10_18_2015 03_08_37.csv',...
    'data/walking10_18_2015 05_52_07.csv','data/zumba10_17_2015 04_25_25.csv', 'data/cupidShuffle10_17_2015 10_14_44.csv',...
    'data/wobble10_17_2015 10_52_26.csv', 'data/grownWomanParnter10_17_2015 03_53_18.csv',...
    'data/rihannahCake10_18_2015 12_55_05.csv','data/LoseMyBreath10_18_2015 01_42_09.csv',...
    'data/justDance10_18_2015 01_40_02.csv', 'data/pressure10_18_2015 01_34_11.csv',...
    'data/salsapartner10_17_2015 03_46_48.csv', 'data/salsaWithRicky10_17_2015 07_36_51.csv'};

labels = {'walking','walkingAtColab','walkingInHallway','walkingInCircles','walkingSideWalk', 'walkingSidewalkAgain','zumba',...
    'cupidShuffle','wobble','grownWoman','cake', 'loseMyBreath', 'justDance', 'pressure', 'salsaAnton', 'salsaRicky' };

avgAmpRaw = [];
avgAmp = [];
timestamp = [];
accMag = [];
lpfAccMagBucket = [];
freqPower = [];
frequencies = [];
variationFreq = [];
variationAmp = [];
maxFreqPower = [];
maxFreq = [];
avgAmplitude = [];
numPeaks = [];
threeTopFreq = [];
threeTopAmp = [];
numHighFreq = [];
avgFreq = [];

peaksAll = [];

lpf = 15;
bucketInt = 1/30;
secondsStart = 4;
secondsEnd = 32;





%Get data
for i = 1:length(data)
    
    %Run lowpass filter and bucket data
    [a,b,c] = runLowPassFilter...
        (data{i}, lpf, bucketInt, secondsStart,secondsEnd);
    
    avgAmpRaw = [avgAmpRaw mean(b)];
    lpfAccMagBucket =[lpfAccMagBucket c];

    bucketTimestamp = (1: length(lpfAccMagBucket))'/30;
 
    %Create frequency domain
    [d, e] = periodogram((c - mean(c)), hamming(length(c)), [], 1/bucketInt);
    freqPower = [freqPower, d];
    frequencies = [frequencies, e];

 
    %Find the number of peaks in the spectogram (arbitrarily defined as > .003)
    [peaks, locs] = findpeaks(d);
    
    isPeakAboveT = peaks>.003;
    
    %Find number of peaks above a threshold
    numPeaks = [numPeaks sum(isPeakAboveT)];
    
    %Separate out common frequencies and find their average and variation
    peaksAboveTLoc = locs .* isPeakAboveT;
    peaksAboveTAmp = peaks .* isPeakAboveT;
    
    %Strip out zeros
    peaksAboveTLoc(all(peaksAboveTLoc==0,2),:)=[];
    peaksAboveTAmp(all(peaksAboveTAmp==0,2),:)=[];
    
    FreqPeaksAboveT = [];
    
    
    for j = 1:length(peaksAboveTLoc)
        FreqPeaksAboveT = [FreqPeaksAboveT e(peaksAboveTLoc(j))];
        
    end
    
    avgFreq = [avgFreq mean(FreqPeaksAboveT)];
    variationFreq  = [variationFreq std(FreqPeaksAboveT)];
    
    avgAmp = [avgAmp mean(peaksAboveTAmp)];
    variationAmp = [variationAmp std(peaksAboveTAmp)];

    
end



%Make PCA Vector
danceProfiles = [numPeaks;avgFreq;variationFreq;variationAmp;avgAmp;avgAmpRaw];

profileTitles = {'numPeaks','avgFreq','variationFreq','variationAmp','avgAmp','avgAmpRaw'};

[coeff, score, latent] = pca(danceProfiles);

%Plot PCA coefficients
figure
scatter(coeff(1:6,1),coeff(1:6,2),100,[1,0.4,0.6]);
hold all
scatter(coeff(7:9,1),coeff(7:9,2),100,[0,1,1]);
hold all
scatter(coeff(10:14,1),coeff(10:14,2),100,[.2,.3,1]);
hold all
scatter(coeff(15:16,1),coeff(15:16,2),100,[.7,.7,.3]);
hold off
legend('walking', 'structured dancing', 'unstructured dancing', 'salsa')

xlabel('First Component');
ylabel('Second Component');

hold off

%Print whether difference in walking and dancing is significant for all
%variables
for i = 1:length(profileTitles)
    profileTitles{i}
    [h,p] = ttest2(danceProfiles(i, 1:6), danceProfiles(i, 7:16))
end