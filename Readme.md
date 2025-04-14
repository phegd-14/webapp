This is a info on how to run the damn thing(for intenal use only 😜)
docker build -t my-backend-app . 
k create ns webapp   
kns webapp      
k apply -f frontend-api.Deployment.yaml -n webapp 
k apply -f webapp-secrets.yaml -n webapp   
k apply -f backend-api.Deployment.yaml -n webapp  
k get deployments
