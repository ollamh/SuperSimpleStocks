# SuperSimpleStocks

This is a sample project to implement some class which will calculate 
stock market formulas based on user input.
 
1. First, I envision a model of this exchange. I assume there is a main 
object which stays alive and provides a user with an interface for 
dealing with stocks, such as buying, selling, adding stocks, removing 
them from exchange and getting all share index for all stocks volume 
weighted prices. I assume if no date range mentioned, this index will
be calculated based on last 5 minutes trades. I assume the timestamps
are timezone naive ones.
 
2. Second, I assume a class which is storing information about stock and 
encapsulate all methods for calculating p/e ratio and dividend yield.
also, it stores all trades made with this stock and presents a method
to retrieve them.

3. Third, a class representing trade, which is used mainly for
storing and providing an interface for access to it's properties.
 
4. Then, I create a python 3.4 project, using virtual environment. All 
necessary packages are defined in requirements.txt file. For the Debian
based linux, installation process will be:


	 sudo apt-get install python-pip
     pip install virtualenv
     pip install virtualenvwrapper
     mkdir ~/.virtualenvs


Put inside your ~/.bashrc:
 
      if [ `which virtualenvwrapper.sh` ]; then 
        export WORKON_HOME=$HOME/.virtualenvs
        source `which virtualenvwrapper.sh`
        export PIP_RESPECT_VIRTUALENV=true
      fi

Then, create a projects environment:

    mkvirtualenv sss --python=python3
    pip install -r requirements.txt
 
And every time you need to enable project environment, you need to
 run:
 
    workon sss
 
After you finish with that:
 
    deactivate
 
5. Now, I create a tests module for defining unit tests. Also, I use
nose and coverage python packages for getting more useful output. Then
I define .coveragerc file, which contains settings for coverage. Nose
automatically scans project directory and uses all files starting with
test_* to build a test set. Also, for checking code I use flake8 tool.
  
To run tests you need to run in terminal:
  
    nosetests tests -v --with-coverage
    
To check code with flake8 you run (for example):

    flake8 --max-complexity 10 sss/gbce.py

Where instead of gbce.py you can put any file.
  
6. Also, I provide a sample data file, which is defined in the task PDF.
I assume it will be used in calculating. This data will be used for
testing, but also can be used as initial data for the project.
 
To load data into GBCE class:
     import json
  
     with open('data/stocks.json', 'r') as f:
         gbce = GBCE(json.loads(f.read())
          
This will load into gbce object a set described in the task.
   
7. The usage of the classes could be like this:


    from sss import GBCE, Stock
    
    gbce = GBCE()
    
    gbce.add_stock('CMS', 'Common', 200, 8)
    gbce.add_stock('PMT', 'Preferred', 100, 10, 0.04)


Now, you have two stocks and you can do operations:


    gbce.buy('CMS', 20.5, 300)
    gbce.sell('PMT', 30.7, 150)

    stock = gbce.get_stock('CMS')
    stock.p_e_ratio(100)
    
    stock.volume_weighted_stock_price()


    
    
       
    

 
