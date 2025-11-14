"""
Storage Services Checker - S3, EFS, FSx, Glacier, Backup, etc.
"""
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError, BotoCoreError

from app.services.aws.base import AWSServiceChecker


class StorageChecker(AWSServiceChecker):
    """Checker for AWS Storage services"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.s3_client = self.session.client('s3')
        self.efs_client = self.session.client('efs')
        self.fsx_client = self.session.client('fsx')
        self.glacier_client = self.session.client('glacier')
        self.backup_client = self.session.client('backup')
    
    def get_service_name(self) -> str:
        return "storage"
    
    def check_service(self, operation: str, **kwargs) -> Dict[str, Any]:
        """
        Execute storage service operations
        
        Supported operations:
        - s3: list_buckets, list_objects, get_bucket_location, etc.
        - efs: describe_file_systems, describe_mount_targets, etc.
        - fsx: describe_file_systems, describe_backups, etc.
        - glacier: list_vaults, describe_vault, etc.
        - backup: list_backup_vaults, list_backup_jobs, etc.
        """
        service = kwargs.pop('service', 's3')
        
        try:
            if service == 's3':
                return self._check_s3(operation, **kwargs)
            elif service == 'efs':
                return self._check_efs(operation, **kwargs)
            elif service == 'fsx':
                return self._check_fsx(operation, **kwargs)
            elif service == 'glacier':
                return self._check_glacier(operation, **kwargs)
            elif service == 'backup':
                return self._check_backup(operation, **kwargs)
            else:
                raise ValueError(f"Unsupported storage service: {service}")
        except (ClientError, BotoCoreError) as e:
            return self._handle_error(e, operation)
    
    def _check_s3(self, operation: str, **kwargs) -> Dict[str, Any]:
        """S3 operations"""
        if not hasattr(self.s3_client, operation):
            raise ValueError(f"Unsupported S3 operation: {operation}")
        
        method = getattr(self.s3_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "s3",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_efs(self, operation: str, **kwargs) -> Dict[str, Any]:
        """EFS operations"""
        if not hasattr(self.efs_client, operation):
            raise ValueError(f"Unsupported EFS operation: {operation}")
        
        method = getattr(self.efs_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "efs",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_fsx(self, operation: str, **kwargs) -> Dict[str, Any]:
        """FSx operations"""
        if not hasattr(self.fsx_client, operation):
            raise ValueError(f"Unsupported FSx operation: {operation}")
        
        method = getattr(self.fsx_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "fsx",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_glacier(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Glacier operations"""
        if not hasattr(self.glacier_client, operation):
            raise ValueError(f"Unsupported Glacier operation: {operation}")
        
        method = getattr(self.glacier_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "glacier",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_backup(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Backup operations"""
        if not hasattr(self.backup_client, operation):
            raise ValueError(f"Unsupported Backup operation: {operation}")
        
        method = getattr(self.backup_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "backup",
            "operation": operation,
            "data": response,
            "success": True,
        }
