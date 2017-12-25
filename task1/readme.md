<h1>Task 1: Hadoop Streaming</h1>

This is a task where we were asked to process a file in a specific way using hadoop streaming.

1. Для каждого значения antiNucleus вычислить СРЕДНЕЕ значение prodTime
2. Взять только те строки, у которых prodTime выше СРЕДНЕГО для соответствующего ему antiNucleus
3. Для каждого antiNucleus посчитать
    1. Количество уникальных значений eventFile
    2. Среднее значение Pt

<b>Fields:</b>
<pre>
0. antiNucleus INT
1. eventFile UINT
2. eventNumber INT
3. eventTime DOUBLE
4. histFile UINT
5. multiplicity INT
6. NaboveLb INT
7. NbelowLb INT
8. NLb  INT
9. primaryTracks INT
10. prodTime DOUBLE
11. Pt  FLOAT
12. runNumber INT
13. vertexX  FLOAT
14. vertexY  FLOAT
15. vertexZ  FLOAT
</pre>


<h2>Local debug</h2>

<pre>
cat 1-input/star2002-sample.csv | python 1-average_prodTime/map.py | sort -k1,1 | python 1-average_prodTime/reduce.py > 1-output/output-1.txt

cat 1-output/output-1.txt | python 2-unique_eventFile/map.py | sort -k1,1 | python 2-unique_eventFile/reduce.py > 2-output/output-2.txt

cat 1-output/output-1.txt | python 3-average_Pt/map.py | sort -k1,1 | python 3-average_Pt/reduce.py > 3-output/output-3.txt
</pre>

<h2>Hadoop streaming</h2>

<b>1. Launch docker container with hadoop</b>

<code>docker run -it sequenceiq/hadoop-docker:2.7.1 /etc/bootstrap.sh -bash</code>


<b>2. Find out container name (using docker CLI)</b>

<code>docker ps</code>


<b>3. Load files to docker container (using docker CLI)</b>

<pre>
docker cp 1-input/star2002-sample.csv zealous_bassi:input.csv
docker cp 1-average_prodTime/map.py zealous_bassi:map-1.py
docker cp 1-average_prodTime/reduce.py zealous_bassi:reduce-1.py
docker cp 2-unique_EventFile/map.py zealous_bassi:map-2.py
docker cp 2-unique_EventFile/reduce.py zealous_bassi:reduce-2.py
docker cp 3-average_Pt/map.py zealous_bassi:map-3.py
docker cp 3-average_Pt/reduce.py zealous_bassi:reduce-3.py
</pre>

<b>4. Inside container: create directory in hdfs and load input there</b>

<code>
cd $HADOOP_PREFIX
</code>
<br>
<code>
bin/hdfs dfs -mkdir input-1
</code>
<br>
<code>
bin/hdfs dfs -put /input.csv ./input-1/sample.csv
</code>
<br>
<br>

<b>5. Launch hadoop-streaming job #1 (average prodTime)</b>

First Map reads the file and processes its fields. Then Reduce computes average value of prodTime and returns only those entries that have prodTime value greater.

In my case, after pasting the following command I had to press Enter twice.

<pre>
bin/hadoop jar share/hadoop/tools/lib/hadoop-streaming-2.7.1.jar \
-input input-1 \
-output output-1 \
-mapper map-1.py \
-reducer reduce-1.py \
-file /map-1.py \
-file /reduce-1.py \
</pre>

Load results from hdfs to docker container:

<code>
bin/hdfs dfs -get ./output-1/part-00000 /output-1-hadoop.txt
</code>
<br>
<br>


Load results from container to local storage (using docker CLI):

<code>
docker cp zealous_bassi:output-1-hadoop.txt 1-output/output-1-hadoop.txt
</code>
<br>
<br>


<b>6. Job #2 (unique eventFile)</b>

Second MapReduce reads output of the first MapReduce (filtered file contents) and counts unique values of eventFile for each antiNucleus value.

<pre>
bin/hadoop jar share/hadoop/tools/lib/hadoop-streaming-2.7.1.jar \
-input output-1 \
-output output-2 \
-mapper map-2.py \
-reducer reduce-2.py \
-file /map-2.py \
-file /reduce-2.py \
</pre>

<code>
bin/hdfs dfs -get ./output-2/part-00000 /output-2-hadoop.txt
</code>
<br>
<br>

<code>
docker cp zealous_bassi:output-2-hadoop.txt 2-output/output-2-hadoop.txt
</code>
<br>
<br>


<b>7. Job #3 (average Pt)</b>

Final MapReduce again reads output of the first MapReduce and computes average value of Pt for each antiNucleus.

<pre>
bin/hadoop jar share/hadoop/tools/lib/hadoop-streaming-2.7.1.jar \
-input output-1 \
-output output-3 \
-mapper map-3.py \
-reducer reduce-3.py \
-file /map-3.py \
-file /reduce-3.py \
</pre>

<code>
bin/hdfs dfs -get ./output-3/part-00000 /output-3-hadoop.txt
</code>
<br>
<br>

<code>
docker cp zealous_bassi:output-3-hadoop.txt 3-output/output-3-hadoop.txt
</code>
<br>
<br>


<h2>Results</h2>

Ultimately, all output from hadoop-streaming jobs matches that from local debug. Only detail is that the final MapReduce outputs slightly less precise numbers, e.g.
<pre>
local:  0,5.125591148121347
hadoop: 0,5.12559114812	
</pre>
