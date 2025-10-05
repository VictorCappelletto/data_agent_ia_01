"""
DPL Agent v3.0 - Response Formatter

Provides clean, professional formatting for specialist responses.
Focuses on UX without emojis or unnecessary decorations.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


# ============================================================================
# RESPONSE FORMATTING
# ============================================================================

class ResponseFormatter:
    """
    Format specialist responses for clean, professional UX.
    
    All formatters:
    - Remove emojis
    - Use consistent styling
    - Focus on readability
    - Professional output
    """
    
    @staticmethod
    def format_troubleshooting(
        diagnosis: str,
        severity: str,
        confidence: float,
        root_cause: Optional[str],
        immediate_actions: List[str],
        investigation_steps: List[str],
        relevant_tools: List[str],
        escalation_needed: bool
    ) -> str:
        """
        Format troubleshooting analysis response.
        
        Args:
            diagnosis: Error diagnosis
            severity: Error severity level
            confidence: Confidence score (0-1)
            root_cause: Root cause description
            immediate_actions: List of immediate actions
            investigation_steps: List of investigation steps
            relevant_tools: List of relevant tools
            escalation_needed: Whether escalation is needed
            
        Returns:
            Formatted troubleshooting response
        """
        sections = []
        
        # Header
        sections.append("TROUBLESHOOTING ANALYSIS")
        sections.append("=" * 50)
        sections.append("")
        
        # Summary
        sections.append(f"Diagnosis: {diagnosis}")
        sections.append(f"Severity: {severity.upper()}")
        sections.append(f"Confidence: {confidence * 100:.0f}%")
        sections.append("")
        
        # Root Cause
        sections.append("Root Cause Candidates:")
        sections.append(root_cause or "Requires further investigation")
        sections.append("")
        
        # Immediate Actions
        if immediate_actions:
            sections.append("Immediate Actions:")
            for i, action in enumerate(immediate_actions, 1):
                sections.append(f"  {i}. {action}")
            sections.append("")
        
        # Investigation Steps
        if investigation_steps:
            sections.append("Investigation Steps:")
            for i, step in enumerate(investigation_steps, 1):
                sections.append(f"  {i}. {step}")
            sections.append("")
        
        # Relevant Tools
        if relevant_tools:
            sections.append("Relevant Tools:")
            for tool in relevant_tools:
                sections.append(f"  - {tool}")
            sections.append("")
        
        # Escalation
        escalation_text = "YES - Escalate immediately" if escalation_needed else "Not required"
        sections.append(f"Escalation: {escalation_text}")
        
        return "\n".join(sections)
    
    @staticmethod
    def format_bug_resolution(
        bug_type: str,
        resolution_steps: List[str],
        related_tools: List[str],
        estimated_time: Optional[str] = None
    ) -> str:
        """
        Format bug resolution response.
        
        Args:
            bug_type: Type of bug
            resolution_steps: List of resolution steps
            related_tools: List of related tools
            estimated_time: Estimated resolution time
            
        Returns:
            Formatted bug resolution response
        """
        sections = []
        
        sections.append("BUG RESOLUTION GUIDE")
        sections.append("=" * 50)
        sections.append("")
        
        sections.append(f"Bug Type: {bug_type}")
        if estimated_time:
            sections.append(f"Estimated Time: {estimated_time}")
        sections.append("")
        
        sections.append("Resolution Steps:")
        for i, step in enumerate(resolution_steps, 1):
            sections.append(f"  {i}. {step}")
        sections.append("")
        
        if related_tools:
            sections.append("Related Tools:")
            for tool in related_tools:
                sections.append(f"  - {tool}")
        
        return "\n".join(sections)
    
    @staticmethod
    def format_performance_optimization(
        issue: str,
        recommendations: List[str],
        expected_improvement: Optional[str] = None
    ) -> str:
        """
        Format performance optimization response.
        
        Args:
            issue: Performance issue description
            recommendations: List of optimization recommendations
            expected_improvement: Expected performance improvement
            
        Returns:
            Formatted performance optimization response
        """
        sections = []
        
        sections.append("PERFORMANCE OPTIMIZATION")
        sections.append("=" * 50)
        sections.append("")
        
        sections.append(f"Issue: {issue}")
        if expected_improvement:
            sections.append(f"Expected Improvement: {expected_improvement}")
        sections.append("")
        
        sections.append("Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            sections.append(f"  {i}. {rec}")
        
        return "\n".join(sections)
    
    @staticmethod
    def format_quality_report(
        entity_name: str,
        dimension: str,
        findings: List[str],
        status: str
    ) -> str:
        """
        Format data quality report.
        
        Args:
            entity_name: DPL entity name
            dimension: Quality dimension checked
            findings: List of findings
            status: Overall status
            
        Returns:
            Formatted quality report
        """
        sections = []
        
        sections.append("DATA QUALITY REPORT")
        sections.append("=" * 50)
        sections.append("")
        
        sections.append(f"Entity: {entity_name}")
        sections.append(f"Dimension: {dimension}")
        sections.append(f"Status: {status}")
        sections.append("")
        
        sections.append("Findings:")
        for i, finding in enumerate(findings, 1):
            sections.append(f"  {i}. {finding}")
        
        return "\n".join(sections)
    
    @staticmethod
    def format_workflow_status(
        workflow_name: str,
        status: str,
        details: Dict[str, Any]
    ) -> str:
        """
        Format workflow status response.
        
        Args:
            workflow_name: Workflow name
            status: Current status
            details: Additional details
            
        Returns:
            Formatted workflow status
        """
        sections = []
        
        sections.append("WORKFLOW STATUS")
        sections.append("=" * 50)
        sections.append("")
        
        sections.append(f"Workflow: {workflow_name}")
        sections.append(f"Status: {status}")
        sections.append("")
        
        if details:
            sections.append("Details:")
            for key, value in details.items():
                sections.append(f"  {key}: {value}")
        
        return "\n".join(sections)
    
    @staticmethod
    def format_reprocessing_plan(
        entity_name: str,
        date_range: str,
        urgency: str,
        steps: List[str],
        notify_teams: List[str]
    ) -> str:
        """
        Format reprocessing coordination plan.
        
        Args:
            entity_name: DPL entity to reprocess
            date_range: Date range for reprocessing
            urgency: Urgency level
            steps: List of steps
            notify_teams: Teams to notify
            
        Returns:
            Formatted reprocessing plan
        """
        sections = []
        
        sections.append("REPROCESSING COORDINATION PLAN")
        sections.append("=" * 50)
        sections.append("")
        
        sections.append(f"Entity: {entity_name}")
        sections.append(f"Date Range: {date_range}")
        sections.append(f"Urgency: {urgency.upper()}")
        sections.append("")
        
        sections.append("Steps:")
        for i, step in enumerate(steps, 1):
            sections.append(f"  {i}. {step}")
        sections.append("")
        
        if notify_teams:
            sections.append("Teams to Notify:")
            for team in notify_teams:
                sections.append(f"  - {team}")
        
        return "\n".join(sections)


# ============================================================================
# COMMON FORMATTERS
# ============================================================================

class CommonFormatters:
    """
    Reusable formatting utilities for consistent output.
    """
    
    @staticmethod
    def format_list(items: List[str], numbered: bool = True, indent: int = 2) -> str:
        """
        Format list of items consistently.
        
        Args:
            items: List of items to format
            numbered: Use numbers vs bullets
            indent: Indentation spaces
            
        Returns:
            Formatted list
        """
        indent_str = " " * indent
        if numbered:
            return "\n".join(f"{indent_str}{i}. {item}" for i, item in enumerate(items, 1))
        return "\n".join(f"{indent_str}- {item}" for item in items)
    
    @staticmethod
    def format_key_value(data: Dict[str, Any], indent: int = 2) -> str:
        """
        Format key-value pairs consistently.
        
        Args:
            data: Dictionary to format
            indent: Indentation spaces
            
        Returns:
            Formatted key-value pairs
        """
        indent_str = " " * indent
        return "\n".join(f"{indent_str}{key}: {value}" for key, value in data.items())
    
    @staticmethod
    def format_section(title: str, content: str, level: int = 1) -> str:
        """
        Format section with title and separator.
        
        Args:
            title: Section title
            content: Section content
            level: Heading level (1 or 2)
            
        Returns:
            Formatted section
        """
        separator_char = "=" if level == 1 else "-"
        separator = separator_char * len(title)
        return f"{title}\n{separator}\n{content}"
    
    @staticmethod
    def clean_whitespace(text: str) -> str:
        """
        Remove excessive whitespace and clean text.
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        lines = [line.strip() for line in text.split('\n')]
        return '\n'.join(line for line in lines if line)
    
    @staticmethod
    def truncate(text: str, max_length: int = 100, suffix: str = "...") -> str:
        """
        Truncate text to maximum length.
        
        Args:
            text: Text to truncate
            max_length: Maximum length
            suffix: Suffix to add if truncated
            
        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix

