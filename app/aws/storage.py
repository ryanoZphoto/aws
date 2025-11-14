"""Storage service integrations (S3, EFS, etc.)."""
from typing import Dict, Any
from app.aws.base import AWSServiceBase, AWSServiceError


class StorageService(AWSServiceBase):
    """Storage service integration."""
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of storage services."""
        results = {}
        
        # S3 Health Check
        try:
            s3 = self.get_client("s3")
            response = s3.list_buckets()
            results["s3"] = {
                "status": "healthy",
                "bucket_count": len(response.get("Buckets", [])),
            }
        except Exception as e:
            self._handle_error(e, "S3 health check")
        
        # EFS Health Check
        try:
            efs = self.get_client("efs")
            response = efs.describe_file_systems(MaxItems=1)
            results["efs"] = {
                "status": "healthy",
                "service_available": True,
            }
        except Exception as e:
            self._handle_error(e, "EFS health check")
        
        return results
    
    def list_resources(self, service: str = "s3", **kwargs) -> Dict[str, Any]:
        """
        List storage resources.
        
        Args:
            service: Service name (s3, efs, etc.)
            **kwargs: Additional filters
        """
        if service == "s3":
            return self._list_s3_buckets(**kwargs)
        elif service == "efs":
            return self._list_efs_filesystems(**kwargs)
        else:
            raise AWSServiceError(f"Unsupported storage service: {service}")
    
    def _list_s3_buckets(self, **kwargs) -> Dict[str, Any]:
        """List S3 buckets."""
        s3 = self.get_client("s3")
        try:
            response = s3.list_buckets()
            
            buckets = []
            for bucket in response.get("Buckets", []):
                # Get bucket location
                try:
                    location_response = s3.get_bucket_location(Bucket=bucket["Name"])
                    region = location_response.get("LocationConstraint") or "us-east-1"
                except:
                    region = "unknown"
                
                buckets.append({
                    "name": bucket.get("Name"),
                    "creation_date": bucket.get("CreationDate").isoformat() if bucket.get("CreationDate") else None,
                    "region": region,
                })
            
            return {
                "service": "s3",
                "resource_type": "buckets",
                "count": len(buckets),
                "buckets": buckets,
            }
        except Exception as e:
            self._handle_error(e, "List S3 buckets")
    
    def _list_efs_filesystems(self, **kwargs) -> Dict[str, Any]:
        """List EFS file systems."""
        efs = self.get_client("efs")
        try:
            response = efs.describe_file_systems()
            
            filesystems = []
            for fs in response.get("FileSystems", []):
                filesystems.append({
                    "file_system_id": fs.get("FileSystemId"),
                    "creation_token": fs.get("CreationToken"),
                    "life_cycle_state": fs.get("LifeCycleState"),
                    "size_in_bytes": fs.get("SizeInBytes", {}),
                })
            
            return {
                "service": "efs",
                "resource_type": "file_systems",
                "count": len(filesystems),
                "file_systems": filesystems,
            }
        except Exception as e:
            self._handle_error(e, "List EFS file systems")
