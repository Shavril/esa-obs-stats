# esa-obs-stats
Small utility to produce statistics from ADES astrometric observations.

As per ESA requirements, when reporting the observations on the monthly report, ESA wants to be provided the following 
information:

> Include a table in the report with the name (provisional and/or designated) of the targets, the V mag and the time 
> on sky (number of images times the exposure time) and a flag for being or not reported to the MPC.

## Usage

To generate the statistic,
1. Clone the repository.
2. Put the ADES `.xml` files with observations into folder `/obs-data/`.
3. This project uses `Poetry` for package management.  
   Complete package versions are specified in `pyproject.toml` file.  
   When you have poetry installed, go to the directory with .toml file,  
   and run `poetry install`.
4. Run `poetry run python main.py`. 

## Input

The input comes as `.xml` files in `/obs-data/`.  
The files contain astrometric observations in [ADES format](https://minorplanetcenter.net/iau/info/ADES.html).  
Only part of the file is used to produce the statistic.  
Minimal working example:

```xml
<ades version="2017">
  <obsBlock>
	<obsData>
      <optical>
        <trkSub>A11gr7L</trkSub>
        <obsTime>2024-12-26T17:27:59.727Z</obsTime>
        <mag>17.3</mag>
        <exp>3</exp>
      </optical>
    </obsData>
  </obsBlock>
</ades>
```

## Output

The produced statistics is saved as `result.txt` file.  
It looks like this:  

```
TARGET         V mag  Time on sky Reported to the MPC?
=======================================================                  
2012 AD3       19.7   100.0       Y                                     
2016 JW5       19.5   80.0        Y                   
2016 VR5       16.7   80.0        Y 
```
