# SDE Online Assessment
Submitted by Salman Sharif

## Solution description
Solution was created using python 3.7.6
All unit testing were also done using that version of python
Solution executable is called common.py
Usage for common.py is: python common.py inputFile.json, outputFile.json

Running `docker build .` will build and run the unit test. 

**If pyInstaller worked** Solution executable would be in the dist directory. moving and renaming this file to `sde-test-solution` should work. This has not been varified as of right now. sample `sde-test-solution` is included but might not work on your machines. This was used on my own machine and I did the steps above to get that executable to work

**Dockerfile was not completed**. Dockerfile does show the steps to create the executable named `sde-test-solution`. Specifically to create that executable, use `pyInstaller` and that will create a file in the `/submission/dist/` directory. Please note this has not been varified as I was unable to get docker working on my machine. 

### Asumptions:
- Inputfile is in the correct format as described in the problem description
- Outputfile is generated automatically and replaces any existing files with that name

### Algorithm overview:
1. open the input json files and read the contents into memory as a json dict
2. seperate out the government and corporate bonds when based on type. Validate the data as well
3. compare each corporate bond with each government bond to find nearest government bound as described in problem description
4. creaete and append the nearest government bond to corporate bond to the resulting list
5. open and write that resulting list to output file

### Complexity analysis:
Runtime of this algorithm is O(N*M) where N is number of corporate bonds, M is number of government bonds. Reason for this is in the algoritms step 3, we need to compare each corporate bond with all other government bonds. This is the most time complexing step in the algorithm

Space complexity is O(N+M). Reason for this is we are storing the data in memory and as a result when we open the files to read them, they take up the most memory. 
