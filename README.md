# Git Statistics
This is a mini-project for generating statistics based on git repositories. There has been taken Github as a version control systems (VCS).

The file, named **Git_Data_Extraction_and_Processing** is used for extracting the data from each VCS via APIs. The list of entities retrieved for a single Github repository:
- Branches
- Commits
- Pull requests
- Issues

Github API is rich and it even provides a Stats API which gets some important statistics without having to make multiple calls to the entities APIs.

All data get stored in a MySQL database in order to make it possible to generate visualizations and reports on some BI tool later. There has also been included the option of storing them in CSV files for better retrieval afterwards.

The `data` folder contains generated CSV files for the Apache Spark repository and those data are later used for analysis.

The file, named **Git_Data_Analysis** contains interesting data analysis on the generated data. The insights include:
- Number of commits by hour
- Number of commits by date
- Top contributors along with their commits
- Active Pull Requests
- Pull Requests by label
- Issues