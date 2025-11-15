"""Compute service integrations (EC2, Lambda, ECS, etc.)."""
from typing import Dict, Any, List
from app.aws.base import AWSServiceBase, AWSServiceError
from app.core.logging import logger


class ComputeService(AWSServiceBase):
    """Compute service integration."""
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of compute services."""
        results = {}
        
        # EC2 Health Check
        try:
            ec2 = self.get_client("ec2")
            response = ec2.describe_regions()
            results["ec2"] = {
                "status": "healthy",
                "available_regions": len(response.get("Regions", [])),
            }
        except Exception as e:
            self._handle_error(e, "EC2 health check")
        
        # Lambda Health Check
        try:
            lambda_client = self.get_client("lambda")
            response = lambda_client.list_functions(MaxItems=1)
            results["lambda"] = {
                "status": "healthy",
                "service_available": True,
            }
        except Exception as e:
            self._handle_error(e, "Lambda health check")
        
        # ECS Health Check
        try:
            ecs = self.get_client("ecs")
            response = ecs.list_clusters(maxResults=1)
            results["ecs"] = {
                "status": "healthy",
                "service_available": True,
            }
        except Exception as e:
            self._handle_error(e, "ECS health check")
        
        return results
    
    def list_resources(self, service: str = "ec2", **kwargs) -> Dict[str, Any]:
        """
        List compute resources.
        
        Args:
            service: Service name (ec2, lambda, ecs, etc.)
            **kwargs: Additional filters
        """
        if service == "ec2":
            return self._list_ec2_instances(**kwargs)
        elif service == "lambda":
            return self._list_lambda_functions(**kwargs)
        elif service == "ecs":
            return self._list_ecs_clusters(**kwargs)
        else:
            raise AWSServiceError(f"Unsupported compute service: {service}")
    
    def _list_ec2_instances(self, **kwargs) -> Dict[str, Any]:
        """List EC2 instances."""
        ec2 = self.get_client("ec2")
        try:
            filters = kwargs.get("filters", [])
            response = ec2.describe_instances(Filters=filters)
            
            instances = []
            for reservation in response.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    instances.append({
                        "instance_id": instance.get("InstanceId"),
                        "instance_type": instance.get("InstanceType"),
                        "state": instance.get("State", {}).get("Name"),
                        "launch_time": instance.get("LaunchTime").isoformat() if instance.get("LaunchTime") else None,
                        "tags": {tag["Key"]: tag["Value"] for tag in instance.get("Tags", [])},
                    })
            
            return {
                "service": "ec2",
                "resource_type": "instances",
                "count": len(instances),
                "instances": instances,
            }
        except Exception as e:
            self._handle_error(e, "List EC2 instances")
    
    def _list_lambda_functions(self, **kwargs) -> Dict[str, Any]:
        """List Lambda functions."""
        lambda_client = self.get_client("lambda")
        try:
            response = lambda_client.list_functions()
            
            functions = []
            for func in response.get("Functions", []):
                functions.append({
                    "function_name": func.get("FunctionName"),
                    "runtime": func.get("Runtime"),
                    "memory_size": func.get("MemorySize"),
                    "timeout": func.get("Timeout"),
                    "last_modified": func.get("LastModified"),
                })
            
            return {
                "service": "lambda",
                "resource_type": "functions",
                "count": len(functions),
                "functions": functions,
            }
        except Exception as e:
            self._handle_error(e, "List Lambda functions")
    
    def _list_ecs_clusters(self, **kwargs) -> Dict[str, Any]:
        """List ECS clusters."""
        ecs = self.get_client("ecs")
        try:
            response = ecs.list_clusters()
            cluster_arns = response.get("clusterArns", [])
            
            if cluster_arns:
                describe_response = ecs.describe_clusters(clusters=cluster_arns)
                clusters = []
                for cluster in describe_response.get("clusters", []):
                    clusters.append({
                        "cluster_name": cluster.get("clusterName"),
                        "status": cluster.get("status"),
                        "running_tasks_count": cluster.get("runningTasksCount", 0),
                        "pending_tasks_count": cluster.get("pendingTasksCount", 0),
                    })
            else:
                clusters = []
            
            return {
                "service": "ecs",
                "resource_type": "clusters",
                "count": len(clusters),
                "clusters": clusters,
            }
        except Exception as e:
            self._handle_error(e, "List ECS clusters")
