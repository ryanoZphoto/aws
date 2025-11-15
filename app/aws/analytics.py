"""Analytics service integrations (Athena, Redshift, etc.)."""
from typing import Dict, Any
from app.aws.base import AWSServiceBase, AWSServiceError


class AnalyticsService(AWSServiceBase):
    """Analytics service integration."""
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of analytics services."""
        results = {}
        
        # Athena Health Check
        try:
            athena = self.get_client("athena")
            response = athena.list_work_groups(MaxResults=1)
            results["athena"] = {
                "status": "healthy",
                "service_available": True,
            }
        except Exception as e:
            self._handle_error(e, "Athena health check")
        
        # Redshift Health Check
        try:
            redshift = self.get_client("redshift")
            response = redshift.describe_clusters(MaxRecords=1)
            results["redshift"] = {
                "status": "healthy",
                "service_available": True,
            }
        except Exception as e:
            self._handle_error(e, "Redshift health check")
        
        return results
    
    def list_resources(self, service: str = "athena", **kwargs) -> Dict[str, Any]:
        """
        List analytics resources.
        
        Args:
            service: Service name (athena, redshift, etc.)
            **kwargs: Additional filters
        """
        if service == "athena":
            return self._list_athena_workgroups(**kwargs)
        elif service == "redshift":
            return self._list_redshift_clusters(**kwargs)
        else:
            raise AWSServiceError(f"Unsupported analytics service: {service}")
    
    def _list_athena_workgroups(self, **kwargs) -> Dict[str, Any]:
        """List Athena workgroups."""
        athena = self.get_client("athena")
        try:
            response = athena.list_work_groups()
            
            workgroups = []
            for wg in response.get("WorkGroups", []):
                workgroups.append({
                    "name": wg.get("Name"),
                    "state": wg.get("State"),
                    "creation_time": wg.get("CreationTime").isoformat() if wg.get("CreationTime") else None,
                })
            
            return {
                "service": "athena",
                "resource_type": "workgroups",
                "count": len(workgroups),
                "workgroups": workgroups,
            }
        except Exception as e:
            self._handle_error(e, "List Athena workgroups")
    
    def _list_redshift_clusters(self, **kwargs) -> Dict[str, Any]:
        """List Redshift clusters."""
        redshift = self.get_client("redshift")
        try:
            response = redshift.describe_clusters()
            
            clusters = []
            for cluster in response.get("Clusters", []):
                clusters.append({
                    "cluster_identifier": cluster.get("ClusterIdentifier"),
                    "cluster_status": cluster.get("ClusterStatus"),
                    "node_type": cluster.get("NodeType"),
                    "number_of_nodes": cluster.get("NumberOfNodes"),
                })
            
            return {
                "service": "redshift",
                "resource_type": "clusters",
                "count": len(clusters),
                "clusters": clusters,
            }
        except Exception as e:
            self._handle_error(e, "List Redshift clusters")
