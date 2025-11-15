"""Database service integrations (RDS, DynamoDB, etc.)."""
from typing import Dict, Any
from app.aws.base import AWSServiceBase, AWSServiceError


class DatabaseService(AWSServiceBase):
    """Database service integration."""
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of database services."""
        results = {}
        
        # RDS Health Check
        try:
            rds = self.get_client("rds")
            response = rds.describe_db_instances(MaxRecords=1)
            results["rds"] = {
                "status": "healthy",
                "service_available": True,
            }
        except Exception as e:
            self._handle_error(e, "RDS health check")
        
        # DynamoDB Health Check
        try:
            dynamodb = self.get_client("dynamodb")
            response = dynamodb.list_tables(Limit=1)
            results["dynamodb"] = {
                "status": "healthy",
                "service_available": True,
            }
        except Exception as e:
            self._handle_error(e, "DynamoDB health check")
        
        return results
    
    def list_resources(self, service: str = "rds", **kwargs) -> Dict[str, Any]:
        """
        List database resources.
        
        Args:
            service: Service name (rds, dynamodb, etc.)
            **kwargs: Additional filters
        """
        if service == "rds":
            return self._list_rds_instances(**kwargs)
        elif service == "dynamodb":
            return self._list_dynamodb_tables(**kwargs)
        else:
            raise AWSServiceError(f"Unsupported database service: {service}")
    
    def _list_rds_instances(self, **kwargs) -> Dict[str, Any]:
        """List RDS instances."""
        rds = self.get_client("rds")
        try:
            response = rds.describe_db_instances()
            
            instances = []
            for instance in response.get("DBInstances", []):
                instances.append({
                    "db_instance_identifier": instance.get("DBInstanceIdentifier"),
                    "engine": instance.get("Engine"),
                    "engine_version": instance.get("EngineVersion"),
                    "db_instance_status": instance.get("DBInstanceStatus"),
                    "db_instance_class": instance.get("DBInstanceClass"),
                    "allocated_storage": instance.get("AllocatedStorage"),
                })
            
            return {
                "service": "rds",
                "resource_type": "instances",
                "count": len(instances),
                "instances": instances,
            }
        except Exception as e:
            self._handle_error(e, "List RDS instances")
    
    def _list_dynamodb_tables(self, **kwargs) -> Dict[str, Any]:
        """List DynamoDB tables."""
        dynamodb = self.get_client("dynamodb")
        try:
            response = dynamodb.list_tables()
            
            tables = []
            table_names = response.get("TableNames", [])
            
            # Get details for each table
            for table_name in table_names:
                try:
                    table_response = dynamodb.describe_table(TableName=table_name)
                    table = table_response.get("Table", {})
                    tables.append({
                        "table_name": table.get("TableName"),
                        "table_status": table.get("TableStatus"),
                        "item_count": table.get("ItemCount", 0),
                        "table_size_bytes": table.get("TableSizeBytes", 0),
                    })
                except Exception:
                    # If we can't describe a table, just include the name
                    tables.append({
                        "table_name": table_name,
                        "table_status": "unknown",
                    })
            
            return {
                "service": "dynamodb",
                "resource_type": "tables",
                "count": len(tables),
                "tables": tables,
            }
        except Exception as e:
            self._handle_error(e, "List DynamoDB tables")
