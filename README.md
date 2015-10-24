# dance dance
## Ellen Van Wyk, Vincent van den Goor, Ricky Holtz
        
### the project
accelerometers have been used for a variety of applications; we're interested in seeing what they can tell us about dancers
        
### goals & research questions
We can collect data from a variety of sources (dance teams on campus, experienced dancers vs. non-dancers) and see if we can find distinct patterns. First, however, we have some questions to investigate, like:

- What is a dance? Can we identify dancing as a specific activity?
- Can we distinguish these dance styles from each other?
- How do we represent accelerometer data to other humans in a way that's useful and meaningful?
- How do you do this in real time? Dancing happens over time, so a single data point doesn't tell us much about the overall activity.
        
### process
We started our project by just collecting lots of different accelerometer data. this set us up for doing exploratory data analysis (EDA). Very early on, we realized that our project could go in a variety of directions; specifically, our project had components of **classification** (e.g., walking vs dancing), **visualization** (e.g., how do we represent accelerometer data for humans), and **familiarization** (i.e., learning how to work with accelerometer data in the first place).

We primarily used an app called [SensorLog](https://itunes.apple.com/us/app/sensorlog/id388014573?mt=8) to collect data. We faced a couple of hiccups with this, since SensorLog seems to have some errors in data collection that we can't really explain. We managed to get access to a home-grown accelerometer app, but faced the issue of our data having different formats to work in.

![two graphs on top of each other; the top graph has staggered clusters of lines increasing from bottom left to top right; the graph on the bottom is a smooth y=x curve](/img/low-pass-filter.png)
**Figure**: example of oddities in SensorLog data. The x-axis is the sample, and the y-axis is the associated time. We would expect a smooth line (as in the gyroTimeStamp) but sometimes see the strange steps for logging time. This is the same data source!

Overall, however, our project started to look promising fairly early. After some less-than-promising visualizations like the spectrogram below, we were feeling concern; some minor signal processing helped make our data much more promising, though.

![a multicolor graph with no clear patterns](/img/spectrogramSeanPaul.png)

As our data cleaning became more sophisticated, we also began to collect more intentional data. In order to deal with the problem of **classification**, we collected data for _line dances_ (the wobble and the cupid shuffle(, _structured dance_ (zumba and salsa), and _motion data_ (walking and running). This data was usable for our work with **visualization**.

### results
Some of our key findings were:

#### the low pass filter
we were able to get a mess of data like this:

![jagged lines on a graph](/img/amplitude.png)

to look more like this:

![smooth curves on a graph](/img/low-pass-filter.png)

We can see that an activity like walking provides much more of a regular cycle than a dance like salsa. This graph is also providing some interesting information, like which pocket the accelerometer is in, since we can see global maxima when the foot associated with the accelerometer pocket hits the ground. This data also leads us to...

#### principle component analysis
![a graph featuring clusters of walking data sets in the top left, and clusters of various dances in the bottom right](/img/pca-cluster.png)

These images show distinct clusters between walking activity and dancing data. This is particular data set doesn't distinguish dances from each other, however, and we need to collect a larger number of sample sizes to make this meaningful - right now, our n is about 3... Which may or may not be related to the fact that we have three team members.

#### 3d visualization
![accelerometer data of a person walking in 3D space](/img/3d-viz.gif)

Accelerometer data can be displayed in three dimensional space to provide a computational representation of where the accelerometer is in space. So, we have some sense of what a dance physically looks like, which is a step in the direction of visualizing this information in a human-consumable manner. The visualization above is a sped-up version of a person (note how we can see the person's altitude change as they walk uphill.)

**node server**
![a dense paragraph of alphanumeric characters littered with ampersands, equal signs, and other symbols](/img/raw-server.png)
raw data from SensorLog

![json objects with data descriptions as keys, and associated sensor samples as values](/img/server-json.png)
The node server allows us to pipe SensorLog data over a local network; this sets us up for future work in real time visualization of sensor data. In particular, this cleans the data up in a easily readable JSON format - this could be stored in a database, or accessed for immediate processing and visualization.

### next steps
Overall, some of our basic questions seem to be answered:

- _What is a dance? Can we identify dancing as a specific activity?_
Yes! Dance is a specific type of motion, and accelerometer data can be used to differentiate from other common behaviors that occur alongside dance - like walking.

- _Can we distinguish these dance styles from each other?_
For the moment, no. Dance could probably be described as "rhythmically frenetic." So, while we can distinguish dancing from walking, there's simply too much noise to make a meaningful differentiation between the different types of dance with our current data set.

- _How do we represent accelerometer data to other humans in a way that's useful and meaningful?_
We have a lot of work to do on this front. Our visualizations have primarily worked as a proof of concept, and our current visualization seems intimately tied to the realistic motion, but this doesn't necessarily feel like it adheres to a meaningful principle of information visualization - we'd have to consider something like pre-attentive processing to see whether it actually means something to people.

- _How do you do this in real time? Dancing happens over time, so a single data point doesn't tell us much about the overall activity._
This is a great question, past-selves. We'll get back to you at the end of P2. (:

**Moving forward**, we need to investigate that real-time work, but we could do a lot to retest the work we've done more rigorously. There's a lot of opportunity to collect data, and the representational work is still in its infancy. We also might want to start considering the ability to fool the sensors - and, realistically, thinking about this in terms of its applications. This concept is exciting, but also easily misapplied. We have to do a lot of consideration for how this would work in real-world situations.

_thanks for reading! we've also attached a poster below_

[![poster representation of dance dance project](/img/p1Poster.png)](/img/p1Poster-full.png)
