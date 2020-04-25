# Barcoder Generator 1.0.0

1. Creates n (>100000) random k-length sequence 
2. Conduct random sampling of 1/30*n x m times to ensure Hamming distance >= 20% (kmer-length)
3. Remove sequences with Hamming Distance <= 20%
4. Create a Histogram for Hamming Distance Count
5. Ensure Sequences are Unique (In Future Version)

'''bash
python barcode_generation.py <number of sequence> <length of sequence> <sample size> <number of sampling> <Minimum Hamming Distance> <Number of Core> <Prefix for File names>
'''

 # Example:
'''bash
python barcode_generation.py 300000 20 10000 20 0.40 3 300k_20l
'''

This will generate 300000 random sequences with a length of 20. It will random sampled 20 times with a 10000 sample size. Hammding distance of less than 0.4 * l = 8 is removed into another seperate file for post-processing. HD argument can receive percentage in floating number (ie. HD < 1) or receive integers ie. HD > 1. Optional arguments are Number of Core (default is 1) and Prefix for file name.  
