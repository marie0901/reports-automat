"""Base plugin system for report generation."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd


class BaseReportPlugin(ABC):
    """Abstract base class for report plugins."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name identifier."""
        pass
    
    @property
    @abstractmethod
    def supports_multiple_files(self) -> bool:
        """Whether plugin supports multiple input files."""
        pass
    
    @abstractmethod
    def process_csv(self, csv_path: Path) -> pd.DataFrame:
        """Read and process CSV file(s)."""
        pass
    
    @abstractmethod
    def transform_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Transform data into report structure."""
        pass
    
    @abstractmethod
    def generate_excel(self, report_data: Dict[str, Any], output_path: Path) -> None:
        """Generate Excel file from report data."""
        pass
    
    def validate_input(self, csv_path: Path) -> bool:
        """Validate input file(s) exist and are readable."""
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        return True
    
    def execute(self, input_path: Path, output_path: Path) -> None:
        """Execute full report generation pipeline."""
        self.validate_input(input_path)
        data = self.process_csv(input_path)
        report_data = self.transform_data(data)
        self.generate_excel(report_data, output_path)
