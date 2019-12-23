# Git Statistics
This is a mini-project for generating statistics based on git repositories. There have been taken two version control systems (VCS) for generating the statistics: Gitea and Github.

There have been used relevant APIs for retrieving entity information for each VCS. List of entities retrieved:
 - Organizations
 - Users
 - Repositories
 - Branches
 - Commits
 
Github API is richer and it even provides a Stats API which gets some important statistics without having to make multiple calls to the entities APIs.

All data get stored in a MySQL database in order to make it possible to generate visualizations and reports on some BI tool later.