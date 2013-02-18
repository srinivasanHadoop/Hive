#!/bin/sh
export s1=$(whoami)
s2="root"
if [ "x$s1" == "x$s2" ]
	then
	   OS=`cat /etc/*-release | awk {'print $1}'`
		if [ "$OS" = "CentOS" -o "$OS"!="Red" ]
		then
		     yum install dialog
			dialog --title "Hive WordCount Program Example" --backtitle "Local  input file path" --inputbox "Enter the local  Source path" 8 60 2>/tmp/sp.$$
			sp=`cat /tmp/sp.$$`
			$HIVE_HOME/bin/hive -e "CREATE TABLE sampleword (line STRING)";
			$HIVE_HOME/bin/hive -e "LOAD DATA LOCAL INPATH '$sp' OVERWRITE INTO TABLE sampleword";
			$HIVE_HOME/bin/hive -e "CREATE TABLE word_count_Result AS SELECT word, count(1) AS count FROM (SELECT explode(split(line, '\s')) AS word FROM sampleword) w GROUP BY word ORDER BY word";
		else
		    sudo apt-get install dialog
			dialog --title "Hive WordCount Program Example" --backtitle "Local  input file path" --inputbox "Enter the local  Source path" 8 60 2>/tmp/sp.$$
			sp=`cat /tmp/sp.$$`
			$HIVE_HOME/bin/hive -e "CREATE TABLE sampleword (line STRING)";
			$HIVE_HOME/bin/hive -e "LOAD DATA LOCAL INPATH '$sp' OVERWRITE INTO TABLE sampleword";
			$HIVE_HOME/bin/hive -e "CREATE TABLE word_count_Result AS SELECT word, count(1) AS count FROM (SELECT explode(split(line, '\s')) AS word FROM sampleword) w GROUP BY word ORDER BY word";
		fi
	else
	  echo "change the user into root"
	fi
