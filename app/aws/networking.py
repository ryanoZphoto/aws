"""Networking service integrations (VPC, CloudFront, etc.)."""
from typing import Dict, Any
from app.aws.base import AWSServiceBase, AWSServiceError


class NetworkingService(AWSServiceBase):
    """Networking service integration."""
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of networking services."""
        results = {}
        
        # VPC Health Check
        try:
            ec2 = self.get_client("ec2")
            response = ec2.describe_vpcs(MaxResults=1)
            results["vpc"] = {
                "status": "healthy",
                "service_available": True,
            }
        except Exception as e:
            self._handle_error(e, "VPC health check")
        
        # CloudFront Health Check
        try:
            cloudfront = self.get_client("cloudfront")
            response = cloudfront.list_distributions(MaxItems=1)
            results["cloudfront"] = {
                "status": "healthy",
                "service_available": True,
            }
        except Exception as e:
            self._handle_error(e, "CloudFront health check")
        
        return results
    
    def list_resources(self, service: str = "vpc", **kwargs) -> Dict[str, Any]:
        """
        List networking resources.
        
        Args:
            service: Service name (vpc, cloudfront, etc.)
            **kwargs: Additional filters
        """
        if service == "vpc":
            return self._list_vpcs(**kwargs)
        elif service == "cloudfront":
            return self._list_cloudfront_distributions(**kwargs)
        else:
            raise AWSServiceError(f"Unsupported networking service: {service}")
    
    def _list_vpcs(self, **kwargs) -> Dict[str, Any]:
        """List VPCs."""
        ec2 = self.get_client("ec2")
        try:
            response = ec2.describe_vpcs()
            
            vpcs = []
            for vpc in response.get("Vpcs", []):
                vpcs.append({
                    "vpc_id": vpc.get("VpcId"),
                    "cidr_block": vpc.get("CidrBlock"),
                    "state": vpc.get("State"),
                    "is_default": vpc.get("IsDefault", False),
                    "tags": {tag["Key"]: tag["Value"] for tag in vpc.get("Tags", [])},
                })
            
            return {
                "service": "vpc",
                "resource_type": "vpcs",
                "count": len(vpcs),
                "vpcs": vpcs,
            }
        except Exception as e:
            self._handle_error(e, "List VPCs")
    
    def _list_cloudfront_distributions(self, **kwargs) -> Dict[str, Any]:
        """List CloudFront distributions."""
        cloudfront = self.get_client("cloudfront")
        try:
            response = cloudfront.list_distributions()
            
            distributions = []
            for dist in response.get("DistributionList", {}).get("Items", []):
                distributions.append({
                    "distribution_id": dist.get("Id"),
                    "domain_name": dist.get("DomainName"),
                    "status": dist.get("Status"),
                    "enabled": dist.get("Enabled"),
                })
            
            return {
                "service": "cloudfront",
                "resource_type": "distributions",
                "count": len(distributions),
                "distributions": distributions,
            }
        except Exception as e:
            self._handle_error(e, "List CloudFront distributions")
