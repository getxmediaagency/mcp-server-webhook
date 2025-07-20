"""
Human-in-the-Loop Manager for MCP Server

This module provides human approval workflow integration that allows:
- Action approval requests and responses
- Approval workflow management
- Approval history tracking
- Integration with external approval systems
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List, Callable
import time
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ApprovalRequest:
    """Data class for approval request information."""
    request_id: str
    action_name: str
    params: Dict[str, Any]
    timestamp: float
    status: str  # 'pending', 'approved', 'rejected', 'expired'
    approver: Optional[str] = None
    comments: Optional[str] = None
    approval_time: Optional[float] = None
    expiration_time: Optional[float] = None


class HumanLoopManager:
    """
    Manager for human-in-the-loop approval workflows.
    
    Features:
    - Approval request creation and tracking
    - Approval workflow management
    - Approval history and audit trail
    - Configurable approval requirements
    - Integration with external approval systems
    """
    
    def __init__(self, approval_timeout: int = 3600):  # 1 hour default timeout
        """
        Initialize the human loop manager.
        
        Args:
            approval_timeout: Timeout in seconds for approval requests
        """
        self.approval_timeout = approval_timeout
        self.logger = logging.getLogger('human_loop')
        
        # Store approval requests and requirements
        self.pending_approvals: Dict[str, ApprovalRequest] = {}
        self.approval_history: List[ApprovalRequest] = []
        self.approval_requirements: set = set()
        
        # Callback for external approval systems
        self.approval_callbacks: List[Callable] = []
        
        # Start background task for cleanup
        asyncio.create_task(self._cleanup_expired_approvals())
        
        self.logger.info("Human loop manager initialized")
    
    def add_approval_requirement(self, action_name: str):
        """
        Add an action to the approval requirements list.
        
        Args:
            action_name: Name of action that requires approval
        """
        self.approval_requirements.add(action_name)
        self.logger.info(f"Added approval requirement for action: {action_name}")
    
    def remove_approval_requirement(self, action_name: str):
        """
        Remove an action from the approval requirements list.
        
        Args:
            action_name: Name of action to remove from approval requirements
        """
        if action_name in self.approval_requirements:
            self.approval_requirements.remove(action_name)
            self.logger.info(f"Removed approval requirement for action: {action_name}")
    
    def requires_approval(self, action_name: str) -> bool:
        """
        Check if an action requires human approval.
        
        Args:
            action_name: Name of action to check
            
        Returns:
            True if approval is required, False otherwise
        """
        return action_name in self.approval_requirements
    
    async def create_approval_request(
        self, 
        request_id: str, 
        action_name: str, 
        params: Dict[str, Any],
        approver: Optional[str] = None
    ) -> ApprovalRequest:
        """
        Create a new approval request.
        
        Args:
            request_id: Unique request identifier
            action_name: Name of action requiring approval
            params: Action parameters
            approver: Optional specific approver
            
        Returns:
            Created approval request
        """
        expiration_time = time.time() + self.approval_timeout
        
        approval_request = ApprovalRequest(
            request_id=request_id,
            action_name=action_name,
            params=params,
            timestamp=time.time(),
            status='pending',
            approver=approver,
            expiration_time=expiration_time
        )
        
        self.pending_approvals[request_id] = approval_request
        
        self.logger.info(f"Created approval request {request_id} for action: {action_name}")
        
        # Notify external approval systems
        await self._notify_approval_callbacks(approval_request)
        
        return approval_request
    
    async def process_approval(
        self, 
        request_id: str, 
        approved: bool, 
        comments: str = "",
        approver: str = "unknown"
    ) -> Optional[Dict[str, Any]]:
        """
        Process an approval response.
        
        Args:
            request_id: Request ID to approve/reject
            approved: True for approval, False for rejection
            comments: Optional comments from approver
            approver: Name of the approver
            
        Returns:
            Action result if approved, None if rejected
        """
        if request_id not in self.pending_approvals:
            raise ValueError(f"Approval request {request_id} not found")
        
        approval_request = self.pending_approvals[request_id]
        
        # Check if request has expired
        if approval_request.expiration_time and time.time() > approval_request.expiration_time:
            approval_request.status = 'expired'
            approval_request.comments = "Request expired"
            self.logger.warning(f"Approval request {request_id} expired")
            
            # Move to history
            self.approval_history.append(approval_request)
            del self.pending_approvals[request_id]
            
            return None
        
        # Update approval request
        approval_request.status = 'approved' if approved else 'rejected'
        approval_request.approver = approver
        approval_request.comments = comments
        approval_request.approval_time = time.time()
        
        self.logger.info(
            f"Approval request {request_id} {approval_request.status} by {approver}"
        )
        
        # Move to history
        self.approval_history.append(approval_request)
        del self.pending_approvals[request_id]
        
        if approved:
            # Execute the approved action
            from .action_registry import ActionRegistry
            # Note: This would need access to the action registry
            # For now, return the action parameters for execution
            return {
                'action_name': approval_request.action_name,
                'params': approval_request.params,
                'approved_by': approver,
                'approval_time': approval_request.approval_time
            }
        
        return None
    
    def get_pending_approvals(self) -> List[Dict[str, Any]]:
        """
        Get list of pending approval requests.
        
        Returns:
            List of pending approval request information
        """
        pending = []
        
        for request_id, approval_request in self.pending_approvals.items():
            pending.append({
                'request_id': request_id,
                'action_name': approval_request.action_name,
                'params': approval_request.params,
                'timestamp': approval_request.timestamp,
                'expiration_time': approval_request.expiration_time,
                'approver': approval_request.approver
            })
        
        return pending
    
    def get_approval_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get approval history.
        
        Args:
            limit: Maximum number of history entries to return
            
        Returns:
            List of approval history entries
        """
        history = []
        
        for approval_request in self.approval_history[-limit:]:
            history.append(asdict(approval_request))
        
        return history
    
    async def _notify_approval_callbacks(self, approval_request: ApprovalRequest):
        """
        Notify external approval systems of new approval requests.
        
        Args:
            approval_request: The approval request to notify about
        """
        for callback in self.approval_callbacks:
            try:
                await callback(approval_request)
            except Exception as e:
                self.logger.error(f"Error in approval callback: {str(e)}")
    
    async def _cleanup_expired_approvals(self):
        """Background task to clean up expired approval requests."""
        while True:
            try:
                current_time = time.time()
                expired_requests = []
                
                for request_id, approval_request in self.pending_approvals.items():
                    if (approval_request.expiration_time and 
                        current_time > approval_request.expiration_time):
                        expired_requests.append(request_id)
                
                for request_id in expired_requests:
                    approval_request = self.pending_approvals[request_id]
                    approval_request.status = 'expired'
                    approval_request.comments = "Auto-expired"
                    
                    self.logger.info(f"Auto-expired approval request: {request_id}")
                    
                    # Move to history
                    self.approval_history.append(approval_request)
                    del self.pending_approvals[request_id]
                
                # Sleep for 60 seconds before next cleanup
                await asyncio.sleep(60)
                
            except Exception as e:
                self.logger.error(f"Error in approval cleanup: {str(e)}")
                await asyncio.sleep(60)
    
    def add_approval_callback(self, callback: Callable):
        """
        Add a callback for external approval system integration.
        
        Args:
            callback: Async function to call when approval requests are created
        """
        self.approval_callbacks.append(callback)
        self.logger.info("Added approval callback")
    
    def get_approval_stats(self) -> Dict[str, Any]:
        """
        Get approval workflow statistics.
        
        Returns:
            Dictionary with approval statistics
        """
        total_approvals = len(self.approval_history)
        approved_count = sum(1 for req in self.approval_history if req.status == 'approved')
        rejected_count = sum(1 for req in self.approval_history if req.status == 'rejected')
        expired_count = sum(1 for req in self.approval_history if req.status == 'expired')
        
        return {
            'total_approvals': total_approvals,
            'approved': approved_count,
            'rejected': rejected_count,
            'expired': expired_count,
            'pending': len(self.pending_approvals),
            'approval_rate': approved_count / total_approvals if total_approvals > 0 else 0
        }
