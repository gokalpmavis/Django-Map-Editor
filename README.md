# DjangoMapEditor
This is a simple map editor web application which uses Django. 

In this web application, you can create a map of an environment by objects which made up of unit squares. Multiple users can edit the same map at the same time by seeing eachothers processes. To avoid the conflict changes there is a system that forces client to mark the area that he/she is currently working on, so other clients who working on the same map cannot change the marked area which belongs to someone else. In other words, to make deleting, adding and moving operations, the locations which client is doing these operations should belong to this client’s progress area. 

A location can belong only one progress area at a time and the changes in this area will be visible for the other clients when the owner of this area stops this progress. The system uses simple sqlite database which contains map objects and environmental aspect objects which belongs to just one map with a “Foreign Key” relation such as building model, natural element model(water or tree) and road model.
