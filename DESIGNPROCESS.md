# The DAG
This document is a justification of the design choices I have made in order to create the piece of code you have in front of you. It may not be the most complete, the most perfect or the most beautiful, but it is mine.

The DAG itself is comprises of three main tasks, which create, respectively, the bronze, silver and gold layers, as their names indicate. The other two tasks are there for monitoring and logging uses.

# The layers
Following the medallion architecture, we have `bronze`, `silver` and `gold` layers. For the sake of modularization, I have separated them into three distinct scripts, each one named after its corresponding layer. I believe the amount of code is small enough that I could have written one bigger script; I even believe I could have even wrote all the functions inside the DAG itself and have them be `python_callables` to each task, but I didn't for three main reasons: 1. The aforementioned modularization; 2. This would have made the debugging process harder and 3. I started the development process by writing each layer separately and testing them as I progressed. 

## Bronze
The `bronze` layer is responsible for determining the amount of breweries to fetch by reading the `metadata` page and then for retrieving information from each one by sending a `GET` request. All the information is then stored inside a `JSON` file. This was a suitable format given that the information already had a JSON-like structure and the file was fairly small (4.7 MB), so I wasn't too worried about issues like compression and performance bottlenecks from I/O operations. In that scenario, I reckon I would have used (concurrency)[https://pythonfluente.com/#concurrency_models_ch].

## Silver
The `silver` layer fetches data from the `bronze` layer and runs a minor transformation: standardizing the names of the columns. If you simply save the file partitioning it by location without doing this, you will find that there are two countries with very similar names. They are the `"United States"` and the `" United States"`. See the difference? There are some breweries listed in the `" United States"`, with whitespace in front of the word `United`. Furthermore, since some countries have names with more than one word, they make for really bad column names and partition names, so I replaced the spaces with underscores.

## Gold
The `gold` script is probably the simplest of all. It gets the data from the `silver` layer, aggregates it by country and type, and counts them, so that we can see how many breweries of each type there are in each country. This part of the script was done using `pandas` due to the fact that the amount of data was fairly small. The same result could be achieved using a computer cluster set up with Spark, but it isn't worth the effort due to the size of the data. What's more, even the code would have turned out to be very similar.

# Monitoring and error-handling
The DAG has two other tasks. The first one is concerned with the possibility of the API requests being refused for some reason or another and resulting in an empty bronze layer. In this scenario, one would be alerted by way of the task's logs, which would display a warning regarding the fact. The pipeline won't break in case this happens. It is important to notice that the API requests are, by far, the least reliable component of the pipeline. Other error-handling features exist in the scripts, such as the care in using `makedirs` and `os.path.join` to create directories in a valid manner across different operating systems. The last task is there to register the completion of the pipeline.

# Room for improvement
There are many aspects of the pipeline which could be improved upon but weren't. This happened mostly due to time constraints. One week was time enough to write this pipeline and document it with care, but it also happened to have been a very busy week for me due to a myriad of factors. Some aspects worthy of mention: implementing more transformations in the code, writing the `silver` and gold layers in Pyspark, setting up more tasks in the DAG and containerizing the application. 