# InternetTopologyZoo

### Internet Topology Zoo long term data store.

The Internet Topology Zoo's web page https://topology-zoo.org/ will be
loosing support at some time in the not too distant future. Hence we
have constructed a number of places to obtain the data. One is here,
and the other main one is in
[figshare](https://doi.org/10.25909/30153949) with DOI
[https://doi.org/10.25909/30153949](https://doi.org/10.25909/30153949).



### Details

This is a collection of over 250 telecommunications networks transcribed into GraphML and GML for easy use in network topology projects.

Original site for the data is https://topology-zoo.org/index.html

The data is describe primarily in 1 paper, but there are several additional works:

    + **The Internet Topology Zoo**, Simon Knight, Hung X. Nguyen, Nickolas Falkner, Rhys Bowden, Matthew Roughan, IEEE Journal on Selected Areas in Communications, Vol. 29, No. 9, October 2011
    + **I Can See For Miles: Re-visualising The Internet**, S. Knight, N. Falkner, H.X. Nguyen, P. Tune, M. Roughan, IEEE Network, Vol.26, Issue 6, pp.26-32, November-December 2012.
    + **Planarity of Data Networks**, Rhys Bowden, Hung X. Nguyen, Nickolas Falkner, Simon Knight, Matthew Roughan, International Telecommunications Conference, September, 2011, San Francisco.
    + **Realistic Network Topology Construction and Emulation from Multiple Data Sources**, Simon Knight, Hung Nguyen, Nickolas Falkner, Matthew Roughan, Technical Report, May, 2012.

The data is included in two main formats (each in a self contained tar.gz file).

    + GraphML
    + GML

These are two well-supported and portable graph formats that allow the metadata to be stored with the graph including geolocation of nodes and some classification data for the types of networks.

There are two additional sets of data

    + maps: stores PNGs of each network, in case you want to see them or check your own visualisations.
    + sources: provides the source images used to generate the data. These were not distributed with the original topology-zoo dataset, but form the provenance of the data, and may be of historical interest. So we include there here, noting that they are all over 15 years old. 

There is a python toolset to help work with this data, that could be
installed using easy_install topzootools but it hasn't been maintained
for a decade, and is unlikely to work. Its source can be found at
[https://github.com/sk2/topzootools/tree/master/TopZooTools](https://github.com/sk2/topzootools/tree/master/TopZooTools)
if needed, but most of it should be accessible to modern tools for
working with graphs and networks. 

### Citation

If you use the data, please cite the first paper on the list, ie

```
@ARTICLE{6027859, 
	 author={Knight, S. and Nguyen, H.X. and Falkner, N. and Bowden, R. and Roughan, M.}, 
	 journal={IEEE Journal on Selected Areas in Communications}, title={The Internet Topology Zoo}, 
	 year={2011}, 
	 month={October}, 
	 volume={29}, 
	 number={9}, 
	 pages={1765--1775}, 
	 keywords={Internet Topology Zoo;PoP-level topology;meta-data;network data;network designs;network structure;network topology;Internet;meta data;telecommunication network topology;}, 
	 doi={10.1109/JSAC.2011.111002}, 
	 ISSN={0733-8716},
}
```


