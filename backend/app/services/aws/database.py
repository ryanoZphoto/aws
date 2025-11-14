"""
Database Services Checker - RDS, Aurora, DynamoDB, ElastiCache, etc.
"""
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError, BotoCoreError

from app.services.aws.base import AWSServiceChecker


class DatabaseChecker(AWSServiceChecker):
    """Checker for AWS Database services"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rds_client = self.session.client('rds')
        self.dynamodb_client = self.session.client('dynamodb')
        self.elasticache_client = self.session.client('elasticache')
        self.neptune_client = self.session.client('neptune')
        self.docdb_client = self.session.client('docdb')
        self.timestream_client = self.session.client('timestream-query')
    
    def get_service_name(self) -> str:
        return "database"
    
    def check_service(self, operation: str, **kwargs) -> Dict[str, Any]:
        """
        Execute database service operations
        
        Supported operations:
        - rds: describe_db_instances, describe_db_clusters, etc.
        - dynamodb: list_tables, describe_table, scan, query, etc.
        - elasticache: describe_cache_clusters, describe_replication_groups, etc.
        - neptune: describe_db_clusters, describe_db_instances, etc.
        - docdb: describe_db_clusters, describe_db_instances, etc.
        - timestream: list_databases, list_tables, etc.
        """
        service = kwargs.pop('service', 'rds')
        
        try:
            if service == 'rds':
                return self._check_rds(operation, **kwargs)
            elif service == 'dynamodb':
                return self._check_dynamodb(operation, **kwargs)
            elif service == 'elasticache':
                return self._check_elasticache(operation, **kwargs)
            elif service == 'neptune':
                return self._check_neptune(operation, **kwargs)
            elif service == 'docdb':
                return self._check_docdb(operation, **kwargs)
            elif service == 'timestream':
                return self._check_timestream(operation, **kwargs)
            else:
                raise ValueError(f"Unsupported database service: {service}")
        except (ClientError, BotoCoreError) as e:
            return self._handle_error(e, operation)
    
    def _check_rds(self, operation: str, **kwargs) -> Dict[str, Any]:
        """RDS operations"""
        if not hasattr(self.rds_client, operation):
            raise ValueError(f"Unsupported RDS operation: {operation}")
        
        method = getattr(self.rds_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "rds",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_dynamodb(self, operation: str, **kwargs) -> Dict[str, Any]:
        """DynamoDB operations"""
        if not hasattr(self.dynamodb_client, operation):
            raise ValueError(f"Unsupported DynamoDB operation: {operation}")
        
        method = getattr(self.dynamodb_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "dynamodb",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_elasticache(self, operation: str, **kwargs) -> Dict[str, Any]:
        """ElastiCache operations"""
        if not hasattr(self.elasticache_client, operation):
            raise ValueError(f"Unsupported ElastiCache operation: {operation}")
        
        method = getattr(self.elasticache_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "elasticache",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_neptune(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Neptune operations"""
        if not hasattr(self.neptune_client, operation):
            raise ValueError(f"Unsupported Neptune operation: {operation}")
        
        method = getattr(self.neptune_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "neptune",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_docdb(self, operation: str, **kwargs) -> Dict[str, Any]:
        """DocumentDB operations"""
        if not hasattr(self.docdb_client, operation):
            raise ValueError(f"Unsupported DocumentDB operation: {operation}")
        
        method = getattr(self.docdb_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "docdb",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_timestream(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Timestream operations"""
        if not hasattr(self.timestream_client, operation):
            raise ValueError(f"Unsupported Timestream operation: {operation}")
        
        method = getattr(self.timestream_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "timestream",
            "operation": operation,
            "data": response,
            "success": True,
        }
