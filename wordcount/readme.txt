Hi Chennai Hadoop User Group Memebers,
       I make this program in user friendly. That is why i wrote this program in shell scripting.
	   
How to run this program?
1.first extarct the file by using unzip command
   $unzip worcount.zip
2.Export the hive installation directory in your .bashrc file
   $ cd ~
   $ vi .bashrc(enter the below two line at the end of the file)
        export HIVE_HOME=<hive installtion directory>
		export PATH=${HIVE_HOME}/bin:${PATH}
   
   $ source .bashrc
3.change the mode of the wordcount.sh file.
   $ chmod 777 worcount.sh
4.Run the shell script program in your system
   $ ./wodcount.sh
5.when you start to run the shell script program. It will display the inputdialog box,just enter where is your input file is located in your system.
6.onece the hive operation is completed,the wordcount program result will be stored in word_count_Result 
	   
	   
  