"""Security service integrations (IAM, Cognito, etc.)."""
from typing import Dict, Any
from app.aws.base import AWSServiceBase, AWSServiceError


class SecurityService(AWSServiceBase):
    """Security service integration."""
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of security services."""
        results = {}
        
        # IAM Health Check
        try:
            iam = self.get_client("iam")
            response = iam.get_account_summary()
            results["iam"] = {
                "status": "healthy",
                "service_available": True,
            }
        except Exception as e:
            self._handle_error(e, "IAM health check")
        
        return results
    
    def list_resources(self, service: str = "iam", **kwargs) -> Dict[str, Any]:
        """
        List security resources.
        
        Args:
            service: Service name (iam, cognito, etc.)
            **kwargs: Additional filters
        """
        if service == "iam":
            return self._list_iam_users(**kwargs)
        else:
            raise AWSServiceError(f"Unsupported security service: {service}")
    
    def _list_iam_users(self, **kwargs) -> Dict[str, Any]:
        """List IAM users."""
        iam = self.get_client("iam")
        try:
            response = iam.list_users()
            
            users = []
            for user in response.get("Users", []):
                users.append({
                    "user_name": user.get("UserName"),
                    "user_id": user.get("UserId"),
                    "arn": user.get("Arn"),
                    "create_date": user.get("CreateDate").isoformat() if user.get("CreateDate") else None,
                    "path": user.get("Path"),
                })
            
            return {
                "service": "iam",
                "resource_type": "users",
                "count": len(users),
                "users": users,
            }
        except Exception as e:
            self._handle_error(e, "List IAM users")
