for i in {1..10}
do
    python3 standard_GA.py parameters1.txt output1 $i
    python3 island_model.py parameters1.txt output2 $i
done
python3 plot_data.py