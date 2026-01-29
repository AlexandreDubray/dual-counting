#parallel --bar -j 8 python dual_mc.py {} :::: benchmarks/sat_inst.txt
#for file in $(cat benchmarks/sat_inst.txt);
#do
#    python dual_mc.py $file
#done


echo "instance,td-width" > td-stats.csv
parallel -j  8 --bar python dual_mc.py {} :::: benchmarks/sat_inst.txt >> td-stats.csv
