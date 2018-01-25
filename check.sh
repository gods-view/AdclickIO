#!/bin/bash
count1=`ps -ef | grep ad_statis_new.py | grep -v "grep" | wc -l`
echo $count1

if [ $count1 -gt 0 ]; then
    echo "Good."
else
    echo "Down!"
    result1=`nohup python3 /home/ec2-user/tracking/AdClickIO/affiliate/ad_statis_new.py 0 > log/ad_statis.log 2>&1 &`
    echo $result1
fi

count2=`ps -ef | grep update_state.py | grep -v "grep" | wc -l`
echo $count2

if [ $count2 -gt 0 ]; then
    echo "Good."
else
    echo "Down!"
    result2=`nohup python3 /home/ec2-user/tracking/AdClickIO/dsp/module/update_state.py > update_state.log 2>&1 &`
    echo $result2
fi

count3=`ps -ef | grep updateCost.py | grep -v "grep" | wc -l`
echo $count3

if [ $count3 -gt 0 ]; then
    echo "Good."
else
    echo "Down!"
    result3=`nohup python3 /home/ec2-user/tracking/AdClickIO/dsp/module/updateCost.py > updateCost.log 2>&1 &`
    echo $result3
fi

count4=`ps -ef | grep update_website.py | grep -v "grep" | wc -l`
echo $count4

if [ $count4 -gt 0 ]; then
    echo "Good."
else
    echo "Down!"
    result4=`nohup python3 /home/ec2-user/tracking/AdClickIO/dsp/module/update_website.py > update_website.log 2>&1 &`
    echo $result4
fi

count5=`ps -ef | grep single_task.py | grep -v "grep" | wc -l`
echo $count5

if [ $count5 -gt 0 ]; then
    echo "Good."
else
    echo "Down!"
    result5=`nohup python3 /home/ec2-user/tracking/AdClickIO/affiliate/single_task.py > single_task.log 2>&1 &`
    echo $result5
fi
