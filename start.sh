#!/bin/sh
#trucking统计
nohup python3 affiliate/ad_statis.py 0 > log/ad_statis.log 2>&1 &
nohup python3 affiliate/single_task.py > single_task.log 2>&1 &
nohup python3 dsp/module/update_state.py > update_state.log 2>&1 &
nohup python3 dsp/module/getCost.py > getCost.log 2>&1 &
nohup python3 dsp/module/updateCost.py > updateCost.log 2>&1 &
nohup python3 dsp/module/update_website.py > update_website.log 2>&1 &
