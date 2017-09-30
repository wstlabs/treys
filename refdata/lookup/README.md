These 2 files represented the saved OrderedDict structs of the respective names as 
members of the LookupTable object, in their natural CSV representation, from a
timepoint fairly early in the porting effort.  

So if we mess anything up in attempting to refactor the generating process for these 
tables, we should be able to detect that fairly quickly by comparing to the  
reference snapshots.

Note that even though these tuple streams represent OrderedDict, they're not in
rank order (that is, not ordered by value); but rather, by insertion order (which,
we later found, was not montone by rank).  But that's OK.  The sole purpose of  
representing these tables as OrderedDicts internally was to be able to do traversals 
in a reproducible order, if needed (for example, when saving to output files).

