"""
Progress tracking for extraction jobs.
"""
from dataclasses import dataclass, field
from typing import List
import time


@dataclass
class ExtractionProgress:
    """Tracks progress and errors during extraction."""

    start_time: float = field(default_factory=time.time)
    success_count: int = 0
    error_count: int = 0
    errors: List[str] = field(default_factory=list)

    def record_success(self):
        """Record a successful extraction."""
        self.success_count += 1

    def record_error(self, error: str):
        """Record an extraction error."""
        self.error_count += 1
        self.errors.append(error)

    def get_summary(self) -> dict:
        """Get summary statistics."""
        total = self.success_count + self.error_count
        success_rate = (self.success_count / total * 100) if total > 0 else 0
        duration = time.time() - self.start_time

        return {
            "total": total,
            "success": self.success_count,
            "errors": self.error_count,
            "success_rate": success_rate,
            "duration_seconds": duration
        }

    def print_summary(self):
        """Print formatted summary."""
        summary = self.get_summary()

        print(f"\n{'='*60}")
        print(f"EXTRACTION COMPLETE")
        print(f"{'='*60}")
        print(f"Total: {summary['total']}")
        print(f"Successful: {summary['success']}")
        print(f"Errors: {summary['errors']}")
        print(f"Success rate: {summary['success_rate']:.1f}%")
        print(f"Duration: {summary['duration_seconds']:.1f}s")

        if self.errors:
            print(f"\nError details:")
            for i, error in enumerate(self.errors[:5], 1):
                print(f"  {i}. {error}")
            if len(self.errors) > 5:
                print(f"  ... and {len(self.errors) - 5} more")
