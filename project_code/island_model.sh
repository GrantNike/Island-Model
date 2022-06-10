for i in {1..10}
do
    python3 island_model.py parameters1.txt output1 $i
    python3 island_model.py parameters2.txt output2 $i
    python3 island_model.py parameters3.txt output3 $i
done
python3 plot_data3point.py